#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compose_page.py — 页面合成器：背景板 + 独立黏土件（黏土字 / 黏土卡片 / 黏土胶囊）→ 整页成品

这是 meiyao-clay-ppt 的新核心：**字和图分开做，最后合成**。
- 背景板来自 ImageGen（黏土场景 + 完整全身人物 + 留白），本来就不带正文
- 所有文字都是 clay_text.py 现场"捏"出来的黏土件，透明底，随便摆、随便改
- 改文案 = 改 JSON 里的字符串，不重新出图、不花积分

用法：
    python compose_page.py --config pages.json

pages.json 结构：
{
  "pages": [
    {
      "bg": "bg/page07_clean.png",
      "out": "out/page07.png",
      "elements": [
        {"type":"text",  "text":"我踩的坑", "cap":54, "x":120, "y":40, "color":"cream"},
        {"type":"card",  "head":"只抄了描述文字", "body":"人物每页都变样，一个啾啾变成两个丸子头",
                         "width":524, "x":40, "y":96, "accent":"orange"},
        {"type":"badge", "text":"3 小时实操课", "cap":32, "x":70, "y":470, "color":"orange"}
      ]
    }
  ]
}
坐标 x/y 以**成品页面像素**为单位（背景图原尺寸），左上角为原点。
"""
import argparse
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clay_text import render_clay_text, render_clay_badge, render_clay_card  # noqa

# 配色名 → RGB，跟随风格库；shadow 用画面里最深的那个色系，字才"贴得住"
PALETTE = {
    "cream":  (241, 231, 214),
    "white":  (247, 243, 236),
    "orange": (240, 169, 60),
    "yellow": (238, 190, 74),
    "green":  (150, 196, 92),
    "mint":   (140, 205, 175),
    "pink":   (232, 160, 170),
    "purple": (126, 98, 196),
    "deep":   (78, 63, 138),
    "brown":  (140, 106, 78),
    "navy":   (46, 62, 112),
}
SHADOW = {
    "purple": (40, 30, 78),
    "deep":   (40, 30, 78),
    "navy":   (18, 26, 54),
    "brown":  (58, 40, 28),
}


def _c(name, default=(241, 231, 214)):
    if isinstance(name, (list, tuple)):
        return tuple(name)
    return PALETTE.get(str(name).lower(), default)


def _shadow(name):
    if isinstance(name, (list, tuple)):
        return tuple(name)
    return SHADOW.get(str(name).lower(), (40, 30, 78))


def compose(cfg):
    bg = Image.open(cfg["bg"]).convert("RGBA")
    if "size" in cfg:
        bg = bg.resize(tuple(cfg["size"]), Image.LANCZOS)
    for el in cfg.get("elements", []):
        t = el.get("type", "text")
        col = _c(el.get("color", "cream"))
        sh = _shadow(el.get("shadow", "purple"))
        sc = el.get("scale", 1.0)
        if t == "text":
            im = render_clay_text(
                el["text"],
                cap_height=el.get("cap", 60) * sc,
                base=col,
                font=el.get("font", "noto"),
                weight=el.get("weight", 900),
                shadow=sh,
                letter_gap=el.get("letter_gap", 0.052),
                outline=el.get("outline", 0.0) * sc if el.get("outline") else 0.0,
                out_path=el.get("save"),
            )
        elif t == "badge":
            im = render_clay_badge(
                el["text"],
                cap_height=el.get("cap", 32) * sc,
                base=col,
                text_color=_c(el.get("text_color", "brown"), (70, 52, 38)),
                shadow=sh,
                extra_left=el.get("extra_left", 0.0),
                out_path=el.get("save"),
            )
        elif t == "card":
            im = render_clay_card(
                el.get("head", ""),
                el.get("body", ""),
                width=el.get("width", 520) * sc,
                head_size=el.get("head_size", 26) * sc,
                body_size=el.get("body_size", 16) * sc,
                base=col,
                shadow=sh,
                accent=_c(el["accent"]) if el.get("accent") else None,
                out_path=el.get("save"),
            )
        else:
            raise ValueError("unknown element type: %s" % t)
        x, y = int(el.get("x", 0)), int(el.get("y", 0))
        if el.get("align") == "right":
            x = bg.width - im.width - x
        elif el.get("align") == "center":
            x = (bg.width - im.width) // 2 + x
        bg.alpha_composite(im, (x, y))
    out = cfg["out"]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    bg.convert("RGB").save(out, quality=cfg.get("quality", 95))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", default=None, help="只合成指定 out 文件名（调试用）")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    done = []
    for pg in cfg["pages"]:
        if a.only and a.only not in pg["out"]:
            continue
        done.append(compose(pg))
        print("ok ->", pg["out"])
    print("total", len(done))


if __name__ == "__main__":
    main()
