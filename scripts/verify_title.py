#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""标题自检 —— 确认这台机器渲出来的标题仍符合「标题唯一正解」的定稿规格。

用法：
    python verify_title.py

判据（全部机检，不靠肉眼）：
    ① 字形/字号     ink 宽高比、ink 宽高 —— 与金标准同体量
    ② 描边          边宽/字高 —— **必须是"细边"**（八六实测 ~0.02 字高），
                    不是厚奶油垫（0.06+ 就是用户骂的"纯文字框"）
    ③ 配色          字面暖橙黄 + 边色米白 —— 与金标准比
    ④ **没有长条底板** 金面底边下方不允许出现连续的横条（用户两次点名的问题）
    ⑤ 颗粒          字面要有可见的细腻肌理（不是纯平涂）

**什么时候跑**：① 换机器 / 别人拿到 skill 后第一次用；② 改过 clay_text.py 之后；
③ 每页标题交付前。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

import clay_text

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(SKILL, 'assets', 'ref-title', 'gold_metrics.json')
WALL = (46, 30, 74)

TOL = {
    'aspect_ratio': 0.20,
    'ink_w': 0.05,            # 相对
    'ink_h': 3,               # 绝对 px
    'edge_over_height': 0.010,
    'face_median_rgb': 14,
    'edge_median_rgb': 26,
    'base_plate_ratio': 0.45,  # 硬上限
}


def measure(a):
    R = a[..., 0].astype(np.int16)
    G = a[..., 1].astype(np.int16)
    B = a[..., 2].astype(np.int16)
    gold = ndi.binary_opening((R > 150) & (R - B > 55) & (G > 75) & (G < 215) & (B < 150),
                              np.ones((2, 2)))
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    cream = ndi.binary_opening((mn > 150) & ((mx - mn) < 75), np.ones((2, 2)))
    gy, gx = np.where(gold)
    gy0, gy1, gx0, gx1 = gy.min(), gy.max(), gx.min(), gx.max()
    ih, iw = gy1 - gy0 + 1, gx1 - gx0 + 1

    d = ndi.distance_transform_edt(~gold)
    ring = cream & (d > 0) & (d < ih * 0.5)
    v = d[ring]

    wall = a[max(0, gy0 - ih), 2].astype(np.int16)
    worst = 0
    for off in range(1, 9):
        y = gy1 + off
        if y >= a.shape[0]:
            break
        non = np.abs(a[y].astype(np.int16) - wall).max(axis=-1) > 26
        idx = np.where(non)[0]
        if len(idx):
            for s in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
                worst = max(worst, len(s))

    lum = (R * .299 + G * .587 + B * .114).astype(np.float32)
    inner = ndi.binary_erosion(gold, np.ones((3, 3)))
    hf = lum - ndi.median_filter(lum, size=3)
    return {
        'ink_wh': [int(iw), int(ih)],
        'aspect_ratio': float(iw / ih),
        'edge_over_height': float(v.mean() / ih) if ring.sum() else 0.0,
        'face_median_rgb': [int(x) for x in np.median(a[gold], axis=0)],
        'edge_median_rgb': [int(x) for x in np.median(a[ring], axis=0)] if ring.sum() else [0, 0, 0],
        'grain_hf_std': float(hf[inner].std()),
        'base_plate_ratio': float(worst / iw),
    }


def main():
    if not os.path.exists(GOLD):
        print('缺少金标准：%s' % GOLD)
        return 2
    gold = json.load(open(GOLD, encoding='utf-8'))
    print(clay_text.font_report())
    print('金标准：%s  cap=%s  ink=%s' % (gold.get('text'), gold.get('cap_height'), gold['ink_wh']))
    print('')

    t = clay_text.render_title_clay(gold.get('text', '改法清单'),
                                    cap_height=gold.get('cap_height', 80))
    bg = Image.new('RGB', t.size, WALL)
    bg.paste(t, (0, 0), t)
    got = measure(np.asarray(bg))

    ok = True
    print('%-14s %16s %16s %10s  %s' % ('指标', '金标准', '本机', '偏差', '判定'))

    def rel(name, key, tol_rel, fmt='%.4f'):
        nonlocal ok
        g, v = float(gold[key]), float(got[key])
        d = v - g
        good = abs(d) <= tol_rel * max(abs(g), 1e-6)
        ok = ok and good
        print('%-14s %16s %16s %+10s  %s' % (name, fmt % g, fmt % v,
                                             '%.4f' % d, 'OK' if good else 'FAIL'))

    gv = gold['ink_wh']; vv = got['ink_wh']
    gw_ok = abs(vv[0] - gv[0]) <= gv[0] * TOL['ink_w']
    gh_ok = abs(vv[1] - gv[1]) <= TOL['ink_h']
    ok = ok and gw_ok and gh_ok
    print('%-14s %16s %16s %10s  %s' % ('ink 宽x高', '%dx%d' % tuple(gv), '%dx%d' % tuple(vv),
                                        '%+d/%+d' % (vv[0] - gv[0], vv[1] - gv[1]),
                                        'OK' if (gw_ok and gh_ok) else 'FAIL'))
    rel('宽高比', 'aspect_ratio', 0.20)
    rel('边宽/字高', 'edge_over_height', 0.010 / max(gold['edge_over_height'], 1e-6))

    for key, name in (('face_median_rgb', '字面中位色'), ('edge_median_rgb', '边色中位色')):
        g, v = gold[key], got[key]
        d = max(abs(a - b) for a, b in zip(g, v))
        good = d <= TOL[key]
        ok = ok and good
        print('%-14s %16s %16s %10d  %s' % (name, g, v, d, 'OK' if good else 'FAIL'))

    # ④ 底板
    g, v = gold['base_plate_ratio'], got['base_plate_ratio']
    good = v <= TOL['base_plate_ratio']
    ok = ok and good
    print('%-14s %16s %16s %10s  %s' % ('底板横条比', '%.3f' % g, '%.3f' % v, '%.3f' % (v - g),
                                        'OK' if good else 'FAIL'))
    # ⑤ 颗粒
    g, v = gold['grain_hf_std'], got['grain_hf_std']
    good = v >= gold['grain_hf_std'] * 0.5
    ok = ok and good
    print('%-14s %16s %16s %10s  %s' % ('字面颗粒', '%.2f' % g, '%.2f' % v, '%.2f' % (v - g),
                                        'OK' if good else 'FAIL'))

    print('')
    print('结论：%s' % ('PASS —— 标题符合定稿规格，可以出页' if ok
                     else 'FAIL —— 见上面 FAIL 行；先看字体解析，再查 pad/bold/grain'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
