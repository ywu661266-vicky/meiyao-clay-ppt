# -*- coding: utf-8 -*-
"""
remove_watermark.py — 去除出图平台自动盖在右下角的 AIGC 水印（"AI生成 / WORKBUDDY"）。

背景
----
内置 ImageGen 生成的**每一张图**，右下角都会被平台自动盖一个半透明白色浮标
（上排 "AI生成"，下排 "WORKBUDDY" 品牌条）。这个浮标**不归模型管**——
prompt 里写 "No watermark" 完全无效（已实测）。所以必须在出图后处理掉。

原理
----
水印的位置与尺寸随图片**短边等比缩放**（实测）：
    短边 s = min(W, H)
    水印宽 ≈ 0.1074 * s      水印高 ≈ 0.0488 * s
    右下边距 ≈ 0.0098 * s
例：1024x1024 → 约 110x50 px；1024x576 → 约 62x28 px。
按公式定位后，用 cv2.inpaint(TELEA) 修补空洞。
（对比过"镜像补块"方案：镜像会留下可见补丁痕，inpaint 肉眼干净，故采用 inpaint。）

用法
----
    python scripts/remove_watermark.py <图片文件或目录> [更多路径...]
    python scripts/remove_watermark.py <目录> --suffix _clean --pad 5
输出：同目录下 `<原名><suffix>.png`（不会覆盖原图）。
"""
import argparse
import os
import sys

try:
    import numpy as np
    import cv2
    from PIL import Image
    _HAVE_CV2 = True
except Exception:  # noqa: BLE001
    # 同事新机没装 opencv/numpy 时，降级为纯 PIL 处理，绝不卡死
    from PIL import Image, ImageFilter
    _HAVE_CV2 = False


def watermark_bbox(W, H, pad=5):
    """按短边等比公式算出水印包围盒（含 pad 外扩）。"""
    s = min(W, H)
    w = round(0.1074 * s)
    h = round(0.0488 * s)
    mg = round(0.0098 * s)
    x0 = max(0, W - mg - w - pad)
    y0 = max(0, H - mg - h - pad)
    x1 = min(W, W - mg + pad)
    y1 = min(H, H - mg + pad)
    return x0, y0, x1, y1


def clean_array(arr, pad=5, dilate=2, radius=6):
    """arr: HxWx3 RGB uint8 -> 去水印后的同尺寸数组。"""
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = watermark_bbox(W, H, pad)
    mask = np.zeros((H, W), np.uint8)
    mask[y0:y1, x0:x1] = 255
    if dilate:
        k = np.ones((dilate * 2 + 1, dilate * 2 + 1), np.uint8)
        mask = cv2.dilate(mask, k, 1)
    return cv2.inpaint(arr, mask, radius, cv2.INPAINT_TELEA)


def clean_file(path, suffix="_clean", pad=5):
    im = Image.open(path).convert("RGB")
    if _HAVE_CV2:
        out = clean_array(np.array(im), pad=pad)
        root, ext = os.path.splitext(path)
        dst = f"{root}{suffix}{ext}"
        Image.fromarray(out).save(dst)
        return dst
    # 纯 PIL 降级：水印多在右下角纯色区，用整图轻高斯模糊后只回填该区域
    blurred = im.filter(ImageFilter.GaussianBlur(radius=9))
    x0, y0, x1, y1 = watermark_bbox(*im.size, pad)
    region = blurred.crop((x0, y0, x1, y1))
    im.paste(region, (x0, y0))
    root, ext = os.path.splitext(path)
    dst = f"{root}{suffix}{ext}"
    im.save(dst)
    return dst


def iter_images(targets):
    exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
    for t in targets:
        if os.path.isdir(t):
            for root, _dirs, files in os.walk(t):
                for f in sorted(files):
                    if f.lower().endswith(exts) and "_clean" not in f:
                        yield os.path.join(root, f)
        elif os.path.isfile(t) and t.lower().endswith(exts):
            yield t


def main():
    ap = argparse.ArgumentParser(description="去除出图平台右下角的 AIGC 水印")
    ap.add_argument("targets", nargs="+", help="图片文件或目录")
    ap.add_argument("--suffix", default="_clean", help="输出后缀，默认 _clean")
    ap.add_argument("--pad", type=int, default=5, help="水印框外扩像素，默认 5")
    args = ap.parse_args()

    files = list(iter_images(args.targets))
    if not files:
        print("没有找到可处理的图片")
        return 1
    if not _HAVE_CV2:
        print("[warn] 未检测到 opencv/numpy，已用纯 PIL 降级去水印（效果略弱，建议 pip install opencv-python-headless numpy）")
    for p in files:
        try:
            dst = clean_file(p, suffix=args.suffix, pad=args.pad)
            print(f"[ok] {os.path.basename(p)} -> {os.path.basename(dst)}")
        except Exception as e:  # noqa: BLE001
            print(f"[fail] {p}: {e}", file=sys.stderr)
    print(f"完成：{len(files)} 张")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
