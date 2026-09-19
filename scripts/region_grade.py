#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
region_grade.py —— **按区域定向分级**（HSV 级），补 `tone_match.py` 的盲区。

为什么需要它（2026-09-19 第 9 页 v3 实测）：
  `tone_match.py --hue-ramp` 是**按明度**把紫色族映射到三段紫阶，
  它**默认假设参考图的明度顺序是单调的**（深底 V≈0.32 < 机身 V≈0.47 < 亮面 V≈0.60）。
  但模型出图经常把顺序搞反 —— 第 9 页 v3 实测：背景 V=0.435 / H=271，
  卡框 V=0.353 / H=303。**背景比卡框还亮**，于是 hue-ramp 把背景判成"中间调"→ 给成 277°，
  卡框反而落在"暗部"→ 给成 253°，整幅的紫就烂在一起。
  这种图无论怎么调 hue-ramp 参数都救不回来，必须**先按几何区域把明度顺序摆正**。

能做的事（每条规则 = 一个几何区域 × 一个颜色选择器 × 一组 HSV 动作）：
  - region : inside / outside  —— inside 用 box；outside 用一个或多个 keep 框的补集
  - select : 在 h/s/v 上各给一个区间（度 / 0~1 / 0~1），只有落进来的像素被改
  - 动作   : hue(色相吸附,度) / sat(饱和倍数) / val(明度倍数)
             blend_to(混向某个 RGB) / blend_k(混合强度)
  - feather: 几何边界羽化像素数（默认 12，避免出现硬接缝）
  - ramp   : 可选，在选中的像素里**再按明度**做三段紫阶（同 tone_match）

用法：
  python region_grade.py --scene in.png --out out.png --spec grade.json
  python region_grade.py --scene in.png --out out.png --spec grade.json --report

grade.json 示例（第 9 页 v3 实际用的）：
[
 {"region":"outside",
  "keep":[[94,200,242,505],[268,200,412,505],[438,200,579,505],[605,200,740,505],[756,120,1024,570]],
  "select":{"h":[200,350],"s":[0.10,1.0],"v":[0.10,1.0]},
  "hue":252,"hue_k":0.88,"sat":1.32,"val":0.74,"feather":26},

 {"region":"inside","box":[94,200,242,505],
  "select":{"h":[275,355],"s":[0.22,1.0],"v":[0.12,0.66]},
  "hue":277,"hue_k":0.90,"sat":1.10,"val":1.08,"feather":6},

 {"region":"inside","box":[94,200,242,505],
  "select":{"h":[0,70],"s":[0,0.40],"v":[0.55,1.0]},
  "blend_to":[234,206,179],"blend_k":0.42,"feather":6}
]
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clay_text import _blur  # noqa: E402


def _geom_mask(shape, rule):
    """按 region 生成几何掩膜（0~1，浮点），并按 feather 羽化。"""
    H, W = shape
    m = np.zeros((H, W), np.float32)
    if rule.get("region", "inside") == "inside":
        boxes = [rule["box"]]
        for x0, y0, x1, y1 in boxes:
            m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = 1.0
    else:
        m[:] = 1.0
        for x0, y0, x1, y1 in rule.get("keep", []):
            m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = 0.0
    f = float(rule.get("feather", 12))
    if f > 0:
        m = _blur(m, f)
    return np.clip(m, 0, 1)


def _color_mask(h, s, v, sel):
    """颜色选择器 → 0/1 掩膜；h/s/v 区间缺省表示不限。"""
    m = np.ones(h.shape, bool)
    if "h" in sel:
        lo, hi = sel["h"]
        d = np.abs((h - lo + 180.0) % 360.0 - 180.0)
        m &= (d <= (hi - lo) / 2.0) if hi >= lo else ((h >= lo) | (h <= hi))
    if "s" in sel:
        m &= (s >= sel["s"][0]) & (s <= sel["s"][1])
    if "v" in sel:
        m &= (v >= sel["v"][0]) & (v <= sel["v"][1])
    return m


def _ramp_apply(hn, vn, inb, ramp):
    """在选中像素内按明度映射三段紫阶。"""
    v_lo, v_mid, v_hi = ramp.get("v_lo", 0.25), ramp.get("v_mid", 0.45), ramp.get("v_hi", 0.62)
    h_d, h_m, h_l = ramp.get("h_dark", 253.), ramp.get("h_mid", 277.), ramp.get("h_light", 296.)
    t = np.clip((vn - v_lo) / max(1e-6, v_mid - v_lo), 0, 1)
    t2 = np.clip((vn - v_mid) / max(1e-6, v_hi - v_mid), 0, 1)
    tgt = h_d + (h_m - h_d) * t
    tgt = tgt + (h_l - h_m) * t2
    k = float(ramp.get("k", 1.0))
    delta = (tgt - hn + 180.0) % 360.0 - 180.0
    return (hn + delta * (k * inb)) % 360.0


def apply_vignette(im, amount, start=0.55):
    """径向暗角（乘法，只压暗、绝不涂黑）。

    amount: 0~1，四角相对中心的压暗比例（参考基线四角≈中心×0.35 → 取 0.55~0.65）
    start : 从归一化半径多少开始压（0=从中心就开始；0.55=只压外围）
    """
    if amount <= 0:
        return im
    arr = np.asarray(im).astype(np.float32)
    H, W = arr.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - (W - 1) / 2.0) / max(1.0, (W - 1) / 2.0)
    dy = (yy - (H - 1) / 2.0) / max(1.0, (H - 1) / 2.0)
    d = np.sqrt(dx * dx + dy * dy) / np.sqrt(2.0)          # 0=中心, 1=四角
    t = np.clip((d - start) / max(1e-6, 1.0 - start), 0, 1) ** 1.5
    arr = np.clip(arr * (1.0 - float(amount) * t)[..., None], 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def run(spec, scene, out, report=False, vignette=0.0, vig_start=0.55):
    im = Image.open(scene).convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    hsv = np.asarray(im.convert("HSV")).astype(np.float32) / 255.0
    hn, sn, vn = hsv[:, :, 0] * 360.0, hsv[:, :, 1], hsv[:, :, 2]

    for i, rule in enumerate(spec):
        gm = _geom_mask(hn.shape, rule)
        cm = _color_mask(hn, sn, vn, rule.get("select", {}))
        alpha = gm * cm.astype(np.float32)
        if alpha.max() < 1e-3:
            continue
        n_before = int((alpha > 0.5).sum())

        if rule.get("hue") is not None:
            k = float(rule.get("hue_k", 1.0))
            hn = (hn + ((rule["hue"] - hn + 180.0) % 360.0 - 180.0) * (k * alpha)) % 360.0
        if "ramp" in rule:
            hn = _ramp_apply(hn, vn, alpha, rule["ramp"])
        if rule.get("sat") is not None:
            sn = np.clip(sn * (1.0 + (float(rule["sat"]) - 1.0) * alpha), 0, 1)
        if rule.get("val") is not None:
            vn = np.clip(vn * (1.0 + (float(rule["val"]) - 1.0) * alpha), 0, 1)

        if "blend_to" in rule:
            tgt = np.array(rule["blend_to"], np.float32) / 255.0
            k = float(rule.get("blend_k", 0.4)) * alpha
            cur = np.asarray(Image.fromarray(
                (np.stack([hn / 360.0, sn, vn], -1) * 255).astype(np.uint8), "HSV").convert("RGB")
            ).astype(np.float32) / 255.0
            mix = cur * (1 - k[..., None]) + tgt * k[..., None]
            hh2 = np.asarray(Image.fromarray((np.clip(mix, 0, 1) * 255).astype(np.uint8))
                             .convert("HSV")).astype(np.float32) / 255.0
            hn, sn, vn = hh2[:, :, 0] * 360.0, hh2[:, :, 1], hh2[:, :, 2]

        if report:
            print(f"  [{i}] region={rule.get('region','inside')} 命中 {n_before:7d}px "
                  f"({n_before / (hn.shape[0] * hn.shape[1]) * 100:.1f}%)")

    out_hsv = np.stack([hn / 360.0, sn, vn], -1)
    res = Image.fromarray((np.clip(out_hsv, 0, 1) * 255).astype(np.uint8), "HSV").convert("RGB")
    res = apply_vignette(res, vignette, vig_start)
    if out:
        res.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--spec", required=True, help="JSON：规则数组")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--vignette", type=float, default=0.0,
                    help="径向暗角强度 0~1（乘法只压暗）。四角要压到参考的 ~31/255 → 0.55~0.65")
    ap.add_argument("--vig-start", type=float, default=0.55,
                    help="从归一化半径多少开始压（默认 0.55，只压外围，不动主体）")
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    print("->", run(spec, args.scene, args.out, report=args.report,
                   vignette=args.vignette, vig_start=args.vig_start))


if __name__ == "__main__":
    main()
