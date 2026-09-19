#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
patch_region.py — 局部抹除（inpaint）：去掉画面里多余的道具、残留水印、重复元素。

为什么需要（2026-09-19 实测）：
  图片模型经常"多给一个"东西 —— 本次头部本该只有 1 个红心，出了 2 个；
  货架上还多冒出一个白色小人偶。重出图一次 5~10 积分且提示词未必听话，
  而局部 inpaint 用周围像素补回来，几乎无痕、不花积分。

用法：
    python patch_region.py <图> --box 890,55,980,165 --out fixed.png
    python patch_region.py <图> --box 890,55,980,165 --box 100,200,180,260 --out fixed.png

坐标是像素 (x0,y0,x1,y1)，左上为原点；建议框比目标物多留 8~12px 余量。
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    print('[!] 需要 opencv：pip install opencv-python-headless')
    sys.exit(1)


def patch(path, boxes, out_path, radius=5):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im)[:, :, ::-1].astype(np.uint8).copy()   # RGB -> BGR
    mask = np.zeros(a.shape[:2], np.uint8)
    for (x0, y0, x1, y1) in boxes:
        mask[max(0, y0):y1, max(0, x0):x1] = 255
    res = cv2.inpaint(a, mask, radius, cv2.INPAINT_TELEA)
    Image.fromarray(res[:, :, ::-1]).save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('--box', action='append', required=True,
                    help='x0,y0,x1,y1（可重复传多次抹多个区域）')
    ap.add_argument('--radius', type=int, default=5, help='修补半径，默认 5')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    boxes = [tuple(int(v) for v in b.split(',')) for b in a.box]
    out = a.out or os.path.splitext(a.target)[0] + '_patched.png'
    print('->', patch(a.target, boxes, out, a.radius), '  抹除区域:', boxes)


if __name__ == '__main__':
    main()
