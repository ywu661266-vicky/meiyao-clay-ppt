# 提示词模板（已验证）

> ## ⚠️ 第一性原理：字和图都要黏土，分件做、最后贴成一体
>
> - **背景板（ImageGen）**：黏土场景 + **完整全身人物** + 给文字留白；**不要**在整页里写正文。
> - **黏土件（`scripts/clay_text.py`）**：所有文字——大标题 / 正文 / 标签——**单独捏成黏土件**，
>   再用 `scripts/compose_page.py` 贴回画面。改字只改字符串，不重出图。
>
> **错法 1（必翻车）：** 让模型在整页里写正文 → 中文一多必错字乱码（实测出过"抓技技能 / 技拔卡"），
> 而且改一个字就得重出整张图。
> **错法 2（一眼假）：** 正文用**扁平字体的文本框**叠在图上 → 没厚度没投影，不在黏土的光照里，明显分家。
>
> **规则：**
> 1. 背景板 prompt 必须写清"**哪块留白、留白区禁止出任何东西**"。
> 2. **A 路**：让模型顺带烘 **≤8 字** 的黏土标题（省一次贴字，但字要重出才能改）。
>    **B 路（推荐）**：背景板**一个字都不出**，标题也交给 `clay_text.py` —— 字数、位置、颜色全可控。
> 3. **正文一律走 `clay_text.py` 的 `card` 版式**（黏土卡片 + 清晰文字）——这是"字多又一体"的解法。
> 4. 第 0 节的"黏土字材质句"只在**走 A 路**（让模型烘字）时才需要写。
>
> 核心写法：**场景与材质用英文（模型理解更稳），要出现在图上的中文原样写进 prompt 并用单引号括起来。**
>
> **场景从哪来？** 不要每次现编——封面场景从 `references/style-library.md`【封面款式库 CV1–CV6】选，内页场景从【内页款式库 IN1–IN14】选，人物款式从【人物款式库 A–F】选。**换场景块 = 换花样；逐字不动的人物段 + 参考图 = 保一致。**

---

## 0. 黏土立体字（Clay Lettering）标准描述段

任何需要出字的模板，都把下面这段拼进去：

```
The '{文字}' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, visible clay thickness, subtle fingerprints and sculpting marks on every letter, casting soft real shadows onto the plaque beneath. Handmade clay lettering, NOT flat printed text, NOT a digital font overlay.
```

**字块颜色**（按配色选，要和画面协调但保证对比度）：
| 铭牌底色 | 字块颜色 | 写法 |
|---|---|---|
| 奶油白（默认） | 深可可棕 | `deep chocolate-brown clay letters` |
| 奶油白 | 深藏蓝 | `deep navy clay letters` |
| 深色底（无铭牌） | 奶油白 | `cream-white clay letters` |

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

## 2. 封面（Cover）· 1024×576

> 用途：整页效果确认图。**主标题以黏土立体字烘进图。**
> 场景不要每次现编——从 `references/style-library.md`【封面款式库 CV1–CV6】任选一个场景块替换下面的桌面场景（云岛 / 工具台 / 知识书架 / 直播间 / 咖啡工位 / 阶梯图书馆），人物段照旧不动。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation cover. The SAME little kid character from the reference image — identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length chibi proportion — standing upright in the scene, COMPLETE FULL BODY from the top of her hair down to her shoes, NOT cropped by any frame edge, with clear empty margin above her hair and below her shoes. She wears {换装，见 character-style.md 换装清单}. She is placed inside the scene, interacting with it, sharing the same light as the props. On the desk: a laptop showing a colorful spreadsheet of cells, clay books, a potted plant, a coffee mug, small clay star decorations. Deep blue gradient background with scattered clay stars. At the top center, a wide cream-colored clay ribbon plaque; on it, the title '{标题}' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, deep chocolate-brown clay, visible thickness and fingerprints on every letter, casting soft real shadows onto the plaque. Handmade clay lettering, not flat printed text. Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. High-end educational presentation cover. Make every Chinese character clearly readable and correctly formed.
```

**要点：**
- **人物同样要「完整全身」**：`COMPLETE FULL-BODY figure ... NOT cropped by any frame edge`，比例 `about 2.5–3 head-lengths`（Q 版小孩）。封面裁半截同样算不合格。
- 中文标题用**单引号原样包住**，句末追加 `Make every Chinese character clearly readable and correctly formed.`
- 标题放在**顶部居中奶油铭牌**上，下方留人物与桌面
- 配色词（`Deep blue gradient`）随方案替换；字块颜色随铭牌底色替换
- **务必保留** `sculpted from thick 3D polymer-clay letters` / `not flat printed text` 这两句，这是出效果的关键
- **用 Phase 1 的全身锚点图作 `image1`**（只靠文字描述会漂移）

---

## 3. 目录页（Table of Contents）· 1024×576

> **标题与卡片标签都烘进图**（黏土字），不再留空给脚本。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen table of contents slide. Six rectangular clay cards arranged in a 3x2 grid on a blue clay workbench, each card carrying a small clay icon (a document, a spray bottle, a calculator, a bar chart, stacked cards, a camera). A friendly small clay robot assistant sits at the corner. Clay books, a potted plant and a coffee cup decorate the scene. Deep blue gradient background, soft directional lighting, rich dimensional shadows. At the top center, a cream-colored clay ribbon plaque; on it the title '课程目录' is sculpted from thick 3D raised polymer-clay letters with visible thickness and fingerprints, casting soft shadows. Each card carries a short raised clay-letter label: '数据读取', '数据清洗', '数据汇总', '数据可视化', '批量分类', '照片变表格' — all sculpted as chunky rounded 3D clay letters, deep chocolate-brown, not flat printed text. Tactile soft clay, rounded friendly shapes. Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

> 卡片的**编号**（01–06）也可以要，但中文标签优先。标签控制在 **4–5 个字以内**，字越少越不容易写错。
> **更稳的做法：目录页背景板只出"卡片 + 小图标"（卡片面上留空），标签文字用 `clay_text.py` 的 `badge` 贴上去** —— 想改哪个标签就改哪个，不用重出图。

---

## 4. 内容页背景板 · 1024×576（A 路 / B 路）

> 内容页的背景板只负责**画面**：完整全身人物 + 场景 + 留白。
> **A 路** = 让模型顺带烘一个 ≤8 字的黏土标题；**B 路（推荐）** = 一个字都不出，标题和正文全交给 `clay_text.py`。
> 场景块从 `references/style-library.md`【内页款式库 IN1–IN14】任选，相邻页不重复。
> **两条路都必须把 Phase 1 的全身锚点图作为 `image1` 传入。**

**B 路模板（推荐：背景板完全不出字）**

```
BACKGROUND PLATE ONLY. Use image1 as the LOCKED character identity.
{把第 1 节那段全身人物描述逐字粘过来}
Create a premium handcrafted polymer-clay diorama, 16:9 widescreen presentation slide background, {配色} gradient wall.

LAYOUT: The RIGHT 40% of the frame holds the girl as a COMPLETE FULL-BODY figure standing on a small round clay podium — her ENTIRE body from the top of her hair down to her shoes completely visible inside the frame, head to toe, NOT cropped by any frame edge, NOT hidden behind furniture or props, with clear empty margin above her hair and below her shoes. Keep her face locked to the reference image: identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length chibi proportion. She wears {换装}. Beside her feet only {道具1} and {道具2}.

The LEFT 55% of the frame must be a COMPLETELY EMPTY smooth gradient wall — NO cards, NO boxes, NO shelves, NO icons, NO frames, NO props in the left area; it is deliberately reserved blank space for text that will be added later.

Absolutely NO text, NO letters, NO numbers, NO labels anywhere in the image — no title, no plaque, no signage. The whole frame is picture only.

Handmade polymer-clay texture with subtle fingerprints, soft studio lighting, rounded friendly shapes, unmistakably handmade clay, not photorealistic, not anime, not glossy plastic. No watermark, no logo.
```

**A 路模板（让模型顺带烘标题，省一次贴字）**

```
BACKGROUND PLATE ONLY, no body text. Use image1 as the LOCKED character identity.
{全身人物描述 + 场景描述同上}

At the top center, a wide cream-colored clay ribbon plaque; on it the title '{标题}' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, visible clay thickness, subtle fingerprints, casting soft real shadows onto the plaque. Handmade clay lettering, NOT flat printed text.

Absolutely NO text anywhere in the image except that one title. No watermark, no logo, no numbers.
```

> ⚠️ 走 A 路时标题一旦写错就得重出整张图；**要反复改字的页，一律走 B 路**。

---

## 4.1 文字这一层怎么贴（`pages.json` 的 elements）

背景板出完之后，文字全部由 `scripts/clay_text.py` 捏件 + `scripts/compose_page.py` 贴：

```json
{
  "bg": "bg/page07_clean.png",
  "out": "out/page07.png",
  "elements": [
    { "type": "text",  "text": "我踩的坑", "cap": 54, "x": 120, "y": 40, "color": "cream" },
    { "type": "card",  "head": "只抄了描述文字",
      "body": "人物每页都变样，一个啾啾变成两个丸子头，脸也不一样",
      "width": 524, "x": 40, "y": 96, "accent": "orange" },
    { "type": "card",  "head": "想让图里直接写字",
      "body": "让模型在画面里画中文，结果全是错字乱码，还塞不下内容",
      "width": 524, "x": 40, "y": 210 },
    { "type": "badge", "text": "3 小时实操课", "cap": 32, "x": 70, "y": 470, "color": "orange" }
  ]
}
```

- `type:"text"` → 黏土字（大标题 / 章节字 / 强调短语），**字数不限**
- `type:"card"` → 黏土卡片（正文首选），`head` 一行标题 + `body` 自动换行，一条 body 建议 **≤ 26 字**
- `type:"badge"` → 黏土胶囊标签（徽章 / 页脚 / 分类）
- 一页放 **3–5 个 card** 比较舒服；卡片横向留白要避开人物那一侧

---

## 5. 总结 / 结尾页（Summary）· 1024×576

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen closing slide. Theme: {总结主题}. The SAME little kid character from the reference image — identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length chibi proportion — standing COMPLETE FULL BODY from the top of her hair down to her shoes, NOT cropped by any frame edge, wearing {换装}, giving a small encouraging gesture beside a small clay robot that gives a thumbs up, next to a blue clay desk with a laptop showing a completed dashboard, a trophy, a checkmark and stars. Deep blue gradient background with floating clay stars and soft bokeh. On the left, a large cream-colored clay plaque; on it the title '{标题}' is sculpted from thick 3D raised polymer-clay letters with visible thickness, rounded edges and fingerprints, casting soft real shadows. Handmade clay lettering, not flat printed text. Tactile soft clay with fingerprints and sculpted texture, rounded friendly shapes, soft directional lighting, rich dimensional shadows. Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

---

## 6. 改图（Image-to-Image）

> 用户说"把这张的 X 换成 Y"时使用：把原图作为 `image1` 传入，prompt 只描述**要改的部分**，并保留其余。

```
Keep everything unchanged, including the clay lettering and its sculpted 3D texture. Only change {被改元素} to {目标元素}. Preserve the same polymer-clay texture, composition, lighting, background and all existing text. No watermark.
```

参数：`image1: <原图路径>`，可选 `input_fidelity`（调高更贴近原图）。

**改字的写法**（用户说"标题改成 XX"）：
```
Keep the entire scene unchanged. Only replace the clay lettering on the cream plaque with '{新文字}', sculpted from the same thick 3D raised polymer-clay letters, same color, same thickness, same soft shadows, casting real shadow on the plaque. Handmade clay lettering, not flat printed text. Make every Chinese character clearly readable and correctly formed.
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
