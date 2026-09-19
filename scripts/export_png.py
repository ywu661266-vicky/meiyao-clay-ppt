#!/usr/bin/env python3
"""Meiyao Clay PPT —— 把 .pptx 渲染成 PNG 预览图（需本机装了 PowerPoint）。

用途：交付前把 PPTX 逐页导成 PNG 给用户看真实效果（含真实字体排版），
     避免"只看背景图猜效果"。

用法：
    python export_png.py "out.pptx"                       # 输出到 out_preview/
    python export_png.py "out.pptx" "D:/xx/preview_v2"     # 指定输出目录
    python export_png.py "out.pptx" --width 1920           # 指定宽度（默认 1920）

原理：调用本机 PowerPoint（win32com / COM 自动化），
     Presentation.Export(folder, "PNG", W, H) 会把每页导成 slide1.PNG ...
     需要安装 Microsoft Office PowerPoint；未安装会给出降级说明。
"""
from __future__ import annotations

import argparse
import os
import sys


def export(pptx_path: str, out_dir: str, width: int) -> int:
    pptx_path = os.path.abspath(pptx_path)
    out_dir = os.path.abspath(out_dir)
    if not os.path.exists(pptx_path):
        print(f"[error] 找不到文件：{pptx_path}", file=sys.stderr)
        return 2
    os.makedirs(out_dir, exist_ok=True)

    try:
        import win32com.client  # type: ignore
    except ImportError:
        print("[error] 缺少 pywin32（win32com）。请先安装：pip install pywin32", file=sys.stderr)
        return 3

    app = None
    pres = None
    try:
        app = win32com.client.Dispatch("PowerPoint.Application")
        # WithWindow=False 在部分版本会报错，回退为默认打开
        try:
            pres = app.Presentations.Open(pptx_path, ReadOnly=True, WithWindow=False)
        except Exception:
            pres = app.Presentations.Open(pptx_path, ReadOnly=True)
        height = int(round(width * 9 / 16))
        # Export 会把所有页导成 slide1.PNG, slide2.PNG ...
        pres.Export(out_dir, "PNG", width, height)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] PowerPoint 导出失败：{exc}", file=sys.stderr)
        print("       确认已安装 Microsoft PowerPoint（WPS 不支持该 COM 导出）。", file=sys.stderr)
        return 4
    finally:
        try:
            if pres is not None:
                pres.Close()
        except Exception:
            pass
        try:
            if app is not None:
                app.Quit()
        except Exception:
            pass

    files = sorted(
        [f for f in os.listdir(out_dir) if f.lower().endswith(".png")],
        key=lambda s: (len(s), s),
    )
    print(f"[ok] 已导出 {len(files)} 张到 {out_dir}")
    for f in files:
        print("   -", f)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="PPTX → PNG 预览（PowerPoint COM）")
    ap.add_argument("pptx", help="待导出的 .pptx 路径")
    ap.add_argument("out_dir", nargs="?", default=None, help="输出目录，默认 <pptx名>_preview/")
    ap.add_argument("--width", type=int, default=1920, help="截图宽度，默认 1920")
    args = ap.parse_args()

    out_dir = args.out_dir
    if not out_dir:
        base = os.path.splitext(os.path.abspath(args.pptx))[0]
        out_dir = base + "_preview"
    return export(args.pptx, out_dir, args.width)


if __name__ == "__main__":
    raise SystemExit(main())
