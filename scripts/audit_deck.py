#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_deck.py — 成品验收（交付前必跑）

本脚本不看"好不好看"，只看**结构对不对**。因为 skill 被分享出去之后，
最常见的翻车不是审美问题，而是下面这些"一眼就知道没走完流程"的硬伤：

  1. 整页被模型烘成一张图（正文也交给模型写）→ 中文必错字，且改字要重出图
  2. 图片不是 16:9，嵌进 16:9 页面 → 左右/上下出现空白条
  3. 页面没铺满 → 四周留出纯色边
  4. 没有讲师备注 → 讲课没词
  5. 版式页页一样 → 全册一个模子
  6. 图片分辨率太低 → 投影糊

用法：
    python audit_deck.py a.pptx [b.pptx ...] [--json out.json]

退出码：0 = 全过；1 = 有问题（会列出每一条）
"""
import argparse
import io
import json
import os
import sys

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

EMU_IN = 914400.0
MIN_W = 1600          # 推荐最小图宽（满意版是 1920；低于 1600 提示）
FILL_TOL = 0.004      # 面积覆盖率容差（0.4%）


def _bar_ratio(im):
    """检测左右/上下纯色边条占比（把 4 个角当底色，逐列/逐行比较）"""
    w, h = im.size
    px = im.convert("RGB").load()
    corner = px[1, 1]
    def close(c, t=12):
        return all(abs(c[i] - corner[i]) <= t for i in range(3))
    cols = 0
    for x in range(w):
        same = 0
        for y in range(0, h, max(1, h // 40)):
            if close(px[x, y]):
                same += 1
        if same >= (h // max(1, h // 40)) * 0.95:
            cols += 1
        else:
            break
    rows = 0
    for y in range(h):
        same = 0
        for x in range(0, w, max(1, w // 40)):
            if close(px[x, y]):
                same += 1
        if same >= (w // max(1, w // 40)) * 0.95:
            rows += 1
        else:
            break
    return cols / w, rows / h


def _dhash(im, size=8):
    im = im.convert("L").resize((size + 1, size))
    px = list(im.getdata())
    bits = []
    for r in range(size):
        for c in range(size):
            bits.append(1 if px[r * (size + 1) + c] > px[r * (size + 1) + c + 1] else 0)
    return bits


def _ham(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def audit(path):
    prs = Presentation(path)
    sw, sh = prs.slide_width, prs.slide_height
    slide_ratio = sw / sh
    rep = {
        "file": os.path.basename(path),
        "slides": len(prs.slides._sldIdLst),
        "slide_size_in": [round(sw / EMU_IN, 2), round(sh / EMU_IN, 2)],
        "is_16_9": abs(slide_ratio - 16 / 9) < 0.02,
        "pages": [],
        "problems": [],
    }

    hashes = []
    for idx in range(rep["slides"]):
        s = prs.slides[idx]
        pg = {"n": idx + 1, "shapes": len(s.shapes), "pictures": 0, "texts": 0,
              "cover": 0.0, "img_size": None, "notes": 0, "bar_lr": (0, 0), "issues": []}
        area = 0.0
        big = None
        for shape in s.shapes:
            if shape.shape_type == 13:  # PICTURE
                pg["pictures"] += 1
                area += (shape.width or 0) * (shape.height or 0)
                if big is None or (shape.width or 0) * (shape.height or 0) > big[0]:
                    big = ((shape.width or 0) * (shape.height or 0), shape)
            if shape.has_text_frame and shape.text_frame.text.strip():
                pg["texts"] += 1

        pg["cover"] = round(area / (sw * sh), 3) if sw * sh else 0

        notes = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
        pg["notes"] = len(notes)

        if big is not None:
            shp = big[1]
            im = Image.open(io.BytesIO(shp.image.blob))
            pg["img_size"] = list(im.size)
            iw, ih = im.size
            pg["img_ratio"] = round(iw / ih, 3)
            if abs(iw / ih - slide_ratio) > 0.02:
                pg["issues"].append(
                    "图片比例 %.2f 与页面 %.2f 不符 → 投影出空白边" % (iw / ih, slide_ratio))
            if iw < MIN_W:
                pg["issues"].append("图片宽仅 %dpx，投影会糊" % iw)
            lr, tb = _bar_ratio(im)
            pg["bar_lr"] = (round(lr, 3), round(tb, 3))
            if lr > 0.02 or tb > 0.02:
                pg["issues"].append("图内自带纯色边条 左右%.0f%% / 上下%.0f%%" % (lr * 100, tb * 100))
            hashes.append((idx + 1, _dhash(im)))

        if pg["cover"] < 1 - FILL_TOL:
            pg["issues"].append("元素未铺满（覆盖 %.0f%%）" % (pg["cover"] * 100))
        # 备注只作提示，不列问题（满意版本身就没备注）
        if pg["notes"] < 10:
            pg["warn"] = "没写讲师备注（建议补）"

        rep["pages"].append(pg)

    # 版式撞车：dHash 距离 < 10 视为同一版式
    dup = []
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            d = _ham(hashes[i][1], hashes[j][1])
            if d < 10:
                dup.append((hashes[i][0], hashes[j][0], d))
    rep["layout_dups"] = dup

    for pg in rep["pages"]:
        for it in pg["issues"]:
            rep["problems"].append("P%d %s" % (pg["n"], it))
    if dup:
        rep["problems"].append(
            "版式撞车 %d 对：%s" % (len(dup), ", ".join("P%d≈P%d" % (a, b) for a, b, _ in dup[:12])))
    if not rep["is_16_9"]:
        rep["problems"].append("页面不是 16:9")
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out = []
    bad = 0
    for f in a.files:
        r = audit(f)
        out.append(r)
        print("=" * 72)
        print("%s  %d 页  页面 %sx%s 英寸  16:9=%s" %
              (r["file"], r["slides"], r["slide_size_in"][0], r["slide_size_in"][1], r["is_16_9"]))
        for pg in r["pages"]:
            flag = "OK " if not pg["issues"] else "!! "
            print("  %sP%-2d 图%d 文%d 覆盖%3.0f%% 备注%3d字 图%s %s" %
                  (flag, pg["n"], pg["pictures"], pg["texts"], pg["cover"] * 100,
                   pg["notes"], pg["img_size"], "; ".join(pg["issues"])))
        if r["problems"]:
            bad += 1
            print("  ---- 问题 %d 条 ----" % len(r["problems"]))
            for p in r["problems"][:40]:
                print("   ·", p)
        else:
            print("  ---- 全部通过 ----")
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("json ->", a.json)
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
