#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clay_props.py — 散落小道具渲染器（石粒 / 草叶 / 爱心 / 星星 / 齿轮屑）

为什么需要它（2026-09-19 第 9 页第三轮）：
  参考页（八六 p10）里**没有一个角落是空的地面** —— 地面靠散落的小物件点满：
  石粒、草叶、爱心、星星、齿轮屑。它们"没有独立信息量"，但没有它们画面就空。
  第 9 页是 **4 条**（参考是 7 条），条带只占帧高 41%，左列下方必然空出一段，
  靠这些小道具补回来。

风格约束（必须与整图生成的主场景一致）：
  · 光从左上来 → **高光在左上，投影落在右下**
  · 每件都有**接触影 + 落影**（羽化椭圆），贴地才不飘
  · 上亮下暗 + 右下侧壁（薄，物体小不用做厚）
  · 颗粒 0.10~0.16（跟场景的哑光软陶一致）

用法：
    from clay_props import render_pebble, render_leaf, scatter
    im = render_pebble(20, seed=3)          # → RGBA
    scatter(scene, [(x, y, 'pebble', 22, 0.7)], out='out.png')
"""
import argparse
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clay_text import _blur, _darken, _grain, _lighten, _mix, _over, _rgb, _shift


# ---------------------------------------------------------------- 通用着色

def _shade(mask, base, ss=3, shadow=(24, 14, 42), shadow_strength=0.85,
           depth=0.085, hi=0.42, lo=0.30, grain=0.13, seed=7, light="tl"):
    """把一张掩膜着成"一块黏土"：侧壁 + 顶面 + 高光 + 内影 + 接触影 + 落影

    mask  : (H,W) float 0..1（已在最终尺寸上，内部按 ss 超采样由调用方保证）
    depth : 侧壁厚度 = 尺寸 × depth
    hi/lo : 上缘高光 / 下缘内影强度
    """
    H, W = mask.shape
    d = float(max(H, W))
    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)
    bc = _rgb(base)

    # 落影（往右下）+ 接触影
    fall = _blur(_shift(mask, d * 0.075, d * 0.135), d * 0.135)
    near = _blur(_shift(mask, d * 0.015, d * 0.045), d * 0.045)
    rgb, alpha = _over(rgb, alpha, _rgb(shadow),
                       np.clip(np.maximum(fall * 0.60, near * 0.92), 0, 1) * shadow_strength)

    # 侧壁（向下挤出）
    side = _blur(_shift(mask, 0, d * depth), d * depth * 0.55)
    rgb, alpha = _over(rgb, alpha, _mix(_darken(bc, 0.42), _rgb(shadow), 0.25),
                       np.clip(side * 1.45, 0, 1))

    # 顶面：上亮下暗
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gy = np.clip(yy / max(1.0, H), 0, 1)
    face = _mix(_lighten(bc, 0.13), _darken(bc, 0.13), gy)
    k = max(1.2, d * 0.075)
    te = np.clip(mask - _shift(mask, 0, k), 0, 1)
    face = _mix(face, _lighten(bc, hi), np.clip(te * 0.85, 0, 1))
    be = np.clip(mask - _shift(mask, 0, -k * 1.2), 0, 1)
    face = _mix(face, _darken(bc, lo), np.clip(be * 0.80, 0, 1))
    # 左上柔光斑
    if light == "tl":
        gl = np.clip(1.0 - (((xx / max(1.0, W)) * 1.15) + ((yy / max(1.0, H)) * 0.95)), 0, 1)
        face = _mix(face, _lighten(bc, 0.22), np.clip(gl * 0.45, 0, 1))
    if grain > 0:
        g = _grain((H, W), d * 0.10, seed=seed)[..., None]
        face = np.clip(face * (1 + (g - 0.5) * 2 * grain), 0, 1)
    rgb, alpha = _over(rgb, alpha, face, mask)
    return rgb, alpha


def _finish(rgb, alpha, out_path):
    out = np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2)
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    a = np.asarray(img)[:, :, 3]
    ys, xs = np.nonzero(a > 2)
    if len(ys):
        img = img.crop((max(0, xs.min() - 2), max(0, ys.min() - 2),
                        min(img.width, xs.max() + 3), min(img.height, ys.max() + 3)))
    if out_path:
        img.save(out_path)
    return img


# ---------------------------------------------------------------- 各道具

def render_pebble(size=22, base=(148, 130, 156), seed=1, squash=0.84,
                  out_path=None, shadow=(26, 14, 46), **_):
    """不规则黏土石粒（最万能 —— 参考页地面上散着好几块）"""
    ss = 4
    S = int(size * ss)
    rng = np.random.default_rng(seed)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    # 椭圆 + 多频噪声扰动边缘 → 每块都不一样
    prof = []
    for i in range(64):
        a = i * math.pi / 32.0
        r = 1.0 + 0.10 * math.sin(a * 2 + rng.uniform(0, 3)) \
            + 0.06 * math.sin(a * 3 + rng.uniform(0, 3)) \
            + float(rng.uniform(-0.022, 0.022))
        prof.append(r)
    # 拉到目标长宽比（横躺一点）
    pts = [(S / 2 + math.cos(i * math.pi / 32.0) * S / 2 * prof[i] * 1.04,
            S / 2 + math.sin(i * math.pi / 32.0) * S / 2 * prof[i] * squash)
           for i in range(64)]
    d.polygon(pts, fill=255)
    mask = np.asarray(m).astype(np.float32) / 255.0
    mask = _blur(mask, ss * 1.1)
    mask = np.clip((mask - 0.20) / 0.80, 0, 1)
    img = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (int(S / ss), int(S / ss)), Image.LANCZOS)
    mask = np.asarray(img).astype(np.float32) / 255.0
    rgb, a = _shade(mask, base, ss=ss, shadow=shadow, depth=0.10,
                    hi=0.34, lo=0.30, grain=0.15, seed=seed + 3)
    return _finish(rgb, a, out_path)


def render_leaf(size=26, base=(126, 148, 82), seed=2, out_path=None,
                shadow=(26, 14, 46), curl=0.30, **_):
    """一片弯草叶（参考图地面/角落里到处是）"""
    ss = 4
    S = int(size * ss)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    # 两条对称贝塞尔包成柳叶形（细长：长宽比 ≈ 2.6，太圆就不像叶子）
    top, bot = [], []
    N = 26
    for i in range(N + 1):
        t = i / N
        x = S * (0.07 + 0.86 * t)
        w = S * 0.155 * math.sin(math.pi * t) ** 0.70
        bend = S * curl * (t ** 2 - 0.5 * t)          # 叶尖下弯
        top.append((x, S * 0.50 - w + bend))
        bot.append((x, S * 0.50 + w + bend))
    d.polygon(top + bot[::-1], fill=255)
    mask = np.asarray(m).astype(np.float32) / 255.0
    mask = _blur(mask, ss * 1.0)
    mask = np.clip((mask - 0.20) / 0.80, 0, 1)
    img = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (int(S / ss), int(S / ss)), Image.LANCZOS)
    mask = np.asarray(img).astype(np.float32) / 255.0
    rgb, a = _shade(mask, base, ss=ss, shadow=shadow, depth=0.075,
                    hi=0.40, lo=0.24, grain=0.13, seed=seed + 3)
    return _finish(rgb, a, out_path)


def render_heart(size=20, base=(198, 82, 92), seed=3, out_path=None,
                 shadow=(26, 14, 46), **_):
    """小爱心（八六的招牌点缀）"""
    ss = 4
    S = int(size * ss)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    r = S * 0.26
    d.ellipse([S * 0.50 - 2 * r, S * 0.50 - 2 * r + r * 0.10,
               S * 0.50, S * 0.50 + r * 0.10], fill=255)
    d.ellipse([S * 0.50, S * 0.50 - 2 * r + r * 0.10,
               S * 0.50 + 2 * r, S * 0.50 + r * 0.10], fill=255)
    d.polygon([(S * 0.50 - 2 * r * 0.98, S * 0.50 + r * 0.10),
               (S * 0.50 + 2 * r * 0.98, S * 0.50 + r * 0.10),
               (S * 0.50, S * 0.50 + 2 * r * 1.22)], fill=255)
    mask = np.asarray(m).astype(np.float32) / 255.0
    mask = _blur(mask, ss * 0.95)
    mask = np.clip((mask - 0.22) / 0.78, 0, 1)
    img = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (int(S / ss), int(S / ss)), Image.LANCZOS)
    mask = np.asarray(img).astype(np.float32) / 255.0
    rgb, a = _shade(mask, base, ss=ss, shadow=shadow, depth=0.085,
                    hi=0.45, lo=0.26, grain=0.10, seed=seed + 3)
    return _finish(rgb, a, out_path)


def render_star(size=16, base=(228, 186, 88), seed=4, out_path=None,
                shadow=(26, 14, 46), **_):
    """小五角星"""
    ss = 4
    S = int(size * ss)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = S * (0.46 if i % 2 == 0 else 0.20)
        pts.append((S / 2 + math.cos(a) * rad, S / 2 + math.sin(a) * rad))
    d.polygon(pts, fill=255)
    mask = np.asarray(m).astype(np.float32) / 255.0
    mask = _blur(mask, ss * 1.0)
    mask = np.clip((mask - 0.22) / 0.78, 0, 1)
    img = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (int(S / ss), int(S / ss)), Image.LANCZOS)
    mask = np.asarray(img).astype(np.float32) / 255.0
    rgb, a = _shade(mask, base, ss=ss, shadow=shadow, depth=0.085,
                    hi=0.45, lo=0.26, grain=0.10, seed=seed + 3)
    return _finish(rgb, a, out_path)


def render_gear(size=26, base=(190, 152, 84), seed=5, out_path=None,
                shadow=(26, 14, 46), teeth=8, **_):
    """小齿轮屑（工坊感）"""
    ss = 4
    S = int(size * ss)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    r0 = S * 0.30
    for i in range(teeth):
        a = i * 2 * math.pi / teeth
        d.ellipse([S / 2 + math.cos(a) * S * 0.36 - S * 0.075,
                   S / 2 + math.sin(a) * S * 0.36 - S * 0.075,
                   S / 2 + math.cos(a) * S * 0.36 + S * 0.075,
                   S / 2 + math.sin(a) * S * 0.36 + S * 0.075], fill=255)
    d.ellipse([S / 2 - r0, S / 2 - r0, S / 2 + r0, S / 2 + r0], fill=255)
    mask = np.asarray(m).astype(np.float32) / 255.0
    mask = _blur(mask, ss * 0.9)
    mask = np.clip((mask - 0.22) / 0.78, 0, 1)
    img = Image.fromarray((mask * 255).astype(np.uint8), "L").resize(
        (int(S / ss), int(S / ss)), Image.LANCZOS)
    mask = np.asarray(img).astype(np.float32) / 255.0
    rgb, a = _shade(mask, base, ss=ss, shadow=shadow, depth=0.095,
                    hi=0.40, lo=0.28, grain=0.12, seed=seed + 3)
    # 中孔
    hole = Image.new("L", (mask.shape[1], mask.shape[0]), 0)
    rr = size * 0.115
    ImageDraw.Draw(hole).ellipse([mask.shape[1] / 2 - rr, mask.shape[0] / 2 - rr,
                                  mask.shape[1] / 2 + rr, mask.shape[0] / 2 + rr],
                                 fill=255)
    hm = np.asarray(_blur(np.asarray(hole).astype(np.float32) / 255.0, 1.0))
    out = np.concatenate([rgb * 255.0, a[..., None] * 255.0], axis=2)
    img2 = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    img2.putalpha(Image.fromarray(((a * (1 - hm)) * 255).astype(np.uint8), "L"))
    return _finish(np.asarray(img2)[:, :, :3].astype(np.float32) / 255.0,
                   np.asarray(img2)[:, :, 3].astype(np.float32) / 255.0, out_path)


BUILDERS = {
    "pebble": render_pebble,
    "leaf": render_leaf,
    "heart": render_heart,
    "star": render_star,
    "gear": render_gear,
}


def scatter(scene_path, items, out_path=None, **kw):
    """把散落道具贴到场景上。

    items: [(x, y, kind, size_px, scale, rot_deg, seed), ...]
           x/y 是**道具中心的最终坐标**（场景像素坐标系），scale 会再乘 size_px
    """
    scene = Image.open(scene_path).convert("RGBA")
    for it in items:
        x, y, kind = it[0], it[1], it[2]
        size = it[3] if len(it) > 3 else 20
        scale = it[4] if len(it) > 4 else 1.0
        rot = it[5] if len(it) > 5 else 0.0
        sd = it[6] if len(it) > 6 else 0
        col = it[7] if len(it) > 7 else None
        fn = BUILDERS[kind]
        kwargs = dict(size=max(6, int(size * scale)), seed=sd)
        if col:
            kwargs["base"] = col
        prop = fn(**kwargs)
        if rot:
            prop = prop.rotate(rot, resample=Image.BICUBIC, expand=True)
        scene.alpha_composite(prop, (int(x - prop.width / 2), int(y - prop.height / 2)))
    if out_path:
        scene.convert("RGB").save(out_path)
    return scene


def _selftest(outdir="."):
    kinds = ["pebble", "leaf", "heart", "star", "gear"]
    cell = 150
    sheet = Image.new("RGB", (cell * len(kinds), cell), (142, 118, 176))
    for i, k in enumerate(kinds):
        for j, sz in enumerate((14, 22, 32)):
            im = BUILDERS[k](size=sz, seed=j * 7 + i)
            sheet.paste(im, (i * cell + 48 + j * 6, 40 + j * 22), im)
    p = os.path.join(outdir, "_props_selftest.png")
    sheet.save(p)
    print("-> ", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="selftest", help="selftest | scatter")
    ap.add_argument("--scene")
    ap.add_argument("--items", help="JSON: [[x,y,kind,size,scale,rot,seed,color],...]")
    ap.add_argument("--out", default="out.png")
    a = ap.parse_args()
    if a.mode == "scatter":
        import json
        scatter(a.scene, json.load(open(a.items, encoding="utf-8")), a.out)
    else:
        _selftest(os.path.dirname(os.path.abspath(a.out)) or ".")


if __name__ == "__main__":
    main()
