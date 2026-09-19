#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""可移植性验证 —— 回答用户那句「**人家拿了我的 skill，还能出同款吗？**」

做法：把 `clay_text._FONT_CANDIDATES` 里所有**非内置**的系统字体路径清空，
模拟"别人拷走 skill 到一台没装中文字体的机器上"，然后渲一遍标题、比金标准。

PASS = 只靠 skill 自带字体也能出同款标题 → 可移植性成立。

用法：
    python verify_portable.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import Image

import clay_text
import verify_title as V          # 复用同一套量测口径，避免"两把尺子"

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILTIN_DIR = os.path.abspath(os.path.join(SKILL, 'assets', 'fonts'))
GOLD = os.path.join(SKILL, 'assets', 'ref-title', 'gold_metrics.json')


def go_clean_machine():
    """把候选表里的系统字体全部删掉，只留 skill 内置的那一份。"""
    killed = []
    for name, cands in clay_text._FONT_CANDIDATES.items():
        keep = [p for p in cands if os.path.abspath(p).startswith(BUILTIN_DIR)]
        if not keep:
            keep = [os.path.join('__NO_SUCH_DIR__', 'missing.ttf')]
        killed.append((name, len(cands) - len(keep)))
        clay_text._FONT_CANDIDATES[name] = keep
    return killed


def check(gold, tag):
    t = clay_text.render_title_clay(gold.get('text', '改法清单'),
                                   cap_height=gold.get('cap_height', 80))
    bg = Image.new('RGB', t.size, V.WALL)
    bg.paste(t, (0, 0), t)
    got = V.measure(np.asarray(bg))

    ok = True
    print('\n【%s】' % tag)
    print('%-14s %16s %16s %10s  %s' % ('指标', '金标准', '实测', '偏差', '判定'))

    def line(name, g, v, tol):
        nonlocal ok
        d = float(v) - float(g)
        good = abs(d) <= tol
        ok = ok and good
        print('%-14s %16s %16s %+10.4f  %s' % (name, '%.4f' % g, '%.4f' % v, d,
                                               'OK' if good else 'FAIL'))

    gw, gh = gold['ink_wh']
    vw, vh = got['ink_wh']
    good = abs(vw - gw) <= gw * 0.05 and abs(vh - gh) <= 3
    ok = ok and good
    print('%-14s %16s %16s %10s  %s' % ('ink 宽x高', '%dx%d' % (gw, gh), '%dx%d' % (vw, vh),
                                        '%+d/%+d' % (vw - gw, vh - gh), 'OK' if good else 'FAIL'))
    line('宽高比', gold['aspect_ratio'], got['aspect_ratio'], V.TOL['aspect_ratio'])
    line('边宽/字高', gold['edge_over_height'], got['edge_over_height'], V.TOL['edge_over_height'])
    for key, name in (('face_median_rgb', '字面中位色'), ('edge_median_rgb', '边色中位色')):
        d = max(abs(a - b) for a, b in zip(gold[key], got[key]))
        good = d <= V.TOL[key]
        ok = ok and good
        print('%-14s %16s %16s %10d  %s' % (name, gold[key], got[key], d,
                                            'OK' if good else 'FAIL'))
    good = got['base_plate_ratio'] <= V.TOL['base_plate_ratio']
    ok = ok and good
    print('%-14s %16s %16s %10s  %s' % ('底板横条比', '%.3f' % gold['base_plate_ratio'],
                                        '%.3f' % got['base_plate_ratio'], '-',
                                        'OK' if good else 'FAIL'))
    return ok


def main():
    if not os.path.exists(GOLD):
        print('缺少金标准：%s' % GOLD)
        return 2
    gold = json.load(open(GOLD, encoding='utf-8'))

    print('=' * 66)
    print('可移植性验证：模拟「别人拷走 skill 到没有中文字体的机器」')
    print('=' * 66)
    print('\n[改造前] 本机字体解析：')
    print(clay_text.font_report().replace('字体解析：', '', 1))

    killed = go_clean_machine()
    print('\n[模拟] 已移除的系统字体条目：')
    for name, n in killed:
        if n:
            print('  %-5s 去掉 %d 个系统候选' % (name, n))
    print('\n[改造后] 干净机器字体解析：')
    print(clay_text.font_report().replace('字体解析：', '', 1))

    ok = check(gold, '干净机器 · 只靠 skill 内置字体')

    print('\n' + '=' * 66)
    print('结论：%s' % ('PASS —— 别人拷走 skill 也能出同款标题（字体自包含）' if ok
                     else 'FAIL —— 可移植性不成立，检查 assets/fonts/NotoSansSC-VF.ttf'))
    print('=' * 66)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
