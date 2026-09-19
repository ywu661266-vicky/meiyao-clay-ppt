#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tone_match.py — 黏土风成图「色调校正」收尾脚本

为什么需要它：
  图片模型即使 prompt 里写了 "richly saturated / NOT grey"，
  出来的图仍常偏灰：饱和度低、奶油色发白、背景不够深。
  靠反复出图去抠这一项，边际收益极低（实测改了 6 版仍有差距）。
  更有效的做法是出图后做一次定向色彩校正，把色调对齐参考基线。

参考基线（八六老师课件页实测，1536×1024 级别）：
  饱和度 ≈ 0.615 | 画面平均亮度 ≈ 83 | 四角中位亮度 ≈ 31 | 亮部 B-R ≈ -86

实测效果（第 8 页《转折点来了》）：
  校正前 饱和 0.385 / 亮 88.3 / 角 44.4 / 亮部B-R -57.1
  校正后 饱和 0.545 / 亮 81.3 / 角 37.2 / 亮部B-R -87.3

用法：
  python tone_match.py <图片路径或目录>                  # 默认参数，输出 *_tone.png
  python tone_match.py <dir> --sat 1.5 --contrast 1.10   # 自定义
  python tone_match.py <dir> --analyze                   # 只量化不写文件

注意：「适中」是审美铁律 —— 别为了追基线把饱和度/对比度一路拉满，
      越过 ~1.5x 就容易变得又艳又脏。宁可欠一点。
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance


def analyze(path):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    W, H = im.size
    af = a / 255.0
    mx = af.max(2)
    mn = af.min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0).mean()
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    m = max(4, int(min(W, H) * 0.06))
    corners = np.concatenate([
        lum[:m, :m].ravel(), lum[:m, -m:].ravel(),
        lum[-m:, :m].ravel(), lum[-m:, -m:].ravel(),
    ])
    thr = np.percentile(lum, 80)
    b_minus_r = float((a[lum >= thr][:, 2] - a[lum >= thr][:, 0]).mean())
    return dict(sat=float(sat), lum=float(lum.mean()),
                corner=float(np.median(corners)), b_minus_r=b_minus_r)


def grade(path, out_path, sat=1.34, warm_r=1.028, cool_b=0.968,
          contrast=1.045, brightness=0.995, vignette=0.0,
          hue_lock=None, hue_strength=0.92, hue_lo=258.0, hue_hi=352.0,
          hi_rolloff=0.0, hi_start=0.86, hi_keep=0.40, gamma=1.0,
          hue_ramp=0.0, ramp=None):
    im = Image.open(path).convert('RGB')

    # 0) HSV 阶段：「三段紫阶」+ 选择性色相吸附 + 提饱和（一次往返，避免量化累积）
    #
    #    A) hue_ramp —— **三段紫阶**（本文件最重要的一招）
    #       铁律：参考图的"高级紫"不是一种紫，而是**按明度拉开的三段紫**：
    #         深靛蓝紫底 H≈253 (32,18,82)  →  紫罗兰机身 H≈277 (97,59,120)
    #         →  藕荷色亮面 H≈294-297 (150,112,154)
    #       三段跨 41°。只写"purple"时模型会把整幅压到同一段蓝紫（实测 H 240/241/245，
    #       跨度仅 5°）→ 单调、发冷、发平，就是"不好看"的物理原因。
    #       所以按像素明度 t 把紫色族重映射到 [h_dark, h_mid, h_light] 三点折线，
    #       只动紫色族（橙/绿/奶油/红不受影响）。
    #    B) hue_lock —— 单一锚点吸附，用于只偏一点点的场合。
    if (hue_lock is not None and hue_strength > 0) or abs(sat - 1.0) > 1e-3:
        h, s, v = im.convert('HSV').split()
        hn = np.asarray(h).astype(np.float32) / 255.0 * 360.0      # 度
        if hue_lock is not None and hue_strength > 0:
            lo, hi, band = hue_lo, hue_hi, 12.0
            wgt = (np.clip((hn - (lo - band)) / band, 0, 1)
                   * np.clip(((hi + band) - hn) / band, 0, 1))
            hn = hn + ((hue_lock - hn + 180.0) % 360.0 - 180.0) * (hue_strength * wgt)
            hn = hn % 360.0
        h = Image.fromarray(np.clip(hn / 360.0 * 255.0, 0, 255).astype(np.uint8))
        if abs(sat - 1.0) > 1e-3:
            s = s.point(lambda x: min(255, int(x * sat)))
        im = Image.merge('HSV', (h, s, v)).convert('RGB')

    # 2) 暖化：抬 R、压 B（奶油色往 rgb(218,192,153) 靠）
    if abs(warm_r - 1.0) > 1e-3 or abs(cool_b - 1.0) > 1e-3:
        a = np.asarray(im).astype(np.float32)
        a[:, :, 0] = np.clip(a[:, :, 0] * warm_r, 0, 255)
        a[:, :, 2] = np.clip(a[:, :, 2] * cool_b, 0, 255)
        im = Image.fromarray(a.astype(np.uint8))

    # 2.5) 高光滚降：模型爱把奶油色打成纯白（参考基线纯白只占 0.8%，成图常 5%+），
    #      白花花一片就是"塑料/廉价感"的来源。把 V>hi_start 的部分按 hi_keep 压缩。
    if hi_rolloff > 0:
        a = np.asarray(im).astype(np.float32)
        v = a.max(2) / 255.0
        m = v > hi_start
        if m.any():
            v2 = np.where(m, hi_start + (v - hi_start) * hi_keep, v)
            a = a * (v2 / np.maximum(v, 1e-6))[..., None]
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    # 3) gamma 提亮（模型常把画面整体压暗，暗部尤其闷；gamma>1 提亮中间调与暗部）
    if abs(gamma - 1.0) > 1e-3:
        inv = 1.0 / gamma
        lut = [min(255, int(round((i / 255.0) ** inv * 255))) for i in range(256)]
        im = im.point(lut * 3)

    # 3.5) 对比 / 亮度微调（暗角更沉、亮部更透）
    if abs(contrast - 1.0) > 1e-3:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    if abs(brightness - 1.0) > 1e-3:
        im = ImageEnhance.Brightness(im).enhance(brightness)

    # 4) 径向暗角：把四角压暗到基线（角亮度 ≈31），但只做乘法压暗，不会涂成死黑
    if vignette > 0:
        a = np.asarray(im).astype(np.float32)
        h, w = a.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.4142
        t = np.clip((r - 0.34) / 0.66, 0, 1) ** 1.45
        a *= (1.0 - vignette * t)[..., None]
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    # 5) **三段紫阶**（必须放在最后：暖化 R↑B↓ 会把紫重新拽向洋红，放前面会被抵消）
    #    参考图的"高级紫"不是一种紫，而是按明度拉开的三段：
    #      深靛蓝紫底 H≈253 (32,18,82) → 紫罗兰机身 H≈277 (97,59,120) → 藕荷亮面 H≈294 (150,112,154)
    #    三段跨 41°。若整幅只有一段紫（实测模型常给 H 240/241/245，跨度仅 5°），
    #    画面就会"单调、发冷、发平"——这是"不好看"的物理原因。
    #    只重映射紫色族（src_lo~src_hi 且饱和度达标），橙/绿/奶油/红一律不动。
    if hue_ramp and hue_ramp > 0:
        cfg = dict(dict(src_lo=200.0, src_hi=350.0, s_min=0.06,
                        v_lo=0.25, v_mid=0.45, v_hi=0.62,
                        h_dark=253.0, h_mid=277.0, h_light=296.0), **(ramp or {}))
        h, s, v = im.convert('HSV').split()
        hn = np.asarray(h).astype(np.float32) / 255.0 * 360.0
        sn = np.asarray(s).astype(np.float32) / 255.0
        vn = np.asarray(v).astype(np.float32) / 255.0
        inb = ((hn >= cfg['src_lo']) & (hn <= cfg['src_hi']) & (sn >= cfg['s_min']))
        dm = max(1e-6, cfg['v_mid'] - cfg['v_lo'])
        dh = max(1e-6, cfg['v_hi'] - cfg['v_mid'])
        t_lo = np.clip((vn - cfg['v_lo']) / dm, 0, 1) * 0.5
        t_hi = 0.5 + np.clip((vn - cfg['v_mid']) / dh, 0, 1) * 0.5
        t = np.where(vn <= cfg['v_mid'], t_lo, t_hi)
        tgt = np.where(t <= 0.5,
                       cfg['h_dark'] + (cfg['h_mid'] - cfg['h_dark']) * (t / 0.5),
                       cfg['h_mid'] + (cfg['h_light'] - cfg['h_mid']) * ((t - 0.5) / 0.5))
        delta = (tgt - hn + 180.0) % 360.0 - 180.0        # 最短角差
        hn2 = (hn + delta * (hue_ramp * inb.astype(np.float32))) % 360.0
        h2 = Image.fromarray(np.clip(hn2 / 360.0 * 255.0, 0, 255).astype(np.uint8))
        im = Image.merge('HSV', (h2, s, v)).convert('RGB')

    im.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target', help='图片路径或目录')
    ap.add_argument('--sat', type=float, default=1.34, help='饱和度倍数，默认 1.34')
    ap.add_argument('--warm-r', type=float, default=1.028, help='R 通道倍数')
    ap.add_argument('--cool-b', type=float, default=0.968, help='B 通道倍数')
    ap.add_argument('--contrast', type=float, default=1.045)
    ap.add_argument('--brightness', type=float, default=0.995)
    ap.add_argument('--vignette', type=float, default=0.0,
                    help='径向暗角强度 0~0.5，用来把四角亮度压到基线 ≈31（背景偏亮时用 0.20~0.32）')
    ap.add_argument('--hue-lock', type=float, default=None,
                    help='把紫色区间(默认 258~352°)吸附到该色相(度)。参考基线靛紫 H≈249，'
                         '模型常给成洋红紫 H≈303 —— 差 50° 就是"发粉发灰"的根因。建议 254~258')
    ap.add_argument('--hue-strength', type=float, default=0.92, help='吸附强度 0~1，默认 0.92')
    ap.add_argument('--hue-lo', type=float, default=258.0, help='待吸附色相下界(度)')
    ap.add_argument('--hue-hi', type=float, default=352.0, help='待吸附色相上界(度)')
    ap.add_argument('--hi-rolloff', type=float, default=0.0,
                    help='高光滚降开关(>0 生效)。参考基线纯白仅占 0.8%，成图常见 5%%+，'
                         '白花一片=廉价感。建议 0.4')
    ap.add_argument('--hi-start', type=float, default=0.86, help='高光起点(0~1)')
    ap.add_argument('--hi-keep', type=float, default=0.40, help='高光压缩后保留比例')
    ap.add_argument('--gamma', type=float, default=1.0,
                    help='提亮曲线，>1 提亮中间调与暗部（模型出图整体偏闷时用 1.20~1.40）')
    ap.add_argument('--hue-ramp', type=float, default=0.0,
                    help='三段紫阶强度 0~1（推荐 1.0）。按明度把紫色族映射到 '
                         '253°深靛底 / 277°紫罗兰机身 / 297°藕荷亮面 三个锚点，'
                         '解决"整幅只有一段蓝紫 → 单调发冷发平"的问题。'
                         '只动紫色族，橙/绿/奶油/红不受影响')
    ap.add_argument('--ramp-src-lo', type=float, default=200.0, help='紫色族源色相下界(度)')
    ap.add_argument('--ramp-src-hi', type=float, default=350.0, help='紫色族源色相上界(度)')
    ap.add_argument('--ramp-h-dark', type=float, default=253.0, help='暗部目标色相(深靛底)')
    ap.add_argument('--ramp-h-mid', type=float, default=277.0, help='中间调目标色相(机身)')
    ap.add_argument('--ramp-h-light', type=float, default=297.0, help='亮部目标色相(藕荷亮面)')
    ap.add_argument('--ramp-v-lo', type=float, default=0.25, help='暗端锚点明度')
    ap.add_argument('--ramp-v-mid', type=float, default=0.50, help='中间锚点明度')
    ap.add_argument('--ramp-v-hi', type=float, default=0.65, help='亮端锚点明度')
    ap.add_argument('--analyze', action='store_true', help='只量化，不写文件')
    ap.add_argument('--out', default=None,
                    help='指定输出路径（单图模式）。不传则输出 <原名>_tone.png；'
                         '⚠️ 同一张图跑多组参数做对比时务必传 --out，否则后一次会覆盖前一次')
    args = ap.parse_args()

    if os.path.isdir(args.target):
        files = [os.path.join(args.target, f) for f in sorted(os.listdir(args.target))
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                 and '_clean' in f and 'tone' not in f]
    else:
        files = [args.target]

    if not files:
        print('[!] 没有找到可处理的图（目录模式下只处理文件名含 _clean 的图）')
        sys.exit(1)

    for p in files:
        before = analyze(p)
        if args.analyze:
            print(f'[analyze] {os.path.basename(p)}  '
                  f'饱和{before["sat"]:.3f} 亮{before["lum"]:.1f} '
                  f'角{before["corner"]:.1f} 亮部B-R{before["b_minus_r"]:.1f}')
            continue
        base, ext = os.path.splitext(p)
        if args.out and not os.path.isdir(args.target):
            out = args.out
        else:
            out = base + '_tone.png'
        ramp = dict(src_lo=args.ramp_src_lo, src_hi=args.ramp_src_hi,
                    v_lo=args.ramp_v_lo, v_mid=args.ramp_v_mid, v_hi=args.ramp_v_hi,
                    h_dark=args.ramp_h_dark, h_mid=args.ramp_h_mid,
                    h_light=args.ramp_h_light)
        grade(p, out, args.sat, args.warm_r, args.cool_b, args.contrast,
              args.brightness, args.vignette,
              args.hue_lock, args.hue_strength, args.hue_lo, args.hue_hi,
              args.hi_rolloff, args.hi_start, args.hi_keep, args.gamma,
              args.hue_ramp, ramp)
        after = analyze(out)
        print(f'[ok] {os.path.basename(p)}')
        print(f'     饱和 {before["sat"]:.3f} -> {after["sat"]:.3f}   '
              f'亮 {before["lum"]:.1f} -> {after["lum"]:.1f}   '
              f'角 {before["corner"]:.1f} -> {after["corner"]:.1f}   '
              f'亮部B-R {before["b_minus_r"]:.1f} -> {after["b_minus_r"]:.1f}')
        print(f'     目标基线：饱和≈0.60  亮≈83  角≈31  亮部B-R≈-86')
        print(f'     -> {out}')


if __name__ == '__main__':
    main()
