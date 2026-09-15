# ImageGen 参数与踩坑（WorkBuddy 原生）

## 1. 调用方式

ImageGen 是 **deferred tool**，不在默认工具列表里。调用顺序：

1. `ToolSearch`，参数 `tool_names: ["ImageGen"]`，载入 schema
2. `DeferExecuteTool`，`toolName: "ImageGen"`，`params: {...}`

## 2. 参数表（以实际 schema 为准）

| 参数 | 必填 | 说明 |
|------|------|------|
| `prompt` | ✅ | 英文写场景，中文写要出现在图上的字 |
| `size` | — | `"1024x1024"`（方图/角色）、`"1024x576"`（16:9 页）、`"1024x1536"`、`"1536x1024"` |
| `image1` / `image2` / `image3` | — | 图生图输入，本地路径或 http(s) URL；用了 image1 才能用 image2/3 |
| `input_fidelity` | — | 图生图时控制与原图贴近程度 |
| `output_dir` | — | 自定义输出目录；不填则落在工作区 `generated-images/` |
| `quality` / `style` / `background` / `footnote` / `revise` | — | 按需使用 |

> 确认：`ImageGen` 实际上**不存在** `aspect_ratio` 参数。传 `aspect_ratio` 会直接报错：
> `root: must NOT have additional properties`。比例只能用 `size` 控制。

## 3. 三条实测踩坑

### 坑 1 · 比例参数不存在
❌ `{"prompt": "...", "aspect_ratio": "16:9", "size": "1024x576"}`
✅ `{"prompt": "...", "size": "1024x576"}`

### 坑 2 · 中文标题其实能渲染（关键发现）
早期 skill 一律要求 `no written words`，但实测：**只要给出准确的中文字符串 + 明确要求"清晰可读"，中文标题能正确生成。**
写法要点：
1. 中文字符串用**单引号原样**写进 prompt，如 `Chinese title text 'AI + Excel 数据处理实战'`
2. 追加 `Make the Chinese text on the cream plaque clearly readable.`
3. 文字放在**图上的奶油铭牌**里，不要让模型自由排版

✅ 实测成功案例：封面标题 `AI + Excel 数据处理实战` 完全正确、无错字。
⚠️ 但**不要依赖它渲染长段落/多行正文**——正文一律交给脚本叠加。

### 坑 3 · 右下角水印
内置出图右下角带 `AI生成 WORKBUDDY` 水印。排版本就要避开右下角：文字放左侧/顶部，别放右下。

## 4. 一致性策略

- **主要手段**：每页 prompt 里逐字重复同一段人物 + 风格描述（见 `prompts.md`）。
- **加强手段**：需要角色高度一致时，把角色锚点图作为 `image1` 传入做 image-to-image，prompt 描述"在保持该角色的前提下新增场景"。
- **验收**：批量前先抽 1 页比对角色，五官/发型/发饰/眼镜/服装有无漂移。

## 5. 输出位置约定

- 默认：`<工作区>/generated-images/`
- 文件名：prompt 截断 + 时间戳，例如 `A_premium_handcrafted_polymer__2026-09-03T02-19-12.png`
- 合脚本时按"时间戳顺序 + 页码映射"取图，建议在 `slides.json` 里显式写路径，不要靠猜。
