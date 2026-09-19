# assets/ref-title/ —— 标题金标准

| 文件 | 是什么 | 能不能用来标定参数 |
|---|---|---|
| `gold_title.png` | **本机可复现**的金标准样本：`render_title_clay('改法清单', cap_height=80)` 放在纯紫墙上 | ✅ **就用它** |
| `gold_metrics.json` | 它的 7 项期望指标（ink 宽高比 / 边宽 / 面色 / 边色 / **底板横条比** / 颗粒 等） | ✅ |
| `_DEPRECATED_p9_title_model_baked.png` | 从**第 9 页底图 `scene_p9v4_grain.png`** 里裁下来的「改法清单」 | ❌ **禁止** |

## 为什么那个旧样本被作废（重要）

第 9 页的标题**不是 `clay_text` 合成的**，是**出图模型直接画在底图上**的。
证据：

- `scene_p9v4_grain.png`（第 9 页的底图）里标题已经存在；
- 四个字体（noto / sthu / msyh / deng）× 三档字号，对它做**墨迹掩膜 IoU 最高只有 0.64**
  （同一字体同一文字应 > 0.9）；
- 它那种「笔画粗细不匀 + 端点是不规则圆瘤 + 带暖光晕 + 强颗粒」是**生成模型特征**，
  任何字体都做不出来。

所以拿它当金标准去调代码参数，**方向从一开始就错了** —— 第 10 页怎么调都会"不一样"。
第十一轮的结论：**标题只能用同一套可复现的写法**（= `render_title_clay`），
并且第 9 页那页的旧标题已经用 `cv2.inpaint` 抹掉、换成了同款写法（`page09_改法清单_v7.png`）。

## 验收

```bash
python scripts/verify_title.py        # 7 项 PASS/FAIL（含"底板横条比"）
python scripts/verify_portable.py    # 模拟"别人那台没有中文字体"
```
