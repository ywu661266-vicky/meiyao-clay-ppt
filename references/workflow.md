# 工作流详解（三步确认法）

核心目的：**用最少的出图额度，换用户最满意的结果。** 每次出图前先想清楚"用户要看到什么才能判断对错"。

---

## Phase 0 · 收集素材

一次问清，不要挤牙膏：

1. **内容**：主题 + 每页要讲什么。
   - 有文件就先读文件（`.md` / `.docx` / `.pptx` / `.html`），从里面提取真实内容，不编造。
   - 用户只给关键词时，先列出拟定的页目录（如：封面 / 目录 / 6 个场景 / 总结），**让用户确认页数和顺序**，再动图。
2. **人物**：见 `references/character-style.md`（**人物"百变、不定死"**：脸/画风统一，衣服姿态场景可换）。画风基准 = 圆框眼镜 + 深色发 + 约 2.5–3 头身 Q 版小孩，或让用户用一句话说清想要的形象。
3. **配色**：默认深蓝；一句"要换配色吗"即可，别展开长篇选项。

---

## Phase 1 · 角色锚点（1 张）

- 生成 1 张 `1024x1024`，**完整全身**站立（头顶到鞋子全部在画面内，上下都留白），中性灰底。
  - ⚠️ 别只出半身：后续页面都要求全身，模型会自己"补"下半身，服装和比例就跑偏。**锚点直接给全身，后面才稳。**
  - prompt 写死 `COMPLETE FULL-BODY figure, ENTIRE body from the top of the hair down to the shoes completely visible, head to toe, NOT cropped`，并给比例 `about 2.5–3 head-lengths`（Q 版小孩）。
- **当场给用户看**，并逐条列出"我核对的特征"（发型/发饰/眼镜/服装/**是否全身完整**），让他一眼确认。
- 不合格 → 按反馈改特征重出 1 张；**永远单张迭代，不批量。**

**话术模板：**
> 这版人物特征对不对？我核对：深色发顶髻 + 粉发带 ✅ 圆框眼镜 ✅ 约 2.5–3 头身 Q 版小孩 ✅ 全身完整（头到脚没裁） ✅。对的话我出封面，不对你说哪要改，我重出。

---

## Phase 2 · 封面（1 张背景板 + 1 张合成成品）

1. 生成 1 张 `1024x576` **背景板**（场景 + 完整全身人物，标题位留白）。
2. 用 `scripts/clay_text.py` 捏封面上的字件，再用 `scripts/compose_page.py` 贴上去 → **成品封面**。
3. **构图自检**：字要有厚度、有投影、和人物道具**同一光照方向**；像"扁平贴字"或"塑料浮雕"就回 `clay_text.py` 调参（`depth` / `shadow` / `stroke_ratio`）重贴，不要给用户看。
4. 给用户看时明确说：**"这一张代表整页效果：场景 + 人物 + 黏土字。"**
5. 用户确认 OK → 进入批量；不 OK → 改，仍单张迭代。

**为什么封面必须是"成品"：** 用户判断"对不对"靠的是**完整一页的观感**，光给人物看不出效果。而**字是不是黏土做的、有没有和画面贴成一体**，恰恰是整套图成败的分水岭。

**字件怎么捏（封面常用组合）：**
| 位置 | 件类型 | 说明 |
|------|--------|------|
| 主标题 | `text` | `cap` 取画面宽度的 7–9%，米白，两行时第二行可着色强调 |
| 副标题 | `badge` | 半透明感的胶囊，`cap` 约主标题 1/3 |
| 信息标签（班次/讲师） | `badge` | 橙/绿等对比色，`extra_left` 留出小头像位 |
| 底部标语 | `text` | 与主标题同色系，`cap` 约主标题 55% |

---

## Phase 3.0 · 【强制】出图前逐条抄「豆包八条」（2026-09-19 用户第三次点名）

> 用户原话：「**要遵守豆包的逐字改法，那 8 条。你一定要每次都知道这个。**」
> 病理是"做着做着就忘了"——所以**不靠记忆，靠复制**：下面 8 段英文**必须原样出现在每一张内页 prompt 里**，
> 不是"知道就行"。出图前把 8 段贴完，再开始写场景；少一段就重来。

### 🚨 出图前四查（2026-09-20 用户点名追加，每张图按下单前过一遍，一条不过就不许下单）

1. **人物锚点带了吗？** —— 凡是画面里有人的底图，**必须把已定稿的人物锚点图作为 `image1` 传入**
   （当前锚点：`D:/needs/clay_deck/_anchor_girl_p10.png`，丸子头+米白发带+圆眼镜+白外套米裙）。
   只靠文字描述模型会自由发挥年龄/发型/发色 —— 第 2 页 v1 没传锚点，人物被画成**灰发老人**，整页报废。
   prompt 里同时抄回脸部锁定句（`Keep EXACTLY the same little kid character from the reference image: identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical clay-material look and identical 2.5–3-head-length chibi proportion. Only the clothing, the pose and the surrounding scene may change.`）。
2. **留白写死了吗？** —— 要放文字的区域必须在 prompt 里写死 EMPTY 句（LEFT THIRD … reserved for text），
   且**不能多留**：留白区只占该放文字的面积，多留就是"大面积空白"。
3. **满版密度够吗？** —— 对照【三·六 满版密度铁律】：四角、底边都有内容（道具贴边、被裁切），
   交付前跑 6×3 网格纹理自检，空旷格 >3 就回炉；左列条带下方空着 → 走【三·二十二】散道具补。
4. **几何与全册统一吗？** —— 条带几何照抄定稿页：`x0=0.045W, x1=0.345W, bar_h=58, gap=14,
   text_ratio=0.50`（第 10 页 v12 标定值），**不许每页现调**；标题字号=模型款字面高 89。

**A. 语义配对（比八条更靠前，用户先看这个）**

**N 条内容 = N 件道具**，每件道具必须能**单独读出**对应那条的意思。
- 自检问句：把这条道具单独截出来给人看，他能不能说出这是哪一条？说不出 → 换道具。
- 反例（实际被用户打回）：第 10 页「从改到造：复制一份 / 改个名字 / 调成我的」配了
  **女孩剪皮革 + 书 + 裁切机** —— 三件道具**跟哪一条都对不上**，纯属"工厂里随便摆的"。
  用户原话：「你觉得这个女孩配的这个图是合适的吗？」
- 正例（同一页改法）：**复印机吐纸 = 复制一份｜木名牌 + 刻字笔 = 改个名字｜印章 + 印泥 = 调成我的**。
- 拿不准就先写「道具 → 对应条目」两列表，对不上就删掉重想，再看下面八条。

**B. 八条逐字 block（照抄进 prompt）**

| # | 中文要点 | 必须粘进 prompt 的英文原文 |
|---|---|---|
| 1 | 道具不许关进框/卡片/格子 | `Every prop lies FREELY on the tabletop and the floor — tilted, overlapping, partly hidden behind one another, unevenly spaced. There is NO card, NO panel, NO frame, NO box, NO grid holding any prop.` |
| 2 | 人物坐/跪地，不上台座 | `She is SITTING / KNEELING directly ON THE FLOOR. Not on any pedestal, platform, step, disc or podium. Heavy contact shadow puddling right beneath her. Her body is partly tucked behind the table. NO pedestals or platforms anywhere.` |
| 3 | 三层纵深（近/中/远） | `Strong three-plane depth: FOREGROUND — large props at the bottom edge, partly CROPPED by the frame; MIDGROUND — the main scene shifted to the RIGHT, off-centre; BACKGROUND — a clean crisp wall with shelves / hanging tools at the top edge, clearly readable and sharp, NOT blurred, NOT fogged.` |
| 4 | 硬主光左上 + 互投 + 闭塞阴影 | `LIGHTING — the single most important part: ONE strong key light from the UPPER LEFT. Every object casts SOFT LARGE SHADOWS onto each other and onto the floor. Strong ambient occlusion in every crevice, corner and contact point. Clear light-to-dark falloff across the scene. NOT flat front lighting, NOT even studio lighting.` |
| 5 | 背景有颗粒 + 斑驳（**但绝不许雾**） | `The wall carries subtle noise grain and uneven tonal mottling — NEVER a flat solid fill, and NEVER hazy.` |
| 5b | **空气必须干净（用户第六轮点名）** | `COLOR AND AIR — the whole scene is DEEPLY SATURATED rich violet like #4A2E7A / #5B3A93, NOT pale, NOT grey-lavender, NOT washed out. The air is CRYSTAL CLEAR: absolutely NO fog, NO mist, NO haze, NO smoke, NO dust, NO atmospheric bloom, NO light beam, NO glow wash anywhere. Everything is in sharp focus with strong local contrast.` |
| 6 | 标题黄黏土字 + 奶油描边，**无长条底座** | `The title is sculpted from thick 3D raised clay letters in WARM YELLOW, each letter carrying a thin CREAM WHITE outline. Do NOT put any bar, plank, slab or strip underneath the title.` |
| 7 | 装饰随机撒不排齐 | `Small hearts, leaves, pebbles and a star are sprinkled RANDOMLY here and there — uneven and asymmetric, never in a neat row.` |
| 8 | 冷暖对比（木色 + 暖橙黄） | `NATURAL WOOD TAN props (wooden workbench, wooden crate, wood tool handles) plus warm orange-yellow accents, for real warm-cool contrast against the purple.` |

**C. 布局骨架（第 0 步，先于场景）**

先翻 `assets/ref-86/` 选骨架，**不许默认左列+右景**。条数决定骨架：

| 本页内容条数 | 骨架 | 依据 |
|---|---|---|
| **1–3 条** | **一整列，不许拆左右**；条带可略放大、纵向居中，靠**场景丰富度**补画面 | 用户原话：「它总共就 3 条，你还非要分成左右，干啥呀？这样会不会显得内容太少？」→ 3 条硬拆 = 每边更少 |
| 4–5 条 | 左列一整列 + 右侧自由场景（八六 p10 / p15 / p16） | 八六 36 页里"左列+右景"只有 p10/p29，其余多为一列或左右双列 |
| 6 条以上 | 居中大标题 + 左右双列（八六 p30/p26/p21） | 条数够才撑得起两边 |

**D. 出图纪律：一次只出「当前这一页」的 1 张（用户第六轮点名）**

> 用户原话：「**你下次不要一下子出那么多张图，消耗我太多积分了。你就改这第 10 页的话，
> 那你就出这第 10 页的这个图。**」

- 单张 5~10 积分，一次 3 张 = 15~30 积分；而"3 选 1"的收益远小于"**先把 prompt 写对**"。
  **默认 1 张**；改单页就只出这一页。
- 确实需要多张候选时，**先说明并得到用户同意**再出。
- 出图前自检（比出 3 张便宜得多）：
  ① **主体是不是"唯一的一个大物件"**？② 空气词里有没有 haze / fog / mist？（有就删）
  ③ 左/右侧留白写死了没有？④ 豆包八条（含 5b 空气）逐条粘完了没有？
  ⑤ **有没有写成 `(1)…(2)…(3)…` 三条枚举**？（有就改成 `THE ONE HERO OBJECT … three parts:
     (a) its LEFT side … (b) its FRONT … (c) its RIGHT side …`，否则模型会摆成三件并排展品）
  ⑥ 有没有正面写死"少"：`ONLY the …` / `the floor is CLEAN and nearly EMPTY — NO piles of
     junk, NO scattered flowers, NO debris`？**"适配"≠"堆道具"（【三·三十·3】）**

- **成页后机检（不出图、0 积分，每版必跑）**：
  ① **条带文字逐字块扫描**（【三·三十一】）：所有字块中心 y 相差 ≤ 1px —— 防"一"字上浮；
  ② **徽章数字留白**：绿饼内 ink 的上/下、左/右留白各差 ≤ 2px，ink 高/饼径 0.44~0.50（【三·三十·2】）。
  ③ **标题走【三·三十二】模型款**：首选出底图时让模型把标题画上；或从模型画好的底图里
     抠 RGBA 素材贴上（脚本 `D:/needs/clay_deck/_extract_p10_title.py`，字面高统一 89）。
     `clay_text.render_title_clay()` **只许兜底/占位**，交付前必须换模型款；
  ④ **标题最后贴**（在全页暗角/颗粒之后；贴前面会被压暗 ~9%）；
     **按墨迹对齐，墨迹不许压在背景的木质道具/实景上**（否则被读成"长条底板"）；
     且**全册字号与墨迹位置统一**（两页才真的同款）；
  ⑤ **换机器 / 别人第一次用 skill** → 先跑 `python scripts/verify_portable.py`（砍掉系统字体再渲一遍，
     证明内置字体够用；当前 PASS）；

---

## Phase 3 · 批量内页（出的是"背景板"）

页数结构（按需裁剪）：

| 页型 | 数量 | 背景板内容 | 文字怎么来 |
|------|------|----------|-----------|
| 封面 | 1 | 完整全身人物 + 场景（标题位留白） | `clay_text.py` 贴：主标题 + 副标题胶囊 + 信息标签 |
| 目录 | 1 | 完整全身人物 + 场景 + 卡片格（卡面留空） | `clay_text.py` 贴：标题字 + 每个卡片一个 `badge` 标签 |
| 内容页 | N | 完整全身人物 + 场景 + **文字区整块留白** | `clay_text.py` 贴：标题字 + 3–5 张 `card` 承载正文 |
| 总结 | 1 | 完整全身人物 + 场景 | `clay_text.py` 贴：标题字 + 要点卡片 |

- 全部 `size: "1024x576"`，**都必须带 Phase 1 的全身锚点图作 `image1`**。
- 每页 prompt 只改两样：**场景块、留白侧**。
- **每页场景块从 `references/style-library.md`【内页款式库 IN1–IN14】任选**，相邻页不重复；一致性靠参考图，多样性靠换场景块。
- **⚠️ 版式也要换，不只是场景（2026-09-18 用户点名"两页差不多"后补）**：正文区骨架从 `style-library.md`【**内页版式库 LP1–LP10**】里挑，**相邻页不得复用同一版式**，一套 ≥13 页至少用 **6 个不同版式**。只换道具、骨架不变 = 用户一眼看穿"每页一样"。挑版式 + 挑场景块都要**贴该页语义**（讲踩坑→LP2 VS / IN4 裂开；讲转折→LP3 中心大匾 / IN6 灯泡；讲流程→LP6 编号流程 / IN10 步道）。
- prompt 里**用方位词 + 占比把版式写死**（`TOP:` / `CENTRE OF THE FRAME` / `LEFT COLUMN, about 46%` / `BELOW the plaque: four tiles in one row` / `RIGHT SIDE:`）。只写"infographic"模型会自己滑回默认骨架。
- **背景板一个字都不写**（B 路），文字区整块留白并在 prompt 里写死：
  `The LEFT 55% is a COMPLETELY EMPTY wall — NO text, NO cards, NO icons; reserved blank space for text added later.` + `Absolutely NO text, NO letters, NO numbers anywhere in the image.`
- 留白侧要和文字件摆放一致：`left` → 留左 55%（卡片贴左边）；`right` → 留右 45%。
- 想省事可走 A 路：让模型顺带烘一个 **≤8 字** 的黏土标题，正文仍然自己贴。**要反复改字的页一律走 B 路。**

**（2026-09-17 实测补充）纯短标签的「信息图页」直接整图烘字，比贴字更自然。**
当一页的**全部文字都是短标签**（标题 + 词 + 一句话说明，例如 Prompt / Skill / Agent 这类概念对照页、四层结构的信息图），把**所有文字都逐条写进出图 prompt、让模型一次烘进图**，成品明显优于「背景板 + `clay_text.py` 贴字」：字和场景同一次捏出来，光照/材质天然一致，不会出现「扁平贴纸浮在画面上」的违和感。对照样本：八六老师的参考海报（顶部标题横幅 + 三列概念 + 概念定义条 + 流程名牌，**所有**文字都烘进图）按此法一次到位、中文零错字。
- 判定口径：整页文字**全是短句/词**（无成段正文）→ 走 A 路整图烘字；出现**成段正文**（一句话以上、要反复改）→ 仍走 B 路贴 `card`。
- prompt 写法：把每处文字**逐条列清位置 + 内容**，并写死 `Every piece of text is sculpted raised clay lettering — thick, plump, rounded, with clearly visible thickness and real drop shadows, same material and lighting as the scene. NOT flat printed text. Every Chinese character must be perfectly formed, correctly spelled and clearly legible.`
- 仍要跑 Phase 3.5 去水印；出图后逐字核对有无错字，错字就重出（不要试图后期改字）。

**⚠️ `render_clay_card` 只给「成段正文」用（2026-09-18 实测）**：它是**扁平**奶油圆角块 + 平贴字。一页全是短标签却用它，成品会一眼像"PPT 上贴了张卡片"，和整图烘字的页摆在一起格格不入。**短标签页一律整图烘字，不要贴 `card`。**

### 八六式「信息图内容页」整图烘字版式模板（可直接套，实测中文零错字）

| 区 | 内容 |
|----|------|
| 顶部 | 靛紫色**缎带横幅**（两端剪口）；标题 ≤6 字，厚圆奶油黏土浮雕；两端缀橙星／红叶／绿叶 |
| 左侧 ~46% | **3 条等宽奶油胶囊卡**竖排等距：紫色圆角方**徽章（内嵌奶油图标）**＋右侧两段字——彩色关键词（橙/紫/绿）＋ 深藏青说明句（**≤16 字**） |
| 右侧 ~54% | **立体黏土场景**：紫色拱门（门板奶油盾徽）＋门前 3 块步道石与粗箭头＋人物**全身**立于门侧（手举小印章/道具）＋拱顶小机器人＋门口工具箱/扳手/齿轮/书 |

prompt 写法：
- 三行文字**逐条列清位置 + 内容**（`- TOP capsule — badge icon: … Text: "…" in THICK RAISED ORANGE-CLAY LETTERS, followed by "…" in THICK RAISED DARK-NAVY-CLAY LETTERS`）；
- 写死材质句：`CRITICAL: every piece of text in this slide is sculpted raised clay lettering — thick, plump, rounded, clearly visible thickness, soft bevels and real drop shadows, exactly the same material and lighting as the clay scene. NOT flat printed text, NOT flat stickers.`；
- 背景写 `deep saturated violet-purple gradient background with a soft darker vignette`（**有暗角才立得住**，平渐变会让整页发飘）；
- 仍要抄回「人物完整全身」+「脸部锁定句（见 `character-style.md`）」，并带锚点图作 `image1`。

**为什么背景板不出正文（结论）**：中文笔画密度高，图片模型在**整页**里写一句话说明就必错字乱码（实测"抓技技能"），而且改一个字就要重出整张图。文字单独做件，才能"一页写满内容 + 想改就改"。

---

## Phase 3.5 · 去水印（硬性，每张都跑）

```bash
python scripts/remove_watermark.py <出图目录>
```

出图平台会在**每一张**图右下角自动盖 `AI生成` / `WORKBUDDY` 白色浮标，**prompt 关不掉**（写 `No watermark` 也没用，它不是模型画的）。
按"短边等比"公式定位水印框，再用 `cv2.inpaint(TELEA)` 修补。**带水印的图不许交付、不许进 PPTX。**

---

## Phase 4 · 贴黏土字 → 合成成品页 → 装进 PPTX

**第一步：把黏土件贴到背景板上（新流程的核心）**

1. 写 `pages.json`：
   ```json
   {
     "pages": [
       {
         "bg": "bg/page07_clean.png",
         "out": "out/page07.png",
         "elements": [
           { "type": "text",  "text": "我踩的坑", "cap": 54, "x": 120, "y": 40, "color": "cream" },
           { "type": "card",  "head": "只抄了描述文字",
             "body": "人物每页都变样，一个啾啾变成两个丸子头，脸也不一样",
             "width": 524, "x": 40, "y": 96, "accent": "orange" },
           { "type": "badge", "text": "3 小时实操课", "cap": 32, "x": 70, "y": 470, "color": "orange" }
         ]
       }
     ]
   }
   ```
2. 运行：
   ```bash
   python scripts/compose_page.py --config pages.json
   ```
   → 输出成品页 PNG（背景 + 黏土字一体）。**改文案只改这个 JSON 重跑，不花积分。**

**第二步：装进 PPTX**

1. 写 `slides.json`，每页指向**成品页 PNG**，`text_mode:"baked"`：
   ```json
   {
     "image": "out/page07.png",
     "text_mode": "baked",
     "notes": "讲师备注"
   }
   ```
2. 运行：
   ```bash
   python scripts/build_pptx.py --config slides.json --out "主题_黏土风.pptx"
   ```
3. 校验：页数、16:9 尺寸、**右下角无水印**（Phase 3.5 已跑）、**字和画面是一体的**。

> `text_mode`：`baked` = 页面已经是成品图，脚本不再叠任何字（**默认做法**）；
> `overlay` = 脚本用真字体叠字（**不推荐**，只在个别页明确要"可编辑扁平字"时用，`layout` 可选 `cards`/`steps`/`bullets`）。
> ⚠️ 用 `baked` 的页**不要**再写 `title`，否则会叠出两层字。

---

## Phase 4.5 · 成品页自检（交付前）

`compose_page.py` 的输出**本身就是成品页 PNG**，直接打开逐页看三件事：

1. 黏土字 / 卡片有没有**压到人物**、有没有**出画**；
2. **留白够不够**（字件挤在边角 = 背景板留白没留够，回 Phase 3 重出该页背景）；
3. **光照是否一致**——字的投影方向、柔硬程度要和人物的投影对得上，对不上就调 `clay_text.py` 的 `shadow` / `depth` 再贴。
4. **满版密度**（整图烘字的页必查）：切 6×3 网格算每格 RGB 标准差，**最低格 ≥45、平均 ≥55、空旷格（＜40）= 0**。不达标就是用户说的"**边上是空的**"，回 Phase 3 按 `style-library.md`【三·六 满版密度铁律】重出，**不许交付**（自检脚本见该节）。

> 只有在用 `overlay`（扁平字）时才需要 `python scripts/render_preview.py --config slides.json --out preview_dir`。
> 本机 PowerPoint 的 COM 自动化常被系统拒绝（报"服务器运行失败"），`scripts/export_png.py` 不一定可用，**以 PNG 为准**。
> 没过关 → 改 `pages.json` 的坐标/文案重跑，别直接交付。

---

## Phase 4.6 · 色调校正（整图烘字的页必做）

图片模型很难靠 prompt 把色调一次性调对（实测改了 6 版，饱和度仍卡在 0.38，参考是 0.615）。
**出图后跑一次脚本校正，比反复重出图便宜得多、也准得多。**

```bash
python scripts/tone_match.py <目录或图片>        # 输出 *_tone.png
python scripts/tone_match.py <目录> --analyze    # 只量化不写文件

# 2026-09-19 二次修正后的「标准一套」（治"单调发冷 / 塑料白 / 发闷"三件套）：
python scripts/tone_match.py <图> \
    --hue-ramp 1.0 \                       # ★核心：三段紫阶 253/277/296（治"整幅只有一段蓝紫"）
    --hi-rolloff 0.28 --hi-start 0.86 \    # 高光滚降，压掉纯白（治"塑料感"）
    --sat 1.50 --gamma 1.30 \              # 提饱和 + 提亮中间调（治"发闷发暗"）
    --contrast 1.06 --warm-r 1.05 --cool-b 0.95 --vignette 0.20

# 明度分布和参考不同时，按自己图的紫主色明度重新标定紫阶锚点：
#   --ramp-v-lo 0.29 --ramp-v-mid 0.44 --ramp-v-hi 0.58
# （旧的 --hue-lock 单一吸附仅在"只偏一点点"时用；整幅一种紫时用 --hue-ramp）
```

⚠️ **紫阶/色相校正必须在最后一步做**：暖化（R↑B↓）会把紫重新拽向洋红 15~20°，放前面会被抵消。脚本已固定顺序。

对齐基线（八六老师课件页实测）：

| 饱和度 | 平均亮度 | 四角中位亮度 | 明暗倍率 | 亮部 B−R | 高饱和暖色锚点 |
|---|---|---|---|---|---|
| ≈ 0.60 | ≈ 83 | ≈ 31 | ≈ 40x | ≈ −86 | ≥ 7% |

**另一组更硬的基线（紫阶 / 高光 / 蓝紫配比）**：

| 指标 | 参考基线 | 说明 |
|---|---|---|
| **紫阶跨度** | **≥ 35°**（实测 41~58°） | 主色里紫族的 max(H)−min(H)。**<20° 就是"整幅只有一段紫" → 单调发平**（【三·十】） |
| 三档落点 | 约 253° / 277° / 295° | 深靛底 / 紫罗兰机身 / 藕荷亮面，按明度递增 |
| **蓝族占比 H∈[200,250)** | ≈ 21%（**≤ 40%**） | 超 40% = 机器被画成钴蓝，一定丑 |
| **紫罗兰占比 H∈[250,300)** | ≈ 32% | 应为主力 |
| 洋红紫占比 H∈[300,350) | ≈ 6%（**≤ 15%**） | 超 15% = 偏粉、廉价 |
| 暖 / 冷紫 比 | ≈ 0.59（**≥ 0.5**） | < 0.5 画面偏冷 |
| 背景暴露率 | ≈ 27%（**≤ 35%**） | > 35% = 机器之间空隙大、不够满 |
| 纯白 V>0.95 占比 | **≤ 1%** | 超过 3% 就是"塑料感"（【三·十一】） |
| 明度分位 | p10 0.196 / p50 0.416 / p90 0.886 | 三段都要贴，光提平均亮度没用 |
| 纹理空格(6×3) | **0 格 < 30** | 有平区就是"空"（【三·三】） |

实测收益：饱和 0.385→0.545、亮度 88.3→81.3、四角 44.4→37.2、亮部 B−R −57→−87。
第 8 页二次修正：蓝族 52.1%→0.0%、紫罗兰 9.2%→56.7%、暖色 31.4%→39.0%（= `--hue-ramp 1.0` 的收益）。
⚠️ 参数别拉满（饱和度 >1.5x 会又艳又脏），「适中」是铁律。
✅ 但**色相类校正（`--hue-ramp` / `--hue-lock`）可以给到 1.0** —— 那是"纠偏"不是"加料"，不违背适中原则。
🆕 若模型"多给一个"道具，用 `scripts/patch_region.py` 局部补掉（【三·十三】），别重出图。
🆕 觉得"丑"但说不出哪不对 → 先跑 k-means 主色诊断（【三·十四】），**不要凭感觉改 prompt 重出图**。

---

## Phase 5 · 交付

- `present_files` 交付 `.pptx` + 封面/角色预览图。
- 附一句：页数 / 主题 / 配色 / **文字全部是黏土件贴上去的**（改文案只改 `pages.json`，不用重新出图）。

---

## 常见翻车与对策

| 现象 | 原因 | 对策 |
|------|------|------|
| 一整套图全废 | 没先确认人物就批量 | 严格执行 Phase 1 单张确认 |
| 人物每页长得不一样 | 只靠文字描述，模型自由发挥 | **把角色锚点图作为 `image1` 传入做 image-to-image**；实测只抄文字会出现"锚点 1 个啾啾 → 封面 2 个丸子头" |
| 每张图右下角都有 `AI生成`/`WORKBUDDY` | 出图平台自动盖的浮标，prompt 关不掉 | 出图后跑 `python scripts/remove_watermark.py <目录>` |
| **明明是黏土风却很"假"** | **文字是扁平字体叠上去的**（没厚度、没投影、光照不对） | 文字一律用 `clay_text.py` 捏成**黏土件**再贴（`text`/`card`/`badge`），别用扁平文本框 |
| 字和图"不在一个世界" | 投影方向 / 柔硬程度和人物对不上 | 调 `clay_text.py` 的 `shadow`（用画面里最深的那个色系）、`depth`（字高的 4–9%）、投影模糊半径 |
| 黏土字发灰、像水泥浮雕 | 侧壁太厚、太暗 | `depth` 降到字高的 4–5%，侧壁色往**暖**走不要往灰走（脚本内部已做暖化）；投影给足 |
| 汉字笔画糊成一坨 | 描边加肥过头 + 字距太紧 | `stroke_ratio` 保持 0.010–0.016，`letter_gap` 0.04–0.07；字小就别加描边 |
| 同一页出现两层标题 | 背景板烘了字，贴字时又贴了一行 | 走 B 路（背景板不出字）；或 `slides.json` 该页**不写 `title`** |
| 用户觉得"看不到效果" | 只给了无字背景板 | 一定要给**合成后的成品页**（场景 + 人物 + 黏土字） |
| 中文出现错字/乱码 | 让图片模型在**整页**里画了正文或小标签 | 背景板 prompt 写死 `Absolutely NO text, NO letters, NO numbers anywhere in the image`；文字全部走 `clay_text.py` |
| 用户说"**边上是空的**／不如参考图耐看" | 构图**没满版**：道具孤立漂浮、中央一块大匾、底部是几块分离小瓦 | 按 `style-library.md`【三·六 满版密度铁律】：prompt 加 FULL-BLEED 句 + 主场景"特写且被左右边缘裁切" + 底部条写 full-width + 四角填角加暗角；**用 6×3 网格纹理自检到空旷格 = 0 再交付** |
| 每页"看着都差不多" | 只换了道具（IN），没换正文骨架（LP） | 按 `style-library.md`【三·五 版式库 LP1–LP10】排版式分配表，相邻页不复用同一版式 |
| **用户说"丑"** | ①道具跟文字没关系（抄了别的页的道具）②色调发灰 ③主色不成体系 | 按 `style-library.md`【三·七 元素语义匹配】逐道具问"删掉它这页的话会变少吗"，不会就换成对应文字的道具；再按【三·八 色调铁律】跑 `tone_match.py` 校正 |
| 画面"发灰、没精神" | prompt 抠色调的边际收益极低（实测 6 版仍差 0.23 饱和度） | 出图后跑 `python scripts/tone_match.py <目录>`，对齐基线表（饱和 ≈0.60 / 亮 ≈83 / 角 ≈31 / 亮部 B−R ≈−86） |
| 画面"很空"但元素不少 | 紫色只做出了一层（全落在 232–245 的蓝区），缺亮面藕荷色 | 按【三·十】给**三个数值锚点**做三段紫阶（253/277/295）+ 道具用两种紫；**别写"三层渐变"这种含糊说法，一定带 RGB** |
| 暗角处出现大片死黑平区 | 把"暗角"理解成"把角落涂黑" | 明确 `vignette darkens but does NOT blacken` + `props extend into all four corners, simply lying in shadow` |
| **内页只有标题、写不进内容** | 想靠图片模型"画"出成段文字 | 正文做成 `card` 黏土件贴上去（3–5 张/页），**字数不受限、改字不用重出图** |
| **整页短标签却贴了 `card`，成品像"PPT 贴了张卡片"** | `render_clay_card` 天生扁平，只适合成段正文 | 短标签页走**整图烘字**（见 Phase 3 的「八六式信息图版式模板」）；只有成段正文 / 要反复改字才用 `card` |
| 用户连着几轮说"**丑 / 没高级感**"却说不出原因 | **紫只做了一种** —— 不管偏洋红(H≈303)还是偏蓝(H≈245)，整幅只有一段紫读作"平、冷、廉价"。参考图的紫是**按明度拉开的 253/277/295 三段**（【三·十】） | prompt 给**三个 RGB 数值锚点**（见【三·十】照抄段）；兜底 `tone_match.py --hue-ramp 1.0` |
| **"照上一版的结论修了，反而更难看"** | 上一版结论只对了一半（"改成统一靛紫"→ 紫阶跨度掉到 5°，单调发冷）。**先诊断再改** | 跑 k-means 三主色 + 紫阶跨度（【三·十四】），确认"蓝族/紫罗兰/洋红紫"三个桶的占比，别只看单一色相 |
| 画面"**塑料感 / 廉价**" | 奶油色被打成纯白（V>0.95 占 **5.7%**，参考只 0.82%，差 7 倍） | prompt 加 `HIGHLIGHT RULE: highlights SOFT and CREAMY, brightest near rgb(222,165,112), nothing is #FFFFFF`；兜底 `--hi-rolloff 0.28`（【三·十一】） |
| 画面整体**灰蒙蒙**（饱和 < 0.45） | prompt 用了 `pale mauve / lilac` 这类**没给 RGB 的颜色词**，模型理解成"褪色的灰藕"（实测 0.366） | 颜色词一律带数值；兜底 `--sat 1.5~1.75` |
| 像"**摆拍的小场景**"而不是"大片" | 物件没冲出画框，四周留了一圈背景紫 | prompt 写 `AGGRESSIVE CLOSE-UP: the left machine IS CUT OFF by the LEFT frame edge and the right machine by the RIGHT edge. No empty background strip down either side.`（【三·十二】） |
| **机器各管各的、中间有竖向空隙** | 只写了"高、密"，没写"机器之间要连起来" | prompt 加 `joined to one another by thick pipes, elbows, valves and conduits so the whole middle band reads as ONE continuous connected machine. NO vertical strip of empty background between the stations.`（【三·十二】） |
| **上方一大片空、机器又矮又光板** | 没给机器设「高度预算」和「零件密度」 | prompt 写死 `machines START at y=18% and RUN DOWN TO y=66%` + `DETAIL DENSITY: rivets/bolts/gauges/valves/dials/knobs/levers…`（【三·十二】） |
| 底部条**四条右端参差不齐**，像坏掉的表格 | 逐行给了不同的 `x1_ratio` | `clay_band.py --x1 0.755`（或 0.975）让四条齐平；**别逐行设右端**（【三·九】） |
| 模型"**多给一个**"道具（多一个红心 / 货架上多一个人偶） | 提示词约束不住（写了 `exactly ONE` 照样给两个） | 用 `scripts/patch_region.py --box x0,y0,x1,y1` 局部 inpaint 补掉，**别重出图**（【三·十三】） |
| **用户说"不像/不对"，反复调坐标仍不到** | 两张图**生成路线根本不同**（整图烘字 vs 贴字） | 先比"路线"再比参数：路线不一致就换路线重做，别在坐标上抛光 |
| **用户说"对勾/徽章像图标，不像黏土"** | 徽章是「平涂圆 + 细线矢量图标」+ 一圈浅色描边 | 走【三·二十】**层叠黏土徽章**：圆饼（落地影 → 底侧壁 → 顶面渐变 → 上缘亮边）＋ 对勾（自己的影 → 侧壁 → 顶面），**无描边**；直径 = 条高 × **0.80** |
| 徽章绿圆**整个不见了**（只剩一个勾） | `ImageDraw.polygon` 用「绕两圈」的点列表画圆 → **自交、填充退化** | 用 `ellipse` 画圆 + 掩膜噪声扰动（`clay_band.py` 已修） |
| 徽章**明暗渐变看不出来、一片花** | 条带级整体颗粒 `grain=0.30` 把渐变打成噪点 | 条带级降到 **0.16**，徽章内部各自 0.05~0.06（【三·二十】） |
| **小字（<30px）上缘发灰、"像被削掉一半"** | 走了 `render_clay_text`，它的 `top_edge` 亮边在 20px 字上占 10% 字高 | 字形高 < 30px 一律走【三·二十一】**纯字体 + 压印**；≥30px 才用 `render_clay_text` |
| 几条之间**缝是亮的**，读成"一张纸上的几行字" | 只做了整块投影，没做逐条投影 | 每条各自投一次影（【三·二十三】），缝才会暗（参考实测缝 rgb(16,10,39)） |
| 正文块**比参考页少**（4 条 vs 参考 7 条）→ 左列下半**空出一大块** | ①想把 4 条放大填满（元素等比膨胀、比例失真）②道具贴底边排成一条线（读成碎屑） | 走【三·二十二】：条高只 ×1.12、右端保持参考值、条带**下移到标题正下方**（`top ≈ 帧高 × 0.36`）、剩余地面用 `clay_props.py` 散落小道具**聚散布点**补 |
| **人物被裁掉半截 / 只有半身** | prompt 没写全身约束，模型自由裁切 | 写死 full-body 句式（见 Phase 1/铁律 3）；**出图后自查头顶与脚下是否都在画面内**，裁了就重出 |
| **每套图的封面都长一个样** | 封面 prompt 写死了固定场景（紫桌子+机器人+书+绿植+咖啡杯） | 从 `style-library.md`【封面款式库 CV1–CV6】换场景块；内页同理换 IN 场景块 |
| 整套图"太重复、翻页没惊喜" | 每页都用同一个场景骨架 | 相邻页换不同场景块，一套 ≥13 页至少 8 个不同场景块 |
| **条内文字"糊在一起 / 像图标"** | ①小字走 `render_clay_text`（厚侧壁 + 圆润化，笔画被加胖）②`letter_gap` 只有 0.02（**字距 = 字高的 2%**，八六是 20%）③条面 `--grain 0.16` 把字面打成花 | 深底浅色小字一律走 **`render_crisp_text`**（【三·二十四】）：字距 = 字高 × 0.11、不做强 gamma 压制、**深色方向性描边**（右下 ×1.55）、颗粒降到 0.11 |
| **文字没地方放 / 左列被道具塞满** | 出图 prompt 没声明留白 → 模型把工具墙、架子全塞满左侧 | prompt 里写死「the LEFT THIRD must stay almost EMPTY, reserved so text can be placed there later」（【三·二十五】）。**出了图救不回来，只能重出** |
| **出图后少了几张 / 某页被别的页顶掉** | 并行出图时 prompt **前缀相同**且同一秒完成 → 文件名（prompt 截断+时间戳）撞车，后写覆盖先写 | 每个 prompt 用**不同的开头词**（Use / Keep / Retain / Scene…），或分批串行出图 |
| 文字压在水印上 | 版式没避开右下角 | 文字统一放左/上，右下留空 |
| **用户说"他的图是生动形象的、是真实的"** | 画的是**通用机械**（一堆仪表齿轮），看不出在加工什么 | 按 `style-library.md`【三·九 可读生产线】把画面做成**从左到右能读出来的流程**：原料 → 加工（配铭牌命名）→ 成品，进料端画"原始形态"、出料端画"成品形态" |
| **底部四条通栏标签条塌成 2×2 / 内容重复** | 交给图片模型烘字 | 用 `scripts/clay_band.py` 渲染（真字体，零错字）；`--top` 取"人物鞋底行 + 6px" |
| **板上的标签条塞不下字 / 文字溢出条右端** | 没量板面宽度，直接套"通栏条"参数；或写超过 6 字 | 按【三·十五 嵌条法】先量板面边界与凹槽行，`--x0/--x1` 收窄到板面；**每条 ≤6 字**，长句交给口播/备注；要写长句必须先让板更宽（重出图） |
| 人物被底部条带切掉脚 | 条带 `--top` 拍脑袋定的 | 先量内容/人物最低行再定 `--top`（量法见【三·九】代码片段） |
| **用户说「框框像另外的画风，不是和板子一体」** | 走了【三·十五 嵌条法】——条嵌在道具板面的凹槽里，板一层、条一层，必然读成"贴纸" | **改走【三·十六 浮条法】**：条浮在**背景**上，整列同色、条间留缝露背景、徽章独立色；出图时把这一整块区域**留空**，别让模型画板 |
| **用户说「场景像乱凑的，要真正服务于内容」** | 画面是"一个车间里堆满道具"（齿轮/颜料罐/爱心/叶子当填充），只有板/一个道具和标题有关 | 主场景只留**一个动作**（第 9 页 = 扁塌灰板 → 厚圆奶油板 + 一把抹刀）；**每个道具问一遍"删掉它这页的话会变少吗"**，不会就换掉（【三·十六】+【三·七】） |
| **画面读成"卡片板式 PPT"**（道具被关进卡片/面板里、等距等分、人物站在圆台底座上） | 出图时把道具当成"往卡片里摆"，模型又默认给人加底座 | **改走【三·十九 自由场景叙事】**：① 道具**散落在场景里**，不关进框不排齐；② 人物**跪/坐地**，prompt 显式写 `NO pedestals or platforms` + `partly tucked behind the bench`；③ 要**三层纵深**（前景被下边缘裁切 / 中景偏右 / 后景清晰可读的墙）；④ **硬主光左上 + 物体互投 + 闭塞阴影**（放单独一段并写 `the single most important part`）；⑤ 标题立体字**不加长条底座**；⑥ 背景要颗粒+斑驳不平涂（**不许雾**）；⑦ 加**木色道具**给冷暖对比 |
| **背景"干净但单调、没有空间氛围感"** | 模型给的是平涂色块 | prompt 显式否定 `NEVER a flat solid fill`；出图后仍平就叠**亮部保护的高斯颗粒**（代码见【三·十九】） |
| **用户说「画面与内容不匹配，像是随意堆元素而已」**（比上一条更重） | 道具与文案**一条都对不上**——4 条改法配的是齿轮/木槌/罐子/爱心 | 走【三·十七】：**N 条内容 = N 件道具**，数量与顺序都一一对应；并列项用**卡式**（N 张卡，每卡一件对应道具），共同动作才用一个场景（p10 的漏斗）。反面道具清单见【三·十七】 |
| **卡的"框"读起来像另一套画风 / 像贴纸** | 把文字做成胶囊条贴到卡面上（卡一层、条一层） | 走【三·十七 卡面排字法】：文字**直接排进卡面留白**，深棕近黑 + 下缘浅色亮边，用 `clay_cardtext.py` |
| **一套图里只有一种紫、整幅发闷发平** | 把 `p02` 底栏的条几何/色调结论套到 `p10` 列式条目上 | **同一个 PPT 里不同的条，几何就是不同的**——量哪一张用哪一张（【三·十七】p10 真几何表：8.4% 条高 / 2.2% 缝 / 徽章 ×0.65 / 字高 ×0.48） |
| **`--hue-ramp` 怎么调都救不回来、紫烂在一起** | 模型把**明度顺序搞反**（背景 V=0.435 比道具 V=0.353 还亮）→ ramp 把背景判成"中间调"、道具判成"暗部" | 先用 `region_grade.py` 按**几何区域**把明度顺序摆正，再谈色相（【三·十八】；`feather ≥12`，否则出硬接缝） |
| **左列清单页被"空旷格=0"逼着往左列塞道具** | 密度基线**一档通用**——【三·六】的 0 格是在满版机器页（p02/p28）上标定的 | 按版式**分档**判：LP1 左列版拿**八六 p10** 当基线（最低 ~32 / 平均 ~55 / 3 格 <45 即达标）（【三·十六】） |
| **出图后左右两块背景有明显竖直接缝** | prompt 分区留白会让模型画成两张不同的背景 | 合成前做**单调横向压深**（左深右浅）+ 左区向背景靛紫靠拢，顺带吃掉接缝（【三·十六】步骤 2） |
| **黏土条表面是"光滑塑料"、没有颗粒** | 颗粒加在**超采样之前**，3× 降采样把高频噪点平均掉了（实测高频 std 1.23 vs 参考 5.09） | 颗粒必须在 `img.resize(...)` **之后**按最终分辨率生成（`clay_band.py` 已修，`--grain 0.30`） |
| **浅色奶油字在紫条上发虚、读不出立体** | 只压了字，没垫深色晕 | 先垫 `halo`（模糊字掩膜 ×2.05 − 字掩膜，α 0.95）再压字（`clay_band.py` 已内置） |
| **"文字全挤在左边、图在右边，人家怎么左右都有、标题在中间？"**（2026-09-19 晚第四轮定案） | 开工没选骨架，直接被 `render_label_band`/`compose` 的**默认行为（左列 + 右景）**吸走；八六 36 页里这种只有 **p10/p29 两页** | **每页第一件事：翻八六 → 选骨架【三·二十六】**。A 居中标题+左右双列 / B 居中标题+横向分栏 / C 左列+右景。**默认不是 C。** 骨架 A 的左右双列 = `render_label_band` 调两次贴两次（左 `x0 0.030→0.258`、右 `x0 0.478→0.700`） |
| **出图后"左半边是一整块空墙" → 用户读成"融入感差"** | ①prompt 只写"留空给文字"，没写"墙要有颗粒/渐变/暗角"②画面本身被切成"一半空一半满" | prompt 四段式写死（左条带区 / 中央主体 / 右条带区 / 人物压右边缘被裁）＋补一句 "**the wall must have rich clay grain, subtle light falloff and a soft vignette — never a flat empty void**"（【三·二十六】） |
| **条数只有 2~3 条时，"怎么摆都不像参考"** | 想把少量条**放大**去填满参考的 4~8 条尺寸 → 徽章/字等比膨胀、比例失真 | 条高只比参考 ×1.1 上下，**用"左右分布 + 中央主体"把画面撑开**，别用尺寸填（【三·二十六】）。剩余地面再用 `clay_props.py` 散落道具补 |
| 页数不对/顺序乱 | 没先确认目录 | Phase 0 先定页目录再出图 |
