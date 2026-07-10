---
title: Python 与数据分析
description: 用 Python 完成数据读取、清洗、分析、建模与可视化
tags:
  - Python
  - 数据分析
---

# Python 与数据分析

Python 相关内容会围绕数据分析的完整流程展开：读取数据、清洗数据、探索数据、建模分析和可视化表达。

## 常用工具

| 工具 | 用途 |
| --- | --- |
| NumPy | 数值计算、数组操作 |
| pandas | 表格数据处理 |
| Matplotlib | 基础可视化 |
| seaborn | 统计图形 |
| scikit-learn | 机器学习模型 |
| Jupyter | 交互式分析与作业整理 |

## 计划文章

- pandas 常用操作速查。
- 数据清洗的基本流程。
- 如何把作业代码整理成可复现笔记。
- 图表如何服务于结论，而不是只追求好看。

## 示例代码

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C"],
    "score": [88, 92, 79],
})

print(df.describe())
```
