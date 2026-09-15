#!/usr/bin/env python3
"""Meiyao Clay PPT —— 背景图 → 16:9 PPTX 合成脚本。

把 ImageGen 生成的黏土风页面铺满 16:9 幻灯片，并写入讲师备注。

【默认行为 text_mode="baked"】
    图里的标题/标签已经是「黏土立体字」（烘进画面），脚本**不再叠加任何扁平文字**，
    避免压出双层字、破坏黏土质感。这是本 skill 的推荐用法。

【text_mode="overlay"】
    仅用于「成段正文 / 需要可编辑」的场景，才会在奶油铭牌 safe 区叠加文字，
    并主动避开右下角水印。

用法：
    python build_pptx.py --config slides.json --out "主题_黏土风.pptx"
    python build_pptx.py --config slides.json --out out.pptx --font "Microsoft YaHei"

slides.json 结构：
{
  "title": "整套课的标题（仅用于元数据）",
  "default_font": "Microsoft YaHei",
  "default_text_mode": "baked",          // baked（默认）| overlay
  "slides": [
    {
      "image": "D:/.../cover.png",
      "notes": "讲师备注",                // 可选
      // 图里已烘过黏土标题的页 —— 不要写 title，否则会叠两层字
      "text_mode": "baked"
    },
    {
      "image": "D:/.../body.png",
      "text_mode": "overlay",             // 需要可编辑正文时才用
      "title": "标题文字",
      "subtitle": "副标题",                // 可选
      "bullets": ["要点一", "要点二"],      // 可选
      "notes": "讲师备注",
      "text_side": "left",                // left | right | top，默认 left
      "title_color": "1E3A5F"             // 可选，十六进制（默认深蓝黑）
    }
  ]
}
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
EMU_PER_INCH = 914400

DEFAULT_FONT = "Microsoft YaHei"
TITLE_COLOR_DEFAULT = "1E3A5F"
SUBTITLE_COLOR = "3E5C7A"
BODY_COLOR = "24384F"
PANEL_FILL = "FFF6E3"


def hex_rgb(value: str) -> RGBColor:
    value = value.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def set_run_font(run, name: str, size: float, bold: bool = False, color: RGBColor | None = None) -> None:
    """设置字体，并同时写入 latin / ea / cs，保证中文不回退成宋体。"""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = name
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", name)


def set_alpha(shape, percent: int) -> None:
    """给纯色填充加透明度（percent = 不透明度 0-100）。"""
    solid = shape.fill._xPr.find(qn("a:solidFill"))
    if solid is None:
        return
    clr = solid.find(qn("a:srgbClr"))
    if clr is None:
        return
    for child in list(clr):
        if child.tag == qn("a:alpha"):
            clr.remove(child)
    alpha = clr.makeelement(qn("a:alpha"), {"val": str(int(percent * 1000))})
    clr.append(alpha)


def add_panel(slide, left: Emu, top: Emu, width: Emu, height: Emu) -> None:
    """奶油色半透明圆角底板，保证文字可读。"""
    from pptx.enum.shapes import MSO_SHAPE

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = hex_rgb(PANEL_FILL)
    set_alpha(box, 88)
    box.line.fill.background()
    box.shadow.inherit = False
    return box


def add_textbox(slide, left, top, width, height):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tf


def build_slide(prs: Presentation, item: dict, default_font: str,
                default_text_mode: str = "baked") -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    image = item.get("image")
    if image and os.path.exists(image):
        slide.shapes.add_picture(image, 0, 0, width=prs.slide_width, height=prs.slide_height)
    else:
        print(f"[warn] 背景图不存在，已跳过: {image}", file=sys.stderr)

    notes = item.get("notes")
    if notes:
        slide.notes_slide.notes_text_frame.text = str(notes)

    mode = (item.get("text_mode") or default_text_mode).lower()

    # ---- baked：图里已有黏土立体字，脚本不再叠任何扁平文字 ----
    if mode != "overlay":
        if item.get("title") or item.get("subtitle") or item.get("bullets"):
            print(
                f"[warn] text_mode=baked：图为 {os.path.basename(str(image))}，"
                "已跳过脚本叠字（避免压出双层字）。若确实要叠可编辑正文，请设 text_mode=\"overlay\"。",
                file=sys.stderr,
            )
        return

    # ---- overlay：仅用于成段正文/需要可编辑时 ----
    side = (item.get("text_side") or "left").lower()
    if side == "top":
        panel_left, panel_top = Inches(1.4), Inches(0.5)
        panel_w, panel_h = SLIDE_W - Inches(2.8), Inches(1.9)
    elif side == "right":
        panel_left, panel_top = Inches(7.2), Inches(1.5)
        panel_w, panel_h = Inches(5.4), Inches(4.6)
    else:
        panel_left, panel_top = Inches(0.7), Inches(1.5)
        panel_w, panel_h = Inches(5.4), Inches(4.6)

    title = item.get("title")
    bullets = item.get("bullets") or []
    subtitle = item.get("subtitle")
    if title or bullets or subtitle:
        add_panel(slide, panel_left, panel_top, panel_w, panel_h)

    has_bullets = bool(bullets)
    pad_x = Inches(0.35)
    text_left = panel_left + pad_x
    text_w = panel_w - pad_x * 2

    if title:
        title_h = Inches(1.25) if has_bullets else panel_h - Inches(0.5)
        tf = add_textbox(slide, text_left, panel_top + Inches(0.22), text_w, title_h)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = str(title)
        set_run_font(run, default_font, 30 if has_bullets else 36, True,
                     hex_rgb(item.get("title_color", TITLE_COLOR_DEFAULT)))

    if subtitle:
        tf = add_textbox(slide, text_left, panel_top + Inches(1.35), text_w, Inches(0.6))
        run = tf.paragraphs[0].add_run()
        run.text = str(subtitle)
        set_run_font(run, default_font, 16, False, hex_rgb(SUBTITLE_COLOR))

    if has_bullets:
        body_top = panel_top + (Inches(1.95) if subtitle else Inches(1.6))
        body_h = panel_h - (body_top - panel_top) - Inches(0.3)
        tf = add_textbox(slide, text_left, body_top, text_w, body_h)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        for i, bullet in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(10)
            p.line_spacing = 1.3
            run = p.add_run()
            run.text = f"· {bullet}"
            set_run_font(run, default_font, 16, False, hex_rgb(BODY_COLOR))


def main() -> int:
    ap = argparse.ArgumentParser(description="把黏土风背景图合成为可编辑 16:9 PPTX")
    ap.add_argument("--config", required=True, help="slides.json 路径")
    ap.add_argument("--out", required=True, help="输出 .pptx 路径")
    ap.add_argument("--font", default=None, help=f"中文字体，默认 {DEFAULT_FONT}")
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    font = args.font or cfg.get("default_font") or DEFAULT_FONT
    text_mode = (cfg.get("default_text_mode") or "baked").lower()
    slides = cfg.get("slides") or []
    if not slides:
        print("[error] slides.json 里没有 slides", file=sys.stderr)
        return 1

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    if cfg.get("title"):
        prs.core_properties.title = str(cfg["title"])

    for item in slides:
        build_slide(prs, item, font, text_mode)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    prs.save(args.out)
    print(f"[ok] 已生成 {len(slides)} 页：{args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
