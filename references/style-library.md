# 款式库（Style Library）· 人物 / 封面 / 内页 任意搭配

本 skill 出的每一张图，都是 **「锁定块 + 可变块」** 拼出来的：

- **锁定块（每页都不变）**：人物身份（靠角色锚点参考图 `image1` 锁）、主题配色、铭牌位置、黏土立体字规范。
- **可变块（从库里任选/抽签）**：人物款式、封面场景、内页场景与道具。

> **目标：一致性靠"参考图 + 锁定前缀"，多样性靠"换场景块"。**
> 同一套 ≥13 页的 PPT 至少用 **8 个不同场景块**，相邻页不重复。这样再也不会"每套封面都长一个样"。

---

## 一、人物款式库（Character Presets）

给用户先选"这个 Q 版形象长什么样"。**选定后先出 1 张角色锚点图确认，之后每一页都把它作为 `image1` 传入。**

> ⚠️ **2026-10-11 修订**：人物**不设"唯一默认款"**——用户要求「**百变、不定死**」（脸/画风统一，衣服/姿态/场景可变）。
> **唯一真源 = `references/character-style.md`**，下表 A 款描述已过时，别照抄。
> **画风基准 = 圆框眼镜 + 深色发 + 约 2.5–3 头身 Q 版小孩**（= **用户自己的成品** `assets/examples/cover-excel-example.png`）。
> 下表 B–F 的**多 IP 风格用户明确喜欢**，作为备选款式继续保留。

| 代号 | 款式 | 关键特征 | 画风参考图 | 适合 |
|---|---|---|---|---|
| **A**（画风基准） | ⭐⭐⭐ 画风基准：Q 版小孩 | 深色发顶髻 + 粉色蝴蝶结发带 · 圆框眼镜 · **约 2.5–3 头身** · 蓝裙（衣可换） | **用户成品** `assets/examples/cover-excel-example.png` / `toc-clay-lettering-example.png`；**描述见 `character-style.md`** | 培训 / 汇报 / 晨会 / 通用 |
| **A2** | ⭐⭐ 二类备选：呆板规矩款 | 短发齐刘海 · 头顶小啾啾 · 圆框眼镜 · 白西装 + 米白高领 | `assets/examples/character-anchor-example.png` | 用户点名要"更规矩"时 |
| **B** | Q 版联盟风 | 哑光黏土 · 极圆大头 · 五官极简（点眼 + 弧线笑）· 小身体娃娃 | `assets/style-refs/1027cf08cbafe2dce4b97fbe67d3b82a.jpg`（哈利波特 Q 版） | 轻松 / 活泼 / 大众向 |
| **C** | 古风汉服款 | 双丸子头 + 小花发饰 · 垂耳饰 · 青绿 + 橙汉服 · 大眼黑瞳 + 腮红 | `assets/style-refs/63085bfcf9606efc83a92b11ecc38df6.jpg` | 国风 / 传统文化 |
| **D** | 棕发大眼款 | 棕色长卷发 + 米色蝴蝶结 · 米白背心 + 军绿短裙 + 堆堆靴 · 极简脸大黑眼 | `assets/style-refs/aeb84a6455e7dfbb32eb0bb41eee4057.jpg` | 年轻 / 时尚 / 生活 |
| **E** | 糖果小童款 | 高饱和糖果色 · 圆头小身体 · 三角眼笑脸 | `assets/style-refs/0828eb0e82336d84178114afaee16d2f.jpg` | 亲子 / 儿童 / 低龄 |
| **F** | 粉樱 Q 款 | 粉色调 · 大头小身 · 蝴蝶结 / 兔耳 / 天使翼配饰 | `assets/style-refs/ed3ccaab7a608f2fd844db437f6af697.jpg` | 治愈 / 女性向 |

> 另有 2 张"灵感合集截图"可给用户看风格光谱：`assets/style-refs/c1b18e583c3e655976a14e6c92d57111.jpg`（古风 Q 版小人）、`assets/style-refs/eed73f852a58086d06fbed5af56ed325.jpg`（黏土风 Q 版小人）。

**通用 · 按图复刻画风（已实测可行）**：使用者丢任意一张参考图 → 直接用 `image2` 传入，prompt 写
`Match the EXACT art style of the reference image (image2)`，即可复刻其画风。

> ⚠️ 复刻时**只借它的"画风"**（材质 / 头身比 / 五官画法 / 配色倾向），**不要抄**它的衣服、发型、背景——否则人物会变成参考图里的那个人。
> 标准句式：`Match the EXACT art style of image2 — borrow ONLY its art style (material, head-body ratio, facial style, color mood), NOT its clothes, hairstyle or background.`

**脸更可爱（不换款式，只调脸）**：
```
ONLY make the face cuter: rounder softer face, bigger rounder glossy eyes with large highlights,
fuller soft rosy blush, a tiny nose, a small gentle closed smile (no open mouth, no teeth)
```
—— 头发 / 发饰 / 服装 / 材质一律不动。

---

## 二、封面款式库（Cover Scene Library）

封面 = **人物（锁） + 主标题（黏土立体字，锁） + 场景款式（每套只选 1 个）**。
把下表的"场景块"整段拼进 prompt 即可。

| 代号 | 场景 | 场景块（拼进 prompt） |
|---|---|---|
| **CV1** | 云岛 Sky Island | `she stands on a floating purple clay island among soft fluffy clay clouds, holding a large glowing clay skill card; a small clay hot-air balloon and floating clay puzzle pieces hover in the sky; a small friendly clay robot assistant flies beside her holding a tiny clay star` |
| **CV2** | 工具台 Workbench | `she stands beside a purple clay workbench; on it an open clay toolbox with a wrench, a screwdriver and a gear wheel, plus floating rectangular clay skill cards; a small clay robot assistant holds up one glowing card` |
| **CV3** | 知识书架 Bookshelf | `behind her stands a tall purple clay bookshelf filled with colorful clay books; she pulls one glowing golden clay book; clay books and floating paper pages hover around; a small clay robot stands on a little ladder` |
| **CV4** | 直播间 Live Studio | `she sits at a purple clay streaming desk with a ring light and a camera on a tripod, a small clay microphone and floating like/heart clay icons` |
| **CV5** | 咖啡工位 Desk | `she sits at a cozy purple clay desk with a laptop, a coffee mug with steam, sticky notes and a small potted plant` |
| **CV6** | 阶梯图书馆 Library Stairs | `she climbs a set of purple clay library stairs lined with glowing books and a lantern; floating pages in the air` |

> 主标题放在**顶部居中**的奶油铭牌上，用第 0 节黏土立体字句；字块颜色随铭牌底色（奶油白 → 深可可棕）。

---

## 三、内页款式库（Inner-page Scene Library）

内页 = **人物（锁，`image1`=角色锚点） + 主题配色（锁） + 场景块（任选、任意搭配） + 标题（黏土立体字）**。

| 代号 | 场景 / 母题 | 场景块（拼进 prompt） | 常用道具 |
|---|---|---|---|
| **IN1** | 桌面工位 | `she stands beside a purple clay desk with a laptop; on the desk a chat window made of two clay speech bubbles and a floating link card with a small clay chain-link icon` | 电脑、气泡、链接卡 |
| **IN2** | 终端 / 代码墙 | `she faces a dark purple clay terminal wall with glowing clay command lines and a big curved clay arrow` | 终端窗、克隆箭头 |
| **IN3** | 对话气泡 | `she stands among several large rounded clay speech bubbles floating around her, one showing a small clay checklist` | 气泡、清单 |
| **IN4** | 裂开的两块 | `between two big clay blocks (one a picture block, one a text block) there is a visible gap; she looks at the gap` | 图片块、文字块 |
| **IN5** | 拼图 | `two big clay puzzle pieces lie on a purple clay table, trying to fit but not matching; she holds one piece` | 拼图块 |
| **IN6** | 灯泡灵感 | `a big glowing clay light bulb floats above her head; beside her a close-up thick 3D clay letter block shows raised sculpted letters with fingerprints and real shadows` | 灯泡、黏土字特写 |
| **IN7** | 清单板 | `she points at a purple clay clipboard with a clay pencil; a few small clay checkmarks` | 清单板、笔、对钩 |
| **IN8** | 复制 / 名牌柜 | `she holds a small clay name plaque; beside her a clay copy machine prints an identical second plaque` | 名牌、复印机 |
| **IN9** | 绿植花园 | `she stands in a little purple clay garden with potted plants, vines and a watering can; a small clay mini-version of her stands beside` | 绿植、喷壶、小分身 |
| **IN10** | 流程图步道 | `three big clay stepping stones with arrows form a path in front of her (anchor, cover, batch); small clay signposts; she stands on the first stone` | 步道石、箭头、路牌 |
| **IN11** | 礼物 / 对钩 | `she holds a gift box with a big clay checkmark on top; confetti clay pieces and stars float around` | 礼物盒、对钩、星星 |
| **IN12** | 书架取书 | `she pulls one glowing book from a purple clay bookshelf; floating pages around` | 书架、发光书 |
| **IN13** | 齿轮工具箱 | `she holds a wrench beside a purple clay gear panel and an open toolbox` | 齿轮、扳手、工具箱 |
| **IN14** | 放大镜审查 | `she looks through a big clay magnifying glass at a floating clay document` | 放大镜、文件 |

**搭配规则（避免千篇一律，也避免翻车）：**
1. **相邻页不重复**同一场景块；一套 ≥13 页至少用 **8 个不同**场景块。
2. 场景块**只改"背景 + 道具 + 小物件"**；**人物段与铭牌位置逐字不改**——多样性来自场景，一致性来自人物。
3. 单页道具 ≤ 6 件，宁少勿多；主体占画面 40%–60%。
4. 标题一律**左侧奶油铭牌上的黏土立体字**，与场景块同材质、同光照。

---

## 三·五、内页版式库（Layout Presets）—— 防止"每页都长一样"

> 场景块（IN1–IN14）换的是**道具**；版式（LP1–LP10）换的是**正文区的骨架**。两者都要换，一套图才"像一个系列、又不重样"。
> 对照样本：八六老师的课件 20+ 页，**每页正文骨架都不同**（四宫格 / 横排卡 / 左列＋右大图 / VS 双栏 / 编号流程 / 中心文档加浮标 / 分层堆叠 …）。

| 代号 | 版式名 | 正文区骨架（prompt 里按方位写死） | 适合讲的 |
|---|---|---|---|
| **LP1** | 左列卡 + 右场景 | 左 46%：3 条等宽胶囊（徽章图标 + 彩色关键词 + 深色说明）竖排；右 54%：立体场景 + 人物全身 | 3–4 条并列要点 |
| **LP2** | VS 左右对照 | 左右两块**等大**面板，中间一条闪电／裂缝分隔；面板下各一枚小铭牌；底部通栏结论条 | 前后对比、误区 vs 正解 |
| **LP3** | 中心大匾 + 底格 | 中央一块大匾（金句）＋上方灯泡／光环；**下方一排 4 枚方形瓦片**（图标在上、文字在下）；人物在侧 | 一个金句 + 四要素拆解 |
| **LP4** | 四宫格 | 2×2 四块等大圆角卡，各带徽章图标 + 两行字；人物在右下角 | 四个并列概念／四问 |
| **LP5** | 横排瓦片 | 一排 3–5 块**竖长卡**（图标在上、文字在下）；下方一条通栏小结 | 三到五步／三到五类 |
| **LP6** | 编号流程 | 一条横向编号序列（圆徽章 ①②③ → 粗箭头 → 小面板）；底部通栏；人物在末端 | 步骤、流程 |
| **LP7** | 清单板 | 中央一块大清单板（编号行 + 对钩）；人物在侧持笔 | 清点、改法清单 |
| **LP8** | 中心文档 + 浮标 | 中央一份大文件／窗口道具，四周浮出小气泡标注 | 讲某个文件／目录结构 |
| **LP9** | 分层堆叠 | 3–4 层**错位叠放**的卡片／抽屉，逐层露出 | 渐进、层次、由浅入深 |
| **LP10** | 全宽单场景 | 场景**横贯整个画面**（裂缝／步道／大门），人物在侧；底部一条结论条 | 一个画面说一件事 |

**搭配规则（新增，硬性）：**
1. **相邻页不得复用同一版式**；一套 ≥13 页至少用 **6 个不同版式** + **8 个不同场景块**。
2. 标题形态可保持系列感（顶部缎带 + 黏土浮雕字），**变的是正文区骨架**——别把"换道具"当成"换版式"。
3. 场景块要**挑语义匹配**的：讲踩坑 → IN4 裂开／IN5 拼图；讲转折 → IN6 灯泡；讲流程 → IN10 步道；讲清单 → IN7 清单板；讲沉淀 → IN8 名牌柜／IN12 书架；讲加自己的料 → IN9 绿植；讲审查 → IN14 放大镜。
4. prompt 里**用方位词 + 占比把版式写死**（`TOP:` / `CENTRE OF THE FRAME` / `LEFT COLUMN, about 46%` / `BELOW the plaque: four tiles in one row` / `RIGHT SIDE:`）。**越具体越听话**；只写"信息图"模型会自己滑回默认骨架。

---

## 三·六、满版密度铁律 —— 防止"边上是空的"

> 用户原话："**还是不一样，边上是空的。**"
> 对照八六老师的页：**每一寸画面都被黏土占着**——机器被左右边缘裁切、横贯满幅，底部是贯通全宽的长条，四角有星／叶／心／齿轮。空白只存在于**画面之外**。

**反例特征（一看就是"空"）**：道具**孤立漂浮**、中央一块大匾、四周留一片纯紫底、底部是几块**互相分离**的小方瓦。

### 量化验收口径（交付前必跑）

把成品页切 **6×3 网格**，算每格 RGB 的**标准差**（= 纹理强度）：

| 指标 | 八六参考基线 | 合格线（不许低于） |
|---|---|---|
| 最低格 | 53.0 | **≥ 45** |
| 平均 | 63.6 | **≥ 55** |
| 空旷格（＜40）数量 | 0 | **必须 = 0** |

```python
# 6x3 网格纹理强度自检
from PIL import Image; import numpy as np
a = np.asarray(Image.open(p).convert('RGB')).astype(np.float32); H,W = a.shape[:2]
vals = [a[r*H//3:(r+1)*H//3, c*W//6:(c+1)*W//6].std() for r in range(3) for c in range(6)]
print('最低', round(min(vals),1), '| 平均', round(sum(vals)/len(vals),1), '| 空旷格', sum(v<40 for v in vals))
```

实测：旧版"中心大匾"页 = 最低 16.4 / 平均 41.1 / **空旷格 7** → 用户一眼看出"边上空的"。
改满版后 = 最低 46.1 / 平均 57.9 / **空旷格 0** → 判定合格。

### 把画面撑满的四条 prompt 动作（缺一条就会留空）

1. **写死满版**：`FULL-BLEED COMPOSITION — the frame is PACKED edge to edge. There is NO empty flat background anywhere, no empty purple space in the corners or the side margins, no empty gaps between objects.`
2. **主场景"特写 + 被左右边缘裁切"**（最有效的一条，模型会把场景放大撑满，而不是缩成中心小物）：
   `The main scene is shown as a CLOSE-UP and is CROPPED BY THE LEFT AND RIGHT EDGES of the frame, running continuously off both sides of the picture.`
3. **底部结论条写 full-width**：`each bar spanning the FULL WIDTH of the frame from edge to edge with no gap at either side`（"一排小瓦片"必然留空）。
4. **填角 + 暗角**：标题两侧和四角补星／叶／心／齿轮，并加 `A dark vignette noticeably darkens all four edges and the four corners of the frame.`

---

## 三·七、元素语义匹配铁律 —— 「与文字适配才美」

> 用户原话："**我的画面怎么有点丑啊，与文字适配才美啊，要更贴合文字的配置元素吧。**"

**丑的头号原因不是画技，是道具跟文字没关系。** 实测翻车：第 8 页《转折点来了》稿件写的道具是「**灯泡 + 黏土字特写**」，我却照抄了参考图那页的"锅炉 / 传送带 / 大机器"——元素本身画得挺好，但跟这一页的话**毫无对应**，于是整页读起来像"堆了一堆不相关的黏土"。

**判定动作（每个道具过一遍）**：问「**删掉它，这一页的话会变少吗？**」
- 会变少 → 它承载了信息，留（对应费希纳 6 联想 / 13 双重表象）
- 不会 → 它是装饰，**该换成一个能对应文字的道具**，而不是删掉了事

**对照示例（第 8 页）**：

| 画面上的字 | 应该配的道具 | 不该配的 |
|---|---|---|
| 转折点来了 | 发光**灯泡**（顿悟） | 锅炉、传送带 |
| 文字也要粘土风 | **黏土字特写**（字本身就是黏土捏的） | 平面屏幕、文档图标 |
| 有厚度 | 指向字**笔画侧面**的引线标注 | 一个抽象的"厚度"图标飘在角落 |
| 有圆边 / 有指纹 / 有投影 | 分别指向**圆角 / 字面指纹 / 字下影子** | 各配一个孤立小图标 |

**加分技巧**：把四个特征做成**引线标注（callout）**直接指向主角的对应部位——远看是一块黏土字，近看每条标注都在指它的某个特征。这是"一图两读"，也是让画面"有话说"的关键。

**标注写法（借 Guizang 信息图规范）**：
- 标签 **2–5 个中文字**（6 字是上限），别在画面里塞整句
- 标签**分散到四个方位**，不要全挤在一侧
- 每个标签用一根**短引线**接到它描述的具体部位，不要悬空
- 图内**只放标签**，解释性长句放到版面外或口播里

---

## 三·八、色调与配色铁律 —— 治好"发灰、没精神"

> 用户说"丑"时，除了元素语义，第二个高频原因是**色调发灰**：画面不透、不浓、奶油发白、背景不够深。

**参考基线（八六老师课件页实测，可直接量化比对）**：

| 指标 | 目标值 | 怎么量 |
|---|---|---|
| 饱和度均值 | **≈ 0.60** | HSV 的 S 均值 |
| 画面平均亮度 | **≈ 83** | 0.299R+0.587G+0.114B 的均值 |
| 四角中位亮度 | **≈ 31** | 四角各取 6% 边长的方块，取中位数 |
| 明暗倍率 | **≈ 40x** | 最亮值 ÷ 亮度 2% 分位 |
| 亮部 B−R | **≈ −86** | 最亮 20% 像素的 (B−R) 均值，衡量奶油暖不暖 |
| 高饱和暖色锚点 | **≥ 7%** | H∈[15,50] 且 S>0.45 且 V>0.6 的像素占比 |

**三条最容易踩的坑（全部实测过）**：

1. **「禁脏紫红」用力过猛 → 紫色只剩一层**
   参考的紫横跨 **蓝紫 250 → 紫 295 → 暖紫红 328 三个层次**。
   只写 "clean blue-violet" 会得到清一色 232–243 的单层蓝紫，画面反而单薄。
   → prompt 要写 **三层紫渐变**：`deep royal blue-violet on top (hue ~250), violet-plum in the centre (~290), warmer plum-violet lower down (~325)`；道具的紫也要用**两种紫**（偏蓝的和偏暖的）。

2. **暗角写成"把角落涂黑" → 大片死黑平区**
   参考的暗角里**塞满处于阴影中的道具**。只压暗不填物，空旷格会从 5 涨到 24。
   → 要写：`the corners are NOT empty background — props extend into all four corners, simply lying in shadow`，并明确 `vignette darkens but does NOT blacken`。

3. **奶油色发白 → 整体饱和度上不去**
   参考的奶油是**偏黄的暖奶油 rgb(218,192,153)**（亮部 B−R ≈ −86）；
   偏白的冷奶油 rgb(233,211,192)（B−R ≈ −49）会把整体饱和度拖到 0.4 以下。
   → prompt 里直接写数值：`a WARM CREAMY BEIGE WITH A YELLOW CAST like rgb(218,192,153) — NOT white, NOT cool grey-white`。

**收尾必做：跑一次色调校正**
出图后执行 `scripts/tone_match.py`，把色调对齐上面那张基线表：

```bash
python scripts/tone_match.py <目录或图片>        # 输出 *_tone.png
python scripts/tone_match.py <目录> --analyze    # 只量化不写文件
```

实测（第 8 页）：饱和 0.385→0.545、亮度 88.3→81.3、四角 44.4→37.2、亮部 B−R −57→−87。
**靠 prompt 抠色调改 6 版都到不了，一次脚本校正就到了。**
⚠️ 但「适中」是铁律：参数别一路拉满（饱和度 >1.5x 就开始又艳又脏），宁可欠一点。

---

## 三·九、八六式「可读生产线」复刻清单（2026-09-19 用户三次打回后确立）

> 用户原话："**你看蒸馏真的是蒸馏机器，他的图是生动形象的，是真实的。**"
> 这句是整套方法里最贵的一句话 —— 它区分了「好看的机器」和「能读懂的机器」。

### 病根：通用机械 ≠ 能读懂的机器

实测翻车：紫色机器上挂满仪表、齿轮、旋钮，画得挺精致，但**看不出它在加工什么**，
读起来就是"一堆不相关的黏土"。这类图用户一眼判为"丑"。

### 药方：让画面变成一条**从左到右能读出来的生产线**

参考图（八六《仓颉蒸馏 + Skill Creator》）的可读链条：

```
书架「课程/内容」 → 玻璃烧瓶（瓶身刻「仓颉」、装琥珀液、下有炉火）
   → 弯管 → 传送带上的方块 → 机器开口里的人在组装 → 货架上「SKILL」成品 + 绿勾
```

每一站都能被认出来，观众顺着扫一眼就读懂了"蒸馏 → 组装 → 出货"。

**复刻时必须做的四件事：**

1. **命名每个主要装置**：给机器挂一块小铭牌（参考图是「仓颉蒸馏」「Skill Creator」「SKILL」）。
   prompt 里写死 `a small purple nameplate on the rack reading <2–5 字>`。**铭牌是可读性的关键。**
2. **进料端画"原始形态"，出料端画"成品形态"**：参考图是方块进、SKILL 文件出；
   第 8 页是**扁平的灰蓝字卡进、厚圆的奶油黏土字出**（中间过一道压模滚筒）。
   —— 这条把"转变"画成了实物，比任何箭头都直观。
3. **人物要"在机器里干活"**，不要"站在机器旁边"。参考图的男孩是坐在机器开口里的。
   ⚠️ 但与本 skill 铁律 3（完整全身）冲突 → 折中写法：
   `Its front is a TALL OPEN BAY like a workshop window, and inside that bay the figure stands
   as a COMPLETE FULL-BODY figure, ENTIRE body from the top of her hair down to her shoes
   completely visible inside the opening, NOT cropped by any frame edge.`
   （把"开口"写成"高到装得下整个人"的工作间，两个要求就都满足了。）
4. **四角塞道具**：参考图四角是橙星／红心／绿叶／紫花／齿轮；缺角就是"边上空的"。

### 底部标签条：**必须用脚本渲染，不要交给图片模型**

实测两次交给模型都翻车：
- 第一次：四条塌成 **2×2**（四行变两列）；
- 第二次：「**有指纹**」重复出现两次，四条内容错位。

→ 用 `scripts/clay_band.py` 渲染（真字体，零错字；几何精确；改文案不重出图）。

#### ⚠️ 2026-09-19 二次大修正：条**逐行扫描**后的真几何

前一版把条量成"左起 4.4%、右止 58%、条高 6.8%、缝 1px"——**四个数里错了三个**，
按它做出来的条又短又高、四条右端参差不齐，像一张坏掉的表格。
这次改成**逐行扫描**（按条带四色做色距掩膜，逐行取左端/右端百分位）：

| 项 | 参考实测（1310×739） | 本 skill 取值（1024×576） |
|---|---|---|
| 横向 | **左起 3.8%、右止 75.5%** ← 右侧 24% 是机器下体 + 齿轮/星星 | `x0=0.038w`、`x1=0.755w` |
| **四条右端** | **齐平**（四条右端 x 差 < 1.5%） | 默认齐平；**别逐行给 `x1_ratio`**，参差会像坏表格 |
| 条高 | 40px = **帧高 5.4%** | `bar_h=31`（567 高时 30） |
| 条间缝 | 11px = **帧高 1.5%** | `gap=8`（缝里能透出后面的机器 —— 这是"层叠感"的来源，别填死） |
| 整块位置 | y **70.2% ~ 96.2%**，条下仍留 3.8% 帧高的地面 | `--top ≈ 0.70×帧高`，底部留 4~20px |
| 圆角 | **全圆**（radius = 条高/2） | `radius_ratio=0.5` |
| 四条底色 | 暖砂米 (219,183,140) · 丁香紫 (170,123,180) · 橄榄黄绿 (158,158,48) · 亮橙 (232,140,26) | 同左（`BAR_COLORS`） |
| 文字色 | **深棕近黑 (44,28,22)** ← 不是藏青 | 同左 |
| 字号 | 关键词与说明句**同号同粗**（不是一大一小） | `text_ratio=0.60` + 本条自适应缩号 |
| 徽章 | 圆底（橙/紫/绿/橙红）+ **深棕描边** + 白色图标 | `badge` + `icon` |
| 条下 | 深紫投影 | `shadow` |

**槽位选择（两条都合法，看场景）**：
- **3.8%→75.5%（参考式）**：条右侧留出机器下体/齿轮当"呼吸区"，层叠感最好 —— 但**前提是右下角真有机器或道具**，否则会留一块空紫地。
- **3.8%→97%（通栏式）**：场景右下本来就是空地时用这个，画面更稳、不露空。第 8 页实测用通栏更耐看。

**定位铁律**：条带顶部必须 ≥ 人物鞋底所在行 + 2px（先量人物最低点再定 `--top`）。
⚠️ 别指望"把人物放到 x 62% 之后就不会被盖"—— 条一旦铺到 75.5% 就重叠了；
**位置只能靠量**。（第 8 页实测人物鞋底 y≈434，条顶就定 434。）

```python
# 量内容/人物最低行（用于给 --top 定位）
import numpy as np; from PIL import Image
a = np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
hsv = np.asarray(Image.open(p).convert('HSV')).astype(np.float32)
S, V = hsv[:,:,1]/255, hsv[:,:,2]/255
ground = (S < 0.55) & (V > 0.30) & (V < 0.85)          # "平坦紫地"掩膜
for y in range(a.shape[0]-1, 300, -1):
    if ground[y].mean() < 0.93: print('内容最低行 y =', y); break
```

#### 「八六式条」的两个槽位（别再混用）

| 槽位 | 几何 | 条色 | 文字色 | 用在哪 |
|---|---|---|---|---|
| **底部通栏带** | 左 3.8% → 右 75.5%（或 97% 通栏），条高 **5.4%**，缝 **1.5%** | **四条四色**（米/紫/绿/橙） | 深棕 (44,28,22) | 满版页的结论区（第 8 页、p28） |
| **左列清单条** | 左 4.6% → 右 33.6%，条高 **6.1%**，缝 **4.5%** | **整列同色**（紫罗兰 rgb(126,102,180) 或橄榄绿） | **奶油色** (250,244,232) | 清单/要点页（【三·十六】·第 9 页、p10/p16） |

左列版的完整规格与做法见 **【三·十六 浮条法】**。

#### ⚠️ 颗粒必须在**降采样之后**加（2026-09-19 踩坑）

超采样 ss=3 会把高频噪点**平均掉** —— 条面渲染出来是**光滑塑料面**（实测高频 std 仅 1.23，
参考图是 5.09/行）。修法：把颗粒挪到 `img.resize(...)` **之后**，用 `_grain((H,W), 2.2, seed=99)`
按最终分辨率生成。`--grain 0.30` 时行内 std ≈ 9.5，`0.16` 时 ≈ 5（对齐参考）。

#### 徽章 / 描边（2026-09-19 重写）

- 徽章直径 = **条高 × 1.12**（会微微越出条面上下，和参考一致）；形状 `--badge-shape circle|square`。
- 徽章外圈一道**浅色亮边**（`_lighten(bc,0.60)` 的 ring），再叠下缘厚度 —— 参考图有这道边。
- 浅色字必须**先垫深色柔晕**再压字（`halo = blur(tm,1.15)*2.05 - tm`，α 0.95），
  否则奶油字在紫条上虚浮、读不出立体感。

## 三·十、「紫」的铁律：**不是一种紫，是按明度拉开的三段紫**（2026-09-19 二次修正）

> 第一轮结论："参考是靛蓝紫 H≈249，我做成了洋红紫 H≈303，差 55°" —— **对了一半**。
> 第二轮照这个结论改成"整幅统一靛紫"，做出来**更难看**（用户原话"还没上个好看"）。
> 用 k-means 拆开两版的主色才看清真相：

| 版本 | 三个紫主色的色相 | 跨度 | 结果 |
|---|---|---|---|
| **参考图** | **253° 深靛底 · 277° 紫罗兰机身 · 294° 藕荷亮面** | **41°** | 层次丰富、"高级" |
| 洋红紫版（错） | 301° 底 · 314° 机身 · 308° 亮面 | 13°，且整体偏红 50° | "粉扑扑、发灰、廉价" |
| 统一靛紫版（更错） | 240° 底 · 241° 机身 · 245° 亮面 | **5°** | **单调、发冷、发平** |

**根因**：参考图的"高级紫"= **深靛蓝紫的底 + 紫罗兰的机器 + 藕荷色的亮面**，三段的色相是
**按明度递增**的（越亮越偏暖/偏红）。只做"一种紫"（不管偏红还是偏蓝）都会失去这个层次。

**三条实操**：

1. **prompt 里给三个数值锚点**（照抄）：
```
THREE-STEP PURPLE RAMP, all three steps clearly visible:
(1) deep background INDIGO BLUE-VIOLET, about rgb(32,18,82), hue 253;
(2) machine bodies VIOLET, about rgb(97,59,120), hue 277 — warmer and redder than the background;
(3) lit top surfaces pale MAUVE, about rgb(150,112,154) to rgb(176,146,182), hue 295 —
    soft pink-violet where red and blue are nearly equal.
The three steps span about 40 degrees of hue. Do NOT paint the whole picture one single blue-purple:
NO cobalt, NO navy, NO blue machine bodies. NOT magenta or fuchsia either.
COOL SHADOWS, WARM LIGHTS: in shadow the purple leans slightly blue (~242); on lit tops ~298.
```
⚠️ 反面教训：写 `pale mauve / lilac` 而不给 RGB 时，模型会做成**灰蒙蒙的藕灰**（实测饱和度掉到 0.366）。
**必须给数值。**

2. **兜底校正**（一条命令到位，几乎必做）：
```bash
python scripts/tone_match.py <scene.png> --hue-ramp 1.0 --sat 1.42 --gamma 1.30 \
       --warm-r 1.05 --cool-b 0.95 --vignette 0.20
```
`--hue-ramp` 按像素明度把紫色族重映射到 `253/277/296` 三点折线，**只动紫色族**，
橙/绿/奶油/红一律不碰。可调锚点：`--ramp-h-dark / --ramp-h-mid / --ramp-h-light`、
`--ramp-v-lo / --ramp-v-mid / --ramp-v-hi`（按你自己图的明度分布标定）。

3. **⚠️ 紫阶必须放在最后一步**：暖化（R↑ B↓）会把紫重新拽向洋红 15~20°，
放前面会被抵消。脚本已固定在流程末端执行。

**验收口径**：主色里紫族色相跨度应 **≥ 35°**；三档大致落在 250 / 275 / 295 附近。

<details><summary>老结论（仅供追溯，已被上面取代）</summary>

偏红 55° 的紫，人眼读作"粉扑扑、发灰、廉价"；偏蓝的靛紫才读作"夜里丝绒、高级"。
背景 RGB (27,15,91)、H 249、B−R +64 是参考值。早期 prompt 写
`hue ~250 top, 290 centre, 325 lower` 的分层法是错的（模型让 325 成了主导）。
</details>

---

## 三·十一、高光铁律：**纯白面积 ≤ 1%**

模型爱把奶油色打成纯白，白花一片就是"塑料感 / 廉价感"。

| 指标 | 参考基线 | 过曝版本 |
|---|---|---|
| 亮面 RGB | (222,165,112) 暖奶油，V=0.87 | (252,200,133)，V=1.00 |
| V>0.95 占比 | **0.82%** | **5.75%**（7 倍） |

**prompt 写法**：
```
HIGHLIGHT RULE: all highlights are SOFT and CREAMY, never blown out to pure white.
The brightest clay surfaces stay near rgb(222,165,112). Nothing here is #FFFFFF white.
```
**兜底**：`tone_match.py --hi-rolloff 0.28 --hi-start 0.86 --hi-keep 0.40`
（把 V>0.86 的部分压缩到 0.4 倍，V=1.0 → 0.916）。

---

## 三·十二、机器要「高、密」—— 高度预算 + 零件密度（本轮最后一道差距）

**把参考图和自己的图上下拼成一张对照图**（`_vs.py` 那套），差距一眼可见：
参考图的机器从标题下方 **y 17%** 一直撑到 **y 72%**，表面布满管道/仪表/齿轮/铆钉；
我的是**上方一大片空背景 + 机器又矮又光板**。这不是画风问题，是两个可量化的硬指标：

**① 高度预算**：机器（含所有装置）占帧高 **≈50%**，顶到标题下方、底到 y 66%。
prompt 里写成硬指标，别用"大一点"这种词：
```
MACHINE HEIGHT: they START immediately beneath the title, at about y = 18 PERCENT of the
frame height, and RUN DOWN TO about y = 66 PERCENT. There is NO wide empty background gap
between the title and the tops of the machines. Their bases all rest at about y = 66%.
```

**② 零件密度**：机器表面要有几十个小细节，光板方盒=廉价。
```
DETAIL DENSITY: BUSY, INTRICATE, toy-like miniature machines packed with rivets, bolts,
screws, pipes, elbow joints, valves, round pressure gauges with little needles, dials,
small gears, control knobs, levers, handles, hatch doors, vents and warning plates.
High information density, like a finely made miniature machine model.
NOT smooth plain boxes with flat blank sides.
```

**③ 构图必须是"特写"**：主机器被左右边缘**裁切**，才显大。
```
FRAMING — an AGGRESSIVE CLOSE-UP. The left machine IS CUT OFF by the LEFT frame edge and
the right machine IS CUT OFF by the RIGHT frame edge. No empty background strip down either side.
```
（"摆拍的小场景"= 四周留了一圈背景；"特写的大机器"= 物件冲出画框。用户一眼就能看出这个差别。）

---

## 三·十三、局部修补：模型"多给一个"就用 inpaint，别重出图

模型经常自由发挥：本该 1 个红心给了 2 个、货架上多冒一个小人偶、多一块道具。
**重出图 5–10 积分且提示词未必听话**，用 `scripts/patch_region.py` 抹掉更快更准：

```bash
# 1) 先用色相掩膜定位多余元素
python - <<'PY'
import numpy as np; from PIL import Image
a = np.asarray(Image.open(P).convert('RGB')).astype(np.float32)
r,g,b = a[:,:,0]/255, a[:,:,1]/255, a[:,:,2]/255
red = (r-g>0.22)&(r-b>0.22)          # 找红色块
cols = red[:int(0.25*a.shape[0])].sum(0)
print([ (x, cols[x]) for x in range(0, a.shape[1]) if cols[x]>2 ][:40])
PY
# 2) 抹掉多余的那个（框比目标多留 8~12px）
python scripts/patch_region.py scene.png --box 888,58,986,162 --out scene_fixed.png
```
（靠 `cv2.inpaint` TELEA 算法用周围像素补回来，纯色背景区域几乎无痕。）

---

## 三·十四、诊断法：**"不好看"不要靠感觉，靠 k-means 三主色 + 紫阶跨度**

用户说"丑 / 没上个好看 / 说不出哪不对"时，**别急着改 prompt 重出图**（一版 5–10 积分，
而且很可能是往错的方向改）。先跑一次主色分解，把差距变成数字。

```python
# 1) k-means 取 8 主色 → 打印 RGB / 占比 / 色相 / 饱和 / 明度
#    （脚本：clay_bench 风格，把参考图和自己的图各跑一遍）
# 2) 紫族的色相跨度 = 主色中 H∈[200,350] 且占比>6% 的 max(H) − min(H)
# 3) 背景暴露率 = 以四角+顶边中位色为背景色，统计距离 <0.16 的像素占比
# 4) 6×3 网格纹理 std：最低格 ≥45、平均 ≥55、<30 的格 = 0
```

**实测判读表**（2026-09-19 第 8 页四版实测）：

| 指标 | 参考 | v7 用户偏好 | v11 被否 | v12 修正版 |
|---|---|---|---|---|
| 紫阶跨度 | 58° | 35° | 55°（但落在 225–245 蓝区） | **53°** |
| 蓝族占比 | 21.5% | 0.1% | **52.1%** ← 病根 | **0.0%** |
| 紫罗兰占比 | 32.3% | 31.6% | 9.2% | **56.7%** |
| 暖色合计 | 35.6% | 36.3% | 31.4% | **39.0%** |
| 暖/冷紫比 | 0.59 | 0.63 | 0.48 | **0.68** |
| 背景暴露率 | 26.7% | 39.5% | 29.2% | 38.9% |
| 纹理空格(<30) | 0/18 | 2/18 | 4/18 | 2/18 |

**读法**：
- `蓝族 > 40%` → 机器被画成了钴蓝，**一定丑**（单调发冷）→ 上 `--hue-ramp`。
- `紫阶跨度 < 20°` → 整幅只有一段紫 → 单调发平 → 上 `--hue-ramp`。
- `暖/冷紫比 < 0.5` → 画面偏冷 → 补暖色道具 / `--warm-r`↑。
- `背景暴露率 > 35%` → 机器之间空隙大、不够满 → 只能重出图（prompt 加 DENSITY 段 + 管道连接）。
- `纹理空格 ≥ 1` → 有平区 → 同上。
- 明度 p50 低于参考 0.06 以上 → `--gamma 1.25~1.35`。

**只看一项会误判**：v11 的紫阶跨度 55° 看着"合格"，其实那 55° 全在 225–245 的蓝区里 ——
所以必须**蓝族 / 紫罗兰 / 洋红紫三个桶一起看**，别只看跨度。

`tone_match.py --analyze <图>` 可直接打印饱和 / 亮度 / 四角 / 亮部 B−R 四项基线。

---

## 三·十五、「嵌条法」—— 把标签条嵌进**道具表面**（2026-09-19 第 9 页首创）

> ⚠️ **已降级，日常别用。** 用户看到成品后原话：「**框框像另外的画风，而不是和板子一体**」。
> 原因：板是一层、条是另一层，条必然读成"贴纸"。**清单条目请改走【三·十六 浮条法】。**
> 本节只保留两个仍有用的零件：①「出图时就把槽画出来」的 prompt 写法（要嵌条时才用）；
> ②「窄条字符预算」的算法（条宽 ÷ 字号 → 最多几个字）。

【三·九】讲的是"贴在**画面底部**的通栏条"；这一节讲**另一种槽位**：把标签条嵌进画面里某块**道具的板面**
（清单板 / 文档 / 目录板 / 任何"一块带行的板"）。LP7 清单板、LP8 文档页都靠它落地。

**四步做法（每一步都要量，不能目测）：**

1. **出图时就把"槽"画出来**。prompt 写死：
   `Its face is a smooth lighter VIOLET-MAUVE clay panel carrying FOUR EQUAL HORIZONTAL RECESSED SLOTS stacked one under another with perfectly even spacing — each slot is a shallow empty groove. The panel face and all four grooves must be COMPLETELY BLANK.`
   同时照旧写 `ABSOLUTELY NO TEXT`（板面必须是空的，文字全靠脚本贴）。
   ⚠️ 别要求"板要多宽"就以为会给到位 —— 实测写"x 5%~57%"模型只给了 x 28%~52%（板面仅 **224px** 宽），
   **板面尺寸一律出图后再量**。
2. **量板面边界**：在板面高度取一行（本轮 y=320）、逐列找亮度跳变 → 得 `x0/x1`
   （本轮 298 / 522 → `--x0 0.291 --x1 0.510`）。
3. **量凹槽行**：在板面中央取一列（本轮 x=400）、逐行找局部暗谷 → 本轮 230 / 280 / 330 / 380（间距 50）。
   取 `bar_h = 间距 − 缝`（50 − 8 = **42**）、`top` = 首个凹槽上方一点（**226**），
   **务必检查 4 条把凹槽全盖住**：条间缝落在 268–274 / 316–322 / 364–370，凹槽 280 / 330 / 380 都在条内 ✅。
   （缝一旦压在凹槽上，那条刻痕就会从缝里露出来。）
4. `clay_band.py run --scene <已校色的场景> --rows rows.json --out page.png --top 226 --bar-h 42 --gap 6 --x0 0.291 --x1 0.510`
   —— **`--x0/--x1` 收窄到局部**（不只是通栏用），条就会精确落在板面里。

**窄条的字符预算（关键约束）**：
条宽 224px、高 42px（字号 25px）→ 扣掉徽章 39 + 左右边距，**每条最多 6 个中文字**。
超了脚本会自适应缩号，缩到 `bar_h × 0.36` 仍放不下就会**溢出条的右端**。
→ 所以板上每条只写 **5–6 字的关键词**，解释句放到口播 / 讲师备注里（与【三·七】"图内只放标签"一致）。
**想要更长的句子，必须先让板更宽（重出图），别硬塞。**

**验收（第 9 页实测）**：饱和 0.587 · 四角 32.5 · 6×3 空旷格 **0/18** · 最低 40.6 / 平均 55.2。
板上贴条顺手把"板面那种大片平色"的格子填掉了 —— 空旷格从 5/18 降到 **0/18**。

---

## 三·十六、「浮条法」—— 清单条目要**浮在背景上**，不要嵌进板面（2026-09-19 第 9 页第二轮 · **推翻【三·十五】**）

> 用户原话：「你看下四框八六和我的区别，导致你这一张**框框像另外的画风，而不是和板子一体**，
> 而且始终场景的内容**违和**，场景像是**乱凑一起的**，要真正服务于内容。
> 你多参考这个文件每一张画面，**有时候不用很多元素，而是文字内容**，你看每个排版，内容，文字画面都是适配的。」
> （随消息附上八六老师**36 页原版课件 PDF**：`海南省妇联职场班_从会用AI到拥有自己的Skills_3小时实操课_86老师(8).pdf`）

### 【三·十五 嵌条法】为什么错

嵌条法把标签条塞进一块**大板**的凹槽里。出图得到的是"一块紫板 + 板上一个平色面板"，
再往上贴四条 —— 视觉上就是**两层**：板一层、条一层。条于是读成"贴纸"，不是画面里本来就有的东西。
八六老师**从头到尾没有这么做过**。

### 参考图真相（逐行扫描 p10 / p16 实测）

八六的清单条目是**一根根浮在背景上的厚实黏土胶囊**。宿主是**背景**，不是板。

| 项 | p10（7 条 · 对勾圆徽章） | p16（5 条 · 奶油方徽章） |
|---|---|---|
| 整列横向 | **左起 4.6% · 右止 33.6%**（只占 29% 宽） | 左起 ~4% · 右止 ~60% |
| 条高 | **帧高 6.1%** | 帧高 ~9% |
| 条间缝 | **帧高 4.5%**（缝里**直接露背景紫**） | 帧高 ~5% |
| 整列纵向 | y **18.9% ~ 88.1%** | y ~21% ~ 90% |
| 条面 | 单一**哑光紫罗兰** ≈rgb(126,102,180)，带颗粒 | 单一**橄榄绿** |
| 文字 | **奶油色**粗体 + 深色描边 | 奶油色粗体 |
| 徽章 | 圆，**独立色**（柠檬绿），直径略大于条高 | 圆角方，奶油底 + 彩色图标 |
| 右端 | **全部齐平** | 齐平 |

三条要点：
1. **同一列的条用同一个颜色**（不是四条四色）——靠**徽章**区分，不靠条色。四条四色就回到"贴纸"。
2. 条之间**留缝、缝里露背景**（缝 ≈ 条高 0.7 倍）。缝填死就变成"一整块板"。
3. 条是**浮**的（有明显的下缘投影落在背景上），不是"嵌"的。

### 做法（第 9 页 v2 实测流程）

1. **出图时把左侧一整块区域留空**。prompt 明确写死：
   `ZONE A is the LEFT 42 PERCENT ... Below the title, Zone A is a smooth, even, nearly empty background field — just the flat purple backdrop. Do NOT put machines, tools, jars, gears, plants or props inside Zone A. Keep it quiet and open.`
   标题单独烘在左上（`y = 4% ~ 17%`），并照旧写 `ABSOLUTELY NO TEXT`。
   **别要求"画一块板"** —— 板就是"大片平色 + 凹槽"的来源，也就是违和感的来源。
2. **出图后把左区压深并向背景靛紫靠拢**（不能只调 prompt，模型不会听话）：
   ```python
   tgt = np.array([34., 20., 86.], np.float32)          # 目标深靛紫
   xr  = np.clip((0.66*W - xx) / (0.56*W), 0, 1)        # 左 1.0 → 右 0
   t   = (0.74 * xr) * (1 - tb)                          # tb = 标题区软掩膜（保护，最多压 10%）
   a2  = a*(1-t) + tgt*t
   ```
   **单调横向渐变顺手吃掉"出图时左右两块背景造成的拼缝"**（本轮出图在 x≈44% 有一条硬接缝）。
   再叠一层四角径向暗角（乘法，不涂黑）把四角压到 ~30–70。
3. 合成：
   ```
   clay_band.py run --scene scene_tone.png --rows rows.json --out page09.png \
        --x0 0.046 --x1 0.43 --top 0.305 --bar-h 48 --gap 30 --text-color light
   ```
   每行 `{"key":"先锁人物锚点","bg":[150,120,206],"badge":[236,150,30],"icon":"slabs","light":true}`。

### 「场景要服务内容」的三条硬约束（本轮用户第二个不满）

八六每一页**只有一个主场景，而它是标题的具象比喻**：工具箱 / 流程线 / 工作台 vs 手册 / VS 对比 /
三个物件 / 工作流管线 / 门 / 卡片网格 / 漏斗 / 文件夹 / 分层柜 / 地图 / 实验室 / 齿轮 + 清单。
**不是"一个车间里堆满道具"。**

1. 写完 prompt，**逐个道具问一遍：删掉它，这一页的话会变少吗？** 不会变少 → 换掉，不是留着。
2. 主场景只留**一个动作**。第 9 页 =「一块**扁塌灰蓝**的黏土板（改前）→ 一块**厚圆奶油**的黏土板（改后），
   中间躺一把抹刀」，把"改"直接画成实物对照。同 p34「只改最影响结果的一处」的思路。
3. 四角的星/叶/心/齿轮**可以有**（八六也有），但那是**点缀**，不能替代主场景。

### ⚠️ 密度基线必须**按版式分档**（本轮最重要的修正）

【三·六】的「空旷格必须 = 0、最低 ≥45」是在**满版机器页**（p02 / p28）上标定的。
**左列清单版（LP1 类）的参考基线本来就低**：

| 页 | 6×3 最低 | 平均 | <45 的格 |
|---|---|---|---|
| 八六 p10（左列 7 条） | **32.0** | 55.3 | **3 / 18** |
| 八六 p16（左列 5 条） | 43.0 | 57.3 | 1 / 18 |
| **第 9 页 v2（左列 4 条）** | **35.1** | 54.1 | **3 / 18** |
| 八六 p02 / p28（满版机器） | 46.9 / 40.0 | 63.0 / 60.1 | 0–1 / 18 |

→ 判 LP1 类页面时**拿 p10 当基线**（最低 ~32、平均 ~55、3 格偏平就算达标）。
**别拿 p28 的"0 格"去要求左列版**，否则会为了填满而在左列乱塞道具 —— 正好踩中用户说的"乱凑"。

### 文字优先（用户本轮的另一句原话）

> 「**有时候不用很多元素，而是文字内容**，你看每个排版，内容，文字画面都是适配的」

八六 36 页里**至少三分之一是"文字/清单为主 + 一个小道具 + 人物"**：
p16 五个把 / p19 安全四问 / p23 七维度 / p30 六条需求 / p31 命令清单 / p34 问题→改法表。
**别每页都硬造一个大机器场景。**

---

---

## 三·十七、清单页的**三种承载**：卡式 / 列式 / 底栏式（2026-09-19 第 9 页 v3 后确立）

> 用户原话（第 9 页第二轮打回）：**「不是，是画面与内容不匹配，像是随意堆元素而已」**。
> 前半句（贴纸感）不是重点，**后半句才是**：画面里的东西必须能一条条对上文案。

### 铁律：**N 条内容 = N 件道具，数量与顺序都要一一对应**

八六 p10 的 7 条判据 ↔ 一个"筛选漏斗"场景（漏斗=筛、垃圾桶=淘汰、SKILL 箱=留下），
**场景是这 7 条的共同动作**；而 p24/p26 那种"并列项"页面，则是
**每张卡各自带一件只属于它自己的东西**。两种都合法，但你**不能**"一个场景 + 一堆通用道具"。

**开稿前对每个道具问一遍：删掉它，这页的话会变少吗？不会 → 换掉（不是留着当填充）。**

反面清单（第 9 页 v1/v2 被判定"乱凑"的元凶，全部与文案无关）：
齿轮 · 木槌 · 颜料罐/铅笔筒 · 工具箱 · 机器人 · 红心 · 绿叶 · 紫花 · 挂钩工具墙。
→ 这些**只能出现在"道具本身就是内容"的页面**（如第 8 页的生产线），不能当填空背景。

### 三种承载方式（选一种，别混） 

| | **卡式**（2026-09-19 第 9 页 v3 首创） | **列式**（八六 p10/p16） | **底栏式**（八六 p02/p28） |
|---|---|---|---|
| 形状 | **N 张并排 / 2×2 的黏土卡**，每卡一件对应道具 | 一列**浮在背景上**的胶囊条 | 一条通栏四色横带 |
| 文字 | **直接排进卡面留白**（见下） | 奶油字压在条面上 | 深棕字压在条面上 |
| 横向 | 卡列 x **3%~76%**，人物 x 79%~99% | 条 x **4.7%~33.3%**（宽 28.6%） | x 3.8%~75.5% 或通栏 |
| 适用 | **并列的 N 个同类项**（改法/要点/对比档位） | 同列 N 条短句 | 收尾/总结的 3~4 条 |

### ⚠️ 【三·九】那张表里的"条高 5.4%"**只适用于底栏式**
`p10`（列式）逐行扫描的真几何**完全不同**，别再混用：

| 项 | p10 列式实测（1467×825） | 换算 |
|---|---|---|
| 条高 | **69px** | **帧高 8.4%**（576 高 → **bar_h=48**） |
| 条间缝 | **19px** | **帧高 2.2%**（576 高 → gap=13）← 缝很窄，不是"留一大片背景" |
| 条宽 | **420px，右端齐平**（±1%） | **帧宽 28.6%**（1024 宽 → 宽 293px） |
| 条左起 | x=69 | **帧宽 4.7%** |
| 徽章直径 | **45px** | **条高 × 0.65**（不是 ×1.1！） |
| 徽章左起 | x=86 | 帧宽 5.9%（内缩 1.2%） |
| 文字左起 | x=175 | 帧宽 11.9% |
| 文字高 | **33px** | **条高 × 0.48**（576 高 → 字号 ≈26px，`text_ratio=0.54`） |
| 条面 | 中心 rgb(110,78,158)，上缘高光 rgb(145,104,186) | — |

> **教训**：上一版把 `p02` 的底栏几何（5.4% / 齐平 / 徽章描边）套到 `p10` 的列式条目上，
> 做出来"缝大 2.4 倍、徽章大 1.7 倍、条宽多 34%、字大 30%" → 条看着"胖而散"、和画面不是一套。
> **同一个 PPT 里不同的条，几何就是不同的，量哪一张用哪一张。**

### 卡面排字法（★ 最省事、最不可能"读成贴纸"的一招）

八六 p24 / p26 的清单文字**不是贴在紫底上的胶囊**，而是**直接印在奶油卡面上的深色字**。
文字和卡是同一件东西 → 天然"融为一体"，且**根本不存在"框框像另一套画风"的可能**。

规格（照 p24 实测）：
- 文字色 **深棕近黑 rgb(44,28,22)**（p24 实测最暗 5% = rgb(21,27,7)）
- 卡面 **暖奶油 rgb(234,206,179)**
- 压印 = 暗字 + 下缘一道浅色亮边（`EMBOSS rgb(243,227,205)`，`dy=2`），**不是发光描边**
- 字号自动缩到框宽内（CJK 按 1em、西文按 0.5em 估宽）

工具：`scripts/clay_cardtext.py`
```bash
# 先量出每张卡的**卡面留白框**，再排字
python scripts/clay_cardtext.py --scene scene.png --out page.png --spec rows.json
# rows.json = [{"box":[111,398,224,478], "text":"先锁人物", "size":24}, ...]
```
**量卡面留白的代码**（`V>0.72 & S<0.38` 取奶油面，逐行找连续段；凹槽行会让段断开）：
```python
cream = (V>0.72) & (S<0.38)
# 下半格 = 每列上"最后一段连续奶油"的起点 → 文字框 y0
```

### 文字占比基线（36 页全量实测，用来判断"该不该让文字扛内容"）
| 页 | 文字像素占比 | 页 | 占比 |
|---|---|---|---|
| p24 | **33.6%** | p04 / p14 / p22 | 15.1 / 14.1 / 13.4% |
| p21 | 24.0% | p25 / p32 | 12.0 / 11.1% |
| p35 / p26 / p29 | 19.4 / 19.1 / 18.1% | p31 / p36 / p01 | 9.3 / 9.7 / 7.0% |

→ **36 页里 12 页文字占 ≥10%**。"少堆元素、让文字扛内容"在八六课件里是**主流做法之一，不是例外**。
用户说「有时候并不需要堆很多元素，而是用文字本身来承担内容」= 指的就是 p21/p24/p26/p29/p35 这一类。

---

## 三·十八、区域定向分级 —— `hue-ramp` 救不回来的时候用（2026-09-19 第 9 页 v3 首创）

**病根**：`tone_match.py --hue-ramp` 是**按明度**把紫色族映射到三段紫阶，
它默认**参考图的明度顺序是单调的**（深底 V≈0.32 < 机身 V≈0.47 < 亮面 V≈0.60）。
模型出图经常把顺序搞反 —— 第 9 页 v3 实测：

| 部位 | 模型给的 | 应该在 |
|---|---|---|
| 背景墙 | rgb(70,61,101) **V=0.435** / H=271 | V≈0.32 / H=253 |
| 卡框紫 | rgb(90,55,88) **V=0.353** / H=303 | V≈0.47 / H=277 |

→ **背景比道具还亮**，于是 hue-ramp 把背景判成"中间调"→ 染成 277°，
卡框反而落进"暗部"→ 染成 253°。**整幅的紫就烂在一起，怎么调参数都救不回来。**

**药方**：先用**几何掩膜**把明度顺序摆正，再谈色相。
工具 `scripts/region_grade.py`（规则数组：几何区域 × 颜色选择器 × HSV 动作 × 羽化）：

```bash
python scripts/region_grade.py --scene tone.png --out graded.png --spec grade.json --report
```
```json
[
 {"region":"outside",
  "keep":[[92,200,244,505],[266,200,414,505],[436,200,581,505],[603,200,742,505],[752,115,1024,575]],
  "select":{"h":[200,350],"s":[0.10,1.0],"v":[0.10,1.0]},
  "hue":252,"hue_k":0.88,"sat":1.32,"val":0.74,"feather":26},

 {"region":"inside","box":[92,200,244,505],
  "select":{"h":[275,355],"s":[0.22,1.0],"v":[0.12,0.66]},
  "hue":277,"hue_k":0.90,"sat":1.10,"val":1.08,"feather":6},

 {"region":"inside","box":[92,200,244,505],
  "select":{"h":[0,70],"s":[0,0.40],"v":[0.55,1.0]},
  "blend_to":[234,206,179],"blend_k":0.42,"feather":6}
]
```
- `keep` 里的框 = **不许动**（卡片 / 人物）；`outside` = 它们的补集 = 墙。
- `feather` 必须 ≥12，否则几何边界会出**硬接缝**（第 9 页 v2 就是被这条坑过）。
- `blend_to` 是把奶油往参考色 rgb(234,206,179) 拉，`blend_k 0.42` 刚好。

**验收（第 9 页 v3 实测结果）**：墙 rgb(38,25,82) H=254（参考 32,18,82 H253）/
卡框 277° / 卡面 rgb(220,186,164) / 洋红紫 9.9%→**0.1%** / 蓝族恢复 13.4%。

---

### 圆角外框 + 底部深色条

参考图整幅画面坐在**一块圆角黏土底板**上，最底还有一条深藏青条。
这两样让画面"有边、立得住"，也顺手把四角的空旷格拉上去。

---

## 三·十九、**自由场景叙事 vs 卡片板式** —— 画面感的根子（2026-09-19 第 9 页 v4 定案）

> 用户第四次打回后（附豆包逐维度诊断）确立。**这是本 skill 最容易被忽略、却最决定"像不像八六"的一条。**
> 前面【三·十五~三·十八】解决的是"文字怎么承载"；这一条解决的是**"画面本身怎么搭"**。

### 病根一句话

**把道具"关进框里、摆整齐" = 板式 PPT；把道具"摊在场景里、有前后" = 自由场景叙事。**
八六的每一页都是一个**现场**（工作台、车间、实验室、筛选漏斗），不是一个**容器**。

### 铁律一：禁止把道具关进卡片 / 面板 / 方框 / 格子里

- ✅ 道具**散落在桌面与地面上**：有倾斜、有重叠、有半遮挡、间距不等。
- ❌ "四张等大的卡，每张卡里放一件道具"——**这就是用户说的"卡片板式 PPT 构图"**。
- ❌ 等距等分、对称居中、整齐一列/一行。
- 例外：**文字条目**可以是规整的浮条（八六 p10 左侧七条也是齐的）——
  **判据不是"齐不齐"，而是"道具是不是被框住了"。**

### 铁律二：人物**跪地/坐地**，不要站在圆台底座上

- 八六 p10：男生**跪在地面**上，身体还被大箱子挡住一部分 → 融入环境。
- ❌ 我犯过的错：给人脚下垫一个**圆形台座** → "人物像单独贴上去的，底座割裂"。
- ✅ 要写：`kneeling on the FLOOR. Not on any pedestal, platform, step or disc`
  + `heavy contact shadow puddling right beneath her`（身下有**接触阴影**）
  + `her body is partly tucked behind the bench`（**被道具遮挡一部分**）
- prompt 里必须显式写 `NO pedestals or platforms`——模型默认爱给底座。

### 铁律三：**三层纵深**（近 / 中 / 远），不是"一个平面"

| 层 | 位置 | 内容要求 |
|---|---|---|
| **前景** | 画面下缘，**被下边缘裁切** | 大件道具的局部（木箱角、石块、大齿轮、纸卷），**部分出画** |
| **中景** | 视觉重心，**偏右** | 主场景 + 人物 + 正在使用的道具 |
| **后景** | 上缘 | 带颗粒斑驳的墙（挂板 / 挂工具 / 小架子），**清晰可读、不虚不雾** |

prompt 关键词：`FOREGROUND ... slightly cropped by the frame` / `strong three-plane depth` /
`aerial haze and a fog of depth between the planes`。

### 铁律四：光影是最大的质感差距 —— 硬主光 + 互投 + 闭塞阴影

- ✅ `One strong key light from the UPPER LEFT` + `Objects cast SOFT LARGE SHADOWS onto each other
  and onto the floor`（**互相投影**）+ `Strong ambient occlusion in every crevice, corner and
  contact point`（**闭塞阴影**）
- ❌ 平光 / 正面光 / 阴影单薄 = "偏平光，没有空间氛围感"。
- 这句要放在 prompt 里单独成段并写 `the single most important part`，否则模型默认给均匀布光。

### 铁律五：背景**不是平涂** —— 要有颗粒 + 不均匀斑驳（**但不许雾**，见【三·二十九】）

- prompt：`the wall carries subtle noise grain and uneven tonal mottling — NEVER a flat solid fill,
  NEVER hazy`
- ⚠️ **别写 `soft haze` / `fog` / `mist`**：模型会照做，整幅盖一层灰纱（第 10 页 v4 就是这么翻的）。
- 出图后不够时，用脚本叠一层**亮部保护的高斯颗粒**（见下方"颗粒后处理"）。

### 铁律六：标题**立体黏土字 + 白/奶油描边**，**不加长条底座**

- ✅ 参考：粗黏土字，**黄 + 白描边**。
- ❌ 我犯过的错：字下加一条**橙色长条**当底座 → 豆包："文字卡片是独立相框式模块"。
- prompt：`in WARM YELLOW, each letter carrying a thin CREAM WHITE outline` +
  `Do NOT put any bar, plank, slab or strip underneath the title`。

### 铁律七：装饰要**随机撒**，不要排齐

小爱心 / 绿叶 / 小石块 / 一颗星——`sprinkled RANDOMLY here and there — uneven and asymmetric,
never in a neat row`。整齐的点缀会立刻读成"装饰元素"而不是"场景的一部分"。

### 铁律八：**冷暖对比**要主动给

豆包："紫色为主，白色占比更高，暖色调偏少，整体偏冷"。
→ prompt 里明确要求 **木质道具**（`NATURAL WOOD TAN props`：木工作台、木箱）+ 暖橙黄点缀。
紫底 + 暖木 + 黄标题，才撑得起参考那种"饱和度柔和"的丰富感。

### 骨架推荐：**左列浮条 + 右侧自由场景**（八六 p10 就是这个）

- 左 1/3：文字区（浮条 4~7 条，【三·十六】规格）。
- 右 2/3：自由场景叙事（铁律一~八）。
- prompt 里把左 1/3 写成 `calm zone reserved for text: a clean deep purple wall with subtle grain,
  deliberately kept clear of large props`（**要"留而不空"**——有颗粒有斑驳、但空气是干净的，只是没有大件）。

### 颗粒后处理（出图后墙面仍然太平时）

```python
import numpy as np
from PIL import Image, ImageFilter
a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
H, W = a.shape[:2]
g = np.random.default_rng(19).normal(0, 3.4, (H, W)).astype(np.float32)
gm = np.asarray(Image.fromarray(np.clip(g*20+128, 0, 255).astype(np.uint8))
                .filter(ImageFilter.GaussianBlur(0.55))).astype(np.float32)
gm = (gm - 128) / 20.0
lum = 0.299*a[:,:,0] + 0.587*a[:,:,1] + 0.114*a[:,:,2]
w = np.clip((215 - lum)/215, 0, 1)          # 亮部保护
Image.fromarray(np.clip(a + gm[..., None]*(6.0*w[..., None]), 0, 255).astype(np.uint8)).save(dst)
```

### 八大维度自查表（用户/豆包口径，交付前逐条过）

| 维度 | 合格线 |
|---|---|
| 背景 | 深暗紫 + 细微噪点肌理 + 不均匀斑驳，**不是纯色平涂**；**空气干净（CRYSTAL CLEAR），无雾** |
| 人物 | **融入环境**：跪/坐地、有接触阴影、被道具遮挡一部分、身下有大阴影 |
| 主体道具 | 散落、前后纵深三层、有近中远景；**不被框住、不规整排列** |
| 文字 | 立体黏土字 / 浮条，与载体**融为一体**；**无独立长条底座** |
| 构图 | 非对称、对角线散点、**重心偏右** |
| 光影 | 主光左上、**物体互投**、**闭塞阴影**、层次分明 |
| 装饰 | 零散随机、不对称；**不要整齐排布** |
| 色彩 | 紫底 + **暖橙黄 + 木色**，冷暖对比；不是"紫 + 大面积白" |

---

## 四、拼装模板（可直接复制）

**内页 prompt 结构：**
```
Keep the EXACT same little kid character as the reference image (image1) — identical round face, identical
large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length
chibi proportion, same handmade polymer-clay texture. Only the clothing, the pose and the scene change.
Place her into this scene: a premium handcrafted polymer-clay diorama, 16:9 widescreen slide.
Scene: {从内页款式库选的场景块}.
Deep purple gradient background with a few floating clay stars.
On the left side, a large cream-colored clay plaque; on it the title '{标题}' is sculpted from thick
3D raised polymer-clay letters: raised, chunky, rounded edges, visible clay thickness, subtle
fingerprints, casting soft real shadows onto the plaque. Handmade clay lettering, NOT flat printed
text, NOT a digital font overlay.
Tactile soft clay with fingerprints, rounded friendly shapes, soft directional lighting, rich
dimensional shadows. Unmistakably handmade clay, not photorealistic, not anime, not glossy plastic.
Make every Chinese character clearly readable and correctly formed, no garbled characters.
```

**封面 prompt 结构：** 同上，把 `Scene` 换成封面款式库的场景块，标题放**顶部居中**铭牌，`Deep purple` 换成所选主题色。

**切换人物款式：**
- 用内置款式 **A** → 只靠文字描述 + 已确认的锚点图。
- 用 **B/C/D/E/F** → 把对应 `style-refs/*.jpg` 作为 `image2` 传入，prompt 加：
  `Match the EXACT art style of image2, borrowing ONLY its art style, NOT its clothes/hair/background.`
- 用户丢自己的照片 / 喜欢的画风 → 同上，一律走 `image2`。

---

## 三·二十、**层叠黏土徽章** ——「先贴一个圆，再贴一个对勾」（2026-09-19 晚 · 用户点名）

> 用户原话：「这个小框的字……**跟人家那个还是有区别**。它那个**更像粘土的**，包括前面的那个对勾。
> **都是一块粘土，就是先贴了一个圆，然后再贴了一个对勾，一层一层的似的。**
> 然后我这个就好像**一个图标**似的。」

### 病根

v1 的徽章是「**平涂圆 + 细线矢量图标**」：`ellipse` 填色 + `draw.line` 画勾 + 一圈浅色 ring。
这在屏幕上永远读成 **UI icon**，不是黏土。而且 v1 还给徽章加了浅色描边 ——
**描边一加就彻底回不去了**（【三·十九】也是同一条：立体全靠明暗，不靠线）。

### 参考图逐像素拆解（八六 p10 · 帧 1467×825 · 7 枚徽章）

| 项 | 实测值 | 换算 |
|---|---|---|
| 徽章直径 | 56px | **条高 × 0.80**（徽章**完全收在条内**，v1 的 1.12 是错的） |
| 徽章左端距条左端 | 20px | 条高 × 0.29 |
| 徽章右端 → 文字左端 | 33px | 条高 × 0.47 |
| 圆饼上部 / 下部 | rgb(129,145,37) / rgb(107,125,21) | 上下差**很小**，别做重 |
| 圆饼最亮 | rgb(175,187,79) | **只在一小块**，亮区要小 |
| 圆饼**底侧壁** | rgb(44,31,68) **暗紫黑** | **不是绿**！厚度是被压进阴影里的 |
| 圆饼**落影** | rgb(36,23,61) 很重 | 落在条面上 |
| 对勾 | rgb(234,224,205) 奶油白 | 占圆的 **0.84**；笔画宽 = 直径 × **0.225**（又大又粗）|
| 描边 | **没有** | 立体全靠明暗 + 侧壁 |

### 画法（`scripts/clay_band.py::_badge_layered`）

顺序就是「**一层一层贴**」，从下往上：

1. **圆饼落地投影** —— 右下偏移 d×0.085 / 0.175，羽化 d×0.17，色 `BADGE_SHADOW`，要重
2. **圆饼底侧壁** —— 掩膜下移 d×0.105，色 `_mix(BADGE_SIDE, base, 0.22)`（暗紫黑混一点绿）
3. **圆饼顶面** —— 左上受光径向渐变 `_mix(_darken(base,0.30), BADGE_TOP, gr*0.95)`
4. **上缘亮边（收窄！k = d×0.05）+ 下缘内影**
5. **对勾投影** —— 落在圆饼上（色偏深绿，不是黑）
6. **对勾侧壁** —— 勾掩膜下移 d×0.050，色 rgb(172,158,130)
7. **对勾顶面** —— 奶油白 + 上缘高光 + 下缘内影

**两个坑（都实际踩过）：**

- ❌ `ImageDraw.polygon` 用「绕两圈」的点列表画圆 → **自交，填充退化**
  （实测只剩 1282px 的边环，整个绿圆饼消失）。用 `ellipse` + 掩膜噪声扰动。
- ❌ 条带级的**整体颗粒**（v1 默认 `grain=0.30`）会把徽章的明暗渐变打成噪点，读起来还是「花」。
  **降到 0.16**；徽章内部各自再给 0.05~0.06。

---

## 三·二十一、**小字（字形高 < 30px）走「纯字体 + 压印」**，不要走 `render_clay_text`

`render_clay_text` 的立体逻辑对**大标题**是神器，但它有一条上缘加亮：

```python
k = max(2.0, cap * 0.040)     # cap=20 时 k = 2
face_rgb = _mix(face_rgb, _lighten(b, 0.22), clip(top_edge * 0.28))
```

在 **20px 高的字**上，2px 亮边 = 字高的 **10%** → 字的上半截发灰、下半截深，
放大看就是「**字被削掉一半**」。实测第 10 页牌面三行字（cap=20）就是这么翻的。

**判据：字形高 < 30px 时清晰度优先，改用「纯字体 + 压印」：**

```python
# 1) 真字体画掩膜（ss=4 超采样后降采样，笔画才不会糊）
# 2) 下缘外侧 1.6px 画一道亮色 —— 受光的凹槽外壁
ob  = np.clip(_shift(am, 0, 1.6) - am, 0, 1)
reg = reg + (bright - reg) * (ob * 0.55)[..., None]
# 3) 再压深色字
reg = reg * (1 - am[..., None]) + color * am[..., None]
```

字色 `(52,36,26)` 深棕 · 亮点 `(236,222,196)`。锐利 + 有刻痕感，**不要再叠 grain**。

---

## 三·二十二、`scripts/clay_props.py` —— **散落小道具**是补「空」的正道

**什么时候需要**：正文块比参考页**少**（参考 p10 是 7 条，本课只有 4 条），
左列下方必然空出一段。用户会直接说「**感觉空**、上面那张图**没有任何废元素**」。

**两个错误方向（都试过，都否掉）：**

- ❌ **把 4 条放大到填满左列** → 徽章/文字等比膨胀，比例全失真，反而不像参考。
  「满」是**信息密度**，不是元素尺寸。
- ❌ 道具**贴着画面底边排成一条线** → 读成「碎屑」，不是「散落」。

**正确做法（三层一起用）：**

1. **条带尺码只微调**：4 条时条高 ×1.12（55px vs 参考 49px）、右端**保持参考的 33.6%**
   （`G_BAR_H_N4=52~55` / `G_GAP_N4=13~14` / `G_RIGHT_N4=0.336`）。
2. **条带纵向定位**：紧贴标题下沿往下放（`top ≈ 帧高 × 0.36`，第 9 页取 210），
   让下方只留参考级的一小条地面 → 下面读作「**前景**」而不是「空背景」。
3. **散落小道具补地面**：布点要有**聚散 + 大小梯度**（近大远小），**别均匀、别成行**。

**接口：**

```python
import clay_props
clay_props.scatter(scene_png,
                   [(x, y, "pebble", 20, 1.0, rot_deg, seed, [r,g,b]), ...], out_png)
# kind: pebble | leaf | heart | star | gear
```

每件自带**左上高光 + 右下侧壁 + 接触影 + 落影 + 颗粒**，与主场景硬主光方向一致。
**颜色必须从主场景里采**（别凭感觉）：

```python
a[y0:y1, x0:x1].reshape(-1, 3).mean(0)     # 采已有道具 / 地面
```

---

## 三·二十三、**第 9 页「浮条法」几何·逐像素重测**（2026-09-19 晚第二轮 · 覆盖【三·十六】旧数）

> 【三·十六】表里的「条高 6.1% / 缝 4.5% / 徽章 = 条高 × 0.65」是**误把 p02 底栏的数套到 p10 列式**上。
> 以下为帧 1467×825 上**逐行扫描**的真值，`clay_band.py` 的 `G_*` 常量就是它。

| 项 | 实测 | 比例 |
|---|---|---|
| 条高 | 70px | **帧高 × 0.0848** |
| 条间缝 | 17px | 帧高 × 0.0206 |
| 条中心间距 | 87px | — |
| 条左端 / 右端 | 65px / 493px | 帧宽 × 0.0443 / **× 0.336** |
| 整列纵向 | y 156 → 747 | 帧高 18.9% → 90.5%（总块高 71.6%）|
| 文字高 | 34px | **条高 × 0.49** → 同视觉校准（字重更轻）取 **0.45** |
| 文字左端 | x 174 | 条左 + 条高 × 1.55 |
| 条面 | rgb(108,74,155) | v1 的 124,102,172 偏亮偏灰 |
| 条间缝 | rgb(16,10,39) | **比背景还暗** —— 靠**逐条投影**做出来，不是背景色 |
| 文字色 | rgb(234,224,205) | 奶油，不是近白 |

**逐条投影（关键）**：只做「整块投影」的话，缝里是亮的，几条会读成
「**一张纸上的几行字**」；每条各自投一次影，缝才暗，才读成「几块独立的黏土」。

```python
lfar  = _blur(_shift(pm, SS*0.8, SS*(gap*0.62+2)), SS*2.4)
lnear = _blur(_shift(pm, 0,   SS*(gap*0.34+1)),   SS*1.0)
rgb, alpha = _over(rgb, alpha, _rgb(SEAM_RGB),
                   np.clip(np.maximum(lfar*0.60, lnear*0.92), 0, 1) * 0.95)
```

---

## 三·二十四、**清晰描边字** —— 深底浅色小字的唯一正解（2026-09-19 晚第三轮 · 用户点名「字全都糊在一起了」）

### 病根（用户原话）
> "这四个小框的字儿又看不清了，图标这会儿一模一样了，但是字儿你要写成八六老师那样……它那个字是就是它立体到什么程度，或者是它只是薄薄的一层，但是它每一个字是分明的，是看得清晰的。"

条内文字原来走 `render_clay_text`（厚侧壁 + 强圆润化路线），三处叠加把六个字糊成一坨：
1. `letter_gap=0.020` → **实际字间距只有字高的 2%**（八六是 20%）；
2. `depth = cap × 0.135` → 每个字带 13.5% 字高的侧壁往右下挤，相邻字的侧壁**直接连上**；
3. 那个函数内部 `_blur(ss*0.95)` + `clip((m-0.11)/0.89)` 的"圆润化" → 笔画被加胖。

### 逐像素实测（八六 p10 第一条 · 帧 1467×825，换算到 1024 帧）
| 量 | 八六参考 | 旧版（v5） | 新版（v6） |
|---|---|---|---|
| 字形高 | 23.7px | 27px | 25px |
| 字形宽 | 22px | 25px | 24px |
| **字间距** | **4.7px（字高的 20%）** | **2.4px（9%）** ← 病根 | **5.5px（22%）** |
| 字色 | rgb(234,224,205) | 偏白 | rgb(234,224,205) |
| 暗边 | 深紫、柔、下缘更厚 | 无（反而有白晕） | 深紫柔描边，右下更厚 |

### 画法（`clay_text.py::render_crisp_text`）
1. **字距 = 字高 × 0.11**（CJK 字形自带约 5% 左右留白 → 视觉间隙 ≈ 20%，与八六一致）；
2. **不做强 gamma 压制**：`_blur(m, ss*0.42)` + `clip((m-0.06)/0.94)` —— 只抗锯齿，**不削笔画**；
3. **深色方向性描边**（这才是"分明"的来源）：12 方向环采样 + 右下扇区半径 ×1.55，
   描边色 = 条面深紫 rgb(52,32,86)；描边再 `_blur(ss*0.55)` 柔化 → 读成"压出的暗边"而不是"印刷描边"；
4. **字面近乎平涂**：上缘亮边只 `×0.16×0.34`、下缘暗边 `×0.05×0.26`。
   用户要的就是这个 —— **"薄薄一层，但每个字分明"**。

判据（三句话）：
- "像图标" = 平涂色块 + 细线勾；
- **"糊在一起" = 零字距 + 厚侧壁；**
- **"分明" = 深色描边 + 20% 字距 + 平涂奶油面。**

字号：条内文字 `text_ratio=0.45`（字高 ÷ 条高）；浮行 `text_ratio=0.50`。
条面颗粒 `--grain 0.11`（原来是 0.16，会把字面打成花）。

---

## 三·二十五、**只有 2~3 条时怎么排** —— 一整列 + 条底，**不许拆左右、不许去掉条底**
（2026-09-19 晚第五轮 · 用户两连否后定案）

> 用户原话：「**它为什么不是一条一条的？**」
> 用户原话：「**它总共就 3 条，你还非要分成左右，干啥呀？这样会不会显得内容太少？**」

**两条铁律（都是被否出来的）：**

1. **条底不许省。** 试过 `render_float_list` 的无条底浮行（徽章 + 字直接浮在暗背景上）→
   用户当场打回「为什么不是一条一条的？」。**只要一页读起来是"清单/步骤"，就必须一条一条有底。**
   无条底浮行仅在"这一页确实不是清单、且左右已有别的骨架"时才允许，本课一律不用。
2. **3 条不许拆左右。** 硬拆成"左 2 条 + 右 1 条"后，用户第一反应是"**内容太少**"——
   因为每边只剩 1~2 条，两边都单薄。**3 条就是 3 条，排成一整列。**

**正确做法：**

- **一整列**，条带**加宽**（3 条时条右端放到 **0.42~0.46W**，比 4 条时的 0.336W 宽得多 —— 条少就该条宽），
  条高 ×1.12、gap ×1.08，**纵向居中**在标题下沿到地面之间，别贴着标题也别贴着底边。
- 画面**靠场景的丰富度补**，不靠把元素放大（【三·二十二】）。
- 骨架搭配：**标题居中 + 一整列（左中位置）+ 右侧自由场景** = 八六 p15 的形态
  （p15 是 5 条一整列 + 右侧柜子）。**不要把 3 条劈成两半去"左右都有"。**
- 脚本：仍走 `clay_band.py::render_label_band(rows, width=W, frame_h=H, bar_h=58, gap=14,
  x0=int(W*0.045), x1=int(W*0.44), top=...)`；`render_float_list` **不要用**。

### 两个已踩过的坑
1. **出图必须写死"左三分之一留空"**。第 10 页第一版 prompt 没写 → 模型把**工具墙**塞满左侧，
   文字无处可放，整页作废。正确写法：
   > "the LEFT THIRD of the frame must stay almost EMPTY — only wall, no furniture, no props, no shelf,
   >  that empty area is deliberately reserved so text can be placed there later."
2. **左列压暗的过渡区间要拉到 0.08W → 0.80W**。原图 x≈0.40W 常有一条**墙棱线**，
   过渡区间窄了（如 0.30W→0.64W）会把它显成一条**硬边**，整幅读成"两半拼的"。

---

## 三·二十六、**布局骨架对照表** —— 每页开工前先"选骨架"，不许默认「左列 + 右景」
（2026-09-19 晚第四轮 · 用户点名）

### 病根（用户原话）
> "现在 9 对了，但是 10 它为什么不是一条一条的？而且为什么文字都在左侧，然后图在右侧？
>  他这人家这个为什么能左右都有，然后大标题在中间？你这个怎么全都在左边儿？
>  **你每次都得对比着出，我看你老是做着做着就好像忘了我的规则。**"

**根因**：`render_label_band` / `compose` 的默认行为就是"左列条带 + 右侧场景"，
调用最省事 → 于是**每一页都被同一个骨架吸过去**。
逐页数过八六 36 页：**"左列条带 + 右景"只有 p10、p29 两页**；
其余全部是**「大标题居中 + 内容左右展开」**。

### 八六 36 页的三种骨架（先选骨架，再动手；这是开工第一步）

| 骨架 | 特征 | 参考页 | 适合 |
|---|---|---|---|
| **A 居中标题 + 左右双列** | 大标题横在顶部**正中**；左列 N 条 + 右列 M 条**夹着中央主体物**；人物压在**最右边缘**（常被画框裁掉）；背后是**整面素墙** | p30、p26、p21 | 要点/属性清单（4~8 条），中央有"主角物件" |
| **B 居中标题 + 横向分栏** | 大标题居中；下面 2~4 栏**并排**（每栏 = 卡/条 + 视觉），人物在右；可有底部总结条 | p33、p19、p16、p34 | 步骤/并列项（3~4 个），每项配独立视觉 |
| **C 居中标题 + 左列 + 右景** | 标题居中或左上；文字集中一侧，另一侧全给场景 | p10、p29 | 文字量大、场景本身承担叙事 |

> **默认不是 C。** 一页文案 ≤4 条时先考虑 A 或 B；C 只在"场景本身要讲一个过程"时才用。

### ⚠️ 骨架选择的第一道闸：**先看条数**（2026-09-19 第五轮补，被用户打回后加）

| 本页条数 | 允许的骨架 | 说明 |
|---|---|---|
| **1–3 条** | **一整列，禁止拆左右** | 拆开 = 每边只剩 1~2 条 → 用户读成"**内容太少**" |
| 4–5 条 | 一整列 + 右景（p10/p15/p16）或 横向分栏 B | 条数刚好撑满一列 |
| **6 条以上** | 才可以用骨架 A 的**左右双列**（p30/p26/p21） | 条数够，两边都不单薄 |

**教训**：第 10 页 3 条被硬拆成"左 2 + 右 1"→ 用户原话「它总共就 3 条，你还非要分成左右，干啥呀？」。
**骨架 A 是为了 6 条以上的清单设计的，不是"凡是标题居中就用左右"。**

### 骨架 A 的实测几何（八六 p30 · 帧 1467×825）

| 量 | 值 |
|---|---|
| 大标题 | 居中，y 0.053–0.181H，中心 x ≈ 0.50W |
| 左列条 | x 0.046–0.311W（宽 0.265W） |
| 右列条 | x 0.575–0.80W（**比左列略窄**，给人物让位） |
| 中央主体 | x 0.30–0.58W，撑满 y 0.28–0.92H（画面的"脊"） |
| 人物 | x 0.80–1.00W，**被右边缘裁掉**，不伸到 0.80W 左边 |
| 背后墙 | **整面素墙**（无洞洞板/无货架），只有颗粒 + 渐变 + 暗角 |

### 落地：左右双列就用现有脚本贴两次
`render_label_band` 支持 `x0/x1/top/bar_h/gap` —— **调两次、贴两次**：

```python
lb = clay_band.render_label_band(rows_left,  width=W, frame_h=H, bar_h=60, gap=14,
                                 x0=int(W*0.030), x1=int(W*0.258))
rb = clay_band.render_label_band(rows_right, width=W, frame_h=H, bar_h=60, gap=14,
                                 x0=int(W*0.478), x1=int(W*0.700))
base.alpha_composite(lb, (0, 173))     # 左列
base.alpha_composite(rb, (0, 212))     # 右列：垂直居中于左列两条之间 → 构图最稳
```

**条数 < 4 时不要放大去填满**（元素等比膨胀 = 比例失真）：左 2 右 1 / 左 1 右 2 都行，
**用"左右"把画面撑开**，比把少量条拉到 8 条的尺寸强。

### 出图 prompt 必须写死的四段（不写模型一定做成"一半空一半满"）
```
· LEFT STRIP (left edge to ~28% across), between 28% and 64% of the frame height:
  plain smooth violet clay WALL only — no props, no tools, no furniture.
· MIDDLE (about 26%-62% across): the visual heart of the picture — <中央主体物>.
· RIGHT STRIP (about 62%-80% across), between 30% and 62% of the frame height:
  again plain wall, kept clear on purpose.
· FAR RIGHT EDGE (80%-100% across): the girl is SQUEEZED AGAINST THE RIGHT EDGE —
  she MUST NOT extend left of 80%; partially cut by the right frame edge.
```
⚠️ **"留空"必须配一句"墙要有颗粒 / 渐变 / 暗角，不是一块空白板"** —— 否则模型给一块平灰板，
用户读成"融入感差"（v2 就是这么翻的）。

---

## 三·二十七、**标题四周的点缀** —— 标题不许孤零零浮在墙上
八六几乎每页标题旁都有 **黄星 + 绿叶 + 红爱心**（有时加一条紫色下划线）。
用 `clay_props.scatter` 补：星 `size 21~24 @ 左肩(0.22W, 0.17H)`、
叶 `size 24~27 @ 右肩(0.79W, 0.11H)`、心 `size 18~19 @ (0.85W, 0.18H)`。
**要点：别做太小**（<16px 基本看不见，等于没做）；`rot` 别给太斜（±30° 以上会变成一条细缝）。

---

## 三·二十八、底图后处理的两条硬教训（2026-09-19 第 10 页 v4）

### 1. 去雾只能「压暗」，**绝不能「提饱和」**

> ⚠️ 但**根本上不要让它有雾**：雾是 prompt 里 `soft haze / fog-veiled` 写出来的（见【三·二十九】§3）。
> 后处理是补救手段，不是方案 —— 第 10 页 v4 去雾折腾 3 轮仍偏灰，v5 删掉雾词重出 1 张就干净了。
雾区 = 低饱和 + 中高亮。想让它变紫就顺手提饱和 → **低饱和区的色相本来是不稳定噪声**，
一提饱和立刻显色：奶油纸面、白大褂上冒出**青绿斑**（实测踩过，整页作废）。

正确做法（只动 V，不动 H/S）：
```python
w = (np.clip((0.30-sn)/0.18,0,1) * np.clip((vn-0.42)/0.15,0,1)
     * np.clip((0.84-vn)/0.14,0,1))       # 低饱和 + 中高亮 = 雾；V>0.84 的纸面不动
vn = vn * (1 - 0.30*w)                    # 只压暗
```
压完 4 角/雾区沉下去，整幅立刻接近八六的"深紫"。

### 2. 左下是「墙」而不是「地面」时，别撒小道具
八六的地面**横跨整幅下缘**，所以左下能放积木/心/叶。
若底图左下只有墙（没有地面线），撒 17~36px 的小物只会读成"**脏点**"。

**正解：改成"贴底缘、部分出画的前景大件"** —— `size 52~66`、`y ≈ 0.98~1.02H`，
让它被下边缘裁掉一块，符合【三·十九】铁律三的"前景被下边缘裁切"。

**源头解法**：底图 prompt 里明确写
`the floor surface must run across the FULL WIDTH at the bottom of the frame`，
否则模型会让左下角一直是墙。

---

## 三·二十九、第 10 页 v5 三处定案（2026-09-19 晚·第六轮 · 用户打回"标题虚化 / 1 不居中 / 雾化"）

> 用户原话：「**不对不对，哪个让你写标题是虚化的呀？没有晕染和虚化。** 他还是第 9 页的
> 那个文字写法是对的，**包括这个复制一份 1，为什么不居中啊？一为什么是顶着的？**
> 其次就是。你**雾化**，我觉得雾化是不对的吧。那个背景，你觉得现在的图跟这个内容搭吗？
> 也不是搭的呀。还有，你**下次不要一下子出那么多张图，消耗我太多积分了**。你就改这第 10 页
> 的话，那你就出这个第 10 页的这个图。」

### 1. 标题的奶油描边 = **同一掩膜外扩 rim**，绝不许"两层不同字号叠字"（虚化的真凶）

❌ 旧做法（本页 v1~v4，全部被否）：渲染两张——奶油层 `cap_height=90` + 橙黄层 `cap_height=84`，
   同 seed 叠上去。看着"应该"是描边，实际是**把整行按 90/84≈1.07 倍缩放**：
   行首行尾各偏出 `0.07 × 行宽/2 ≈ 14px`，中间几乎重合 → 观感就是**边缘一圈晕染、
   字像失焦**（用户："虚化 / 晕染"）。

✅ 正解：`render_clay_text(..., rim=CAP*0.097, rim_color=(168,156,142))`
   —— 内部对**同一个 union 掩膜**做 16 向均匀外扩，再 `_blur(ss*0.50)` 只做抗锯齿。
   边缘干净、宽度均匀、不虚。`rim>0` 时把 `outline` 关掉（两者都在 union 外侧，会互相盖）。

⚠️ **但"外扩"只解决了形状 —— 宽度和颜色错了，照样不是黏土块。** 第七轮用户又打回：
「**就只是纯文字框啊**」。`rim=4.6 / (244,238,226)` **已作废**（太薄 + 太亮），
现行取值与标定方法见【三·三十·1】。

### 2. 数字徽章 —— **本节已被【三·三十·2】取代**

第六轮的"字号 0.82 + 下沉 0.030S"只治了**大小**，没治**字形**。第七轮用户仍说
「**这个 1 依然不是居中……第一笔是这么写，但你正常的字它不会这样写**」——
真因是**字体里的数字带衬线脚**。现行三条规则（字形 / 高度 / 光学居中）见【三·三十·2】。

（保留一条仍然有效的操作提醒：**量上下留白时裁剪框中心必须对准饼心**，差 1.5px 就会误判。）

### 3. 底图 prompt 里的 `haze / fog / mist` 是**禁词**（自伤事故）

第 10 页 v4 那幅"灰蒙蒙"不是后处理造成的 —— 是**我自己在 prompt 里写的**：
`a calm deep purple wall with soft haze and subtle grain`、`a fog-veiled tool wall`。
模型老老实实照做，整幅盖了一层灰纱：饱和 0.347（第 9 页 0.509）、四角 49（第 9 页 39）。
用户一句话点破：「**你雾化，我觉得雾化是不对的吧。**」

**改法**：把雾全删，正面明写
`The air is CRYSTAL CLEAR. There is absolutely NO fog, NO mist, NO haze, NO smoke, NO dust,
NO atmospheric bloom, NO light beam, NO glow wash. Everything is in sharp focus.`
再加色号锚点 `DEEPLY SATURATED rich violet like #4A2E7A / #5B3A93, NOT pale, NOT grey-lavender`。
—— 同一套道具、同一构图重出一张：饱和 **0.488**（原 0.347）→ 一句话治好。

> 连带修正【三·十九】的措辞：**"背景要颗粒雾感"里的"雾"是误读**。
> 八六的背景是 **颗粒 + 斑驳 + 明暗过渡**，不是**灰雾**。写 prompt 时用
> `subtle noise grain and uneven tonal mottling`，**一个 haze/fog 字都不要有**。

### 4. 出图纪律：**一次只出当前页要的那 1 张**

用户原话：「**你下次不要一下子出那么多张图，消耗我太多积分了。你就改这第 10 页的话，
那你就出这第 10 页的这个图。**」
一次 3 张 = 15~30 积分，而"选 1 张"带来的提升远小于"先把 prompt 写对"。
拿不准就**先把 prompt 写进对话让用户看一眼**，再出那 1 张。

---

## 五、一句话记忆

> **人物锁在参考图里，标题捏在铭牌上，其余全从款式库里换。**
> 想让整套图"既像一个系列、又不重样"——就靠这句话。
>
> 补一句（2026-09-19 晚）：**条与徽章不是"画"出来的，是「一层一层贴」出来的 ——
> 圆饼贴在对勾下面，对勾贴在圆饼上面，各自带自己的影和侧壁。**
>
> 再补一句（2026-09-19 晚·第四轮）：**每页开工第一件事是「翻八六 → 选骨架」，
> 不许默认「左列 + 右景」。** 八六 36 页里"左列 + 右景"只有 p10、p29 两页，
> 其余全是「**大标题居中 + 内容左右展开**」（【三·二十六】）。

---

## 三·三十、奶油垫块 + 圆饼序号的**尺寸标定**（2026-09-19 深夜 · 第七轮 · 用户打回"纯文字框 / 1 不居中 / 图不适配"）

> ⛔ **本节关于「标题」的部分已被【三·三十二】取代，只保留作历史依据。**
> 本节推荐的是 `render_clay_text(..., rim=CAP*0.097, rim_color=(168,156,142))`；
> **现在标题一律改用 `render_title_clay()`（【三·三十二】），不要再手调 `rim`。**
> 本节里仍然**有效**的是：**圆饼序号数字必须换字体**（`msyhbd`，见下面的 ·2）。


> 用户原话：「明显不对呀，它那个改法清单就是就还是粘土风，就好像一**先铺了一层白色的，
> 然后再铺了一层黄色的**，但是这个后面那个**就只是纯文字框**啊。而且这个 1 **依然不是居中**。
> 就是说它**所有的字都在一个高度上**，你这个 1 第一笔是这么写，但你**正常的字它不会这样写**。
> **这个是什么规则？你自己想一下。** 然后**配的图依然不适配**啊，重新放这一页。
> **不是说要满满的小道具什么的，是真正适配这个的一页。** 你看那个八六那个他也不是说一定
> 纠结于是什么图什么的。你想一下吧。」

### 1. 标题奶油垫块：宽度 **0.097 × cap**、色 **(168,156,142)**，且必须**自带圆台明暗**

第 9 页标题（对）逐像素实测，与两版错的做法对比：

| 量 | 第 9 页 ✅ | v5 ❌「纯文字框」 | v6 首试 ❌「糊成一团」 |
|---|---|---|---|
| cap 高 | 103 | 80 | 74 |
| 环宽 | ≈ 8px | 4.6px | 11.5px |
| 环宽 / cap | **0.078** | 0.058 | 0.156 |
| 环色 | 外缘 **(172,160,146)** → 内缘 **(128,118,108)** | 平涂亮白 (244,238,226) | 平涂灰奶油 |
| 观感 | 白黏土垫块 + 黄黏土面 | 细白描边 = 文字框 | 字被糊住 |

**取值**：`rim = cap × 0.097`、`rim_color = (168,156,142)`（**灰奶油，不是亮白**）。
内部按 `t`（0 = 贴字面 → 1 = 外缘，用两侧距离场 `di/(di+do)` 归一化）做
`_mix(_darken(rc,0.24), _lighten(rc,0.03), t**0.85)` → 复现"外缘受光、内缘是接缝"的圆台面。

**判据（机检口径）**：**环宽 ≈ 笔画宽的 15~20%**。
- 太薄 → 读成"描边 / 文字框"；
- 太厚 → 相邻笔画的环**互相连起来**，字被糊成一团
  （v6 首试的翻车原因：cap 从 80 降到 74 的同时把 rim 提到 0.156cap，比例直接翻倍）。

**标定方法（可复用）**：把第 9 页的同一个字裁出来，与候选参数渲染的字**缩到同一显示高**并排，
同时看两件事 ——（a）环宽，（b）**笔画之间的空隙有没有被填死**。

### 2. 圆饼序号数字的三条规则（`clay_band._icon_mask` 的 `"1".."5"` 分支）

用户问的「**这个是什么规则**」，答案就是这三条：

1. **字形：必须用不带底衬线脚的数字。**
   ⚠️ 坑：`FONTS["noto"] = NotoSansSC-VF.ttf` 的**阿拉伯数字是带衬线脚的**
   （"1" = 旗 + 竖 + 底部横衬线；2/3 也带平底衬线），跟条里圆润的汉字**不是一套**。
   这正是用户说的「**第一笔是这么写，但你正常的字不会这样写**」。
   → 数字单独走 `FONTS["msyh"]`（微软雅黑 Bold）："1" 是干净的旗 + 竖。
   （实测备选：`segoeuib` / `arialbd` 也干净；`Dengb` 的 1 仍带脚，别用。）
2. **高度：数字 ink 高 = 饼径 × 0.44**（旧版按"字号 ×0.82"设，实得 ink 高 0.52d，偏大）。
   反推字号时**按实际渲染出来的 ink 高迭代**，不要按 `font.getbbox()` 的高度 —— 两者差 20%+。
3. **居中：ink 外框中心 + 面积质心，各半**（光学居中）。
   数字的墨量集中在竖笔上，只按外框居中也对不齐"视觉重心"；质心补上另一半。

**判据**：饼心上下留白相等（±1px）、左右留白相等（±1px）。
（v6 实测：上/下 = 15/14、14/15、15/15；左右 18/18、19/20。）
⚠️ 别拿"9 倍放大图"肉眼判 —— 圆饼底下有落地影，看图会觉得数字偏上；**一律上机量**。

### 3. 出图：主体**唯一**，且"适配"≠"堆道具"

用户对"不适配"的定义，从第五轮的"N 条 = N 件道具"到第七轮的"不要满满的小道具"，
其实是一条：**要一个能自圆其说的场景，不要一堆填充物**。

- ❌ v5 的图 =「一张杂货桌 + 三件并排展品 + 满地碎屑（花 / 齿轮 / 石头 / 纸卷 / 小机器人）」。
  主体不清，下半幅全是与内容无关的填充。用户：「**不是说要满满的小道具什么的**」。
- ✅ 八六的做法 = **一个巨大的主体物件 + 人物 + 干净环境**：
  p7 一座门 / p9 一个打开的盒子 / p10 一个大方框容器 / p11 一个大文件夹。
  人物经常只是**站在旁边当吉祥物**，不需要"手在操作"。
- 本页正解 = 一台**"改造机"**（全场唯一大主体）：左侧进空白模板 → 正面挂木名牌 + 刻字笔 →
  右侧出盖了印的成品。**机器本身就是"从改到造"**，三条内容各落在机器的一个部位上，天然连贯。

**prompt 写法**：
- ❌ 不要写 `(1)…(2)…(3)…` 三条枚举 —— 模型会照字面摆成**三件并排展品**；
- ✅ 写成 `THE ONE HERO OBJECT — this is the whole picture. A single BIG … It tells the story
  by itself, three parts: (a) its LEFT side … (b) its FRONT … (c) its RIGHT side …`；
- ✅ 正面写死"少"：`the bench top holds ONLY the machine` /
  `the floor is CLEAN and nearly EMPTY — NO piles of junk, NO scattered flowers, NO debris`。

---

## 三·三十一、**逐字基线 bug**：`render_crisp_text` 不许按"墨迹外框顶对齐"（2026-09-20 凌晨 · 第八轮）

> 用户第八轮原话（核心）：「**不是 1/2/3 序号的问题。是"复制一份"这个文字中出现的问题。**
> **你根本没有认真读取图片……你白白浪费我积分……不允许敷衍。**」

### 症状

条带里"复制一份"的 **"一"字整体上浮约 13px**（别的字中心 y=232，"一"跑到了 219）。
用户连续两轮说"不对"，而我连续两轮都在改**序号数字** —— 方向错了，改得再细也没用。

### 真因（`clay_text.render_crisp_text`）

旧实现**逐字取 `getbbox(ch)`（该字的墨迹外框）→ 裁到墨迹 → 统一贴到"行顶部"**：

- "复/制/份"墨迹是满高的（29px），贴顶 = 正常；
- **"一"的墨迹只有 5px 高**，贴顶就直接飞到上半空。

**任何"低矮字"（一、二、三、点、横）在"按墨迹外框对齐"的实现里都会浮起来。**

### 正解

逐字渲染后**按字体基线对齐**：用字体的 `getmetrics()` 拿 `(ascent, descent)`，
每字贴到 `y = 行顶 + ascent - 字的 ascent 段高度`（即所有字共用同一条基线），
**禁止用每个字自己的 ink bbox 顶边当对齐线**。

### 机检口径（每一版都必须跑）

对条带文字区做**逐字块扫描**（奶油掩膜按列分块），打印每块的 `中心y`：

- 判据：**所有字块的中心 y 相差 ≤ 1px**（"一"这种字块高只有 5px，中心对齐即基线对齐）。
- 修前实测：块中心 232/232/232/**219**/232 —— 一眼见病灶；修后：231.5/232/232/**231**/232 ✅。

### 教训（比 bug 本身更重要）

1. **用户说"是 XX 文字里的问题"时，先把那句话逐字量化，再动手。**
   上一轮我拿着放大图看了半天序号，却没对"复制一份"四个字做过一次逐字块扫描 ——
   一条 10 行的脚本就能量出来的事，拖了两轮、耗了用户的积分。
2. **必须读用户最新的截图。** 第八轮开头发现我上一轮引用的是 15:32 的旧截图，
   而用户 15:49 又发过一张 —— 读错图 = 全部诊断建立在废数据上。
   **铁律：每次回复前先按时间倒序列出截图目录，读时间戳最新的那张。**

---

## 三·三十二、标题**唯一正解 = 出图模型画的黏土标题**（2026-09-20 第十二轮定稿 · 用户"你疯啦"打回后改死）

> 血泪史：第九~十一轮我一直在"用代码复现第 9 页标题"——错方向。
> 第 9 页定稿的「改法清单」是**出图模型画在底图上的**（四个字体对它墨迹 IoU 上限 0.64，代码永远复现不了）。
> 第十一轮我甚至把第 9 页模型标题 inpaint 掉换成代码字 → 被用户怒斥"你疯啦，完全大错特错"。
> **用户钦定的款 = 模型款**：暖橙黄厚实黏土字 + 米白厚圆边 + 悬浮无底板、无横条底座。

### 两款之分

| | 模型款（**正解**） | 代码款（仅兜底/占位） |
|---|---|---|
| 来源 | 出图模型画在底图上（第 9 页定稿 v6、`_p10_base.png` 的「从改到造」） | `clay_text.render_title_clay()` |
| 质感 | 厚实饱满、手捏不规则、暖光晕 | 规整、平 |
| 用途 | **所有正式页的标题** | 模型素材拿不到时的临时占位，交付前必须替换 |

### 模型款的两条获取路径

1. **首选 —— 出底图时让模型画上**：整页底图的 prompt 里直接写标题（中文四字以内成功率高）。
   第 9 页就是这么来的。
2. **0 积分 —— 从模型画好的底图里抠标题当素材**（换字时用别页已画好的同款标题）：
   完整可跑脚本 `D:/needs/clay_deck/_extract_p10_title.py`，七步：
   ① 暖橙黄粗定位（`R-B>60 & R>140 & G>B+25`，连通块取大）→ 得字面 bbox；
   ② bbox 外扩 35% 里用「(亮≥150 ∪ 暖 R-B>60) 且 不偏蓝(R-B>-6)」掩膜把**米白厚边**一并吃进来
      （只判亮度会漏掉字面、只判暖会漏掉白边——两个条件是"或"）；
   ③ `binary_closing + fill_holes` 后按面积滤块；
   ④ **清字缝暗紫**：`(R-B<20) & (lum<135)` 的像素从 alpha 里减掉（MaxFilter(3) 膨胀 + blur1.2 后相减），
      否则字缝夹的墙色贴到哪脏到哪；
   ⑤ 羽化 blur0.9 → RGBA；
   ⑥ 程序化柔影：alpha×0.50、色 (20,12,36)、blur7、偏移 (+5,+10)，合成在标题层之下；
   ⑦ 缩放到第 9 页体量（**字面高 89px** @1024×576），按**墨迹（字面）左上角**定位，**最后贴**。

### 体量与定位标定（1024×576 全页）

- 第 9 页定稿墨迹（字面）**337×89**，位于 (72,70)-(408,158)。
- 第 10 页 v12：字面左上贴 (50,36)，右界 <395（避开横梁/木架）。
- **全册统一：字面高 89px**；其余页按各自版面允许微调 ±6px，但**同一页内不混两款**。

### 贴标题三条硬规矩（不变）

① **最后贴**——在全页暗角/颗粒之后（否则被压暗 ~9%，与别页面色对不上）；
② **墨迹不许压在木质道具/实景上**（会被读成"长条底板"）；
③ **全册字号与体量统一**（字面高 89）。

### verify_title.py 的定位（不要再用错）

它只验证**代码款兜底**对自身标定的一致性——**不能**证明"和第 9 页同款"。
模型款不需要 verify 脚本：它的来源（模型底图/抠图素材）本身就是金标准。

### 配套

- 抠标题素材：`D:/needs/clay_deck/_extract_p10_title.py`（可抄进 skill `scripts/`）
- 第 9 页定稿：`D:/needs/clay_deck/page09_改法清单_定稿.png`（= v6）
- 第 10 页模型标题素材：`D:/needs/clay_deck/_p10_title_model.png`（RGBA，已清缝）
- 作废记录：第十一轮的代码款金标准（`gold_title.png`/`gold_metrics.json`）只对代码款有效；
  `_DEPRECATED_p9_title_model_baked.png` 是从第 9 页抠的模型标题（没错），错的是拿代码款当正解。

## 三·三十三、**满意款 · 瓷砖排版 + Q版人物 + 深蓝墙**（2026-09-20 凌晨 · 用户拿两张满意图点名："排版和人物以及背景"要学到 skill 里）

> 参考样本：
> ① 课程目录页（6 瓷砖阵）；② 「AI + Excel 数据处理实战」封面。
> 用户口径（2026-10-11 更新判级）：**颜色不重要，重点是排版 / 人物 / 背景**；文字效果 = 模型画在奶白板上的棕色黏土字。
> ⚠️ **人物判级**：用户当面把 `character-anchor-example.png`（丸子头素袍款）判为**二类满意（达标但呆板）**，
> 把 `cover-excel-example.png` / `toc-clay-lettering-example.png`（圆框眼镜 Q 版小孩，**用户自己的成品**）判为**最满意**。
> 但**不设唯一默认款**（人物要"百变、不定死"）。以 `references/character-style.md` 为准。
> 两张错误样张（写实人脸 + 浮字面板）只做 PPT 反面案例素材，**不许模仿**。

### 骨架 D：牌匾标题 + 中央瓷砖阵 + 左右人物（目录页/清单页新形态）

- **标题**：奶白纸黏土横幅（两端下垂卷边）或奶白圆角厚牌匾，**居中悬在画面顶部**；
  字是**模型直接画上去的棕色厚圆黏土字**（延续【三·三十二】"模型款=正解"）。
- **主体**：一张大黏土桌，桌面上摆 **N 张奶白圆角瓷砖**（清单 ≥4 条时 2 列网格；
  ≤3 条时单排或沿用晨会条带）。**每张瓷砖 = 1 个黏土小图标（上）+ 1 个黏土词（下）**——
  这就是【三·十七】"N 条内容 = N 件道具"的瓷砖形态，图标必须与词义匹配。
- **人物**：**Q 版 chibi 黏土小女孩**（大头短身、丸子头/发髻、圆眼镜）+ **奶白小机器人**（天线搭档），
  **完整站在地面、不被画面边缘裁掉**。
  ⚠️ **人物位置灵活，不锁死方位**（2026-09-20 用户点名）：女孩/机器人**左右可互换**、
  可一左一右也可同侧，**按每页构图平衡放**，prompt 里写实际想要的方位即可。
  ⚠️ 与晨会骨架 A 的"人物压右边缘被裁"是**两种都合法**的人物处理，按骨架选：瓷砖阵款=完整可见。
- **道具散布**：桌角/地面少量书本、盆栽、咖啡杯等**语义相关**小件；地面保持干净，不堆碎屑。

### 🚨 新旧并存（不要有了新规则就忘旧的）

【三·三十三】只是清单的**另一种形态**（瓷砖阵），**不替代也不废弃**晨会款条带列点——
「1. 2. 3.」小条目 + `render_label_band` 条带 + `render_crisp_text` 小字（【三·二十一】文字工艺、
第五轮"3 条拆左右→一整列"铁律）**照旧有效**。同一册里两种形态可混用：按每页内容挑——
清单要"图标+短词"用瓷砖阵（D）；要"完整句子/编号要点"用旧条带（A/C）。

### 🚨 骨架选择必须按"页"灵活（2026-09-20 用户第十六轮点名）

**不是每页都一个排版**。用户原话："不是所有的都是这个界面这个排版，灵活，知道吧。也可以是直接坐在，
也可以是没有一二三的。" 判据（按页挑，出图前写进当页脚本注释）：
- **瓷砖阵 D**：条目 = 短词/名词（≤6 字）→ 图标+短词最自然；
- **条带 A/C**：条目 = 完整句子或需要编号的要点；
- **无编号版式**：内容是叙事/比喻/单概念 → 干脆不要 1.2.3.（如"转折点来了"只有一句话）；
- **封面 E**：人物居中坐，完全无清单。
**同一册混用是常态**；判断"这页该用哪副骨架"在 Phase 2（选骨架）就要定，不是出图时顺手。

### 🚨 条带字号全列一致（【三·三十四】2026-09-20 用户点名"前面大后面小"）

`render_label_band` **已修**：旧逻辑每条独立缩字（放不下就 ×0.93 到放下为止）→ 长句变小字。
现在**两遍渲染**：先为每条算"放得下的最大字号"，取**全列最小值**统一渲染 ——
所有条带字面高完全一致。**不许改回逐条缩**；若最短句与最长句长度差 >2 倍导致字号被压得太小，
优先**改文案长短相近**，而不是放开字号限制。

**🚨 长句零溢出（2026-09-20 用户第十七轮打回"内容都丢哪去了"+"字号一致"后实测）**：
字放进胶囊前必须**上机标定**，不许默认 `text_ratio=0.50`：
- 实测（x0=0.045W / x1=0.345W / bar_h=58）：行长 ≤8 字 → 0.50 放得下；
  **9~12 字 → 必须 `text_ratio=0.42`**（0.46 时 12 字句仍溢出 +25px）。
- 标定脚本判据：渲条带后量**文字墨迹右缘 ≤ x1−6**，三条全 ≤0 才算过
  （可复用 `render_label_band` + 逐行亮像素右缘量法）。
- **长句先拆条**（在标点处拆，内容一字不丢），拆完还放不下才降 `text_ratio`；
  **宁可拆条、降字号，绝不许溢出胶囊**（用户对文字溢出零容忍）。

### 骨架 E：封面（牌匾居中 + 人物居中坐 + 道具环绕）

标题牌匾居中顶部；Q版女孩**坐在大桌前用笔记本电脑**（画面正中），小机器人站侧后；
四周沿边环绕道具（书堆/盆栽/图表/日历/喇叭等），全部贴墙落地，不留大片空墙。

### 背景第三层：装饰点（在"颗粒+斑驳"之上，**元素可换可改**）

深色黏土墙除了颗粒斑驳，还要**中景散布小装饰**——星星/云朵/圆点只是**示例**，
**按每页主题换**（如字母积木、纸飞机、回形针、胶带、小音符、六总课的"技能"主题可用小齿轮/拼图），
规则只有三条：**贴墙、密度低、体量小**（≈ 字面高 0.3~0.5 倍），
不进标题区、不压主体。禁雾禁晕不变（haze/fog/mist 仍是禁词）。

### 出图 prompt 可复制模板（骨架 D，改 ALL-CAPS 占位符即可）

```
C4D render, ultra-detailed polymer clay diorama, Q-version cartoon,
deep navy clay wall with fine grain and mottled speckle, small clay stars,
clouds and dots stuck on the wall, soft key light from upper left, heavy contact shadows, matte clay.
TOP CENTER: cream paper-clay ribbon banner with curled ends, title "TITLE"
sculpted as thick rounded brown clay letters ON the banner (text is part of the clay).
CENTER: one large clay table holding N cream rounded clay tiles in 2 columns x 3 rows,
each tile = one small clay icon on top + its brown clay label below:
ITEM1 (ICON1), ITEM2 (ICON2), ITEM3 (ICON3), ITEM4 (ICON4), ITEM5 (ICON5), ITEM6 (ICON6).
The tile grid is the ONLY hero arrangement; floor CLEAN, almost no debris.
CHARACTERS (position flexible — swap sides or stack same side to balance each page):
Keep the EXACT same little kid character as the reference image — identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical 2.5–3-head-length chibi proportion, standing on the floor, COMPLETE FULL BODY visible, NOT cropped;
small cream clay robot with antenna standing nearby.
A few props: stacked books, potted plants, coffee cup. 8k, shallow depth of field.
NO realistic human face, NO floating text boxes, NO translucent panels, NO watermark.
```

- 封面（骨架 E）只改 CENTER 段：`CENTER: the girl SITTING at a big clay desk typing on a laptop, robot standing beside her, props arranged around the edges: ...`
- 负面词**每次必带**：`NO realistic human face, NO floating text boxes, NO translucent panels`——
  这三条就是两张错误样张的病因（写实人脸=机械化、浮字面板=文字不是黏土实体）。
- 颜色按课程主题自由换（用户已明确"颜色不重要"），但**瓷砖必须奶白/米白**（深底上唯一的信息载体）。

### 首测对比出的两条可选加强（想更贴近满意原图时加进 prompt）

- **瓷砖平铺贴桌、不要立式展示架**：模型爱自由发挥成"带腿展示板"，
  要 A 图那种"贴在桌面"就在 CENTER 段加：
  `the tiles lie FLAT on the table top like inlaid slabs, NOT in a standing frame or easel`；
- **字再大一号**：`labels are LARGE bold brown clay letters filling the lower half of each tile`。

---

## 三·三十五 排版样式库（2026-09-20 · 八六 36 页全量归纳 · 防止"整册一个模子"）

> 背景：用户点名批评"出过的就可以不出了/那么刻板那么死板"，本节是对八六 36 页原版
> （`assets/ref-86/`）逐页归纳出的 **20 种版式语汇**。铁律见本节末尾。

### 版式目录（按内容形态选用，prompt 里写清楚结构再出图）

| # | 版式名 | 结构 | 适用内容 |
|---|--------|------|----------|
| 1 | 封面式 | 左上大标题 + 中央巨型主体 + 人物 + 右下信息胶囊 | 封面 |
| 2 | 流程带式 | 居中标题 + 横向编号圆点流程（1→4）+ 底部小胶囊列 | 步骤/时间线 |
| 3 | 对比式 | 居中标题 + 左右两大板（中缝 VS）+ 底部结论条 | before/after、优劣对照 |
| 4 | 三块横排+链条 | 三大块横排 + 底部箭头链（A→B→C） | 概念分工+协作关系 |
| 5 | 框图连线式 | 中央节点 → 箭头分叉到多个小框 | 架构/组合关系 |
| 6 | 左列表右场景 | 左侧条带列（4-6条）+ 右侧大场景 | 条目 ≤6 且场景感强 |
| 7 | 判断卡阵 | 2x2 或 1x4 卡片，每卡带 ✓/✗ 标签 + 底部结论 | 分类判断、能不能做 |
| 8 | 瓷砖阵 | 3x2 瓷砖格子（图标+词）+ 人物一侧 | 目录/总览 |
| 9 | 档案柜式 | 打开的柜子分层露出文件 + 标注小条 | 组成结构、文件夹剖析 |
| 10 | 实验对照式 | 两块展示板并排 + 底部双徽章结论 | 实验对比 |
| 11 | 文档特写式 | 一张大纸特写居中 + 右侧编号要点列 | 单文档拆解（SKILL.md 等） |
| 12 | 渐进披露式 | 左列表 + 右柜子分层点亮 | 分层加载/按需展开 |
| 13 | 箭头递进式 | 左列表 → 中央大箭头 → 右成品（v0→v1） | 改造前后 |
| 14 | 路线图式 | 蜿蜒小路连多个站点 + 左上标题 | 渠道/来源/路径 |
| 15 | 四问横排卡 | 1-4 编号卡横排 + 警示闸门场景 + 底部警示条 | 检查清单（≤4条） |
| 16 | 实验架式 | 架子上摆多个样品 + 人物讲解 | 多案例陈列 |
| 17 | 对照实验式 | 顶部信息条 + 左右结果对照 + 底部徽章 | A/B 测试结果 |
| 18 | 三步分页式 | "第一步/第二步/第三步"各占一页，中央巨主体 + 侧条带 | 大步骤拆页 |
| 19 | 清单勾选式 | 中央大清单纸（行=图标+字+✓）+ 人物抱成品 | 完成标准、验收单 |
| 20 | 收尾升华式 | 左上标题 + 左小结列 + 右大工具箱发光 + 底部徽章 | 结尾/总结 |

### 换版式四条铁律

1. **相邻两页不许同版式**；全册同一版式 **≤3 页**（条带系"左列表右场景"最容易超）。
2. **先看内容形态再选版式**：流程→#2/#4，对比→#3/#10/#13，条目→#6/#7/#8/#15，
   结构→#9/#12，单文档→#11，路径→#14，清单→#19，总结→#20。**不是"上一页怎么排这页就怎么排"。**
3. **每页人物位置/姿态必须换**（左/右/中央、站/坐/跪/探身），机器人同理。
4. 底部结论条（一行胶囊总结）是八六高频件，**多数页都该有**，别只在条带页用。

### 落地方式

- 出整页底图时：把选定版式的结构写进 prompt（TOP/CENTER/BOTTOM 分段写），
  版式表格里那行"结构"描述直接翻译成英文段落。
- 只改版式不出图时：用 `scripts/clay_props.py` + `clay_band.py` 在现有底图上重排条带，
  但**条带系换版式必须重出底图**（骨架长在底图上）。
- 本册排版自检：装册前逐页登记版式编号，违反铁律 1/2 就重排。


## 【三·三十六】⛔ 已废除：禁止对成页做全册统一调色（2026-09-20 05:00 用户叫停）

第 24 轮曾尝试把 15 页全部"校到八六量化基线"（亮度/饱和/紫相/四角），**结果全册偏黄、
四角压出浓重暗角（"镜头感"），用户要求全部回退**。教训：

- **出好的黏土成页一概不再做全局调色**——页间色差只接受在**出图阶段**控制
  （prompt 里写死同一墙色描述，如 `deep indigo-violet speckled wall`）；
- 量化基线（亮≈83 / 四角≈31 / 饱和 0.58-0.60）只用于**验收/诊断**，不用于后处理目标；
- 用户反馈整套"不像一套"时，处理顺序：先看是不是出图 prompt 没写死墙色 →
  重出个别偏差大的页 → **永远不动已验收的成页像素**。
