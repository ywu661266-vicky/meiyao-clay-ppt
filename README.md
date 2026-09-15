# meiyao-clay-ppt · 黏土风课件生成器

> 一套跑在 **WorkBuddy 原生环境**里的黏土风（polymer-clay diorama）PPT / 课件生成技能。
> 用内置 ImageGen 出图 + python-pptx 合成**可编辑**的 16:9 演示文稿。

![封面示例](assets/examples/cover-excel-example.png)

---

## 它能做什么

给一个主题（比如"Excel 数据处理实战"），自动产出一整套**手工黏土定格动画质感**的幻灯片：

- Q 版黏土讲师形象（发型 / 发饰 / 眼镜 / 服装可定制）
- 微缩黏土场景 + 奶油色黏土铭牌 + 中文标题
- 输出 **可编辑** 的 `.pptx`（文字可改、含讲师备注）

## 为什么是"原生"

| | 外部 Codex 版 skill | 本 skill |
|---|---|---|
| 出图 | Codex Image2 | **WorkBuddy 内置 ImageGen** |
| 合成 | 外部脚本 | **python-pptx**（本仓库自带） |
| 额外 hook | 可能混入审美检查流程 | **无，纯本流程** |
| 成本控制 | — | **三步确认法，逐张确认不浪费额度** |

## 核心：三步确认法

**绝不一上来批量出图**，按下面顺序逐步确认：

1. **角色锚点** — 出 1 张 `1024×1024`，确认人物特征
2. **封面** — 出 1 张 `1024×576`，主标题烘进图，确认整页效果
3. **批量内页** — 确认后才生成目录 + 内容页 + 总结页
4. **合成** — `scripts/build_pptx.py` 输出可编辑 PPTX

## 安装

```bash
git clone https://github.com/ywu661266-vicky/meiyao-clay-ppt.git ~/.workbuddy/skills/meiyao-clay-ppt
```

或把本目录整个复制到 `~/.workbuddy/skills/` 下即可。

## 触发方式

在 WorkBuddy 里说：

- "做一套黏土风 PPT"
- "把这个主题做成黏土风"
- "要 Q 版讲师形象的幻灯片"
- "clay style ppt"

## 目录结构

```
meiyao-clay-ppt/
├── SKILL.md                        # 主流程（触发词 / 三步确认法 / 调用规范）
├── references/
│   ├── workflow.md                 # 三步确认法细节 + 翻车对策
│   ├── prompts.md                  # 实测通过的提示词模板
│   ├── style-system.md             # 配色 / 材质 / 构图 / 版式规范
│   └── imagegen-params.md          # ImageGen 参数与踩坑
├── scripts/
│   └── build_pptx.py               # 背景图 → 可编辑 PPTX
└── assets/examples/                # 成功样例
```

## 关键发现（踩坑记录）

- WorkBuddy ImageGen **没有 `aspect_ratio` 参数**，比例只能用 `size`（16:9 → `1024x576`，角色 → `1024x1024`）。
- 混元 **能渲染可读中文标题**：中文字符串用单引号写进 prompt，并追加 `Make the Chinese text clearly readable.`
- 内置出图右下角固定 `AI生成 WORKBUDDY` 水印，版式需避开右下角。

## License

MIT
