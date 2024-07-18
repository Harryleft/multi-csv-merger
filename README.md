# multi-csv-merger
这个 Python 脚本用于合并多个 CSV 文件并清理结果数据。它特别适用于处理具有相同表头但可能存在编码差异的 CSV 文件。

## 功能

- 自动检测并处理不同编码的 CSV 文件
- 合并具有相同表头的多个 CSV 文件
- 删除合并后的数据中完全为空的列
- 详细的日志记录，方便追踪处理过程

## 使用要求

- Python 3.6+
- pandas
- chardet

## 安装依赖

```bash
pip install pandas chardet
```

## 使用方法

1. 克隆此仓库到本地。
2. 在脚本中设置 `folder_path` 变量为包含您要合并的 CSV 文件的文件夹路径。
3. 运行脚本：

```bash
python csv_merger_cleaner.py
```
脚本将在指定文件夹中创建一个名为 `combined_output.csv` 的新文件，其中包含所有合并和清理后的数据。

## 注意事项
- **确保所有需要合并的 CSV 文件都有相同的列结构**。
- 脚本会自动尝试处理不同的常见文本编码。
- 处理大量或大型 CSV 文件时可能需要较长时间。
