import os
import pandas as pd
import chardet
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_csv_with_encoding(file_path):
    # 检测文件编码
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    logging.info(f"Detected encoding for {file_path}: {encoding}")

    # 尝试不同的编码方式
    encodings_to_try = [encoding, 'utf-8', 'gb18030', 'gbk', 'gb2312', 'big5']

    for enc in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            logging.info(f"Successfully read {file_path} with encoding: {enc}")
            return df
        except Exception as e:
            logging.warning(f"Failed to read with {enc}: {str(e)}")

    logging.error(f"Failed to read {file_path} with all attempted encodings")
    return None


# 指定包含CSV文件的文件夹路径
folder_path = r'C:\Users\afkxw\Desktop\IIIF案例\技术栈收集'

# 获取文件夹中所有的CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
logging.info(f"Found {len(csv_files)} CSV files")

# 创建一个空的DataFrame来存储合并后的数据
combined_df = pd.DataFrame()

# 遍历所有CSV文件并合并数据
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = read_csv_with_encoding(file_path)

    if df is None:
        continue

    # 如果combined_df为空，则使用第一个文件的数据（包括表头）
    if combined_df.empty:
        combined_df = df
        logging.info(f"Initialized combined_df with {file}")
    else:
        # 确保列名匹配
        if list(combined_df.columns) != list(df.columns):
            logging.warning(f"Columns in {file} do not match the first file. Attempting to reorder columns.")
            df = df.reindex(columns=combined_df.columns)

        # 追加数据行（不包括表头）
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        logging.info(f"Appended data from {file}")

    logging.info(f"Current combined_df shape: {combined_df.shape}")

# 删除没有数据的列
if not combined_df.empty:
    # 记录删除前的列数
    original_columns = combined_df.shape[1]

    # 删除所有值都为 NaN 的列
    combined_df = combined_df.dropna(axis=1, how='all')

    # 记录删除后的列数
    remaining_columns = combined_df.shape[1]

    logging.info(f"Removed {original_columns - remaining_columns} empty columns.")
    logging.info(f"Final combined_df shape: {combined_df.shape}")

# 将合并后的数据保存为新的CSV文件
if not combined_df.empty:
    output_path = os.path.join(folder_path, 'combined_output.csv')
    combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"Merge completed, output file saved at: {output_path}")
else:
    logging.error("No data was combined. Check the input files and logs for errors.")

print("Process completed. Please check the log for details.")