# 提示词模板（已验证）

> ## ⚠️ 第一性原理：文字必须是**画面的一部分**
>
> 黏土风能成立的唯一原因，是**画面上每一个元素都在同一种物理世界里**——包括文字。
> **标题不是"贴"上去的，是"捏"出来的**：厚实的立体黏土字块，坐在黏土铭牌上，有厚度、有圆边、有指纹、有投影。
>
> **反例（一眼假，必须避免）：** 出图时留一块空铭牌，再用 PPT 脚本叠一行扁平黑体字。
> 扁平字没有厚度和阴影，和画面里其他黏土件不在一个光照/材质体系里，观感会瞬间掉档——
> 这正是"别人照着 skill 做，出不来同款"的头号原因。
>
> **规则：**
> 1. 凡是**标题、页眉、卡片标签、编号**这类视觉锚点文字 → **一律烘进图**，且明确要求是黏土立体字。
> 2. 只有**成段正文、讲师备注**这种不适合捏字的，才走脚本叠加（`text_mode: "overlay"`），且要落在黏土铭牌上、用圆润无衬线字体。
> 3. 出图 prompt 里**不要再写 `No written words`**（那是旧版写法，已废弃）。
>
> 核心写法：**场景与材质用英文（模型理解更稳），要出现在图上的中文原样写进 prompt 并用单引号括起来。**

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

> 用途：定下 Q 版讲师的唯一形象，后续所有页面复用同一段人物描述。

```
A close-up portrait of a cute Q-version polymer-clay girl character. Short black hair with a cute headband, one small bun (small top knot) tied on top of her head, round glasses on her face, warm friendly smile, large expressive eyes. She wears a pretty knee-length A-line dress in a soft color. Oversized head, compact chibi body typical of clay style. Visible handmade polymer-clay texture with subtle fingerprints and sculpted clay marks, soft studio lighting, rich dimensional shadows. Unmistakably handmade clay, not photorealistic, not anime line art, not glossy plastic toy. Light neutral gray background for later compositing. No text, no watermark, no letters, no numbers.
```

**可替换的人物特征位（按用户描述改）：**
| 位置 | 示例 |
|------|------|
| 发型 | `Short black hair` / `long straight black hair parted in the middle` / `wavy brown hair` |
| 发饰 | `with a cute headband` / `with a pink bow` / `with one small bun on top` |
| 眼镜 | `round glasses on her face` / 去掉即无眼镜 |
| 服装 | `a pretty knee-length A-line dress` / `white blazer over a cream blouse` / `purple overalls with a white shirt` |

> 角色锚点图**不带字**是唯一例外——它只是形象基准，不是幻灯片页面。

---

## 2. 封面（Cover）· 1024×576

> 用途：整页效果确认图。**主标题以黏土立体字烘进图。**

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation cover. A cute Q-version clay girl character with short black hair, a cute headband, ONE small bun tied on top of her head, round glasses on her face, wearing a knee-length A-line dress. She sits at a blue clay desk with a laptop showing a colorful spreadsheet of cells. A small friendly clay robot assistant stands next to her. On the desk: clay books, a potted plant, a coffee mug, clay star decorations. Deep blue gradient background with scattered clay stars and floating clay bar charts and pie charts. At the top center, a wide cream-colored clay ribbon plaque; on it, the title 'AI + Excel 数据处理实战' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, deep chocolate-brown clay, visible thickness and fingerprints on every letter, casting soft real shadows onto the plaque. Handmade clay lettering, not flat printed text. Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. High-end educational presentation cover. Make every Chinese character clearly readable and correctly formed.
```

**要点：**
- 中文标题用**单引号原样包住**，句末追加 `Make every Chinese character clearly readable and correctly formed.`
- 标题放在**顶部居中奶油铭牌**上，下方留人物与桌面
- 配色词（`Deep blue gradient`）随方案替换；字块颜色随铭牌底色替换
- **务必保留** `sculpted from thick 3D polymer-clay letters` / `not flat printed text` 这两句，这是出效果的关键

---

## 3. 目录页（Table of Contents）· 1024×576

> **标题与卡片标签都烘进图**（黏土字），不再留空给脚本。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen table of contents slide. Six rectangular clay cards arranged in a 3x2 grid on a blue clay workbench, each card carrying a small clay icon (a document, a spray bottle, a calculator, a bar chart, stacked cards, a camera). A friendly small clay robot assistant sits at the corner. Clay books, a potted plant and a coffee cup decorate the scene. Deep blue gradient background, soft directional lighting, rich dimensional shadows. At the top center, a cream-colored clay ribbon plaque; on it the title '课程目录' is sculpted from thick 3D raised polymer-clay letters with visible thickness and fingerprints, casting soft shadows. Each card carries a short raised clay-letter label: '数据读取', '数据清洗', '数据汇总', '数据可视化', '批量分类', '照片变表格' — all sculpted as chunky rounded 3D clay letters, deep chocolate-brown, not flat printed text. Tactile soft clay, rounded friendly shapes. Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

> 卡片的**编号**（01–06）也可以要，但中文标签优先。标签控制在 **4–5 个字以内**，字越少越不容易写错。

---

## 4. 内容页（Content Page）· 1024×576

> 把 `{主题}` 换成该页要讲的事，`{标题}` 换成该页标题（**≤ 8 字**）。
> 人物描述段落必须原样复制以保持一致。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen slide. Theme: {主题}. A cute Q-version clay girl character with short black hair, a cute headband, ONE small bun tied on top of her head, round glasses on her face, wearing a knee-length A-line dress, standing beside a blue clay desk with a laptop and relevant clay props ({道具1}, {道具2}, {道具3}). A small clay robot assistant helps. Deep blue gradient background with a few floating clay stars. On the left side, a large cream-colored clay plaque; on it the title '{标题}' is sculpted from thick 3D raised polymer-clay letters with visible thickness, rounded edges and fingerprints, casting soft real shadows onto the plaque. Handmade clay lettering, not flat printed text. Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

**每页只做道具的增减，场景骨架、配色、人物描述逐字不变，能显著提升整套一致性。**

示例（Excel 六场景）：
| 页 | 标题（烘进图） | 道具 |
|----|------|------|
| 1 | 数据读取与识别 | 扫描仪、放大镜、文件袋、手机 |
| 2 | 数据清洗 | 喷壶、海绵、肥皂泡、小垃圾桶 |
| 3 | 数据汇总 | 算盘、计算器、成堆硬币、柱状图 |
| 4 | 数据可视化 | 调色盘、画笔、饼图/环形图 |
| 5 | 批量分类处理 | 名片堆、印章、多色文件夹、分拣箱 |
| 6 | 照片截图变表格 | 相机、纸张表单、扫描仪、干净表格屏 |

---

## 5. 总结 / 结尾页（Summary）· 1024×576

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen closing slide. Theme: {总结主题}. A cute Q-version clay girl character with short black hair, a cute headband, ONE small bun tied on top of her head, round glasses on her face, wearing a knee-length A-line dress, standing with a small clay robot giving a thumbs up, beside a blue clay desk with a laptop showing a completed dashboard, a trophy, a checkmark and stars. Deep blue gradient background with floating clay stars and soft bokeh. On the left, a large cream-colored clay plaque; on it the title '{标题}' is sculpted from thick 3D raised polymer-clay letters with visible thickness, rounded edges and fingerprints, casting soft real shadows. Handmade clay lettering, not flat printed text. Tactile soft clay with fingerprints and sculpted texture, rounded friendly shapes, soft directional lighting, rich dimensional shadows. Make every Chinese character clearly readable and correctly formed, no garbled characters.
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
