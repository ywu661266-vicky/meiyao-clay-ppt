# 视觉规范（Style System）

## 1. 风格定义

**Polymer-clay diorama（聚合物黏土微缩定格）**：所有元素都像手工捏出来并摆在微缩摄影棚里打光拍成。
认风格的关键词必须同时出现：`handcrafted polymer-clay`、`tactile soft clay`、`subtle fingerprints`、`sculpted texture`、`rounded friendly shapes`、`miniature studio photography`、`soft directional lighting`、`rich dimensional shadows`。

**反面清单（要明确排除）：**
`not photorealistic` / `not anime line art` / `not glossy plastic toy` / 不要光滑塑料、不要描线动漫、不要 3D 渲染的塑料感。

## 2. 配色方案（Accent 可切换）

背景统一走**深色渐变 + 奶油铭牌**，强调色只换"桌面/道具/点缀"的色相：

| 方案 | 背景 | 桌面/主道具 | 适合主题 |
|------|------|-------------|----------|
| **深蓝（默认）** | deep blue gradient | blue clay desk | 数据 / Excel / 效率工具 / 科技 |
| 紫 | deep purple gradient | purple clay desk | AI / 技能 / 通用培训 |
| 橙 | warm deep-orange gradient | cream-orange desk | 行动 / 商业 / 实战 |
| 绿 | deep teal-green gradient | teal clay desk | 成长 / 自然 / 心理 |

**固定色关系：**
- 黑板/背景：深色渐变（占 60%）
- 奶油铭牌（放标题/文字）：`cream-colored clay plaque`（浅米黄，高频复用，是全套视觉的记忆点）
- 点缀：星星、圆圈、饼图、柱状图等小黏土件（占 10%，别堆满）

## 3. 构图与版式（16:9）

- **奶油铭牌位置**：封面放**顶部居中**；内页统一放**左侧**，给脚本叠字留位置。
- **人物位置**：偏中/偏右，面朝左或朝向桌面。
- **安全区**：四周各留约 5% 边距；文字只落在铭牌区内。
- **水印规避**：内置出图**右下角有 `AI生成 WORKBUDDY` 水印**，任何文字/关键元素都不要放右下角。
- **留白**：单页道具 ≤ 6 件，宁少勿多；主体占画面 40%–60%。

## 4. 文字规范（脚本叠加层）

- 字体：`Microsoft YaHei`（微软雅黑）；标题加粗。
- 封面主标题：32–40pt；内页标题：28pt；正文要点：16–18pt。
- 颜色：铭牌是浅色 → 文字用深蓝黑 `#1E3A5F`；直接压在深色底上时用白 `#FFFFFF`。
- 行距 1.2–1.4，每行 ≤ 18 个汉字；要点每条 ≤ 22 字。
- 需要可编辑 → 走 `scripts/build_pptx.py` 叠加；需要"整页一体感" → 主标题可烘进图（见 `imagegen-params.md`）。

## 5. 一致性自检（每次批量前过一遍）

- [ ] 所有页面同一角色：发型 / 发饰 / 眼镜 / 服装描述逐字相同
- [ ] 所有页面同一配色：背景渐变 + 桌面色一致
- [ ] 所有页面同一铭牌位置（内页都靠左）
- [ ] 没有一页出现多余人物 / 多余文字
- [ ] 标题文字与课件内容一致，无错别字
