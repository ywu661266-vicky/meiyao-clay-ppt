---
name: meiyao-clay-ppt
description: 生成"黏土风（polymer-clay diorama）"课件与演示文稿。当用户要做黏土风 PPT、黏土风课件、Q 版讲师形象演示、把课程内容/大纲做成黏土质感幻灯片，或提到"黏土风""clay style""黏土风配图""粘土风 PPT""捏塑感课件"时使用。核心是"文字也是黏土捏的"——标题/标签一律以黏土立体字烘进画面，绝不用扁平字叠加。以内置 ImageGen 出图 + python-pptx 合成 16:9 PPTX，严格执行"先确认角色锚点 → 再确认封面 → 最后批量内页"三步确认法，避免浪费出图额度。
agent_created: true
---

# Meiyao Clay PPT（原生黏土风课件生成器）

## Overview

把任意主题或课件内容做成一整套**手工黏土定格动画质感**的 16:9 演示文稿：Q 版黏土讲师 + 微缩黏土场景 + 奶油色黏土铭牌上**捏出来的中文立体字**，最后合成为 `.pptx`（保留讲师备注，正文可选可编辑叠加）。

本 skill 面向 WorkBuddy 原生环境：**全程使用内置 ImageGen 出图、python-pptx 合成**，不依赖 Codex / Image2 / 任何外部 API，也不注入额外的审美 hook。

## 何时使用

- "做一套黏土风 PPT / 黏土风课件"
- "把这个主题/大纲做成黏土风"
- "要 Q 版讲师形象的幻灯片"
- "clay style ppt" / "黏土风配图" / "粘土风封面"
- 为课程、活动、汇报做黏土质感的封面或成套配图

## 第一性原理：文字必须是画面的一部分（最重要）

黏土风之所以好看，是因为**画面里所有东西都在同一个物理世界里**——文字也一样。

**标题不是"贴"上去的，是"捏"出来的**：厚实的立体黏土字块，坐在奶油黏土铭牌上，有厚度、有圆边、有指纹、有投影。

> **最容易犯的错：** 出图时留一块空铭牌，再用 PPT 脚本叠一行扁平黑体字。
> 扁平字没有厚度和阴影，和画面里其他黏土件不在一个光照/材质体系里，观感瞬间掉档。
> **这是"照着这个 skill 做却做不出同款"的头号原因。**

因此：

| 文字 | 做法 |
|------|------|
| 标题 / 页眉 / 卡片标签 / 编号 | ✅ **一律烘进图，必须是黏土立体字** |
| 成段正文 | ⚠️ 才走脚本叠加（`text_mode: "overlay"`），落在铭牌上 |
| 讲师备注 | 脚本写入 notes，不进画面 |

出图 prompt 里**不要再写 `No written words`**（旧写法，已废弃）。
标准句式见 `references/prompts.md` 第 0 节，**必须包含**：

```
sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, visible clay thickness,
subtle fingerprints on every letter, casting soft real shadows onto the plaque.
Handmade clay lettering, NOT flat printed text, NOT a digital font overlay.
```

## 三条铁律（必须遵守）

1. **绝不一上来做一大堆。** 出图消耗用户积分。必须按「角色锚点 → 封面 → 内页」逐段推进，每一步只出**最少张数**，用户明确确认 OK 后才进入下一步。
2. **先对齐人物，再谈页面。** 人物的发型、发饰、眼镜、服装先确认；人物不对，整套图都会跑偏，全部作废。
3. **不混入其他流程。** 不套用费希纳审美 hook、不叠加其他 PPT skill 的步骤，严格按本 skill 的唯一流程执行。

## 工作流（Workflow）

### Phase 0 · 收集素材
需要两样东西，缺哪个就问哪个，**一次性问清**，不要反复打断：
1. **内容**：课件大纲 / 要点 / 逐页文字。若用户已有文件（`.md` / `.docx` / `.pptx` / `.html`），先读取并提取，不要凭空编。
2. **人物特征**：想要的 Q 版形象——发色、发型、发饰（发箍/蝴蝶结）、是否戴眼镜、服装（裙子/背带裤/西装）。若用户给了人像照，按照片特征转写。
3. 可选：**配色**。默认「深蓝」，可选 紫 / 橙 / 绿（详见 `references/style-system.md`）。

### Phase 1 · 角色锚点（只出 1 张）
用 `references/prompts.md` 的【角色锚点模板】生成 **1 张 1024×1024** 方图，立刻交给用户确认。
不合格就按用户反馈改特征、**重出 1 张**，仍不批量。

### Phase 2 · 封面确认（只出 1 张）
人物确认后，用【封面模板】生成 **1 张 1024×576** 封面，把主标题以**黏土立体字**烘进图（技法见 `references/prompts.md` + `imagegen-params.md`）。
**自检**：标题有厚度、有投影、和画面其他黏土件同一材质；像"扁平贴字"就重出，别拿给用户看。
交给用户确认——**这一张代表整页效果：人物 + 文字 + 场景**。OK 才批量。

### Phase 3 · 批量内页
按页型生成，全部 `size: "1024x576"`：
- 目录页 × 1
- 内容页 × N（每个知识点/场景各 1 张）
- 总结页 × 1

**每页的标题同样烘进图（黏土立体字）**，不再留空铭牌给脚本叠字。
每页 prompt 中**重复同一段人物描述与风格描述**以保持一致；需要角色强一致时，把 Phase 1 的角色锚点图作为 `image1` 传入做 image-to-image。
文字数量控制：标题 ≤ 8 字，卡片标签 ≤ 5 字。样张与页型细节见 `references/workflow.md`。

### Phase 4 · 合成 PPTX
```bash
python scripts/build_pptx.py --config <slides.json> --out <输出.pptx>
```
脚本把背景图铺满 16:9 页面，写入讲师备注。
**默认 `text_mode: "baked"`——图里已有黏土标题，脚本不再叠任何扁平文字。**
只有成段正文需要可编辑时才用 `text_mode: "overlay"`（叠在奶油铭牌 safe 区，并主动避开右下角水印）。
⚠️ 图里烘过字的页，`slides.json` 里**不要再写 `title`**，否则会叠出两层字。

### Phase 5 · 交付
用 present_files 交付 `.pptx` 与关键页预览图，附一句说明：页数 / 主题 / 配色。

## WorkBuddy 原生出图（关键）

- 工具：内置 **ImageGen**（deferred tool：先 `ToolSearch` 载入 schema，再 `DeferExecuteTool` 调用）。
- 可用参数：`prompt`、`size`、`image1`/`image2`/`image3`、`input_fidelity`、`output_dir`、`quality`、`style`、`background`、`footnote`、`revise`。
- **没有 `aspect_ratio` 参数**——传了会报 `additional properties` 校验错误。比例一律用 `size` 控制：
  - 16:9 幻灯片页 → `size: "1024x576"`
  - 角色方图 → `size: "1024x1024"`
- 生成结果默认落在工作区 `generated-images/` 目录，文件名是 prompt 截断 + 时间戳。

## 资源

- `references/workflow.md` — 三步确认法细节、各页型要点、推荐对话话术
- `references/prompts.md` — 已验证提示词模板（角色锚点 / 封面 / 目录 / 内容页 / 总结页 / 改图）
- `references/style-system.md` — 视觉规范（配色、材质关键词、构图、版式、比例、水印规避）
- `references/imagegen-params.md` — ImageGen 参数与踩坑（含中文渲染技巧）
- `scripts/build_pptx.py` — 背景图 → 可编辑 PPTX 合成脚本
- `assets/examples/` — 已通过确认的成功样例（角色锚点、封面）
