#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clay_cardtext.py —— 把正文**直接排进道具卡面**的留白里（不贴条、不贴纸）。

为什么要这个脚本（2026-09-19 第 9 页 v3，用户原话
「画面与内容不匹配，像是随意堆元素而已」+「框框像另一套画风，没有和板子融为一体」）：
  八六 p24 / p26 的清单文字是**直接印在奶油卡面上**的深色字，不是"贴在紫底上的胶囊"。
  文字与卡面同属一件东西 → 天然"融为一体"，且不可能读成贴纸。

规格（照八六 p24 实测）：
  - 文字色 = 深棕近黑 rgb(44,28,22)（p24 条上文字最暗 5% 实测 rgb(21,27,7)）
  - 卡面   = 暖奶油 rgb(234,206,179)
  - 字号   = 自动缩到框宽以内（CJK 按 1em、西文按 0.5em 估宽）
  - 压印   = 暗字 + 下缘一道浅色亮边（"压进黏土里"的观感，不是发光描边）

用法：
  python clay_cardtext.py --scene in.png --out out.png --spec spec.json
  spec.json =
  [
    {"box":[107,408,229,482], "text":"先锁人物", "size":24},
    {"box":[281,408,399,482], "text":"短句烘字", "size":24},
    ...
  ]
可选字段（每条）：size / color / emboss / line_gap / align(center|left) /
                 pad / max_lines / weight

CLI 便捷用法（同一文本重复 N 个等宽框）：
  python clay_cardtext.py --scene in.png --out out.png \
      --row "107,281,451,618" --box-w 122 --y0 408 --y1 482 \
      --texts "先锁人物,短句烘字,长文贴卡,出图校色"
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clay_text import _load_font, FONTS  # noqa: E402

TEXT_COLOR = (44, 28, 22)
EMBOSS_COLOR = (243, 227, 205)


def _char_w(ch):
    """CJK 1em，西文/数字/标点 0.5em（用于估宽，避免依赖字体度量）。"""
    o = ord(ch)
    if o < 0x2E80:
        return 0.5
    return 1.0


def _est_w(s, size):
    return sum(_char_w(c) for c in s) * size


def fit_size(text, box_w, want=None, pad=8, floor=11):
    """把字号缩到 box_w 以内（单行）。"""
    avail = box_w - pad * 2
    size = want or int(avail / max(0.5, sum(_char_w(c) for c in text)))
    while size > floor and _est_w(text, size) > avail:
        size -= 1
    return size


def draw_one(dr, box, text, size=None, color=TEXT_COLOR,
             emboss=EMBOSS_COLOR, align="center", pad=8, weight=800,
             font="noto", line_gap=1.10, emboss_dy=2, max_lines=1):
    """在 box=[x0,y0,x1,y1] 内排一行字（自动缩号 + 压印）。返回实际字号。"""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    size = fit_size(text, bw, size, pad=pad)

    fpath = FONTS.get(font, font)
    f = _load_font(fpath, size, weight)
    tw = f.getlength(text)
    bb = f.getbbox(text)
    th = bb[3] - bb[1]

    if align == "center":
        tx = x0 + (bw - tw) / 2.0
    elif align == "right":
        tx = x1 - pad - tw
    else:
        tx = x0 + pad
    ty = y0 + (bh - th) / 2.0 - bb[1]

    # 压印：先在下方画一道浅色（黏土被压出的亮边），再压深色字
    if emboss:
        dr.text((tx, ty + emboss_dy), text, font=f, fill=emboss)
    dr.text((tx, ty), text, font=f, fill=color)
    return size


def run(spec, scene, out, font="noto", weight=800, pad=8):
    im = Image.open(scene).convert("RGBA")
    dr = ImageDraw.Draw(im)
    rep = []
    for item in spec:
        s = draw_one(dr, item["box"], item["text"],
                     size=item.get("size"), color=tuple(item.get("color", TEXT_COLOR)),
                     emboss=tuple(item["emboss"]) if item.get("emboss") else EMBOSS_COLOR,
                     align=item.get("align", "center"), pad=item.get("pad", pad),
                     weight=item.get("weight", weight), font=font,
                     emboss_dy=item.get("emboss_dy", 2))
        rep.append((item["text"], s))
    im.convert("RGB").save(out)
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--spec", help="JSON 文件：[{box:[x0,y0,x1,y1], text:...}, ...]")
    ap.add_argument("--row", help="四个（或 N 个）卡片左边界 x，逗号分隔")
    ap.add_argument("--box-w", type=int, help="配合 --row：每张卡面宽度")
    ap.add_argument("--y0", type=int, help="配合 --row：文字框上沿 y")
    ap.add_argument("--y1", type=int, help="配合 --row：文字框下沿 y")
    ap.add_argument("--texts", help="配合 --row：逗号分隔的文本")
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--font", default="noto")
    ap.add_argument("--weight", type=int, default=800)
    ap.add_argument("--pad", type=int, default=8)
    a = ap.parse_args()

    if a.spec:
        spec = json.load(open(a.spec, encoding="utf-8"))
    else:
        xs = [int(v) for v in a.row.split(",")]
        texts = a.texts.split(",")
        spec = [{"box": [x, a.y0, x + a.box_w, a.y1], "text": t, "size": a.size}
                for x, t in zip(xs, texts)]
    rep = run(spec, a.scene, a.out, font=a.font, weight=a.weight, pad=a.pad)
    print("->", a.out)
    for t, s in rep:
        print(f"   {t}  size={s}")


if __name__ == "__main__":
    main()
