---
name: meiyao-clay-ppt
description: 生成"黏土风（polymer-clay diorama）"课件与演示文稿。当用户要做黏土风 PPT、黏土风课件、Q 版讲师形象演示、把课程内容/大纲做成黏土质感幻灯片，或提到"黏土风""clay style""黏土风配图""粘土风 PPT""捏塑感课件"时使用。以内置 ImageGen 出图 + python-pptx 合成 16:9 可编辑 PPTX，严格执行"先确认角色锚点 → 再确认封面 → 最后批量内页"三步确认法，避免浪费出图额度。
agent_created: true
---

# Meiyao Clay PPT（原生黏土风课件生成器）

## Overview

把任意主题或课件内容做成一整套**手工黏土定格动画质感**的 16:9 演示文稿：Q 版黏土讲师 + 微缩黏土场景 + 奶油色黏土铭牌 + 可读中文标题，最后合成为**可编辑**的 `.pptx`。

本 skill 面向 WorkBuddy 原生环境：**全程使用内置 ImageGen 出图、python-pptx 合成**，不依赖 Codex / Image2 / 任何外部 API，也不注入额外的审美 hook。

## 何时使用

- "做一套黏土风 PPT / 黏土风课件"
- "把这个主题/大纲做成黏土风"
- "要 Q 版讲师形象的幻灯片"
- "clay style ppt" / "黏土风配图" / "粘土风封面"
- 为课程、活动、汇报做黏土质感的封面或成套配图

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
人物确认后，用【封面模板】生成 **1 张 1024×576** 封面，把主标题直接烘进图（中文可读，技巧见 `references/imagegen-params.md`）。
交给用户确认——**这一张代表整页效果：人物 + 文字 + 场景**。OK 才批量。

### Phase 3 · 批量内页
按页型生成，全部 `size: "1024x576"`：
- 目录页 × 1
- 内容页 × N（每个知识点/场景各 1 张）
- 总结页 × 1

每页 prompt 中**重复同一段人物描述与风格描述**以保持一致；需要角色强一致时，把 Phase 1 的角色锚点图作为 `image1` 传入做 image-to-image。
每页放什么文字、怎么控制页数，见 `references/workflow.md`。

### Phase 4 · 合成 PPTX
```bash
python scripts/build_pptx.py --config <slides.json> --out <输出.pptx>
```
脚本把背景图铺满 16:9 页面，叠加**可编辑**中文标题 / 要点与讲师备注，文字默认落在左侧奶油铭牌safe区，并**主动避开右下角水印**。

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
