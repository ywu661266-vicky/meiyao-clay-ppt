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

- **奶油铭牌位置**：封面放**顶部居中**；内页统一放**左侧**。铭牌上**直接捏出黏土立体字**——不是留一块空板等脚本叠字。
- **人物位置**：偏中/偏右，面朝左或朝向桌面。
- **安全区**：四周各留约 5% 边距；文字只落在铭牌区内。
- **水印规避**：内置出图**右下角有 `AI生成 WORKBUDDY` 水印**，任何文字/关键元素都不要放右下角。
- **留白**：单页道具 ≤ 6 件，宁少勿多；主体占画面 40%–60%。

## 4. 文字规范

### 4.1 第一原则：文字是画面的一部分

黏土风成立的前提是**同一种物理世界**。文字只要变回"扁平印刷体"，整套图的质感立刻垮掉。
所以：**视觉锚点文字（标题 / 页眉 / 卡片标签 / 编号）一律烘进图，且必须是黏土立体字。**

| 文字类型 | 做法 | 说明 |
|---|---|---|
| 封面主标题 | ✅ 烘进图，黏土立体字 | 字号大、字数少，是整套图的记忆锚点 |
| 内页标题 | ✅ 烘进图，黏土立体字 | ≤ 8 字 |
| 目录卡片标签 | ✅ 烘进图，黏土立体字 | ≤ 5 字，字越少越不易出错 |
| 成段正文 | ⚠️ 可走脚本叠加 | 落在奶油铭牌上，见 4.2 |
| 讲师备注 | 脚本写入 notes | 不进画面 |

### 4.2 黏土立体字的样子（出图时必须描述到位）

- **形体**：厚实、圆润、有块面感的字块，边缘倒圆，笔画之间有黏土挤压的过渡
- **厚度与投影**：字有真实厚度，并在铭牌上投下柔和阴影（这一条最容易被模型忽略，必须写出来）
- **表面**：有指纹、捏塑痕迹、微小起伏——和其他黏土件同一材质
- **颜色**：奶油铭牌上配**深可可棕**或**深藏蓝**；深色底上用**奶油白**
- **必须排除**：扁平印刷字、数码字体叠加、发光描边字、金属/玻璃质感字

标准描述句：
```
sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, visible clay thickness,
subtle fingerprints on every letter, casting soft real shadows onto the plaque. Handmade clay lettering,
NOT flat printed text, NOT a digital font overlay.
```

### 4.3 万不得已走脚本叠字时（`text_mode: "overlay"`）

只有成段正文才用。此时：
- 字体：`Microsoft YaHei`（微软雅黑），正文 16–18pt，不加粗
- 颜色：铭牌是浅色 → 用深蓝黑 `#1E3A5F`；压在深色底上 → 用白 `#FFFFFF`
- 行距 1.2–1.4，每行 ≤ 18 个汉字，每条要点 ≤ 22 字
- **绝不用它叠标题**——标题叠上去就没有厚度和阴影，一眼假

## 5. 一致性自检（每次批量前过一遍）

- [ ] 所有页面同一角色：发型 / 发饰 / 眼镜 / 服装描述逐字相同
- [ ] 所有页面同一配色：背景渐变 + 桌面色一致
- [ ] 所有页面同一铭牌位置（内页都靠左）
- [ ] **标题/标签是黏土立体字**（有厚度、有投影），不是扁平印刷字
- [ ] **字块材质与其他黏土件一致**（有指纹/捏塑痕迹，不是光滑塑料）
- [ ] **中文字形正确无乱码**，逐字核对一遍
- [ ] 没有一页出现多余人物 / 多余文字
- [ ] 标题文字与课件内容一致，无错别字
