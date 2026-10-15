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

### 2.1 不局限主色：莫兰迪 / 马卡龙各 7 套色 + 彩虹系（2026-10-12 扩库，当日再修正）

> 用户原话："**主色完了还有其他配色，比如莫兰迪呀、彩虹的各个颜色、马卡龙配色啊之类的，不局限。**"
> "**莫兰迪 / 马卡龙这两个不各有七个套色，所以不止一个颜色。**"
> 依据：八六《Vibe Coding》45 页里的 5 个学员案例（B29 暖橙 / B30 青蓝 / B31 薄荷绿+粉 / B32 奶杏 / B33 童趣多彩），
> **同一套黏土画风、5 种完全不同配色**——证明这套风格**不锁主色**。见 `references/skeleton-library-81.md` 末节。

除上面 4 套基础色，**允许任意以下色系**（选 1 套，全套内部统一即可）：

#### 莫兰迪 Morandi —— 低饱和灰调，再分 7 个套色（选 1 个套色用全套）

| 莫兰迪套色 | 背景渐变（prompt 词） | 主道具/桌面 | 适合主题 |
|------|----------------------|-------------|----------|
| **① 灰粉 Dusty Rose** | `muted dusty rose-grey gradient` | `greyed rose clay desk` | 温柔、知性、女性向 |
| **② 灰蓝 Slate Blue** | `muted slate-blue grey gradient` | `dusty blue-grey clay desk` | 冷静、专业、科技 |
| **③ 鼠尾草绿 Sage** | `muted sage green-grey gradient` | `sage clay desk` | 自然、疗愈、成长 |
| **④ 灰紫 Muted Mauve** | `muted mauve-grey gradient` | `dusty violet-grey clay desk` | 高级、浪漫、克制 |
| **⑤ 燕麦 Greige** | `warm greige gradient` | `oat-beige clay desk` | 软糯、生活、温和 |
| **⑥ 灰棕 Taupe** | `muted taupe gradient` | `clay-brown clay desk` | 沉稳、大地、职场 |
| **⑦ 灰橘 Terracotta** | `muted terracotta-grey gradient` | `dusty terra-clay desk` | 暖意、行动、复古 |

#### 马卡龙 Macaron —— 明亮粉彩，再分 7 个套色（选 1 个套色用全套）

| 马卡龙套色 | 背景渐变（prompt 词） | 主道具/桌面 | 适合主题 |
|------|----------------------|-------------|----------|
| **① 樱粉 Sakura Pink** | `soft sakura-pink gradient` | `pastel pink clay desk` | 甜美、女性、亲子 |
| **② 天空蓝 Sky Blue** | `soft sky-blue gradient` | `pastel blue clay desk` | 清爽、校园、童真 |
| **③ 薄荷绿 Mint** | `soft mint-green gradient` | `mint clay desk` | 治愈、健康、清新 |
| **④ 柠檬黄 Lemon** | `soft lemon-yellow gradient` | `pastel yellow clay desk` | 明亮、活力、创意 |
| **⑤ 香芋紫 Taro** | `soft taro-purple gradient` | `pastel violet clay desk` | 梦幻、温柔、少女 |
| **⑥ 蜜橘橙 Honey Orange** | `soft honey-orange gradient` | `pastel orange clay desk` | 温暖、活泼、亲和 |
| **⑦ 莓果红 Berry** | `soft berry-red gradient` | `pastel red clay desk` | 热情、节日、吸睛 |

> 莫兰迪 7 套 + 马卡龙 7 套 = **14 个现成套色**，任选其一即全套统一；也可从「基础 4 色」或「彩虹/奶杏/薄荷粉/青蓝」里挑。

#### 其他可选色系（基础 4 色之外）

| 色系 | 背景渐变（prompt 词） | 主道具/桌面 | 适合主题 |
|------|----------------------|-------------|----------|
| **彩虹 / 多彩 Rainbow** | `multi-color playful gradient` | 每张卡/道具**各一色**（红橙黄绿蓝紫轮着来） | 活泼、儿童、创意（一套多色不脏） |
| **奶杏 / 奶油单色 Cream** | `creamy apricot gradient` | `cream-beige clay desk` | 软糯、温和、生活向 |
| **薄荷绿+粉 Mint+Pink** | `mint-green with pink accents` | `mint clay desk, pink props` | 治愈、健康、女性向 |
| **青蓝 Cyan-blue** | `clean cyan-blue gradient` | `cyan clay desk` | 清爽、效率、校园/办公 |

---

#### 【铭牌配色映射表】（换色系时铭牌必须同步换色，❌ 不许默认用 cream）

> **问题背景**：所有 prompt 模板里铭牌默认写 `cream-colored`，换色系时如果不显式改铭牌颜色，模型会把整张图的底部/铭牌区出成大片白色（实测用户skill P07-P10 底带白占比 46-77%，严重超标）。八六原版同色系下底带白仅 0.1-1.5%。
>
> **原则**：铭牌颜色必须与主色方案协调——要么是同色系深浅变化，要么是互补/对比色（需保证文字可读）。

| 主色方案 | 铭牌颜色（prompt 词） | 字块颜色 | 说明 |
|---|---|---|---|
| **深蓝 Deep Blue** | `dark navy blue clay plaque` | `cream-white clay letters` | 深蓝铭牌+奶油字，高对比 |
| **紫色 Purple** | `deep violet clay plaque` | `cream-white clay letters` | 紫铭牌+奶油字 |
| **橙色 Orange** | `warm terracotta clay plaque` | `cream-white clay letters` | 橙铭牌+奶油字 |
| **绿色 Green** | `deep forest green clay plaque` | `cream-white clay letters` | 绿铭牌+奶油字 |
| **莫兰迪 ①-⑦** | `muted [套色] clay plaque` | `cream-white clay letters` | 例：灰粉套→`muted dusty rose clay plaque` |
| **马卡龙 ①-⑦** | `pastel [套色] clay plaque` | `deep brown clay letters` | 马卡龙太浅，铭牌用 pastel，字用深棕保对比 |
| **彩虹 Rainbow** | `multi-colored segmented clay plaque (red/orange/yellow/green/blue/purple segments)` | 每段对应深/奶油色 | 彩虹铭牌分段染色 |
| **奶杏 Cream** | `warm apricot clay plaque` | `deep chocolate-brown clay letters` | 杏色铭牌+深棕字 |
| **薄荷绿+粉** | `mint-green clay plaque with pink accent stripes` | `cream-white clay letters` | 薄荷铭牌+粉条纹点缀 |
| **青蓝 Cyan** | `cyan-blue clay plaque` | `cream-white clay letters` | 青蓝铭牌+奶油字 |

**铭牌 prompt 写法示例**（替换 `{plaque_color}` 为上方表格对应值）：
```
At the top center, a wide {plaque_color} clay ribbon plaque; on it, the title '{标题}' is sculpted from thick 3D polymer-clay letters: raised, chunky, rounded edges, {letter_color}, visible thickness and fingerprints on every letter, casting soft real shadows onto the plaque.
```

**底框/通栏带写法**（换色系时同步）：
- 四色通栏：`a bottom full-width bar with four clay segments in [主色深]/[主色中]/[主色浅]/[对比色]`
- 单色通栏：`a bottom full-width bar in solid [主色] clay with [字色] raised letters`
- 禁止写 `white bar` / `cream bar` / `white frame`——除非选的是「奶杏 Cream」套色

**配色通用规则（任何色系都适用）：**
1. **一套之内只用一个色系 / 一个套色**（一致性 > 多样）；跨套课件可整体换色。
2. **背景 + 铭牌 + 底框三线联动变色**——换色系时三处一起换，别只换背景。铭牌颜色必须随主色方案走（见下方铭牌配色映射表）。
3. **甜系（马卡龙/奶杏/薄荷粉）要把背景压深一点**，否则浅底浅字对比不够、发飘；用 `deep-toned` 而不是 `light`。
4. **彩虹系不是"每样东西随便上色"**，是"每个并列项/卡片各给一个饱和但和谐的主色"，仍要留 60% 深背景。
5. 色系写进 prompt 时，**同时替换"道具/桌面/背景/铭牌/底框"五处**，别只换背景——否则画面会半边新色半边旧色。
6. **⚠️ 铭牌是重灾区**：模型默认把铭牌出成纯白/冷奶油，必须显式写死配色，否则底框白色率会飙到 50%+（实测数据：用户skill P07-P10 底带白占比 46-77%，严重超标）。见【铭牌配色映射表】。
7. **⚠️ 细节框也跟着变色，见 §2.2（这条最容易做错）。**

**⚠️ 换色后 `tone_match.py` 的坑：**
- `--hue-ramp`（253/277/296 三紫锚点）是**紫专用**，非紫配色**不要用它**，否则会把整幅往紫里拽。
- 非紫配色收尾改用 `--hue-lock`（只微调一点）或直接**跳过色调校正**，靠出图阶段把色写死（见【三·三十六】"禁止对成页做全册统一调色"）。
- 判断"该不该校正"：先 `tone_match.py <目录> --analyze` 看饱和/亮度是否已达标（基线见【三·八】），达标就不动。

### 2.2 细节配色铁律：底框 / 条带 / 徽章 / 名片随方案变色，**不许只给白/奶油**（2026-10-12 实测修正）

> **实测证据（底带最下 12% 像素占比，程序化量化）：**
> | 来源 | 白/冷奶油 | 有彩色 |
> |---|---|---|
> | 八六 36 页 | **0.1%** | 24.5% |
> | 八六 45 页 | **1.5%** | 71.7% |
> | 我做的专家技能连接器 10 页 | **24.7%** | 11.5% |
>
> 八六两套的底框/条带**几乎不用白**，全是方案色（彩色占比 24%~72%）；而我那版底框 **24.7% 是白**——
> **正好踩了「高光铁律：纯白面积 ≤ 1%」（三·十一）**，差了 24 倍。用户原话："你加底下的框就只会加白色。"
> 学好八六：**配色要延伸到细节，底框/条带/徽章/名片都要随主色方案走，不是只有主体变色、细节全白。**

**八六式条的两条规范（已验证，照抄）：**
- **底部通栏带**：左 3.8% → 右 75.5%（或 97% 通栏），条高 5.4%，缝 1.5%；**四条四色（米/紫/绿/橙）**，文字深棕 (44,28,22)。满版页结论区用。
- **左列清单条**：左 4.6% → 右 33.6%，条高 6.1%，缝 4.5%；**整列同色（紫罗兰 rgb(126,102,180) 或 橄榄绿）**，文字奶油色 (250,244,232)。清单/要点页用。
（几何与脚本做法见 `references/style-library.md`【三·九 浮条法】第 270–337 行。）

**执行规则（写 prompt / 跑脚本时逐条遵守）：**
1. 底框、通栏带、左列清单条、徽章、小名片、标签卡 —— **颜色一律取自本套主色方案**，不要写 `white box` / `white frame`。
2. 换色系时**五处一起换**：背景 + 道具 + 底框条带 + 徽章 + 名片，避免"半边新色半边白"。
3. 白色只作**最高光小点 / 描边**，纯白面积 ≤ 1%（见三·十一）；奶油铭牌是偏黄暖奶油 rgb(218,192,153)，不是冷白。
4. 提示词里把底框颜色写死，例：
   - 底部通栏带：`a bottom full-width bar with four segments in cream / violet / green / orange, each a clay plaque with deep-brown raised letters`
   - 左列清单条：`a left vertical list bar in solid violet rgb(126,102,180) with cream letters`
   - 莫兰迪/马卡龙套色时，把上面「米/紫/绿/橙」换成该套色的主色（如鼠尾草绿套色→四条用 灰粉/灰蓝/鼠尾草/灰棕）。

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
