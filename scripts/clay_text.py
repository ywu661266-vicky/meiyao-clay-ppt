#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clay_text.py — 黏土立体字 / 黏土铭牌 素材生成器（透明底 PNG）

核心思想：文字层单独做，图片层单独做，最后合成。
- 文字形状由真实字体保证 → 永不乱码、字数不受限、改字只改字符串
- 黏土质感由本脚本渲染 → 厚度 / 侧壁 / 顶面光照 / 高光 / 内阴影 / 颗粒 / 投影

用法：
    python clay_text.py selftest
或作为库：
    from clay_text import render_clay_text, render_clay_badge
    render_clay_text("从会用 AI", "out.png", cap_height=120, base=(243,234,220))
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

# --------------------------------------------------------------------------
# 字体解析（2026-09-20 改）：**内置优先 + 跨平台回退**
#
# 为什么改：原来写死 `C:/Windows/Fonts/...` 绝对路径。**别人把 skill 拷走就必然报错**，
# 等于"这套东西只能在作者这台机器上复现" —— 也就谈不上"下次/别人还能出同款"。
# 现在：skill 自带 `assets/fonts/NotoSansSC-VF.ttf`（Noto Sans SC 为 SIL OFL 1.1，
# 允许随工具分发），**标题/正文的字形因此是自包含的**；系统字体只作为可选增强。
# --------------------------------------------------------------------------
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BUILTIN_FONTS = os.path.join(_SKILL_ROOT, "assets", "fonts")

_FONT_CANDIDATES = {
    # 标题 / 正文主力 —— 已随 skill 内置，任何机器都能出同款字形
    "noto": [
        os.path.join(_BUILTIN_FONTS, "NotoSansSC-VF.ttf"),
        "C:/Windows/Fonts/NotoSansSC-VF.ttf",
        "/System/Library/Fonts/NotoSansSC-VF.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansSC-VF.otf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ],
    # 华文琥珀（手捏感最强）—— Windows 专有，不可分发；缺了就回退 noto
    "sthu": [
        "C:/Windows/Fonts/STHUPO.TTF",
        "/System/Library/Fonts/Supplemental/STHUPO.ttf",
    ],
    # 徽章序号数字 —— 需要"不带底衬线脚"的拉丁数字。
    # ⚠️ 已知限制：NotoSansSC 的阿拉伯数字带底衬线（"1" 有底横），所以数字优先
    #    微软雅黑 Bold；**在无 Windows 字体的机器上会回退到 Noto，数字形态会有差异**。
    "msyh": [
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ],
    "deng": [
        "C:/Windows/Fonts/Dengb.ttf",
        "C:/Windows/Fonts/simhei.ttf",
    ],
}


class _FontRegistry(dict):
    """`FONTS["noto"]` → 当前机器上真实可用的字体文件路径。

    查找顺序：skill 内置 → 系统路径。全找不到时**回退到内置 noto** 并打一次警告，
    绝不静默换字形。
    """

    def __init__(self):
        super().__init__()
        self._warned = set()

    def __getitem__(self, key):
        for p in _FONT_CANDIDATES.get(key, []):
            if p and os.path.exists(p):
                return p
        if key not in self._warned:
            self._warned.add(key)
            print("[clay_text] 找不到字体 %r，回退到内置 NotoSansSC（字形可能与预期不同）" % key)
        return _FONT_CANDIDATES["noto"][0]

    def get(self, key, default=None):
        try:
            return self[key]
        except Exception:
            return default


FONTS = _FontRegistry()


def font_report():
    """打印各字体的解析结果 —— 交付前自检 & 排查"别人那边字形不对"时用。"""
    out = []
    for k, cands in _FONT_CANDIDATES.items():
        path = FONTS[k]
        tag = "内置" if os.path.abspath(path).startswith(os.path.abspath(_BUILTIN_FONTS)) else "系统"
        out.append("  %-5s [%s] %s" % (k, tag, path))
    return "字体解析：\n" + "\n".join(out)


# ---------------------------------------------------------------- 基础工具

def _load_font(path, size, weight=None):
    f = ImageFont.truetype(path, int(size))
    if weight is not None:
        try:
            axes = f.get_variation_axes()
            vals = []
            for a in axes:
                nm = str(a.get("name", "")).lower()
                vals.append(weight if ("weight" in nm or nm == "wght") else a.get("default"))
            f.set_variation_by_axes(vals)
        except Exception:
            pass
    return f


def _fit_font(path, text, target_cap_px, weight=None):
    """反推字号，使单行字形实际高度 ≈ target_cap_px（对 CJK 用 '国' 量高度更准）"""
    probe = "国" if any("\u4e00" <= c <= "\u9fff" for c in text) else "H"
    size = float(target_cap_px)
    for _ in range(4):
        f = _load_font(path, size, weight)
        bb = f.getbbox(probe)
        h = max(1.0, bb[3] - bb[1])
        size *= target_cap_px / h
    return _load_font(path, size, weight)



def _fit_ink_font(path, text, target_ink_px, weight=None, iters=4):
    """反推字号，使**渲染出来的 ink 高**精确 = `target_ink_px`。

    ⚠️ `_fit_font` 只保证"字形框高"≈ target，而汉字实际 ink 高比它**小约 10%**
    （框含 ascent/descent）。所以直接用 `_fit_font(cap_height)` 会得到"要 91 却出 100"，
    别人按文档填数字就会拿到不一样的大小 —— 2026-09-20 发现并修正。
    """
    t_cur = float(target_ink_px)
    f = _fit_font(path, text, t_cur, weight=weight)
    for _ in range(max(2, iters)):
        probe = Image.new("L", (6000, 1600), 0)
        ImageDraw.Draw(probe).text((80, 80), text, font=f, fill=255, anchor="lt")
        a = np.asarray(probe) > 60
        ys, _xs = np.where(a)
        if not len(ys):
            break
        ink = float(ys.max() - ys.min() + 1)
        if abs(ink - target_ink_px) <= 1.5:
            break
        # ⚠️ 必须按**上次用的 target 比例**修正（`t_cur * 目标/实测`）。
        #    写成 `目标²/实测` 会在目标附近**来回震荡**（2026-09-20 踩过）。
        t_cur = t_cur * float(target_ink_px) / ink
        f = _fit_font(path, text, t_cur, weight=weight)
    return f

def _shift(a, dx, dy):
    """亚像素无关的整数平移，零填充。a: float ndarray"""
    dx, dy = int(round(dx)), int(round(dy))
    H, W = a.shape
    out = np.zeros_like(a)
    ys, xs = slice(max(0, dy), H + min(0, dy)), slice(max(0, dx), W + min(0, dx))
    ysrc, xsrc = slice(max(0, -dy), H + min(0, -dy)), slice(max(0, -dx), W + min(0, -dx))
    out[ys, xs] = a[ysrc, xsrc]
    return out


def _blur(a, r):
    if r <= 0:
        return a
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
    return np.asarray(img.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0


def _rgb(c):
    return np.array(c, dtype=np.float32) / 255.0


def _mix(c1, c2, t):
    """c1/c2 为 0..1 的 rgb array(3,)；t 可为标量、2D 权重图或同形数组"""
    t = np.asarray(t, dtype=np.float32)
    while t.ndim < 3:
        t = t[..., None]
    return c1 * (1 - t) + c2 * t


def _darken(c, amount):
    return np.clip(c * (1.0 - amount), 0, 1)


def _lighten(c, amount):
    return np.clip(c + (1.0 - c) * amount, 0, 1)


def _over(rgb, alpha, layer_rgb, layer_a):
    """标准 over 合成（直通 alpha）"""
    la = np.clip(layer_a, 0, 1)
    a = np.clip(alpha, 0, 1)
    out_a = la + a * (1 - la)
    num = (layer_rgb * la[..., None] + rgb * (a * (1 - la))[..., None])
    return num / np.clip(out_a, 1e-6, 1)[..., None], out_a


def _grain(shape, r, seed=7):
    """黏土颗粒纹理：低频噪点 + 高频噪点"""
    rng = np.random.default_rng(seed)
    lo = rng.random(shape)
    lo = _blur(lo, r * 3.0)
    lo = (lo - lo.min()) / max(1e-6, float(np.ptp(lo)))
    hi = rng.random(shape)
    return 0.65 * lo + 0.35 * hi


# ---------------------------------------------------------------- 主渲染

def render_clay_text(text,
                     out_path=None,
                     cap_height=120,
                     base=(242, 233, 219),
                     font="noto",
                     weight=900,
                     depth=None,
                     shadow=(52, 40, 86),
                     shadow_strength=1.0,
                     grain=0.055,
                     hand_made=0.07,
                     outline=0.0,
                     rim=0.0,
                     rim_color=(168, 156, 142),
                     letter_gap=0.045,
                     stroke_ratio=0.013,
                     jitter_rot=1.5,
                     jitter_y=0.010,
                     seed=3,
                     ss=3,
                     pad_ratio=0.85,
                     return_array=False,
                     debug_flat=None):
    """
    把一行（或 \n 多行）文字渲染成黏土立体字透明底 PNG。
    默认是"薄浮雕"模式——浅浅一层贴在背景上，近似平贴，像 86 老师那种自然感。
    想要厚积木感可调 depth 增大 / grain 调高 / shadow 加深。

    cap_height  成品中字形高度（px）
    base        字的主体颜色（米白 / 橙黄 / 奶绿 …）
    depth       侧面厚度，默认 cap_height * 0.018（薄浮雕）；厚积木改 0.10~0.18
    shadow      投影颜色（与背景同色系的最浅暗色，才"贴得住"）
    grain       颗粒强度 0~0.15
    rim         奶油垫块宽度（**成品像素**，0=不画）。标题压在深底上时用它做"白黏土垫块"。
                ⚠️ 太薄（< 0.08cap）会读成"纯文字框"而不是黏土块 —— 用 **0.15 × cap_height**。
                与字形同一掩膜外扩 → 边缘干净、**不会虚**。rim>0 时不要再开 outline。
    rim_color   垫块基色，默认 (168,156,142) 灰奶油（**不是亮白**）。内部会按"外缘亮、贴字面暗"
                的圆台明暗自动着色（实测第 9 页：外缘 ≈(172,160,146)、内缘 ≈(128,118,108)）。
    """
    fp = FONTS.get(font, font)
    fs = cap_height * ss
    font_obj = _fit_font(fp, text, fs, weight)

    lines = text.split("\n")
    line_h = int(fs * 1.32)
    pad = int(fs * pad_ratio)
    gap = fs * letter_gap

    # —— 逐字排版：加字距 + 每字轻微旋转/升降 → 手作错落感（对齐基线就一定像印刷）
    rng = np.random.default_rng(seed)
    line_w = []
    for ln in lines:
        line_w.append(sum(font_obj.getlength(c) for c in ln) + gap * max(0, len(ln) - 1))
    W = int((max(line_w) if line_w else fs) + pad * 2)
    H = int(line_h * len(lines) + pad * 2)

    m_img = Image.new("L", (W, H), 0)
    for li, ln in enumerate(lines):
        x = (W - line_w[li]) / 2.0
        for ch in ln:
            adv = font_obj.getlength(ch)
            if ch.strip():
                bb = font_obj.getbbox(ch)
                cw, chh = max(1, bb[2] - bb[0]), max(1, bb[3] - bb[1])
                sw = max(0, int(round(fs * stroke_ratio)))
                sp = sw + 4
                c_im = Image.new("L", (cw + sp * 2, chh + sp * 2), 0)
                ImageDraw.Draw(c_im).text((sp - bb[0], sp - bb[1]), ch, font=font_obj,
                                          fill=255, stroke_width=sw, stroke_fill=255)
                if jitter_rot:
                    c_im = c_im.rotate(float(rng.uniform(-jitter_rot, jitter_rot)),
                                       resample=Image.BICUBIC, expand=True)
                dy = float(rng.uniform(-1, 1)) * jitter_y * fs if jitter_y else 0.0
                layer = Image.new("L", (W, H), 0)
                layer.paste(c_im, (int(round(x)), int(round(pad + li * line_h + dy))), c_im)
                m_img = ImageChops.lighter(m_img, layer)
            x += adv + gap

    m = np.asarray(m_img).astype(np.float32) / 255.0

    # —— 圆润化：薄浮雕不需要那么"胖"
    m = _blur(m, ss * 0.95)
    m = np.clip((m - 0.11) / 0.89, 0, 1)
    m = m ** 0.92          # gamma 接近 1 → 笔画薄，不糯团
    m = np.clip(m * 1.02, 0, 1)

    # —— 手捏扰动：极轻，保留手作但不破坏薄贴感
    if hand_made > 0:
        rng2 = np.random.default_rng(11)
        nz = rng2.random((H, W)).astype(np.float32)
        nz = _blur(nz, fs * 0.075)
        nz = (nz - nz.min()) / max(1e-6, float(np.ptp(nz)))
        m = np.clip(m * (1.0 + (nz - 0.5) * 2 * hand_made * 0.4), 0, 1)

    cap = fs
    if depth is None:
        depth = cap * 0.018   # 薄浮雕默认：近乎平贴，浅浅一层
    ddx, ddy = 0.20, 0.72   # 侧壁朝右下，角度偏柔和
    nrm = (ddx ** 2 + ddy ** 2) ** 0.5
    ddx, ddy = ddx / nrm, ddy / nrm
    T = max(1, int(round(depth)))   # 薄浮雕可能只有一两像素

    # —— 侧壁轮廓：把 m 沿光反方向外扩 T 像素
    union = m.copy()
    for i in range(1, T + 1):
        union = np.maximum(union, _shift(m, ddx * i, ddy * i))
    # 用距离场度量"离顶面多远"，侧壁明暗才连续
    import cv2
    mm = (m > 0.5).astype(np.uint8) * 255
    dist_to_top = cv2.distanceTransform(255 - mm, cv2.DIST_L2, 5)
    dn = np.clip(dist_to_top / max(1.0, float(T)), 0, 1)

    b = _rgb(base)
    warm = np.array([0.50, 0.42, 0.34], np.float32)
    # 薄浮雕：侧壁几乎跟顶面同色，只微微暗一点点（别发灰、别出厚条）
    side_near = _mix(_darken(b, 0.022), warm, 0.09)
    side_far  = _mix(_darken(b, 0.045), warm, 0.16)
    # 用更宽的 dn 区间：让厚度哪怕只有 1–2px 也柔和过渡
    side_rgb = _mix(side_near, side_far, np.clip(dn * 1.6, 0, 1))
    # 倒角柔化：薄浮雕更软，避免"铣削硬边"
    soft = max(1.0, cap * 0.022)
    union_s = _blur(union, soft)
    m_s     = _blur(m, soft * 0.90)

    # —— 顶面：左上受光，但对比要弱（薄浮雕不是强体积）
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = xx / max(1.0, W)
    ny = yy / max(1.0, H)
    grad = np.clip(1.0 - (0.42 * nx + 0.25 * ny), 0, 1)
    grad = (grad - grad.min()) / max(1e-6, grad.max() - grad.min())
    face_rgb = _mix(_darken(b, 0.040), _lighten(b, 0.035), grad)

    # —— 顶面高光带（上边缘）——薄浮雕只做很轻的一圈
    k = max(2.0, cap * 0.040)
    top_edge = np.clip(m - _shift(m, 0, k), 0, 1)
    face_rgb = _mix(face_rgb, _lighten(b, 0.22), np.clip(top_edge * 0.28, 0, 1))

    # —— 底部内阴影（下边缘）——轻薄
    k2 = max(2.0, cap * 0.050)
    bot_edge = np.clip(m - _shift(m, 0, -k2), 0, 1)
    face_rgb = _mix(face_rgb, _darken(b, 0.11), np.clip(bot_edge * 0.30, 0, 1))

    # —— 边缘柔光 + 颗粒
    edge_glow = np.clip(m - _blur(m, ss * 1.6), 0, 1)
    face_rgb = _mix(face_rgb, _lighten(b, 0.26), np.clip(edge_glow * 0.30, 0, 1))
    if grain > 0:
        g = _grain((H, W), ss * 1.2, seed=hash(text) % 9999)[..., None]
        face_rgb = np.clip(face_rgb * (1.0 + (g - 0.5) * 2 * grain), 0, 1)
        side_rgb = np.clip(side_rgb * (1.0 + (g - 0.5) * 2 * grain), 0, 1)

    # —— 组装
    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)

    # 投影（落影 + 接触影）
    sc = _rgb(shadow)
    far = _blur(_shift(m, cap * 0.030, cap * 0.068), max(1.5, cap * 0.078))
    near = _blur(_shift(m, cap * 0.008, cap * 0.018), max(1.0, cap * 0.024))
    sh_a = np.clip(np.maximum(far * 0.66, near * 0.88) * shadow_strength, 0, 1)
    rgb, alpha = _over(rgb, alpha, sc, sh_a)

    # 外描边暗圈：字压在亮底或中等底色上时，用它把字从背景里"拔"出来
    if outline > 0:
        ring = np.clip(_blur(union, max(1.0, cap * 0.030)) - union, 0, 1)
        rgb, alpha = _over(rgb, alpha, sc, np.clip(ring * outline, 0, 1))

    # 奶油外圈（【三·二十四·补】标题专用）—— 与字形**同一掩膜**均匀外扩 rim 像素。
    # ⚠️ 绝不要再叠一层"更大 cap_height 的同色字"当衬边：两层字号不同 → 逐字抖动不同 →
    #    衬边在行首行尾偏出去十几像素，整体读成「晕染 / 虚化 / 重影」。用户点名否掉。
    if rim > 0:
        R_ = max(1.0, rim * ss)
        outer = union
        for _i in range(16):
            _a = _i * math.pi / 8.0
            outer = np.maximum(outer, _shift(union, math.cos(_a) * R_, math.sin(_a) * R_))
        ring = np.clip(outer - union, 0, 1)
        ring = _blur(ring, max(1.0, ss * 0.50))        # 只做抗锯齿，不做雾化
        ring = np.clip((ring - 0.06) / 0.94, 0, 1)

        # 【三·三十】垫块要有**体积**，不能是一圈平涂细线（用户原话：「就只是纯文字框啊」）。
        # 实测第 9 页定稿：奶油垫块厚 12~24px（cap 95 时 ≈ 0.15cap），
        # 且**外缘亮(≈165,152,138)、贴字面的内缘暗(≈128,118,108)** —— 是一个受光的圆台面。
        # t = 0 贴字面(内) → 1 外缘；用两侧距离场归一化，避免用模糊近似导致的偏色。
        _u8 = (union > 0.5).astype(np.uint8)
        _o8 = (outer > 0.5).astype(np.uint8)
        _di = cv2.distanceTransform(1 - _u8, cv2.DIST_L2, 5)   # 到字面的距离（环内为正）
        _do = cv2.distanceTransform(_o8, cv2.DIST_L2, 5)       # 到外缘的距离（环内为正）
        _t = np.clip(_di / np.maximum(1e-6, _di + _do), 0, 1)
        _rc = _rgb(rim_color)
        rim_rgb = _mix(_darken(_rc, 0.24), _lighten(_rc, 0.03), np.clip(_t ** 0.85, 0, 1))
        rgb, alpha = _over(rgb, alpha, rim_rgb, ring)

    # 侧壁
    rgb, alpha = _over(rgb, alpha, side_rgb, union_s)
    # 顶面
    rgb, alpha = _over(rgb, alpha, face_rgb, m_s)

    out = np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2)
    out = np.clip(out, 0, 255).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")

    # 降采样
    if ss != 1:
        img = img.resize((max(1, W // ss), max(1, H // ss)), Image.LANCZOS)

    # 裁剪
    a = np.asarray(img)[:, :, 3]
    ys, xs = np.nonzero(a > 2)
    if len(ys):
        pad_px = max(1, int(cap_height * 0.03))
        y0, y1 = max(0, ys.min() - pad_px), min(img.height, ys.max() + 1 + pad_px)
        x0, x1 = max(0, xs.min() - pad_px), min(img.width, xs.max() + 1 + pad_px)
        img = img.crop((x0, y0, x1, y1))

    if debug_flat:
        flat = Image.new("RGB", img.size, (90, 76, 150))
        flat.paste(img, (0, 0), img)
        flat.save(debug_flat)

    if return_array:
        if out_path:
            img.save(out_path)
        return img
    if out_path:
        img.save(out_path)
    return img


# ---------------------------------------------------------------- 黏土铭牌 / 胶囊标签

def render_clay_badge(text,
                      out_path=None,
                      cap_height=40,
                      base=(243, 233, 219),
                      text_color=(58, 44, 40),
                      font="noto",
                      weight=800,
                      radius_ratio=0.5,
                      pad_ratio=(0.95, 0.52),
                      depth=None,
                      shadow=(52, 40, 86),
                      shadow_strength=1.0,
                      grain=0.05,
                      ss=3,
                      extra_left=0.0):
    """
    圆角胶囊 / 圆角矩形铭牌，文字压在里面（浅浮雕）。
    extra_left: 左侧额外留白（放小圆头像用），单位为字形高度的倍数
    """
    fp = FONTS.get(font, font)
    fs = cap_height * ss
    font_obj = _fit_font(fp, text, fs, weight)
    bb = font_obj.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py = pad_ratio
    padx, pady = tw * 0 + fs * px, fs * py
    left_extra = fs * extra_left
    W = int(tw + padx * 2 + left_extra)
    H = int(th + pady * 2)
    R = int(min(H, W) * radius_ratio)

    plate = Image.new("L", (W, H), 0)
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=255)
    pm = np.asarray(plate).astype(np.float32) / 255.0
    pm = _blur(pm, ss * 0.5)
    pm = np.clip((pm - 0.18) / 0.82, 0, 1)

    t_img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(t_img).text((padx + left_extra - bb[0], pady - bb[1]),
                               text, font=font_obj, fill=255)
    tm = np.asarray(t_img).astype(np.float32) / 255.0
    tm = _blur(tm, ss * 0.35)
    tm = np.clip((tm - 0.14) / 0.86, 0, 1)

    b = _rgb(base)
    if depth is None:
        depth = fs * 0.085
    T = max(2, int(round(depth)))

    # 板体厚度（向下）
    union = pm.copy()
    dmap = np.zeros_like(pm)
    for i in range(1, T + 1):
        s = _shift(pm, i * 0.18, i)
        new = np.clip(s - union, 0, 1)
        dmap = dmap + new * i
        union = np.maximum(union, s)
    dn = np.clip(dmap / max(1.0, T), 0, 1)
    side_rgb = _mix(_darken(b, 0.10), _darken(b, 0.34), np.clip(dn * 1.3, 0, 1))

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    grad = np.clip(1.0 - (0.55 * xx / max(1, W) + 0.30 * yy / max(1, H)), 0, 1)
    grad = (grad - grad.min()) / max(1e-6, grad.max() - grad.min())
    face_rgb = _mix(_darken(b, 0.10), _lighten(b, 0.09), grad)
    face_rgb = _mix(face_rgb, _lighten(b, 0.45),
                    np.clip(np.clip(pm - _shift(pm, 0, fs * 0.05), 0, 1) * 0.7, 0, 1))

    # 文字：压印（上方暗、下方亮）+ 主色
    tc = _rgb(text_color)
    press_dark = np.clip(tm - _shift(tm, 0, -fs * 0.05), 0, 1)
    tc_rgb = _mix(tc, _darken(tc, 0.55), np.clip(press_dark * 0.8, 0, 1))
    lower_light = np.clip(tm - _shift(tm, 0, fs * 0.05), 0, 1)
    tc_rgb = _mix(tc_rgb, _lighten(b, 0.20), np.clip(lower_light * 0.35, 0, 1))

    if grain > 0:
        g = _grain((H, W), ss * 1.1, seed=abs(hash(text)) % 9999)[..., None]
        face_rgb = np.clip(face_rgb * (1 + (g - 0.5) * 2 * grain), 0, 1)
        side_rgb = np.clip(side_rgb * (1 + (g - 0.5) * 2 * grain), 0, 1)

    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)
    sc = _rgb(shadow)
    far = _blur(_shift(pm, fs * 0.05, fs * 0.10), max(1.5, fs * 0.085))
    near = _blur(_shift(pm, fs * 0.012, fs * 0.028), max(1.0, fs * 0.026))
    sh_a = np.clip(np.maximum(far * 0.58, near * 0.78) * shadow_strength, 0, 1)
    rgb, alpha = _over(rgb, alpha, sc, sh_a)
    rgb, alpha = _over(rgb, alpha, side_rgb, union)
    rgb, alpha = _over(rgb, alpha, face_rgb, pm)
    rgb, alpha = _over(rgb, alpha, tc_rgb, tm)

    out = np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2)
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    if ss != 1:
        img = img.resize((max(1, W // ss), max(1, H // ss)), Image.LANCZOS)

    a = np.asarray(img)[:, :, 3]
    ys, xs = np.nonzero(a > 2)
    if len(ys):
        p = max(1, int(cap_height * 0.06))
        img = img.crop((max(0, xs.min() - p), max(0, ys.min() - p),
                        min(img.width, xs.max() + 1 + p), min(img.height, ys.max() + 1 + p)))
    if out_path:
        img.save(out_path)
    return img


def render_clay_card(head,
                     body="",
                     width=470,
                     head_size=26,
                     body_size=18,
                     base=(246, 240, 228),
                     head_color=(70, 52, 38),
                     body_color=(120, 101, 84),
                     accent=None,
                     font="noto",
                     ss=3,
                     shadow=(48, 36, 80),
                     shadow_strength=1.0,
                     grain=0.04,
                     radius_ratio=0.13,
                     out_path=None):
    """
    黏土卡片件：一块软垫状黏土牌 + 标题 + 自动换行的正文。
    这是"正文也能一体"的答案——正文不交给图片模型，而是做成独立的黏土件再合成。
    """
    fp = FONTS.get(font, font)
    W = int(width * ss)
    hf = _load_font(fp, head_size * ss, 800)
    bf = _load_font(fp, body_size * ss, 480)
    padx = int(W * 0.058)
    pady = int(head_size * ss * 0.70)
    head_lh = int(head_size * ss * 1.46)
    body_lh = int(body_size * ss * 1.70)
    acc_w = int(W * 0.014) if accent else 0
    text_x = padx + (int(acc_w * 2.6) if accent else 0)

    body_lines = []
    if body:
        maxw = W - text_x - padx
        cur = ""
        for ch in body:
            if bf.getlength(cur + ch) <= maxw:
                cur += ch
            else:
                body_lines.append(cur)
                cur = ch
        if cur:
            body_lines.append(cur)
    gap = int(body_size * ss * 0.62) if body_lines else 0
    H = pady * 2 + head_lh + gap + body_lh * len(body_lines)

    plate = Image.new("L", (W, H), 0)
    ImageDraw.Draw(plate).rounded_rectangle(
        [0, 0, W - 1, H - 1], radius=int(min(W, H) * radius_ratio), fill=255)
    pm = np.asarray(plate).astype(np.float32) / 255.0
    pm = _blur(pm, ss * 1.6)
    pm = np.clip((pm - 0.15) / 0.85, 0, 1)

    t_img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(t_img)
    bb = hf.getbbox(head)
    d.text((text_x - bb[0], pady - bb[1]), head, font=hf, fill=255)
    y = pady + head_lh + gap
    for ln in body_lines:
        bb = bf.getbbox(ln)
        d.text((text_x - bb[0], y - bb[1]), ln, font=bf, fill=255)
        y += body_lh
    tm = np.asarray(t_img).astype(np.float32) / 255.0
    tm = _blur(tm, ss * 0.40)
    tm = np.clip((tm - 0.16) / 0.84, 0, 1)

    b = _rgb(base)
    # 软垫厚度
    side = _blur(_shift(pm, 1.6 * ss, 3.4 * ss), 1.3 * ss)
    side_a = np.clip(side * 1.45, 0, 1)
    side_rgb = _darken(b, 0.17)

    # 面板：上亮下暗的柔和渐变
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    gy = yy / max(1.0, H)
    face_rgb = _mix(_lighten(b, 0.045), _darken(b, 0.075), np.clip(gy * 1.05, 0, 1))
    face_rgb = _mix(face_rgb, _lighten(b, 0.22),
                    np.clip(np.clip(pm - _shift(pm, 0, ss * 1.4), 0, 1) * 0.55, 0, 1))

    hc, bc = _rgb(head_color), _rgb(body_color)
    if grain > 0:
        g = _grain((H, W), ss * 1.0, seed=abs(hash(head)) % 9999)[..., None]
        face_rgb = np.clip(face_rgb * (1 + (g - 0.5) * 2 * grain), 0, 1)
        side_rgb = np.clip(side_rgb * (1 + (g - 0.5) * 2 * grain), 0, 1)

    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)
    sc = _rgb(shadow)
    far = _blur(_shift(pm, 1.0 * ss, 3.6 * ss), 3.4 * ss)
    sh_a = np.clip(far * 0.42 * shadow_strength, 0, 1)
    rgb, alpha = _over(rgb, alpha, sc, sh_a)
    rgb, alpha = _over(rgb, alpha, side_rgb, side_a)
    rgb, alpha = _over(rgb, alpha, face_rgb, pm)

    if accent:
        ac = _rgb(accent)
        bar = Image.new("L", (W, H), 0)
        bx = padx
        ImageDraw.Draw(bar).rounded_rectangle(
            [bx, int(pady * 0.75), bx + acc_w, H - int(pady * 0.75)],
            radius=acc_w // 2, fill=255)
        bm = np.asarray(bar).astype(np.float32) / 255.0
        rgb, alpha = _over(rgb, alpha, ac, _blur(bm, ss * 0.5))

    # 文字压印：上缘略深，下缘略亮，暗示"压进黏土里"
    press = np.clip(tm - _shift(tm, 0, -ss * 0.9), 0, 1)
    lift = np.clip(tm - _shift(tm, 0, ss * 0.9), 0, 1)
    hc_rgb = _mix(hc, _darken(hc, 0.45), np.clip(press * 0.55, 0, 1))
    hc_rgb = _mix(hc_rgb, _lighten(b, 0.25), np.clip(lift * 0.30, 0, 1))
    rgb, alpha = _over(rgb, alpha, hc_rgb, tm)

    b_img = Image.new("L", (W, H), 0)
    db = ImageDraw.Draw(b_img)
    y = pady + head_lh + gap
    for ln in body_lines:
        bb = bf.getbbox(ln)
        db.text((text_x - bb[0], y - bb[1]), ln, font=bf, fill=255)
        y += body_lh
    bm2 = np.asarray(b_img).astype(np.float32) / 255.0
    bm2 = _blur(bm2, ss * 0.32)
    bm2 = np.clip((bm2 - 0.16) / 0.84, 0, 1)
    rgb, alpha = _over(rgb, alpha, bc, bm2)

    out = np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2)
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    if ss != 1:
        img = img.resize((max(1, W // ss), max(1, H // ss)), Image.LANCZOS)
    if out_path:
        img.save(out_path)
    return img


# ---------------------------------------------------------------- 自测

def _selftest(outdir):
    os.makedirs(outdir, exist_ok=True)
    BG = (86, 70, 148)
    board = Image.new("RGB", (1280, 720), BG)
    # 底板
    d = ImageDraw.Draw(board)
    d.rounded_rectangle([40, 40, 1240, 500], radius=36, fill=(78, 63, 138))

    specs = [
        ("从会用 AI", (243, 233, 219), "noto", 900, 150),
        ("到拥有自己的 Skills", (243, 233, 219), "noto", 900, 150),
        ("从会用 AI", (243, 233, 219), "sthu", None, 150),
    ]
    y = 70
    for txt, col, fk, wt, cap in specs:
        img = render_clay_text(txt, cap_height=cap, base=col, font=fk, weight=wt,
                               shadow=(40, 30, 78), out_path=os.path.join(
                                   outdir, "t_" + fk + "_" + txt[:4].replace(" ", "_") + ".png"))
        board.paste(img, (70, y, 70+img.width, y+img.height), img)
        y += img.height + 14

    b1 = render_clay_badge("妇联职场班 | 3 小时实操课", cap_height=42, base=(240, 169, 60),
                           text_color=(70, 48, 20), shadow=(40, 30, 78),
                           out_path=os.path.join(outdir, "b1.png"))
    b2 = render_clay_badge("分享人：86 老师", cap_height=42, base=(150, 196, 92),
                           text_color=(38, 56, 24), shadow=(40, 30, 78),
                           out_path=os.path.join(outdir, "b2.png"))
    b3 = render_clay_badge("看懂 · 安装 · 使用 · 制作你的第一个 Skill", cap_height=40,
                           base=(120, 92, 190), text_color=(246, 240, 255),
                           shadow=(30, 22, 60),
                           out_path=os.path.join(outdir, "b3.png"))
    yy = 530
    for bb in (b1, b2):
        board.paste(bb, (70, yy, 70+bb.width, yy+bb.height), bb)
        yy += bb.height + 12
    board.paste(b3, (70, yy, 70+b3.width, yy+b3.height), b3)
    board.save(os.path.join(outdir, "selftest_board.png"))
    print("done ->", outdir)


def render_crisp_text(text,
                      out_path=None,
                      cap_height=27,
                      base=(240, 232, 214),
                      font="noto",
                      weight=800,
                      gap_ratio=0.15,
                      stroke=1.6,
                      stroke_color=(56, 36, 94),
                      stroke_right=0.55,
                      shadow=(46, 26, 72),
                      shadow_strength=0.45,
                      face_top=0.10,
                      face_bot=0.07,
                      grain=0.020,
                      jitter_rot=0.5,
                      jitter_y=0.006,
                      seed=3,
                      ss=4,
                      pad_ratio=0.40,
                      return_array=False):
    """**清晰描边字**——深底上的浅色小字专用（条带内文字 / 铭牌小字）。

    为什么单独开一个：`render_clay_text` 走"厚侧壁 + 强圆润化"路线，笔画会被
    加胖、相邻字会连成一片（实测字距只剩字高 2% → 用户读成"糊在一起"）。
    本函数反过来：
      · **字距 = 字高 × gap_ratio（默认 0.15，视觉间隙约 20%，对齐 86 老师）**
      · **不做强 gamma 压制**，字面是实心平涂 → 笔画分明
      · **深色方向性描边**（光在左上 → 右下侧描边更厚）把每个字从背景"切"开
      · 厚度近乎为零（只有一点上缘亮边 + 下缘暗边），"薄薄一层但每个字分明"

    参数：stroke 是**成品像素**（内部自动 ×ss）；gap_ratio 相对字高。
    """
    fp = FONTS.get(font, font)
    fs = cap_height * ss
    font_obj = _fit_font(fp, text, fs, weight)
    lines = text.split("\n")
    line_h = int(fs * 1.36)
    pad = int(fs * pad_ratio)
    gap = fs * gap_ratio

    rng = np.random.default_rng(seed)
    line_w = []
    for ln in lines:
        line_w.append(sum(font_obj.getlength(c) for c in ln) + gap * max(0, len(ln) - 1))
    W = int((max(line_w) if line_w else fs) + pad * 2)
    H = int(line_h * len(lines) + pad * 2)

    m_img = Image.new("L", (W, H), 0)
    # 【三·三十一】**逐字渲染必须共用 em 框**。
    # 曾经的写法：每字裁到自己的 ink bbox（`chh = bb[3]-bb[1]`）再贴到行顶部 ——
    # 墨迹高的字（"复/制/份" 29px）看着正常，墨迹**矮**的字就整块飞到行顶：
    # "一" 的 ink 只有 5px，顶对齐后中心落在 y219，而同排其它字在 y232 —— 高出 13px。
    # 用户原话：「它所有的字都在一个高度上，你这个 1 很明显它……第一笔是这么写，
    # 但你正常的字它不会这样写。这个是什么规则？你自己想一下。」
    # 正解：所有字都画在**等高的 em 框**里、用**同一个顶部锚点** → 基线天然一致。
    _asc, _desc = font_obj.getmetrics()
    em_h = max(1, _asc + _desc)
    for li, ln in enumerate(lines):
        x = (W - line_w[li]) / 2.0
        for ch in ln:
            adv = font_obj.getlength(ch)
            if ch.strip():
                bb = font_obj.getbbox(ch)
                cw = max(1, bb[2] - bb[0])
                sp = 6
                c_im = Image.new("L", (cw + sp * 2, em_h + sp * 2), 0)
                ImageDraw.Draw(c_im).text((sp - bb[0], sp), ch,
                                          font=font_obj, fill=255)
                if jitter_rot:
                    c_im = c_im.rotate(float(rng.uniform(-jitter_rot, jitter_rot)),
                                       resample=Image.BICUBIC, expand=True)
                dy = float(rng.uniform(-1, 1)) * jitter_y * fs if jitter_y else 0.0
                layer = Image.new("L", (W, H), 0)
                layer.paste(c_im, (int(round(x)), int(round(pad + li * line_h + dy))), c_im)
                m_img = ImageChops.lighter(m_img, layer)
            x += adv + gap

    m = np.asarray(m_img).astype(np.float32) / 255.0
    # 只做抗锯齿级别的柔化 + 轻收紧，**不压笔画**（保住"分明"）
    m = _blur(m, ss * 0.42)
    m = np.clip((m - 0.06) / 0.94, 0, 1)

    # —— 方向性深色描边：光在左上 → 右下侧更厚的暗边（这是"分明"的来源）
    T = max(1.0, stroke * ss)
    outer = m.copy()
    for i in range(12):
        ang = i * math.pi / 6
        outer = np.maximum(outer, _shift(m, math.cos(ang) * T, math.sin(ang) * T))
    TR = T * (1.0 + stroke_right)
    for i in range(8):
        ang = math.radians(25 + i * 16)          # 右下扇区
        outer = np.maximum(outer, _shift(m, math.cos(ang) * TR, math.sin(ang) * TR))
    ring = np.clip(outer - m, 0, 1)
    ring = _blur(ring, ss * 0.55)      # 描边柔一下 → 是"压出的暗边"，不是"印刷描边"

    # —— 字面：奶油平涂 + 极轻上亮下暗（"薄薄一层"，几乎平贴）
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    b = _rgb(base)
    gy = np.clip(yy / max(1.0, H), 0, 1)
    face = _mix(_lighten(b, face_top), _darken(b, face_bot), gy * 1.15)
    k = max(1.0, fs * 0.045)
    te = np.clip(m - _shift(m, 0, k), 0, 1)
    face = _mix(face, _lighten(b, 0.16), np.clip(te * 0.34, 0, 1))
    be = np.clip(m - _shift(m, 0, -k), 0, 1)
    face = _mix(face, _darken(b, 0.05), np.clip(be * 0.26, 0, 1))
    if grain > 0:
        g = _grain((H, W), ss * 1.1, seed=hash(text) % 9973)[..., None]
        face = np.clip(face * (1.0 + (g - 0.5) * 2 * grain), 0, 1)

    rgb = np.ones((H, W, 3), np.float32) * 0.5
    alpha = np.zeros((H, W), np.float32)
    sc = _rgb(shadow)
    far = _blur(_shift(m, fs * 0.030, fs * 0.060), max(1.2, fs * 0.060))
    near = _blur(_shift(m, fs * 0.008, fs * 0.018), max(1.0, fs * 0.020))
    sh_a = np.clip(np.maximum(far * 0.55, near * 0.80) * shadow_strength, 0, 1)
    rgb, alpha = _over(rgb, alpha, sc, sh_a)
    rgb, alpha = _over(rgb, alpha, _rgb(stroke_color), np.clip(ring * 0.98, 0, 1))
    rgb, alpha = _over(rgb, alpha, face, m)

    out = np.clip(np.concatenate([rgb * 255.0, alpha[..., None] * 255.0], axis=2), 0, 255)
    img = Image.fromarray(out.astype(np.uint8), "RGBA")
    if ss != 1:
        img = img.resize((max(1, W // ss), max(1, H // ss)), Image.LANCZOS)
    a = np.asarray(img)[:, :, 3]
    ys, xs = np.nonzero(a > 3)
    if len(ys):
        p = max(1, int(cap_height * 0.10))
        img = img.crop((max(0, xs.min() - p), max(0, ys.min() - p),
                        min(img.width, xs.max() + 1 + p),
                        min(img.height, ys.max() + 1 + p)))
    if out_path:
        img.save(out_path)
    return img


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        _selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
    else:
        print(__doc__)


def render_title_clay(text,
                      out_path=None,
                      cap_height=91,          # = 成品 ink 高（精确）
                      font='noto',
                      weight=900,
                      face=(206, 142, 48),
                      pad=0.026,
                      pad_mid=(230, 223, 211),
                      pad_edge=(243, 238, 228),
                      seam=(208, 200, 186),
                      seam_ratio=0.30,
                      bold=0.030,
                      stretch_x=0.95,
                      letter_gap=0.075,
                      shadow_off=(0.028, 0.075),
                      shadow_blur=0.055,
                      shadow_strength=0.55,
                      shadow_color=(20, 12, 36),
                      grain=0.028,
                      bevel=0.24,
                      seed=11,
                      pad_margin=0.60):
    """【三·三十二】**标题唯一正解** —— 全 13 页标题的唯一入口。

    造型（对照八六 p10「什么最值得做成 Skill？」+ p07「四道边界，必须先讲清」实测校准，
    2026-09-20 第十一轮）—— 八六真实做法是「**厚实饱满的黏土字 + 极细的边缘 + 字悬浮**」：
        · **厚实饱满、字边缘圆润** —— noto weight 900 + `bold=0.030` 等距膨胀
          （方角端点 → 圆角；同时把笔画养胖）
        · **极细的米白边**（八六实测描边色 (245,245,240)，就是近白）—— `pad=0.026`
          （≈2.4px @cap91），贴字面只压深一点点（seam 208,200,186），**不做厚奶油垫**
        · **暖橙黄字面**，带**上缘受光 / 下缘压深**的字面立体（`bevel`）——
          八六 p10 金面实测 (224,157,46)，取 (206,142,48) 留一点暗部
        · **哑光细腻肌理**（`grain=0.028`，细颗粒、低对比；**不是曲奇/饼干的烘焙颗粒感**）
        · **底部柔和厚重阴影** —— 影往下偏（0.028, 0.075）、blur 0.055、强度 0.55
        · **字悬浮，没有长条底板 / 底座** —— `letter_gap=0.075` 让相邻字（含各自的细边）
          保持分离。用户两次点名的"**橙色长条底板托着文字**"的真因：字距为 0 且边很厚时，
          相邻字的边在基线上并成一条连续横条 → 被读成底板。

    结构（从下到上）：柔影 → 细米白边 → 暖橙黄字面（含立体 + 细颗粒）。

    ⚠️ **每页标题都调这个函数**；版面宽窄不同时只允许调 `cap_height`（字号）
       与 `letter_gap`（但要**保持 ≥ 2×(bold+pad)**，否则相邻字的边会连成横条）。
       `cap_height` = **成品 ink 高**（== 你要的字有多高）。
    """
    from scipy import ndimage as ndi
    ss = 3
    # cap_height 的定义 = **成品 ink 高**。先反推"膨胀前"的字形高：
    # bold 是等距外扩，半径 r = bold*cap_height*ss（超采样像素），会让 ink 上下各 +r。
    target = cap_height * ss * max(0.5, 1.0 - 2.0 * bold)
    path = FONTS[font]
    f = _fit_ink_font(path, text, target, weight=weight)
    asc, desc = f.getmetrics()
    gap = letter_gap * cap_height * ss
    line_w = sum(f.getlength(ch) for ch in text) + gap * (len(text) - 1)
    mgn = int(cap_height * ss * pad_margin)
    W = int(line_w) + mgn * 2
    H = asc + desc + mgn * 2
    mi = Image.new('L', (W, H), 0)
    md = ImageDraw.Draw(mi)
    x = float(mgn)
    for ch in text:
        md.text((x, mgn + asc), ch, font=f, fill=255, anchor='ls')
        x += f.getlength(ch) + gap
    M = np.asarray(mi).astype(np.float32) / 255.0
    M = np.clip((M - 0.45) / 0.55, 0, 1)                 # 收紧抗锯齿边

    if abs(stretch_x - 1.0) > 1e-6:
        # 横向标定：第 9 页实测字面宽高比 3.835，noto 原字面 4.15 → 横向压 0.92
        _im = Image.fromarray((M * 255).astype(np.uint8))
        _im = _im.resize((max(1, int(round(_im.width * stretch_x))), _im.height), Image.LANCZOS)
        M = np.asarray(_im).astype(np.float32) / 255.0
        W = M.shape[1]
    if bold > 0:
        # 加粗 + 端点圆化：向外等距膨胀 = 方角变圆角（第9页端点圆角 ≈ 字高 15%）
        d0 = ndi.distance_transform_edt(M <= 0.5)
        # ⚠️ 半径 = bold × cap_height × ss（**不是** bold × ss —— 漏掉 cap_height 会让
        #    膨胀只有零点几像素，看起来"bold 完全没生效"，2026-09-20 踩过）
        M = np.clip((bold * cap_height * ss + 0.5 - d0), 0, 1)
    d_out = ndi.distance_transform_edt(M <= 0.5)         # 到字形距离（像素，外为正）

    pad_px = max(1.0, pad * cap_height * ss)
    P = np.clip(pad_px + 0.5 - d_out, 0, 1)              # 奶油垫
    t = np.clip(d_out / pad_px, 0, 1)                    # 0=贴字面, 1=垫外缘
    pad_rgb_2d = _mix(_rgb(seam), _rgb(pad_mid), np.clip(t / max(seam_ratio, 0.05), 0, 1))
    pad_rgb_2d = _mix(pad_rgb_2d, _rgb(pad_edge), np.clip((t - 0.55) / 0.45, 0, 1))
    ys, xs = np.where(P > 0.05)
    if len(ys):
        y0, y1 = ys.min(), ys.max()
        if y1 > y0:                                      # 垫块整体上亮下暗（很弱）
            gy = np.clip((np.arange(H)[:, None] - y0) / float(y1 - y0), 0, 1)
            pad_rgb_2d = np.clip(pad_rgb_2d * (1.025 - 0.055 * gy[..., None]), 0, 1)

    face_2d = np.ones((H, W, 3), dtype=np.float32) * _rgb(face)
    g = _grain((H, W), cap_height * ss * 0.085, seed)   # 尺度必须 > 降采样倍数，否则被抹平
    face_2d = np.clip(face_2d + (g[..., None] - 0.5) * (grain * 2.0), 0, 1)

    if bevel > 0:
        # 字面立体（豆包口径「厚实饱满的软陶字」）：**上缘受光、下缘压深**。
        # 取字形面内部靠上 / 靠下的窄边，做定向提亮与压深，笔画就有圆截面的体积感，
        # 不会像"平涂贴纸"。
        k = max(1.0, cap_height * ss * 0.030)
        up = _blur(np.clip(M - np.roll(M, int(k), axis=0), 0, 1), int(k * 0.6))
        dn = _blur(np.clip(M - np.roll(M, -int(k), axis=0), 0, 1), int(k * 0.6))
        face_2d = _mix(face_2d, np.ones(3, np.float32), np.clip(up * bevel * 1.15, 0, 1))
        face_2d = _mix(face_2d, np.array([0.42, 0.26, 0.10], np.float32),
                       np.clip(dn * bevel, 0, 1))

    rgb = np.zeros((H, W, 3), dtype=np.float32)
    alpha = np.zeros((H, W), dtype=np.float32)
    u = np.maximum(P, M)
    sh = _blur(_shift(u, shadow_off[0] * cap_height * ss, shadow_off[1] * cap_height * ss),
               max(1.0, shadow_blur * cap_height * ss))
    rgb, alpha = _over(rgb, alpha, _rgb(shadow_color), np.clip(sh * shadow_strength, 0, 1))
    rgb, alpha = _over(rgb, alpha, pad_rgb_2d, P)
    rgb, alpha = _over(rgb, alpha, face_2d, M)

    a8 = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    ys, xs = np.where(a8 > 2)
    m = int(cap_height * ss * 0.14)
    y0c, y1c = max(0, ys.min() - m), min(H, ys.max() + m + 1)
    x0c, x1c = max(0, xs.min() - m), min(W, xs.max() + m + 1)
    out = np.dstack([np.clip(rgb * 255.0, 0, 255).astype(np.uint8), a8])[y0c:y1c, x0c:x1c]
    img = Image.fromarray(out, 'RGBA')
    fw, fh = max(1, img.width // ss), max(1, img.height // ss)
    img = img.resize((fw, fh), Image.LANCZOS)           # 从超采样缩回成品尺寸

    # ⚠️ 颗粒必须在**降采样之后**加。在 ss=3 空间里加的话，那一步缩小会把逐像素噪声
    #    平均掉 —— 实测高频残留只有 1.7，而八六的标题是 8.5，等于"完全没有颗粒感"
    #    （就是用户说的"偏向曲奇/没质感"的反面：太干净、像贴纸）。2026-09-20 踩过。
    if grain > 0:
        arr = np.asarray(img).astype(np.float32)
        R, B = arr[..., 0], arr[..., 2]
        body = ((R - B) > 55) & (R > 150)             # 只加在暖色字面上，别糊到白边
        body = _blur(body.astype(np.float32), max(1.0, cap_height * 0.02))
        n = (_grain((fh, fw), max(1.2, cap_height * 0.050), seed + 3) - 0.5) \
            * (grain * 2.0 * 255.0)
        arr[..., :3] = np.clip(arr[..., :3] + n[..., None] * body[..., None], 0, 255)
        img = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    if out_path:
        img.save(out_path)
    return img
