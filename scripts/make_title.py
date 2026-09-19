#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""标题一键生成 —— 页面上所有标题都从这里出，不许再写第二套标题代码。

用法：
    python make_title.py "从改到造" 88                     # 出 PNG（同名 .png）
    python make_title.py "改法清单" 91 out/title.png       # 指定输出路径
    python make_title.py "改法清单" 91 -o out/title.png    # 同上（--out / -o 均可）
    python make_title.py "从改到造" 88 --on 底图.png 26 26 out.png
        # 直接贴到底图的 (x, y) 上，省掉手工 composite

参数规则（**只允许调这两个**）：
    cap_height  字体高度（≈ 成品 ink 高）。第 9 页 = 91；版面窄时 84~88。
    letter_gap  字距比例，默认 0（第 9 页实测字间空隙 ≈ 0）。**不要为了"松一点"调大**。

其余参数（stretch_x / bold / pad / 面色 / 垫色 / 影）全部由第 9 页实测标定，
**一律不要传** —— 改了就不是同一套了。要动先跑 verify_title.py 看还 PASS 吗。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
import clay_text


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    text = argv[1]
    cap = int(argv[2])
    on = None
    x = y = 0
    out = None
    rest = argv[3:]
    if rest and rest[0] == '--on':
        if len(rest) < 4:
            print('错误：--on 需要三个值：底图路径 x y')
            return 2
        on, x, y = rest[1], int(rest[2]), int(rest[3])
        rest = rest[4:]
    if rest and rest[0] in ('--out', '-o'):
        if len(rest) < 2:
            print('错误：--out / -o 后面要跟输出路径')
            return 2
        out = rest[1]
        rest = rest[2:]
    if out is None and rest:
        out = rest[0]
    if not out:
        out = '%s_%d.png' % (text, cap)
    if not os.path.splitext(out)[1]:
        out += '.png'

    d = os.path.dirname(os.path.abspath(out))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

    t = clay_text.render_title_clay(text, cap_height=cap, letter_gap=0.0)
    if on:
        if not os.path.isfile(on):
            print('错误：找不到底图 %s' % on)
            return 2
        base = Image.open(on).convert('RGBA')
        base.alpha_composite(t, (x, y))
        base.convert('RGB').save(out)
        print('已贴到 %s 的 (%d,%d) → %s  [标题 %dx%d]' % (on, x, y, out, t.width, t.height))
    else:
        t.save(out)
        print('已生成 %s  [标题 %dx%d]' % (out, t.width, t.height))
    print('提示：交付前跑一次 verify_title.py 确认没偏离金标准。')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
