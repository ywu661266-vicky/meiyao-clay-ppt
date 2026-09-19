#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clay_band.py v2 — 「八六式左列清单条」渲染器 + 合成器（层叠黏土徽章版）

为什么需要它（2026-09-19 实测）：
  八六老师课件页的招牌结构是**左列黏土胶囊条**（左侧圆形徽章 + 奶油色文字）。
  实测把这四条交给图片模型烘字，两次都翻车（版式塌成 2×2、关键词重复）。
  结论：**这种高度重复的条状组件不要交给图片模型**，用真字体渲染 → 零错字、几何精确、
  改文案不用重出图。这与 skill 的「分件合成」第一性原理一致。

v2 相对 v1 的三处修正（2026-09-19 晚 · 用户第三轮反馈后逐像素重测 p10）：
  ① **徽章从"平涂圆+细线勾"改成「层叠黏土」**（这是用户点名的那条）：
     参考图里它是**先贴一个圆饼、再贴一块对勾**，两层各自有厚度 ——
       圆饼：落地投影 → 底侧壁（压深的橄榄绿）→ 顶面（左上受光径向渐变）→ 上缘亮边 + 下缘内影
       对勾：自己的投影 → 侧壁 → 顶面（奶油白 + 上缘高光）
     且**没有描边**，立体全靠明暗 + 侧壁，描边一加就回到"图标感"。
  ② **条内文字改走 `render_clay_text` 的黏土浮雕字**（v1 是平涂字 + 黑 halo，读起来像贴纸）：
     奶油白 (248,242,230) + 侧面厚度 + 上缘高光 + 落在条面上的软影，**不要黑描边**。
  ③ **条带几何重测**（v1 的 5.4%/1.5% 是 p02 底栏的数，套错到 p10 列式了）：
     见下方 GEOM 常量。

设计规格（对齐八六 p10 **逐像素实测** 2026-09-19 晚第二轮修正 · 帧 1467×825）：
  条高 70px = 8.48% 帧高 · 条间缝 17px = 2.06% 帧高 · 条中心间距 87px；
  条带占 y 18.9%~90.5%（总块高 71.6% 帧高）；条左起 4.43%、右止 33.6%；
  徽章直径 56px = **条高 × 0.80**（完全收在条内，v1 的 1.12 是错的）；
  徽章左端距条左端 20px = 条高 × 0.29；徽章-文字间距 33px = 条高 × 0.47；
  文字高 34px = **条高 × 0.49**；文字的白色是奶油 (234,224,205)；
  徽章绿 = 橄榄黄绿，顶面 (178,189,95) → 底部侧壁 (70,90,2)，**无描边**。

  ⚠️ 条数少于参考时（参考 7 条、本课 4 条）：**条高与缝按比例放大以填满同一竖向区间**，
     不要留空 —— 留空就是用户说的"空、有废元素"。

单行可选字段：`x1_ratio`（覆盖该条右端；想让四条齐平就都填同一个值）。

用法（CLI）：
    python clay_band.py run --scene scene.png --rows rows.json --out page.png --top 138
    python clay_band.py --rows rows.json --out band.png --width 1024
    python clay_band.py demo --out demo.png

rows.json：
[
  {"key":"先锁人物锚点","bg":[124,102,172],"badge":[140,155,45],"icon":"check"},
  ...
]
可用 icon：check / dots / gear / bird / wrench / star / pin
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clay_text import (_blur, _darken, _grain, _lighten, _load_font, _mix,
                       _over, _rgb, _shift, render_clay_text, render_crisp_text, FONTS)

# ---------------------------------------------------------------- 规格常量
# 参考 p10 实测比例（帧高 825 基准）——改这里就是改全站风格
G_BAR_H   = 0.0848     # 条高 ÷ 帧高
G_GAP     = 0.0206     # 条间缝 ÷ 帧高
G_LEFT    = 0.0443     # 条左端 ÷ 帧宽
G_RIGHT   = 0.336      # 条右端 ÷ 帧宽（参考原值 33.6%）
# ⚠️ 条数少时**不要靠放大元素**填满左列 —— 那会让徽章/文字等比膨胀，失去参考的精致感。
#    参考的"满"是**信息密度**（7 条），不是元素大。4 条的取舍是：
#    「条高只放大 ~27%（62 vs 49）、右端保持参考值」→ 条带占帧高约 51%，
#     左列下方空出来的那一段交给**场景里的散落小道具**（石粒 / 草叶 / 齿轮屑）去点满。
G_RIGHT_N4 = 0.336     # 4 条时的条右端 ÷ 帧宽（同参考值：字号按比例缩，6 字仍放得下）
G_BAR_H_N4 = 52        # 4 条时的条高（px@576 帧高；参考原值 49 —— 只放大 6%）
G_GAP_N4  = 13         # 4 条时的条间缝（参考原值 12）
G_TOP     = 0.189      # 条带顶端 ÷ 帧高
G_BADGE_R = 0.80       # 徽章直径 ÷ 条高（实测 56/70）
G_BADGE_X = 0.29       # 徽章左端到条左端距离 ÷ 条高
G_BADGE_G = 0.47       # 徽章右端到文字左端 ÷ 条高
G_TEXT_H  = 0.45       # 文字高 ÷ 条高（参考实测 0.49，但参考字重更轻；同视觉校准取 0.45）
G_TEXT_GAP = 0.11      # 字间距 ÷ 字高（86 老师实测"视觉间隙 ≈ 字高 20%"，扣掉 CJK 字形自带留白后取 0.11）
G_TEXT_STROKE = 1.6    # 字的外描边厚（成品像素；右下侧再 ×1.55 —— 光在左上）
TEXT_STROKE_COLOR = (52, 32, 86)   # 描边深紫（对比条面 108,74,155 —— 深色描边才把字"切"得开）

BADGE_GREEN  = (128, 144, 38)    # 徽章绿·中调（参考实测 129,145,37 ~ 107,125,21）
BADGE_TOP    = (168, 180, 74)    # 顶面最高亮
BADGE_SIDE   = (38, 26, 60)      # 底侧壁（参考实测 44,31,68 —— 是**暗紫黑**，不是绿）
CHECK_BASE   = (236, 227, 208)   # 对勾奶油白（实测 234,224,205）
TEXT_CREAM   = (234, 224, 205)   # 条内文字奶油白（= 86 老师实测值）
TEXT_DARK    = (44, 28, 22)      # 深棕近黑（印在浅色条上时用）
BAR_BASE     = (108, 74, 155)    # 条面基色（参考实测 108,74,155 —— v1 的 124,102,172 偏亮偏灰）
SEAM_RGB     = (12, 8, 32)       # 条间缝的暗底（参考实测缝 rgb(16,10,39)，比背景还暗）
BADGE_SHADOW = (36, 23, 61)      # 徽章落影（参考实测）

BAR_COLORS = [                    # 备用条色（参考实测）
    (218, 180, 135),   # 0 暖砂米
    (170, 125, 183),   # 1 丁香紫
    (162, 158, 52),    # 2 橄榄黄绿
    (231, 139, 20),    # 3 亮橙
]


# ------------------------------------------------------------------ 图标掩膜

def _icon_mask(size, name, lw_ratio=0.21, ss=3):
    """在 (size,size) 内画图标 → 返回 float 掩膜（0..1）。对勾等均为**圆头粗笔**。"""
    S = int(size * ss)
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    c = S / 2.0
    r = S / 2.0
    lw = max(2, int(S * lw_ratio))

    def _round_line(pts, width):
        d.line(pts, fill=255, width=width, joint="curve")
        for (px, py) in (pts[0], pts[-1]):
            d.ellipse([px - width / 2, py - width / 2,
                       px + width / 2, py + width / 2], fill=255)

    if name == "check":
        _round_line([(c - r * 0.44, c - r * 0.04),
                     (c - r * 0.12, c + r * 0.34),
                     (c + r * 0.50, c - r * 0.44)], lw)
    elif name in ("1", "2", "3", "4", "5"):
        # 序号数字（"三步""几点"类清单用）。
        # 【三·三十】圆饼序号数字三条规则 —— 用户第七轮点名「这个 1 依然不是居中……
        # 它那个 1 第一笔是这么写，但你正常的字不会这样写，这个是什么规则？你自己想一下」：
        #  ① 字形：**必须用不带底衬线脚的数字**。`NotoSansSC-VF` 的阿拉伯数字恰好是带衬线脚的
        #     （"1" = 旗 + 竖 + 底部横衬线），跟条里圆润汉字不是一套 → 看着像"起笔收笔写了三笔"。
        #     这才是"不居中"的真正观感来源。改用 msyhbd（微软雅黑 Bold）："1" 是干净的旗 + 竖。
        #  ② 高度：数字 ink 高 = **饼径 × 0.50**。
        #     ⚠️ 尺度陷阱：本函数的 `S = size * ss`（内部 3 倍画布），而 `size = 饼径 × 0.84`，
        #     所以「饼径 × 0.50」= `S × 0.50 / ss × 0.84` ≈ **`S × 0.60 / ss × …`** ——
        #     直接写 `target = S * 0.50` 实得只有 0.42 饼径，数字小得压不住圆饼。
        #     ⚠️ 也别再用「getbbox 高度迭代」反推字号（getbbox 的 box ≠ 实际 ink）。
        #     正解：先用大字号渲染一次、**实测 ink 高**，再按比例一次性算出目标字号。
        #  ③ 居中：**ink 外框中心 + 面积质心 各半** → 光学居中（数字墨量集中在竖笔，
        #     只按外框居中对不齐视觉重心；只按质心又会偏）。
        target = S * 0.60          # = 饼径 × 0.50（见上方尺度换算）
        _probe = _load_font(FONTS["msyh"], 220)
        _pt = Image.new("L", (560, 400), 0)
        ImageDraw.Draw(_pt).text((40, 40), name, font=_probe, fill=255)
        _pa = np.asarray(_pt).astype(np.float32) / 255.0
        _pys, _pxs = np.nonzero(_pa > 0.45)
        if len(_pys):
            _h0 = float(_pys.max() - _pys.min() + 1)
            f = _load_font(FONTS["msyh"], 220.0 * target / max(1.0, _h0))
            bb = f.getbbox(name)
            gw, gh = max(1, bb[2] - bb[0]), max(1, bb[3] - bb[1])
            _tmp = Image.new("L", (int(gw) + 8, int(gh) + 8), 0)
            ImageDraw.Draw(_tmp).text((4 - bb[0], 4 - bb[1]), name, font=f, fill=255)
            _a = np.asarray(_tmp).astype(np.float32) / 255.0
            _ys, _xs = np.nonzero(_a > 0.45)
            if len(_ys):
                _w = _a[_ys, _xs]
                _ccx = float((_xs * _w).sum() / _w.sum())
                _ccy = float((_ys * _w).sum() / _w.sum())
                _bcx = (_xs.min() + _xs.max()) / 2.0
                _bcy = (_ys.min() + _ys.max()) / 2.0
                _optx = 0.5 * _bcx + 0.5 * _ccx
                _opty = 0.5 * _bcy + 0.5 * _ccy
                d.text((c - bb[0] - (_optx - 4), c - bb[1] - (_opty - 4)),
                       name, font=f, fill=255)
    elif name == "dots":                      # 三个点（表示"几条"）
        for k, dx in enumerate((-0.44, 0.0, 0.44)):
            rr = lw * 0.62
            d.ellipse([c + r * dx - rr, c - rr, c + r * dx + rr, c + rr], fill=255)
    elif name == "gear":
        for i in range(8):
            a = i * math.pi / 4
            _round_line([(c + math.cos(a) * r * 0.34, c + math.sin(a) * r * 0.34),
                         (c + math.cos(a) * r * 0.78, c + math.sin(a) * r * 0.78)],
                        max(2, int(lw * 0.60)))
        rr = r * 0.40
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=255)
    elif name == "bird":                      # 眼睛（"看/盯"）
        d.ellipse([c - r * 0.56, c - r * 0.40, c + r * 0.56, c + r * 0.40],
                  outline=255, width=lw)
        rr = lw * 0.66
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=255)
    elif name == "wrench":                    # 扳手（"改"）
        _round_line([(c - r * 0.44, c + r * 0.44), (c + r * 0.30, c - r * 0.30)],
                    max(2, int(lw * 0.62)))
        for dx, dy, k in ((-0.50, 0.50, 1.0), (0.36, -0.36, 1.0)):
            rr = r * 0.26 * k
            d.ellipse([c + r * dx - rr, c + r * dy - rr, c + r * dx + rr, c + r * dy + rr],
                      outline=255, width=max(2, int(lw * 0.55)))
    elif name == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = r * (0.72 if i % 2 == 0 else 0.30)
            pts.append((c + math.cos(a) * rad, c + math.sin(a) * rad))
        d.polygon(pts, fill=255)
    elif name == "pin":                       # 图钉 / 定位
        rr = r * 0.44
        d.ellipse([c - rr, c - r * 0.78, c + rr, c - r * 0.78 + rr * 2], fill=255)
        _round_line([(c, c - r * 0.30), (c, c + r * 0.72)], max(2, int(lw * 0.55)))
    else:                                     # dot
        rr = r * 0.34
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=255)

    a = np.asarray(m).astype(np.float32) / 255.0
    a = _blur(a, ss * 0.55)                     # 圆润化：黏土不是矢量硬边
    a = np.clip((a - 0.22) / 0.78, 0, 1)
    if S != size:
        img = Image.fromarray((a * 255).astype(np.uint8), "L").resize((int(size), int(size)),
                              Image.LANCZOS)
        a = np.asarray(img).astype(np.float32) / 255.0
    return a


# ------------------------------------------------------------------ 层叠黏土徽章

def _badge_layered(W, H, cx, cy, d, base=BADGE_GREEN, icon="check",
                   bar_rgb=(124, 102, 172), light_from="tl", seed=3):
    """渲染**层叠黏土徽章**：圆饼 + 对勾，各自有厚度与投影。

    这正是用户点名的质感 —— "先贴了一个圆，然后再贴了一个对勾，一层一层的"。
    实现顺序（下→上）：
      ① 圆饼落地投影（落在条面上，偏右下）
      ② 圆饼底侧壁（压深的橄榄绿，向下挤出 d*0.075）
      ③ 圆饼顶面（左上受光的径向渐变）
      ④ 圆饼上缘亮边 + 下缘内影
      ⑤ 对勾投影（落在圆饼上）
      ⑥ 对勾侧壁（暖灰，向下挤出）
      ⑦ 对勾顶面（奶油白 + 上缘高光 + 下缘内影）
    返回 (rgb, alpha)，尺寸 (H,W,3)/(H,W)。
    """
    rng = np.random.default_rng(seed)
    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)

    d = float(d)
    R = d / 2.0
    l, t, rr_, b = cx - R, cy - R, cx + R, cy + R

    # ---- 圆饼掩膜（椭圆 + 极轻手捏扰动；**不要用 polygon 绕两圈**，会自交填充退化）
    SS = 3
    m = Image.new("L", (W * SS, H * SS), 0)
    dd = ImageDraw.Draw(m)
    dd.ellipse([(cx - R) * SS, (cy - R) * SS, (cx + R) * SS, (cy + R) * SS], fill=255)
    cm = np.asarray(m).astype(np.float32) / 255.0
    cm = _blur(cm, SS * 1.0)
    cm = np.clip((cm - 0.16) / 0.84, 0, 1)
    nz = _grain((int(H * SS), int(W * SS)), SS * 2.0, seed=seed + 21)
    cm = np.clip(cm * (1 + (nz - 0.5) * 2 * 0.045), 0, 1)
    cm = np.asarray(Image.fromarray((cm * 255).astype(np.uint8), "L").resize((W, H),
                    Image.LANCZOS)).astype(np.float32) / 255.0
    if cm.max() < 0.05:
        return rgb, alpha

    bc = _rgb(base)
    dark_bg = _rgb(BADGE_SHADOW)

    # ① 圆饼落地投影（往右下偏移，羽化大 → 才有"贴上去"的重量；参考实测落影 rgb36,23,61 很重）
    fall = _blur(_shift(cm, d * 0.085, d * 0.175), d * 0.17)
    near = _blur(_shift(cm, d * 0.02, d * 0.060), d * 0.055)
    rgb, alpha = _over(rgb, alpha, dark_bg,
                       np.clip(np.maximum(fall * 0.72, near * 1.00), 0, 1) * 0.96)

    # ② 底侧壁（向下挤出 = 厚度；参考实测 44,31,68 暗紫黑）
    side = _blur(_shift(cm, d * 0.012, d * 0.105), d * 0.038)
    side_rgb = _mix(_rgb(BADGE_SIDE), bc, 0.22)
    rgb, alpha = _over(rgb, alpha, side_rgb, np.clip(side * 1.55, 0, 1))

    # ③ 顶面：左上受光径向渐变
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gr = np.clip(1.0 - (((xx - (l + R * 0.30)) / max(1.0, d)) * 1.05
                        + ((yy - (t + R * 0.26)) / max(1.0, d)) * 0.85), 0, 1)
    face = _mix(_darken(bc, 0.30), _rgb(BADGE_TOP), np.clip(gr*0.95, 0, 1))
    # ④ 上缘亮边 + 下缘内影
    k = max(1.5, d * 0.058)
    te = np.clip(cm - _shift(cm, 0, k), 0, 1)
    face = _mix(face, _lighten(bc, 0.34), np.clip(te * 0.68, 0, 1))
    be = np.clip(cm - _shift(cm, 0, -k * 0.95), 0, 1)
    face = _mix(face, _darken(bc, 0.38), np.clip(be * 0.80, 0, 1))
    face = np.clip(face * (1 + (_grain((H, W), d * 0.10, seed=seed + 5)[..., None] - 0.5)
                           * 2 * 0.06), 0, 1)
    rgb, alpha = _over(rgb, alpha, face, cm)

    # ⑤⑥⑦ 对勾：一块独立的黏土，压在圆饼上（参考里对勾**占圆的大半**、笔画很粗）
    ic = _icon_mask(int(d * 0.84), icon, lw_ratio=0.225, ss=SS)
    hm_img = Image.new("L", (W, H), 0)
    hm_img.paste(Image.fromarray((ic * 255).astype(np.uint8), "L"),
                 (int(cx - ic.shape[1] / 2), int(cy - ic.shape[0] / 2)))
    hm = np.asarray(hm_img).astype(np.float32) / 255.0

    # ⑤ 对勾投影（落在圆饼面上 → 用深绿而不是黑，才像黏土）
    chk_sh = _blur(_shift(hm, d * 0.030, d * 0.070), d * 0.045)
    rgb, alpha = _over(rgb, alpha, _mix(_rgb(BADGE_SIDE), dark_bg, 0.35),
                       np.clip(chk_sh * 0.85, 0, 1))
    # ⑥ 对勾侧壁
    chk_side = _blur(_shift(hm, d * 0.006, d * 0.050), d * 0.018)
    rgb, alpha = _over(rgb, alpha, _rgb((172, 158, 130)), np.clip(chk_side * 1.45, 0, 1))
    # ⑦ 对勾顶面
    cb = _rgb(CHECK_BASE)
    cf = _mix(_darken(cb, 0.10), _lighten(cb, 0.05), np.clip(gr * 1.15, 0, 1))
    k2 = max(1.2, d * 0.050)
    cf = _mix(cf, _lighten(cb, 0.62), np.clip(np.clip(hm - _shift(hm, 0, k2), 0, 1) * 0.90, 0, 1))
    cf = _mix(cf, _darken(cb, 0.16), np.clip(np.clip(hm - _shift(hm, 0, -k2), 0, 1) * 0.70, 0, 1))
    cf = np.clip(cf * (1 + (_grain((H, W), d * 0.07, seed=seed + 9)[..., None] - 0.5)
                       * 2 * 0.05), 0, 1)
    rgb, alpha = _over(rgb, alpha, cf, hm)
    return rgb, alpha


# ------------------------------------------------------------------ 主渲染

def render_float_list(rows, out_path=None, width=1024, frame_h=576,
                      x0=64, text_x=None, row_h=66, badge_d=42,
                      font="noto", text_ratio=0.50, text_color=None,
                      top=0, text_gap=G_TEXT_GAP, text_stroke=G_TEXT_STROKE,
                      text_stroke_color=None, text_min_gap=20,
                      text_layer=True):
    """【三·二十五】**无条底浮行**——徽章 + 奶油黏土字直接浮在场景上，不画条底色。

    与 `render_label_band` 的分工：
      · `render_label_band`（第 9 页那种）＝ 紫条底 + 徽章锁在条内 → 适合 4 条以上、信息重的页
      · `render_float_list`（本函数）＝ **无条底、徽章悬浮在字左侧** → 适合 2~3 条、
        要跟别的页拉开版式的页（八六 p14/p15/p19 那类"左侧文字列 + 右侧场景"）

    rows: [{"key": "复制一份", "icon": "1", "badge": [128,144,38]}, ...]
    返回透明底 RGBA（尺寸 = width × n*row_h），用 `compose` 或 `alpha_composite` 贴。
    """
    n = len(rows)
    W = int(width)
    H = int(n * row_h)
    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)

    tx_default = x0 + badge_d + text_min_gap
    if text_x is None:
        text_x = tx_default

    # ① 徽章（层叠黏土，直径 = badge_d；比条内徽章大，因为要独立悬浮）
    for i, r in enumerate(rows):
        cy = int(row_h * (i + 0.5))
        bcol = r.get("badge")
        bx = x0 + badge_d / 2.0
        brgb, ba = _badge_layered(W, H, bx, cy, badge_d,
                                  base=tuple(bcol) if bcol else BADGE_GREEN,
                                  icon=str(r.get("icon", "check")), seed=i * 37 + 5)
        rgb, alpha = _over(rgb, alpha, brgb, ba)

    # ② 文字（清晰描边字，垂直居中于行）
    if text_layer:
        d_text = row_h * text_ratio
        for i, r in enumerate(rows):
            line = r.get("key", "")
            if not line:
                continue
            cy = int(row_h * (i + 0.5))
            tcol = r.get("text_color") or text_color or TEXT_CREAM
            scol = r.get("stroke_color") or text_stroke_color or TEXT_STROKE_COLOR
            img = render_crisp_text(line, cap_height=d_text, base=tuple(tcol),
                                    font=font, weight=900,
                                    gap_ratio=text_gap, stroke=text_stroke,
                                    stroke_color=tuple(scol),
                                    shadow=(30, 16, 54), shadow_strength=0.40,
                                    grain=0.018, jitter_rot=0.45, jitter_y=0.005,
                                    pad_ratio=0.36, ss=4, seed=i * 23 + 7)
            arr = np.asarray(img).astype(np.float32) / 255.0
            th, tw = arr.shape[0], arr.shape[1]
            px = max(0, min(int(text_x), W - tw))
            py = max(0, min(int(cy - th / 2.0), H - th))
            sub = (slice(py, py + th), slice(px, px + tw))
            rgb[sub], alpha[sub] = _over(rgb[sub], alpha[sub], arr[:, :, :3], arr[:, :, 3])

    out = np.clip(np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2), 0, 255)
    img_out = Image.fromarray(out.astype(np.uint8), "RGBA")
    if out_path:
        img_out.save(out_path)
    return img_out


def render_label_band(rows, out_path=None, width=1024, bar_h=G_BAR_H_N4, gap=G_GAP_N4,
                      x0=None, x1=None, guard=8, top=None, frame_h=576,
                      radius_ratio=0.5, grain=0.11, shadow=(26, 14, 52),
                      shadow_strength=0.95, font="noto", text_ratio=G_TEXT_H,
                      badge_shape="circle", badge_ratio=G_BADGE_R,
                      text_color=None, icon_color=None, rim=2.0,
                      text_gap=G_TEXT_GAP, text_stroke=G_TEXT_STROKE,
                      text_stroke_color=TEXT_STROKE_COLOR,
                      text_layer=True, badge_text_gap=None, badge_pad=None,
                      debug_text_mask=None):
    """渲染左列清单条整条带（透明底 RGBA），返回 PIL.Image

    几何默认值 = 八六 p10 逐像素实测比例（见文件头）。`bar_h/gap` 可显式传入；
    **4 条要填满参考的 71.6% 竖向区间**，所以条高按条数放大（bar_h 默认 66 就是
    按 4 条反推的）。传 top 时返回的图用于 `compose` 定位。
    """
    n = len(rows)
    if x0 is None:
        x0 = int(width * G_LEFT)
    if x1 is None:
        x1 = int(width * (G_RIGHT if n >= 6 else G_RIGHT_N4))
    x1s = [int(width * r["x1_ratio"]) if r.get("x1_ratio") else x1 for r in rows]
    W = int(width)
    band_h = n * bar_h + (n - 1) * gap
    H = int(band_h)

    SS = 2
    Wb, Hb = W * SS, H * SS
    bh, gp = int(bar_h * SS), int(gap * SS)

    # 条面掩膜
    band = Image.new("L", (Wb, Hb), 0)
    d = ImageDraw.Draw(band)
    for i in range(n):
        y = i * (bh + gp)
        d.rounded_rectangle([x0 * SS, y, (x1s[i] - 1) * SS, y + bh - 1],
                            radius=int(bh * radius_ratio), fill=255)
    bm = np.asarray(band).astype(np.float32) / 255.0
    bm = _blur(bm, SS * 0.9)
    bm = np.clip((bm - 0.16) / 0.84, 0, 1)

    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    rgb = np.ones((Hb, Wb, 3), np.float32) * 0.5
    alpha = np.zeros((Hb, Wb), np.float32)

    # 整块条带投影（往右下）
    sc = _rgb(shadow)
    far = _blur(_shift(bm, SS * 0.9, SS * 2.8), SS * 3.4)
    near = _blur(_shift(bm, SS * 0.2, SS * 0.9), SS * 1.2)
    sh_a = np.clip(np.maximum(far * 0.50, near * 0.74) * shadow_strength, 0, 1)
    rgb, alpha = _over(rgb, alpha, sc, sh_a)

    badge_pad = int(bar_h * G_BADGE_X) if badge_pad is None else badge_pad
    badge_text_gap = int(bar_h * G_BADGE_G) if badge_text_gap is None else badge_text_gap
    d_text = bar_h * text_ratio

    for i, r in enumerate(rows):
        y0 = i * (bh + gp)
        col = r.get("bg")
        base = _rgb(col if col else BAR_COLORS[i % len(BAR_COLORS)])
        cy = y0 + bh // 2
        # 该条掩膜（用条自身的几何重新画，避免相邻条串色）
        rm = Image.new("L", (Wb, Hb), 0)
        ImageDraw.Draw(rm).rounded_rectangle(
            [x0 * SS, y0, (x1s[i] - 1) * SS, y0 + bh - 1],
            radius=int(bh * radius_ratio), fill=255)
        pm = np.asarray(rm).astype(np.float32) / 255.0
        pm = _blur(pm, SS * 0.8)
        pm = np.clip((pm - 0.16) / 0.84, 0, 1)
        # 【三·三十二】**边缘手捏扰动** —— 八六的条是"捏"出来的黏土板，轮廓不是
        # 完美圆角矩形。中尺度噪声把边缘推 ±1~2px（幅度要小，大了会读成毛边锯齿）。
        _en = _grain((Hb, Wb), SS * 4.5, seed=i * 613 + 17)
        pm = np.clip(pm + (_en - 0.5) * 0.40, 0, 1)

        # 逐条投影 —— 参考实测条间缝 rgb(16,10,39) 比背景还暗，靠的就是**每条自己投的影**，
        # 只做"整块投影"缝里就是亮的，条会读成"一张纸上的几行字"而不是几块独立的黏土
        lfar = _blur(_shift(pm, SS * 0.8, SS * (gap * 0.62 + 2)), SS * 2.4)
        lnear = _blur(_shift(pm, 0, SS * (gap * 0.34 + 1)), SS * 1.0)
        rgb, alpha = _over(rgb, alpha, _rgb(SEAM_RGB),
                           np.clip(np.maximum(lfar * 0.60, lnear * 0.92), 0, 1) * 0.95)
        # 条身底侧壁（挤出厚度）
        # 【三·三十二】2.2px → 3.4px、压暗 0.46 → 0.54、强度 1.35 → 1.75：
        # 八六的条下缘是一条**实心暗侧壁**，"实体黏土"全靠它；
        # 只做一条模糊暗边，整条会读成"平涂色块 + 阴影"（用户：「都是实感觉是实体的粘土，
        # 你下面那个就不是」）。
        side = _blur(_shift(pm, SS * 0.5, SS * 3.4), SS * 0.9)
        rgb, alpha = _over(rgb, alpha, _darken(base, 0.54), np.clip(side * 1.75, 0, 1))
        # 条面：上亮下暗（参考实测上 112,78,159 / 下 105,71,150 —— 梯度很弱，别做重）
        gy = np.clip((yy - y0) / max(1.0, bh), 0, 1)
        face = _mix(_lighten(base, 0.045), _darken(base, 0.070), gy)
        # 低频起伏：大半径噪声 → "手捏出来的厚度不均"，不是纯色平涂
        _lo = _grain((Hb, Wb), SS * 22.0, seed=i * 977 + 31)[..., None]
        face = np.clip(face * (1 + (_lo - 0.5) * 2 * 0.085), 0, 1)
        k = max(1.5, SS * rim)
        top_e = np.clip(pm - _shift(pm, 0, k), 0, 1)
        face = _mix(face, _lighten(base, 0.17), np.clip(top_e, 0, 1))
        bot_e = np.clip(pm - _shift(pm, 0, -k * 1.6), 0, 1)
        face = _mix(face, _darken(base, 0.40), np.clip(bot_e * 0.92, 0, 1))
        if grain > 0:
            g = _grain((Hb, Wb), SS * 1.3, seed=i * 131 + 7)[..., None]
            face = np.clip(face * (1 + (g - 0.5) * 2 * grain), 0, 1)
        rgb, alpha = _over(rgb, alpha, face, pm)

        # ---- 层叠黏土徽章
        bcol = r.get("badge")
        d_badge = bh * (r.get("badge_ratio", badge_ratio))
        bx = x0 * SS + badge_pad * SS + d_badge / 2.0
        brgb, ba = _badge_layered(Wb, Hb, bx, cy, d_badge,
                                  base=bcol if bcol else BADGE_GREEN,
                                  icon=r.get("icon", "check"), seed=i * 37 + 5)
        rgb, alpha = _over(rgb, alpha, brgb, ba)

    # ---- 条内文字：黏土浮雕字（独立层，最后贴）
    tx0_map = []
    for i, r in enumerate(rows):
        y0 = i * (bh + gp)
        cy = y0 + bh // 2
        d_badge = bh * (r.get("badge_ratio", badge_ratio))
        tx = x0 * SS + (badge_pad * SS) + d_badge + badge_text_gap * SS
        line = r.get("key", "")
        if r.get("text"):
            line = line + "：" + r["text"]
        avail = x1s[i] * SS - guard * SS - tx
        tx0_map.append((i, y0, cy, tx, avail, line, r))

    if text_layer:
        # 【三·三十四·字号一致】先给每条算"放得下的最大字号"，再取全列最小值统一渲染。
        # 旧逻辑每条独立缩（×0.93 到放下为止）→ 长句变小字，"前面大后面小"（2026-09-20 用户点名）。
        def _fits(line, cap, tcol, i):
            return render_crisp_text(line, cap_height=cap, base=tuple(tcol),
                                     font=font, weight=900,
                                     gap_ratio=text_gap,
                                     stroke=text_stroke * SS,
                                     stroke_color=text_stroke_color,
                                     shadow=(34, 18, 60),
                                     shadow_strength=0.42,
                                     grain=0.018,
                                     jitter_rot=0.45, jitter_y=0.005,
                                     pad_ratio=0.36, ss=1, seed=i * 17 + 3)
        caps = {}
        for (i, y0, cy, tx, avail, line, r) in tx0_map:
            if not line:
                continue
            tcol = r.get("text_color")
            if tcol is None:
                tcol = TEXT_CREAM if not r.get("dark_text") else TEXT_DARK
            cap = float(d_text * SS)
            floor = d_text * SS * 0.62
            for _ in range(8):
                img = _fits(line, cap, tcol, i)
                # 存下的一定是"这一条验证过"的字号：放得下 → 就用它；
                # 到地板 → 用地板（有界微溢出，不再继续缩）。
                if img.width <= avail or cap <= floor:
                    break
                cap = max(floor, cap * 0.93)
            caps[i] = (cap, tcol, img)
        cap_min = min(v[0] for v in caps.values()) if caps else d_text * SS
        for (i, y0, cy, tx, avail, line, r) in tx0_map:
            if not line or i not in caps:
                continue
            _, tcol, _img = caps[i]
            img = _fits(line, cap_min, tcol, i)
            arr = np.asarray(img).astype(np.float32) / 255.0
            th, tw = arr.shape[0], arr.shape[1]
            px, py = int(tx), int(cy - th / 2.0)
            px = max(0, min(px, Wb - tw))
            py = max(0, min(py, Hb - th))
            lay_rgb = arr[:, :, :3]
            lay_a = arr[:, :, 3]
            sub = (slice(py, py + th), slice(px, px + tw))
            rgb[sub], alpha[sub] = _over(rgb[sub], alpha[sub], lay_rgb, lay_a)
    elif debug_text_mask:
        pass

    out = np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2)
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    if SS != 1:
        img = img.resize((W, H), Image.LANCZOS)
    # 颗粒必须在降采样之后加（超采样会把高频噪点平均掉 → 条面变"光面塑料"）
    if grain > 0:
        arr = np.asarray(img).astype(np.float32) / 255.0
        gg = _grain((H, W), 2.2, seed=99)[..., None]
        arr[:, :, :3] = np.clip(arr[:, :, :3] * (1 + (gg - 0.5) * 2 * grain), 0, 1)
        img = Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "RGBA")
    if out_path:
        img.save(out_path)
    return img


def band_top(width=1024, frame_h=576, rows=None, bar_h=66, gap=16):
    """按实测比例算出条带顶端 y（4 条时 ≈ 帧高的 24%，不留空）"""
    return int(frame_h * G_TOP)


def compose(scene_path, rows, out_path, top=None, **kw):
    """把条带贴到场景图上（scene 尺寸为准，宽度自适应）"""
    scene = Image.open(scene_path).convert("RGBA")
    band = render_label_band(rows, width=scene.width, frame_h=scene.height, **kw)
    if top is None:
        top = band_top(scene.width, scene.height, rows)
    if band.width != scene.width:
        band = band.resize((scene.width, int(band.height * scene.width / band.width)),
                           Image.LANCZOS)
    scene.alpha_composite(band, (0, int(top)))
    scene.convert("RGB").save(out_path)
    return out_path


DEFAULT_ROWS = [
    {"key": "先锁人物锚点", "badge": BADGE_GREEN, "icon": "check", "bg": BAR_BASE},
    {"key": "短句整图烘字", "badge": BADGE_GREEN, "icon": "check", "bg": BAR_BASE},
    {"key": "长文自己贴卡", "badge": BADGE_GREEN, "icon": "check", "bg": BAR_BASE},
    {"key": "出图再校色调", "badge": BADGE_GREEN, "icon": "check", "bg": BAR_BASE},
]


def _demo(out):
    W, H = 1024, 576
    bg = Image.new("RGB", (W, H), (31, 24, 91))       # 参考实测条外背景 rgb(31,24,91)
    dd = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        dd.line([(0, y), (W, y)],
                fill=(int(40 - 14 * t), int(31 - 11 * t), int(104 - 24 * t)))
    band = render_label_band(DEFAULT_ROWS, width=W, frame_h=H)
    bg = bg.convert("RGBA")
    bg.alpha_composite(band, (0, band_top(W, H)))
    bg.convert("RGB").save(out)
    print("demo ->", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="run", help="run | demo")
    ap.add_argument("--scene")
    ap.add_argument("--rows")
    ap.add_argument("--out", default="page.png")
    ap.add_argument("--top", type=int, default=None)
    ap.add_argument("--bar-h", type=int, default=66)
    ap.add_argument("--gap", type=int, default=16)
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--x0", type=float, default=None)
    ap.add_argument("--x1", type=float, default=None,
                    help="条右端比例（默认 0.336 = p10 实测）。**四条必须齐平**")
    ap.add_argument("--badge-ratio", type=float, default=G_BADGE_R)
    ap.add_argument("--text-color", default=None,
                    help="dark | light | R,G,B")
    ap.add_argument("--rim", type=float, default=2.0)
    ap.add_argument("--grain", type=float, default=0.30)
    a = ap.parse_args()
    if a.mode == "demo":
        _demo(a.out)
        return
    rows = json.load(open(a.rows, encoding="utf-8")) if a.rows else DEFAULT_ROWS
    kw = {}
    if a.x0 is not None:
        kw["x0"] = int(a.width * a.x0)
    if a.x1 is not None:
        kw["x1"] = int(a.width * a.x1)
    kw["badge_ratio"] = a.badge_ratio
    kw["rim"] = a.rim
    kw["grain"] = a.grain
    if a.text_color == "light":
        kw["text_color"] = TEXT_CREAM
    elif a.text_color == "dark":
        kw["text_color"] = TEXT_DARK
    elif a.text_color:
        kw["text_color"] = tuple(int(v) for v in a.text_color.split(","))
    if a.scene:
        print("-> ", compose(a.scene, rows, a.out, top=a.top, bar_h=a.bar_h, gap=a.gap, **kw))
    else:
        print("-> ", render_label_band(rows, out_path=a.out, width=a.width,
                                       bar_h=a.bar_h, gap=a.gap, **kw))


if __name__ == "__main__":
    main()
