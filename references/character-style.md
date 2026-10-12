# 人物画风规范（CHARACTER STYLE SPEC）· 2026-10-11 修订版（覆盖同日旧版）

> 来源：用户对自己成品的当面指认 + 八六老师 36 页原版**重新读图**复核。
> **地位**：本文件是人物部分的唯一真源。SKILL.md / prompts.md 的人物段都必须从这里取。

---

## 〇、三条前置纠正（2026-10-11 用户当面纠正，最高优先，推翻同日旧版）

1. **不叫"官方样例"。** `assets/examples/cover-excel-example.png`、`toc-clay-lettering-example.png` 是**用户自己项目里做出来的成品**（她的 Excel 课件封面 / 目录页），不是 skill 的"官方样例"。今后一律称「**用户参考成品**」。用户原话：「那明明是我做的，为什么是官方样的？」
2. **人物不设"唯一默认款"。** 用户原话：「人物小人的形象要是**百变的**，可以百变，**不是定死的**」。正确口径 = **画风与脸部特征统一，衣服 / 姿态 / 场景 / 装扮（可男可女）每页可变**；跨套课件也可整体换风格或换 IP。
3. **头身比纠错（上一版写错，作废）。** 旧版写的「4.5–5 头身帅 Q 少年」是**没看图瞎写**的。重新读八六原版（p21「小黑配图 Skill」、p31「交给 Skill Creator」等页）与用户成品后确认：真实是 **约 2.5–3 头身的 Q 版小孩**（头大、身小、手脚短圆）。

---

## 〇·五、角色是谁：**谁用，就是谁的形象**（2026-10-12 用户点名，对外分享的硬要求）

> 用户原话："**角色是谁使用就是谁的形象（要考虑分享出去别人拿来用，不是只能生成我）。**"

**这条是设计前提，不是可选项：** 本 skill 的角色**不是固定某个女孩/男孩**，而是**由使用者决定**。所以：

1. **默认流程**：使用者丢一张**自己的照片**（或喜欢的画风参考图）→ 用 `image2` 传入 → `Match the EXACT art style of image2` / 按其长相生成 Q 版黏土形象。
   - 有照片：`Turn the person in image2 into a 2.5–3-head-length cute polymer-clay chibi kid, keeping their recognizable facial features (hairstyle, glasses, expression mood), but rendered fully in handmade clay.`
   - 只有画风图：只借**画风**（材质/头身比/五官画法/配色倾向），不抄它的衣服发型（见 §一 的通用复刻规则）。
2. **没有照片时**：走 §三 的**角色锚点模板**先出一张，让使用者确认"像不像他/她要的形象"，再进封面/内页。
3. **性别/年龄不锁**：同一张脸**可男可女**（靠发型/衣服/发饰区分），也可做成成人 Q 版——**脸锁、装扮变**。
4. **一次只出 1 张锚点**（见 §五 出图纪律），确认后该锚点图就是全册的 `image1`。
5. **给别人用时的话术**：交付说明里写清"角色锚点用的是谁的/哪张图、要不要换"，让对方能自己替换成自己的形象。

> 一句话：**画风统一，但"这张脸是谁"由使用者说了算。** 分享出去别人也能生成自己的形象，而不是只有美瑶老师那一个女孩。

---

## 一、用户喜欢的成品（判级，**仅供参考，不是"默认款"**）

| 档位 | 实物 | 特征 | 结论 |
|---|---|---|---|
| ⭐⭐⭐ 最满意 | `assets/examples/cover-excel-example.png`、`assets/examples/toc-clay-lettering-example.png`（**都是用户自己的成品**） | **Q 版小孩**：深色头发扎顶髻 + 粉/玫瑰色**蝴蝶结发带**；**圆框眼镜**；圆脸大眼、小嘴微笑、腮红；**蓝色连衣裙（内搭浅色衬衫）**；手工黏土质感；深蓝底 + 漂浮黏土小装饰（星星 / 饼图 / 柱状图） | 用户指着说「跟原版差不多」「蓝衣小人最贴近原版」。**作为画风基准** |
| ⭐⭐ 达标但呆板 | `examples/character-anchor-example.png`（绿裙）、v2/v3 白西装款 | 丸子头、单一素色长袍、**纯色空背景** | 达标不是最佳；可作备选 |
| ⭐ 需改进 | 我们做的 v3 / 锚点 A | 高丸子头 + 白袍 + 空背景 + 双手垂放 | 差距在**有无场景道具**、**姿态有没有戏**、**表情**三处 |
| ❌ 永不出 | **半写实成人戴眼镜女人**（`AI+Excel数据处理实战_黏土风.pptx` 第 1 页那类）、亲子夏令营 3D 黏土 | 写实人脸、成人比例、抽象低幼 | 用户原话：「严重不要的丑的、吓人的，**永远不可能生成那样**」 |

**多 IP 风格保留**：`assets/style-refs/` 里的实物黏土小人照片（Q 版联盟 / 古风汉服 / 棕发大眼 / 糖果小童 / 粉樱治愈）是**允许的其他 IP 画风**——用户明确喜欢「IP 不止一款小人」。（**注意**：复刻 style-refs 时**只借"画风"**——材质 / 头身比 / 五官画法，**别抄它的衣服发型**。）

---

## 二、目标画风（**严格照这个，不许"差不多就行"**）

画风基准 = 八六原版小人 + 用户 `cover-excel` / `toc` 成品，共同点：

| 维度 | 正解 | 常见错法 |
|---|---|---|
| 头身比 | **约 2.5–3 头身的 Q 版小孩**（头大、身小、手脚短圆） | 拉成 4 头以上"少年/成人" ❌ |
| 眼镜 | **圆框眼镜**（圆框醒目、占脸大） | 无眼镜 / 方框 / 细金属框 ❌ |
| 头发 | **深色（黑 / 深棕）**；八六版蓬松短发，用户版**顶髻 + 粉色蝴蝶结发带** | 亮色发 / 写实发丝 ❌ |
| 脸 | 圆脸、大眼、小嘴微笑、腮红，**可爱**；表情随动作变 | 写实五官 / 尖下巴 / 面无表情 ❌ |
| 质感 | 手工黏土，哑光、有指痕 / 捏痕 / 雕塑痕 | 塑料光滑 / 写实渲染 ❌ |
| 服装 | 见 §四 换装表；**一套之内脸锁、衣可换** | 固定一套衣服 ❌ |
| 姿态 | 有戏：指点、招手、坐、站、操作电脑、蹲、钻进设备；**常压画框边** | 双手垂放呆站 ❌ |
| 场景 | 人**嵌在黏土道具场景里**（桌子 / 电脑 / 机器人 / 书架 / 图表），与道具**共用光照** | 纯色空背景前悬空 ❌ |
| 同页多人 | 同一张图可放 **2–4 个同一小人不同动作**，脸和发型一致 | 画成不同角色 ❌ |

**一句话**：**脸 + 画风锁死，衣服 / 姿态 / 场景百变。**

---

## 三、角色锚点模板（**Q 版小孩 · 已按 2.5–3 头身重写**）

出 **1 张 1024×1024** 方图，立刻给用户确认。**一次只出 1 张**，不合格只改一处再重出 1 张。

```
A single premium handcrafted polymer-clay figurine of a cute little kid presenter, about 2.5–3 head-lengths tall (a big round head on a small compact body, short rounded limbs — NOT a tall slender figure, NOT an adult, NOT a 4-head model). COMPLETE FULL BODY from the top of the hair down to the shoes, standing upright, facing the camera, entire body completely visible inside the frame, head to toe, NOT cropped by any frame edge, with clear empty margin above the hair and below the shoes.

Hair: dark (black or deep brown) hair gathered into a neat top bun, with a soft side-swept fringe, and a rose/pink bow headband across the top of the head.

Face: big round cute face, large expressive eyes with clear highlights, small smiling mouth, soft rosy blush. Wearing large ROUND glasses on the nose.

Outfit: a blue pinafore dress over a light cream shirt, tiny rounded shoes. (Clothes may change page to page — see the outfit list.)

Material: handmade polymer clay with visible fingerprints, sculpting marks, and matte soft surfaces on every form; NOT photorealistic, NOT glossy plastic toy, NOT flat anime line art.

Lighting: soft even studio light with gentle contact shadow at the feet. Background: plain light warm grey seamless backdrop for later compositing. No text, no watermark, no letters, no numbers.
```

### 脸部锁定段（**同一套之内每页必抄，一字不改；只锁脸，不锁衣**）

```
Keep EXACTLY the same little kid character as the reference image: identical round face, identical large round glasses, identical dark top-bun hair with the pink bow headband, identical cute clay-material look and identical 2.5–3-head-length chibi proportion. Only the clothing, the pose and the surrounding scene may change.
```

### 可换装清单（换衣服 / 姿势 / 场景即可换页，绝不动脸）

| 场景气质 | 上装 | 下装 | 鞋 |
|---|---|---|---|
| 蓝色主调（用户最爱） | 蓝色背带连衣裙 + 浅色衬衫 | —— | 白色小圆鞋 |
| 紫色主调（八六原版同款） | 紫色围裙 / 背带 + 白衬衫 | 深紫短裤 | 紫色小鞋 |
| 科技白蓝 | 白蓝拼色外套 + 圆领 T | 深蓝短裤 | 白蓝运动鞋 |
| 沉稳黑灰 | 黑灰工装外套 + 灰 T | 深灰长裤 | 黑色小靴 |
| 春日暖调 | 米白针织开衫 | 及膝 A 字裙（任选色） | 米色小鞋 |

> **装扮可男可女**——同一张脸既可做「小女生」也可做「小男生」，靠发型 / 衣服区分，脸不变。

---

## 四、多小人同页规则（原版确实这么用，不会出错）

同一页要出现 2–4 个小人时，prompt 必须写：

```
The SAME character appears {N} times in this scene, each instance with the identical face, identical round glasses and identical hairstyle, but performing DIFFERENT actions — one {action A}, one {action B}, one {action C}. Same face, same hair, same glasses on every instance; only the pose differs.
```

**忌**：不要说 "two girls / two boys"（会被理解成两个不同角色）；要说 `the SAME character, repeated`。

---

## 五、出图纪律（用户当面要求，硬性）

- **一次只出 1 张，先给用户看，不出整套。** 用户原话：「不要冒昧的花我很多积分……你先升（生）一点，然后保证那个不出错再升（生）。」
- **出图前先把"用哪张参考图、什么提示词、只出几张"讲清楚**，不要偷偷批量生成。
- **"严格照参考、不许差不多"**：复刻人格时，脸 / 眼镜 / 发型 / 头身比必须逐项对上；差一点就重出。
- **不叫"官方样例"**：一律说「**用户参考成品**」。
