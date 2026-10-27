# 提示词模板（已验证 · 2026-10-22 按"满意版"重写）

> ## 唯一路径：一页 = 一张 1920×1080 的整图（出图请求用 `size:"1024x576"`，装盘前放大到 1920×1080），字全部烘进去
>
> - **画布（请求尺寸）**：`size:"1024x576"`（16:9，工具实际支持）。出图后脚本放大到 1920×1080 装盘。**不许直接请求 1920x1080（回落 3:2 白边）**，**不许 1536×1024（3:2）**。
> - **结构**：横幅标题 + 副标题 + N 个色块面板 + 底部结论条，**一页 ≥4 个信息块**。
> - **文字**：这一页要上屏的中文**全部原样写进 prompt、用单引号括起来**，句末加
>   `Make every Chinese character clearly readable and correctly formed, no garbled characters.`
> - **材质**：`handmade polymer-clay diorama, subtle fingerprints, soft directional light, rich dimensional shadows, not flat, not vector`
> - **人物**：出现就"完整全身"；**每次出图传两张参考图**——`image1`＝画风锚（满意版对应页），`image2`＝角色锚点（见 §0.5）。
>
> ### 🚫 三条硬禁止（旧版的逃生口，已封）
> 1. **不许**"背景板留白 + 事后贴字"当主路——成品不是用户要的那版。
> 2. **不许**在图上叠扁平字体文本框——没厚度没投影，一眼分家。
> 3. **不许**写"想省事也可以…"这类并列选项。**规则里只准有一条路。**
>
> `clay_text.py` / `compose_page.py` 只作**改字补丁**（用户只想改一两个字、不想重出整图时用），见 §4.1。
>
> 核心写法：**场景与材质用英文（模型理解更稳），要出现在图上的中文原样写进 prompt 并用单引号括起来。**
>
> **场景从哪来？** 不要每次现编——封面场景从 `references/style-library.md`【封面款式库 CV1–CV6】选，内页场景从【内页款式库 IN1–IN14】选，人物款式从【人物款式库 A–F】选。**换场景块 = 换花样；逐字不动的人物段 + 参考图 = 保一致。**
>
> ### §0.5 画风锚定段（每张图 prompt 首行必加，2026-10-22 新增）
>
> ```
> Keep the EXACT handmade polymer-clay art style of image1: same clay material with fingerprints, same dimensional soft lighting and shadows, same color system, same banner and panel design language, same text rendering quality, same cute and lively character feel. Replace ALL text with the new text below and adjust the scene to the new topic. Do NOT copy any text, letters, numbers or layout wording from image1.
> ```
>
> - `image1` ＝ **画风锚**：**默认＝`assets/style-refs/*.jpg` 的实物黏土手作照片**（house 风源头，**不含任何真实人物的脸**，7 张轮换取用）。
>   - ⛔ **不是** `assets/owner-private/P01–P10.png`——那是**作者本人的形象**，默认用它等于把作者的脸喂给外人（隐私铁律 12）。
>   - ✅ 仅当**作者本人**做自己的课件时才可用 owner-private 那套：封面 P01 / 目录 P02 / 内容 P03–P09 轮换 / 总结 P10，就近取。
> - `image2` ＝ **形象锚**：Phase 1 角色锚点图（谁用就是谁的形象）
> - **缺这一段或缺任一张参考图 = 纯文字抽签 = 呆丑版（已实测根因）。**

---


## 0. 黏土立体字（Clay Lettering）标准描述段

任何需要出字的模板，都把下面这段拼进去：

```
The '{文字}' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, visible clay thickness, subtle fingerprints and sculpting marks on every letter, casting soft real shadows onto the plaque beneath. Handmade clay lettering, NOT flat printed text, NOT a digital font overlay.
```

**字块颜色**（按配色选，要和画面协调但保证对比度）：
| 铭牌底色 | 字块颜色 | 写法 |
|---|---|---|
| 奶油白/浅杏（默认） | 深可可棕 | `deep chocolate-brown clay letters` |
| 奶油白 | 深藏蓝 | `deep navy clay letters` |
| **深色底（紫/深蓝/绿/橙等）** | **奶油白** | `cream-white clay letters` |
| **暖色系（马卡龙/彩虹/奶杏）** | **深棕/深藏蓝** | `deep chocolate-brown clay letters` |

> ⚠️ **铭牌颜色必须随方案换**（详见 `references/style-system.md` §2.1 铭牌配色映射表）。❌ 禁止在换色系时仍写 `cream-colored clay plaque`——否则底框白色率会飙到 40-77%。

---

## 1. 角色锚点（Character Anchor）· 1024×1024

> **人物段的唯一真源 = `references/character-style.md`。** 那里有用户的判级、八六原版画法解剖、身份锁定段、换装清单、多小人规则。
> **必须出「完整全身」**：只出半身，后面要全身时模型会自己"补"下半身，服装和比例就漂了。
> **画风基准（不是"唯一默认款"）= 圆框眼镜 + 深色发 + 约 2.5–3 头身 Q 版小孩**（= **用户自己的成品** `cover-excel-example.png` / `toc-clay-lettering-example.png`）。
> **人物要"百变、不定死"**：脸 / 画风锁，衣服 / 姿态 / 场景每页可变、可男可女。

```
A single premium handcrafted polymer-clay figurine of a cute little kid presenter, about 2.5–3 head-lengths tall (a big round head on a small compact body, short rounded limbs — NOT a tall slender figure, NOT an adult). COMPLETE FULL BODY from the top of the hair down to the shoes, standing upright, facing the camera, entire body completely visible inside the frame, head to toe, NOT cropped by any frame edge, with clear empty margin above the hair and below the shoes.

Hair: dark (black or deep brown) hair gathered into a neat top bun, with a soft side-swept fringe, and a rose/pink bow headband across the top of the head.

Face: big round cute face, large expressive eyes with clear highlights, a small smiling mouth, soft rosy blush. Wearing large ROUND glasses on the nose.

Outfit: a blue pinafore dress over a light cream shirt, tiny rounded shoes (clothes may change page to page — see the outfit list in character-style.md).

Material: handmade polymer clay with clear fingerprints, sculpting tool marks and slightly matte soft surfaces on every form; NOT photorealistic, NOT glossy plastic toy, NOT flat anime line art.

Lighting: soft even studio light with gentle contact shadow at the feet. Background: plain light warm grey seamless backdrop for later compositing. No text, no watermark, no letters, no numbers.
```

**脸部锁定段（同一套之内每页必抄，一字不改 —— 只锁脸，不锁衣）：**
```
Keep EXACTLY the same little kid character from the reference image: identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical clay-material look and identical 2.5–3-head-length chibi proportion. Only the clothing, the pose and the surrounding scene may change.
```

**同页多小人（八六原版就这么用，不会出错）：**
```
The SAME character appears {N} times in this scene, each instance with the identical face and identical hairstyle, but performing DIFFERENT actions — one {action A}, one {action B}. Same face, same hair, same glasses on every instance; only the pose differs.
```
> ⚠️ 不要写 "two girls"（模型会理解成两个不同角色），要写 `the SAME character, repeated`。

**换装清单 / 备选人物款式 / 判级**：见 `references/character-style.md`。

> **⚠️ 人物一致性硬规则（已实测）：** 后续**每一页**（封面/目录/内容页/总结页）都**必须**把这张角色锚点图作为 `image1` 传给 ImageGen 做 image-to-image。
> 只靠文字描述会漂移——实测翻车：**锚点图是 1 个头顶啾啾，封面却生成 2 个侧丸子头，脸也变了**。
> 同样地，使用者若提供了**自己的照片**或**喜欢的画风参考图** → 用 `image2` 传入，按其长相与画风生成（"按使用者的形象来"是明确需求）。
>
> **想要脸更可爱**时，不要重写整段人物描述，而是在 image-to-image 的 prompt 里只改脸：
> `ONLY make the face cuter: rounder softer face, bigger rounder glossy eyes with large highlights, fuller soft rosy blush, a tiny nose, a small gentle closed smile (no open mouth, no teeth)` —— 头发、发饰、服装、材质一律不动。

---

## 2. 封面（Cover）· 1024×576（出图请求，装盘放大 1920×1080）

> 用途：整页效果确认图。**标题、副标题、署名全部烘进图**（黏土立体字），不分层贴。
> 场景从 `references/style-library.md`【封面款式库 CV1–CV6】任选一个场景块替换桌面场景，人物段照旧不动。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation cover, 1024x576 (upscaled to 1920x1080 for the slide). The SAME little kid character from the reference image — identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length chibi proportion — standing upright in the scene, COMPLETE FULL BODY from the top of her hair down to her shoes, NOT cropped by any frame edge, with clear empty margin above her hair and below her shoes. She wears {换装，见 character-style.md 换装清单}. She is placed inside the scene, interacting with it, sharing the same light as the props. On the desk: a laptop, clay books, a potted plant, a coffee mug, small clay star decorations. {背景色} gradient background with scattered clay stars.

COMPOSITION (must be exactly this): a large {铭牌色} clay ribbon plaque occupying the TOP-LEFT area; below it two stacked pill labels.

TEXT, all sculpted as thick 3D raised polymer-clay letters with visible thickness, rounded edges, fingerprints and soft real shadows — NOT flat printed text:
- On the big plaque, the main title '{主标题}' in {字块色} clay letters, the largest element.
- On the first pill, the subtitle '{副标题}'.
- On the second pill, '{署名/课程信息}'.

Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. High-end educational presentation cover. Make every Chinese character clearly readable and correctly formed, no garbled characters. No watermark, no logo, no page number.
```

> **{铭牌色} 和 {字块色} 必须根据配色方案替换**（见 `references/style-system.md` §2.1 铭牌配色映射表），❌ 不许留 `cream-colored` 不动。
> 小头像徽章（可选）用 `image2` 传用户的照片，让模型在角上捏一枚小圆牌，写 `'{分享人}'`。

**要点：**
- 出图请求尺寸必须是 **1024×576**，装盘前放大到 1920×1080；出来的不是 16:9 就当场重出。
- **人物要「完整全身」**：`COMPLETE FULL-BODY figure ... NOT cropped by any frame edge`，比例 `about 2.5–3 head-lengths`（Q 版小孩）。
- 中文**原样写进 prompt 并用单引号括起来**，句末保留 `clearly readable and correctly formed`。
- **用 Phase 1 的全身锚点图作 `image1`**（只靠文字描述会漂移）。
- 🚫 不要"空牌匾 + 事后贴字"——那是被否掉的旧路。

---

## 3. 目录页（Table of Contents）· 1024×576（出图请求，装盘放大 1920×1080）

> **标题与 4–6 个卡片标签全部烘进图。**

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen table of contents slide, 1024x576 (upscaled to 1920x1080 for the slide). {背景色} deep gradient background with scattered clay stars and soft vignette.

COMPOSITION: a wide {铭牌色} clay ribbon plaque across the TOP CENTER. Below it, {N} rounded rectangular clay cards in a {2x2 / 3x2} grid, each card in a different color from the palette ({紫}/{绿}/{橙}/{红}) and each carrying a small clay icon ({图标清单}). At the bottom, one long cream clay strip holding a one-line summary.

TEXT, all sculpted as thick 3D raised polymer-clay letters, NOT flat printed text:
- Plaque: '{课程目录}'
- Card 1: '{标签1}'   Card 2: '{标签2}'   Card 3: '{标签3}'   Card 4: '{标签4}'
- Bottom strip: '{一句话概括}'

Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. Make every Chinese character clearly readable and correctly formed, no garbled characters. No watermark, no logo, no page number.
```

> **{铭牌色} / 面板四色 必须按配色方案写死**，❌ 不许留 `cream-colored` 不动。
> 标签 **4–6 个字**最稳；编号（01/02…）直接写进标签，例如 `'01 专家'`。

---

## 4. 内容页 · 1024×576（出图请求，装盘放大 1920×1080，一页一张整图）

> 每页都必须：**横幅标题 + 副标题 + ≥4 个信息块 + 底部结论条**，字全部烘进图。
> 场景块从 `references/style-library.md`【内页款式库 IN1–IN14】任选，相邻页不重复。
> 必须把 Phase 1 的全身锚点图作为 `image1` 传入。

### 4-A 骨架：横幅标题 + 四色面板（最常用）

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation slide, 1024x576 (upscaled to 1920x1080 for the slide). {背景色} deep gradient background with soft vignette and a few clay stars.

COMPOSITION:
- A wide deep-purple clay ribbon plaque across the TOP holding the section title.
- Directly under the plaque, one small cream clay pill holding a subtitle.
- The MIDDLE holds exactly {4} rounded clay panels in one row, each panel a different palette color ({紫}/{绿}/{橙}/{红}), each with ONE clay icon on top and a short clay label at its bottom.
- Across the BOTTOM, one long dark clay strip holding a one-line takeaway, with small clay dots between items.

TEXT, all sculpted as thick 3D raised polymer-clay letters with visible thickness and soft real shadows, NOT flat printed text:
- Plaque: '{本页标题}'
- Subtitle pill: '{一句话副标题}'
- Panel labels: '{标签1}' '{标签2}' '{标签3}' '{标签4}'
- Bottom strip: '{结论一句话}'

Tactile soft clay with subtle fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows, not flat, not vector. Make every Chinese character clearly readable and correctly formed, no garbled characters. No watermark, no logo, no page number.
```

**实例（已通过验收的写法）**：标题 `'三、连接器：给它一扇通往外面的门'`、副标题 `'把外部服务接进来'`、
四个面板 `'查数据' '调服务' '管文件' '发通知'`、底部条 `'已支持 QQ邮箱·腾讯文档·腾讯会议·TAPD·飞书·钉钉 等'`。

### 4-B 骨架：横幅标题 + 左右对比（VS）

```
{same 画布/背景/材质段}
COMPOSITION:
- Top ribbon plaque with the title.
- Below it a small cream pill with a one-line question.
- TWO large clay panels side by side, left in {色A}, right in {色B}; between them a round clay badge with 'VS'.
- Inside each panel: 1–3 short clay lines.
- Bottom-right or bottom-left: the character as a COMPLETE FULL-BODY figure pointing at the conclusion; plus one cream pill with the takeaway.

TEXT (all raised clay letters): '{标题}' / '{副标题}' / '{左边标题}' / '{左边1-3条}' / '{右边标题}' / '{右边1-3条}' / 'VS' / '{结论}'
```

**实例**：`'专家 与 专家团：一张图分清'` + `'一个人干，还是一队人干'` + 左 `'专家 ＝ 一个角色'` / 右 `'专家团 ＝ 一群专家 ＋ 一位团长'`。

### 4-C 骨架：流程带 / 档案清单 / 路线图

见 `references/style-library.md`【三·三十五】20 种版式语汇与 `references/skeleton-library-81.md`。
要点不变：**标题烘进图、每页 ≥4 块、底部有结论条、相邻页不同版式。**

---

## 4.1 改字补丁（**非主路**，只在用户说"只改这几个字"时用）

整图已经出好、只想换一两个词、不想重出图时，才用脚本贴字：

```bash
python scripts/compose_page.py --config pages.json
```

```json
{
  "bg": "out/page07.png",
  "out": "out/page07_v2.png",
  "elements": [
    { "type": "text",  "text": "新的标题", "cap": 54, "x": 120, "y": 40, "color": "cream" }
  ]
}
```

> ⚠️ 这条路的成品**稍逊于整图**（贴上去的字和画面光照很难完全一致），
> 只在"改字成本 < 重出图成本"时用；**不要拿它当整套的生产方式**。

---

## 5. 总结 / 结尾页（Summary）· 1024×576（出图请求，装盘放大 1920×1080）

> 同其他页：**整页一张图，标题与结论条都烘进去**。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen closing slide, 1024x576 (upscaled to 1920x1080 for the slide). {背景色} deep gradient background with floating clay stars and soft bokeh.

COMPOSITION: a large {铭牌色} clay plaque on the LEFT holding the closing title; on the RIGHT the SAME little kid character from the reference image, COMPLETE FULL BODY from hair to shoes, NOT cropped, giving an encouraging gesture beside a small clay robot; at the BOTTOM a long cream clay strip holding the one-line takeaway.

TEXT, all thick 3D raised polymer-clay letters with real shadows, NOT flat printed text:
- Plaque: '{结尾标题}'
- Bottom strip: '{一句话收尾}'

Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. Make every Chinese character clearly readable and correctly formed, no garbled characters. No watermark, no logo, no page number.
```

> **{铭牌色} 必须根据配色方案替换**，❌ 不许留 `cream-colored` 不动。

---

## 6. 改图（Image-to-Image）

> 用户说"把这张的 X 换成 Y"时使用：把原图作为 `image1` 传入，prompt 只描述**要改的部分**，并保留其余。

```
Keep everything unchanged, including the clay lettering and its sculpted 3D texture. Only change {被改元素} to {目标元素}. Preserve the same polymer-clay texture, composition, lighting, background and all existing text. No watermark.
```

参数：`image1: <原图路径>`，可选 `input_fidelity`（调高更贴近原图）。

**改字的写法**（用户说"标题改成 XX"）：
```
Keep the entire scene unchanged. Only replace the clay lettering on the {铭牌色} plaque with '{新文字}', sculpted from the same thick 3D raised polymer-clay letters, same color ({字块色}), same thickness, same soft shadows, casting real shadow on the plaque. Handmade clay lettering, not flat printed text. Make every Chinese character clearly readable and correctly formed.
```

---

## 通用负面约束

**出图页（要中文黏土字）：**
```
No watermark, no page number, no flat printed text, no digital font overlay.
```

> ⚠️ **`No watermark` 管不住平台浮标。** 它只能约束画面里"画出来"的东西；而右下角那个 `AI生成` / `WORKBUDDY` 白色浮标是**出图平台自动盖的**，prompt 里写什么都没用（已实测）。
> 必须在出图后跑 `python scripts/remove_watermark.py <目录>` 抹掉它。**带水印的图不许交付。**

**不带字的图（只有角色锚点）：**
```
No watermark, no page number, no letters, no numbers.
```

**所有模板都建议追加（渲染中文的保险索）：**
```
Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

---

## 中文渲染的三条实操经验

1. **字符数越少越稳。** 标题 ≤ 8 字、卡片标签 ≤ 5 字最保险；13 字以上（含英文符号）也能成，但必须保留"clearly readable / correctly formed"那句。
2. **中英混排没问题**（实测 `'AI + Excel 数据处理实战'` 全对），但英文和中文之间留空格更稳。
3. **一定要写"黏土字"的材质句**：`sculpted from thick 3D polymer-clay letters ... not flat printed text`。只写"有标题"而不写材质，模型很容易给你贴一行扁平黑体——那就是失败版。
4. **绝对不要指望模型在整页里写正文**：中文笔画密度太高，一句话说明就会出错字/缺笔/乱码，改一个字还得重出整张图。
   **正文一律走 `clay_text.py` 的 `card` 版式**（黏土卡片件 + 清晰文字），再由 `compose_page.py` 贴回去 —— 字是黏土件、贴上去一体、字数不受限。这才是"内页写不进内容"的正解。
   **反过来也别用扁平字体文本框糊弄**：那没有黏土厚度和投影，和画面分家，一眼假。
