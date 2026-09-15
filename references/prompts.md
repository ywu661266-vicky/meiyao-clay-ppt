# 提示词模板（已验证）

以下 prompt 均在 WorkBuddy 内置 ImageGen 上**实测通过**。核心写法：**场景与材质用英文（模型理解更稳），要出现在图上的文字用中文原样写进 prompt 并用引号括起来。**

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

---

## 2. 封面（Cover）· 1024×576

> 用途：整页效果确认图。**主标题烘进图**。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen presentation cover. A cute Q-version clay girl character with short black hair, a cute headband, ONE small bun tied on top of her head, round glasses on her face, wearing a knee-length A-line dress. She sits at a blue clay desk with a laptop showing a colorful spreadsheet of cells. A small friendly clay robot assistant stands next to her. On the desk: clay books, a potted plant, a coffee mug, clay star decorations. Deep blue gradient background with scattered clay stars and floating clay bar charts and pie charts. A large cream-colored clay plaque at the top center with clear readable Chinese title text 'AI + Excel 数据处理实战'. Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. High-end educational presentation cover. Make the Chinese text on the cream plaque clearly readable.
```

**要点：**
- 中文标题用**单引号原样包住**，句末再加一句 `Make the Chinese text clearly readable.`
- 标题放在**顶部/左侧奶油铭牌**上，留出下方人物区
- 底图配色词（`Deep blue gradient`）随配色方案替换

---

## 3. 目录页（Table of Contents）· 1024×576

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen slide background for a table of contents page. A blue clay workbench with N numbered clay cards/folders arranged in two rows, each carrying a small clay icon representing one topic (document, gear, chart, magnifier, camera...). A friendly small clay robot assistant sits on the desk. Clay books, a potted plant and a coffee cup decorate the scene. Deep blue gradient background, soft directional lighting. A large cream-colored clay plaque on the LEFT side reserved for the title text. Tactile soft clay with fingerprints and sculpted texture, rounded friendly shapes, rich dimensional shadows. No written words, no letters, no numbers, no watermark, no page number.
```

> 目录页文字由脚本叠加为**可编辑文本**，所以这里写 `No written words`，只留出铭牌空位。

---

## 4. 内容页（Content Page）· 1024×576

> 把 `{主题}` 换成该页要讲的事，其余骨架保持不变，**人物描述段落必须原样复制**以保持一致。

```
A premium handcrafted polymer-clay diorama, 16:9 widescreen slide background. Theme: {主题}. A blue clay desk with a laptop, relevant clay props ({道具1}, {道具2}, {道具3}), and a small clay robot assistant. Deep blue gradient background. A large cream-colored clay plaque on the LEFT side reserved for text. Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich dimensional shadows. No written words, no letters, no numbers, no watermark, no page number.
```

**每页只做一件道具的增减，场景骨架和配色不变，能显著提升整套一致性。**

示例（Excel 六场景）：
| 页 | 主题 | 道具 |
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
A premium handcrafted polymer-clay diorama, 16:9 widescreen slide background for a closing slide. Theme: {总结主题}. A blue clay desk with a laptop showing a completed dashboard, a trophy, a checkmark, stars, a potted plant, books, and a small clay robot giving a thumbs up. A large cream-colored clay plaque on the LEFT side reserved for conclusion text. Deep blue gradient background with floating clay stars and soft bokeh. Tactile soft clay with fingerprints and sculpted texture, rounded friendly shapes, soft directional lighting, rich dimensional shadows. No written words, no letters, no numbers, no watermark, no page number.
```

---

## 6. 改图（Image-to-Image）

> 用户说"把这张的 X 换成 Y"时使用：把原图作为 `image1` 传入，prompt 只描述**要改的部分**，并保留其余。

```
Keep everything unchanged. Only change {被改元素} to {目标元素}. Preserve the same polymer-clay texture, composition, lighting and background. No text, no watermark.
```

参数：`image1: <原图路径>`，可选 `input_fidelity`（调高更贴近原图）。

---

## 通用负面约束（所有模板建议都带）

```
No watermark, no page number, no letters, no numbers.
```
（需要中文标题的封面例外：改为 `No watermark, no page number.`，并加 `Make the Chinese text clearly readable.`）
