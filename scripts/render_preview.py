#!/usr/bin/env python3
"""Meiyao Clay PPT —— 离线预览渲染器：slides.json → 逐页 PNG。

为什么需要它：
    本机 PowerPoint 的 COM 自动化常被系统/沙箱拒绝（报"服务器运行失败"），
    无法把 .pptx 渲染成图。本脚本用 PIL **按与 build_pptx.py 相同的几何**，
    把「背景图 + 真实字体正文」直接画成 1920×1080 PNG，用于交付前预览。
    它是**近似预览**：字体/行距与 PowerPoint 可能有细微差异，
    但足以判断版式、字数、留白是否合适。

用法：
    python render_preview.py --config slides.json --out preview_dir
    python render_preview.py --config slides.json --out preview_dir --width 1920
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# —— 与 build_pptx.py 保持一致的几何（英寸）——
SLIDE_W_IN, SLIDE_H_IN = 13.333, 7.5
PX_PER_IN = 144.0  # 1920 / 13.333

CARD_FILL = (255, 246, 227)
CARD_ACCENT = (107, 75, 181)
CARD_HEAD = (74, 44, 107)
CARD_BODY = (58, 51, 80)
BADGE_TEXT = (255, 255, 255)

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"


def inpx(v: float) -> float:
    return v * PX_PER_IN


def hex_rgb(h: str):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap_cjk(text: str, font, max_w: float, draw: ImageDraw.ImageDraw) -> list[str]:
    """按可用宽度折行；CJK 逐字、ASCII 按词。"""
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        trial = cur + ch
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def content_zone(side: str):
    top, bottom = 1.95, 6.95
    h = bottom - top
    if side == "right":
        return 8.55, top, 4.05, h
    if side == "full":
        return 0.9, top, SLIDE_W_IN - 1.8, h
    return 0.72, top, 6.95, h


def draw_cards(draw, base, zone, items, accent, chead, cbody):
    left, top, width, height = [inpx(v) for v in zone]
    n = len(items)
    if n == 0:
        return
    gap = inpx(0.22)
    card_h = (height - gap * (n - 1)) / n

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # —— 第一遍：把卡片形状画在透明层上，再整体合成到 base（避免盖住文字）——
    for i, it in enumerate(items):
        y = top + i * (card_h + gap)
        od.rounded_rectangle([left, y, left + width, y + card_h], radius=int(inpx(0.16)),
                             fill=CARD_FILL + (235,))
        bar_w = inpx(0.13)
        od.rounded_rectangle([left, y + inpx(0.12), left + bar_w, y + card_h - inpx(0.12)],
                             radius=int(bar_w / 2), fill=accent + (255,))
        d = inpx(0.56)
        bx, by = left + inpx(0.32), y + (card_h - d) / 2
        od.ellipse([bx, by, bx + d, by + d], fill=accent + (255,))
    base.alpha_composite(overlay)

    # —— 第二遍：文字/序号画在 base 最上层 ——
    f_head = load_font(FONT_BOLD, int(inpx(17 / 72)))
    f_body = load_font(FONT_REG, int(inpx(13 / 72)))
    f_badge = load_font(FONT_BOLD, int(inpx(16 / 72)))
    draw = ImageDraw.Draw(base)

    for i, it in enumerate(items):
        y = top + i * (card_h + gap)
        d = inpx(0.56)
        bx, by = left + inpx(0.32), y + (card_h - d) / 2
        draw.text((bx + d / 2, by + d / 2), str(i + 1), font=f_badge,
                  fill=BADGE_TEXT, anchor="mm")
        # 文字
        tx = left + inpx(1.12)
        tw = width - inpx(1.42)
        head = str(it.get("head", "") or "")
        body = str(it.get("body", "") or "")
        heads = wrap_cjk(head, f_head, tw, draw) if head else []
        bodies = wrap_cjk(body, f_body, tw, draw) if body else []
        lh_head = inpx(17 / 72) * 1.22
        lh_body = inpx(13 / 72) * 1.45
        total = len(heads) * lh_head + len(bodies) * lh_body + (inpx(0.05) if heads and bodies else 0)
        cy = y + (card_h - total) / 2
        for ln in heads:
            draw.text((tx, cy), ln, font=f_head, fill=chead)
            cy += lh_head
        if heads and bodies:
            cy += inpx(0.05)
        for ln in bodies:
            draw.text((tx, cy), ln, font=f_body, fill=cbody)
            cy += lh_body


def draw_steps(draw, base, zone, items, accent, chead, cbody):
    left, top, width, height = [inpx(v) for v in zone]
    n = len(items)
    if n == 0:
        return
    gap = inpx(0.2)
    step_h = (height - gap * (n - 1)) / n
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    line_x = left + inpx(0.28)
    if n > 1:
        od.rounded_rectangle([line_x - inpx(0.02), top + inpx(0.3), line_x + inpx(0.02),
                              top + height - inpx(0.3)], radius=inpx(0.02), fill=accent + (140,))
    d = inpx(0.52)
    for i in range(n):
        y = top + i * (step_h + gap)
        dx, dy = line_x - d / 2, y + (step_h - d) / 2
        od.ellipse([dx, dy, dx + d, dy + d], fill=accent + (255,))
    base.alpha_composite(overlay)

    f_head = load_font(FONT_BOLD, int(inpx(17 / 72)))
    f_body = load_font(FONT_REG, int(inpx(13 / 72)))
    f_dot = load_font(FONT_BOLD, int(inpx(15 / 72)))
    draw = ImageDraw.Draw(base)
    for i, it in enumerate(items):
        y = top + i * (step_h + gap)
        dx, dy = line_x - d / 2, y + (step_h - d) / 2
        draw.text((dx + d / 2, dy + d / 2), str(i + 1), font=f_dot, fill=BADGE_TEXT, anchor="mm")
        tx = left + inpx(0.78)
        tw = width - inpx(0.95)
        head = str(it.get("head", "") or "")
        body = str(it.get("body", "") or "")
        heads = wrap_cjk(head, f_head, tw, draw) if head else []
        bodies = wrap_cjk(body, f_body, tw, draw) if body else []
        lh_head = inpx(17 / 72) * 1.22
        lh_body = inpx(13 / 72) * 1.45
        total = len(heads) * lh_head + len(bodies) * lh_body + (inpx(0.05) if heads and bodies else 0)
        cy = y + (step_h - total) / 2
        for ln in heads:
            draw.text((tx, cy), ln, font=f_head, fill=chead)
            cy += lh_head
        if heads and bodies:
            cy += inpx(0.05)
        for ln in bodies:
            draw.text((tx, cy), ln, font=f_body, fill=cbody)
            cy += lh_body



def main() -> int:
    ap = argparse.ArgumentParser(description="slides.json → 逐页 PNG 预览")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1920)
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    slides = cfg.get("slides") or []
    if not slides:
        print("[error] slides.json 里没有 slides", file=sys.stderr)
        return 1

    W = args.width
    H = int(round(W * 9 / 16))
    os.makedirs(args.out, exist_ok=True)
    default_mode = (cfg.get("default_text_mode") or "baked").lower()

    for idx, item in enumerate(slides, 1):
        bg = item.get("image")
        if bg and os.path.exists(bg):
            img = Image.open(bg).convert("RGBA").resize((W, H), Image.LANCZOS)
        else:
            img = Image.new("RGBA", (W, H), (58, 42, 86, 255))
        draw = ImageDraw.Draw(img)

        mode = (item.get("text_mode") or default_mode).lower()
        if mode == "overlay":
            items = item.get("items") or []
            layout = (item.get("layout") or ("cards" if items else "")).lower()
            side = (item.get("content_side") or "left").lower()
            zone = content_zone(side)
            accent = hex_rgb(item.get("accent_color", "#6B4BB5"))
            chead = hex_rgb(item.get("chead_color", "#4A2C6B"))
            cbody = hex_rgb(item.get("cbody_color", "#3A3350"))
            if layout == "cards" and items:
                draw_cards(draw, img, zone, items, accent, chead, cbody)
            elif layout == "steps" and items:
                draw_steps(draw, img, zone, items, accent, chead, cbody)

        out = os.path.join(args.out, f"{idx:02d}.png")
        img.convert("RGB").save(out)
        print(f"[ok] {out}")
    print(f"[ok] 共 {len(slides)} 页 → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
