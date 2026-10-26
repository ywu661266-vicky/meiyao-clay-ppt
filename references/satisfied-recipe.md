# 满意版实测配方（《专家技能连接器_10页》制作实录复原 · 2026-10-22 深夜从会话转录挖出）

> 来源：本会话转录（62d82f01）中 2026-10-11 18:58 ~ 10-12 00:01 的 **36 条真实出图调用**原文。
> 这是唯一被用户确认"都很生动，这套就是我满意的"成品的真实做法。**skill 一切规则以此为准。**

## 一、三步配方（每一步都有实录佐证）

### 第 1 步 · 角色锚点（1024×1024，图生图）
- 18:58–19:18 共 7 条，**每条都传参考图 image1**（`assets/style-refs/` 实物黏土小人照片）。
- prompt 开头固定：
  `Use the reference image as the LOCKED character and art-style source. Reproduce this SAME clay character... Match the EXACT art style, clay material, proportions and rendering of the reference image.`
- 产出：蓝裙、圆框眼镜、顶髻+粉蝴蝶结的黏土小女孩 → 后面所有页的 image2。

### 第 2 步 · 每一页（1024×576，双图锚）
- **每条页面调用都带两张参考图**：
  - `image1` ＝ **已通过的同型参考页**（锁版式 + 画风）：prompt 写 `Follow the LAYOUT of image1` / `EXACTLY the same style, palette and lighting as the reference image: deep purple textured clay wall background...`
  - `image2` ＝ **角色锚点图**（锁脸）：`Use image2 as the character.`
- 新课件的 `image1` 从哪来？→ **`assets/style-refs/*.jpg` 的实物黏土照片**（默认，不含真实人脸）。
  ⛔ 不是 `assets/owner-private/P01–P10.png`——那是作者本人形象，只在作者本人做自己的课件时可用（隐私铁律 12）。
- prompt 骨架：`A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation slide/cover... Deep purple clay wall background with subtle handmade clay texture.`

### 第 3 步 · 迭代修页（不合格重出，毛病写成禁令）
- 实录：对比页连出 5 次（23:01→23:22），每次把上一张的毛病写成否定句追加：
  `NO extra elements. NO empty card, NO blank capsule. There must be no...`
- 装盘前：去水印 → 放大 1920×1080 → python-pptx 0,0 满版。

## 二、关键参数铁律

| 项 | 正确值 | 错值下场 |
|---|---|---|
| 出图 size | **`1024x576`**（16:9） | `1920x1080` 工具不支持 → 回落 3:2 白边（同事版死因） |
| 参考图 | **每张必传** image1（参考页）+ image2（角色锚） | 纯文字生图 = 抽签出呆丑版 |
| 装盘尺寸 | 放大到 **1920×1080** 满版 | 3:2 直接上 = 白边 |
| 迭代 | 一页不合格就重出，毛病变禁令 | 凑合交付 = 整套掉档 |

## 三、给接收方的一句话

> 别问"为什么必须传参考图"——满意版 36 条调用**没有一条是纯文字生成的**。
> 你跳过参考图，就是离开唯一被验证过的路。

## 四、稳定出品三道闸（2026-10-25 补 · 任何人丢照片都必须满足）

1. **必有照片**：没有角色照片（image2）绝不生成人物，先问。纯文字捏人必出丑八怪。
2. **两阶段不可省**：Stage 1 先建角色锚点（`image1`＝**画风锚**（默认 `assets/style-refs/*.jpg` 实物黏土照；仅作者本人时可用 `owner-private/P01.png`）＋ `image2`＝照片 → 产出该人的黏土角色锚点）；Stage 2 起每页都用这张锚点当 `image2`，绝不每页重新拿照片现捏。没走 Stage 1 时，`image2`＝中性模板 `assets/characters/neutral-anchor.png`。
3. **强人设不可省**：每个角色必须有"发型＋≥1 标志性配饰"的成体系人设（参考满意版丸子头＋粉蝴蝶结＋圆框眼镜＋蓝背带裙）。照片素净无标志时，主动提议 1–2 个签名元素并确认——不许滑回"衬衫＋通用笑脸"模板（派派那张 7/10 就是栽在这）。

> 满足这三闸，"你再生成一个你形象的女孩 / 别人生成他形象的人物"都能稳定出跟满意版同款的 house 风 Q 版小人。
