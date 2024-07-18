import os
import pandas as pd
import chardet
import logging
from typing import List, Optional


class CSVMergerCleaner:
    def __init__(self, folder_path: str, remove_empty_cols: bool = True):
        self.folder_path = folder_path
        self.remove_empty_cols = remove_empty_cols
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_csv_files(self) -> List[str]:
        return [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]

    def read_csv_with_encoding(self, file_path: str) -> Optional[pd.DataFrame]:
        encodings_to_try = ['utf-8', 'gb18030', 'gbk', 'gb2312', 'big5']

        # 检测文件编码
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected_encoding = chardet.detect(raw_data)['encoding']

        encodings_to_try.insert(0, detected_encoding)

        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                logging.info(f"Successfully read {file_path} with encoding: {encoding}")
                return df
            except Exception as e:
                logging.warning(f"Failed to read {file_path} with {encoding}: {str(e)}")

        logging.error(f"Failed to read {file_path} with all attempted encodings")
        return None

    def merge_csv_files(self) -> Optional[pd.DataFrame]:
        csv_files = self.get_csv_files()
        logging.info(f"Found {len(csv_files)} CSV files")

        combined_df = pd.DataFrame()

        for file in csv_files:
            file_path = os.path.join(self.folder_path, file)
            df = self.read_csv_with_encoding(file_path)

            if df is None:
                continue

            if combined_df.empty:
                combined_df = df
                logging.info(f"Initialized combined_df with {file}")
            else:
                if list(combined_df.columns) != list(df.columns):
                    logging.warning(f"Columns in {file} do not match. Attempting to reorder columns.")
                    df = df.reindex(columns=combined_df.columns)

                combined_df = pd.concat([combined_df, df], ignore_index=True)
                logging.info(f"Appended data from {file}")

            logging.info(f"Current combined_df shape: {combined_df.shape}")

        return combined_df

    def remove_empty_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.remove_empty_cols:
            logging.info("Skipping removal of empty columns as per user setting.")
            return df

        original_columns = df.shape[1]
        df = df.dropna(axis=1, how='all')
        remaining_columns = df.shape[1]

        logging.info(f"Removed {original_columns - remaining_columns} empty columns.")
        logging.info(f"Final df shape: {df.shape}")

        return df

    def save_output(self, df: pd.DataFrame, output_filename: str = 'combined_output.csv'):
        output_path = os.path.join(self.folder_path, output_filename)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Output file saved at: {output_path}")

    def process(self):
        combined_df = self.merge_csv_files()
        if combined_df is not None and not combined_df.empty:
            cleaned_df = self.remove_empty_columns(combined_df)
            self.save_output(cleaned_df)
        else:
            logging.error("No data was combined. Check the input files and logs for errors.")


def main():
    folder_path = r'[your_csv_files_path]'
    remove_empty_cols = True  # 设置为 False 如果不想删除空列
    merger_cleaner = CSVMergerCleaner(folder_path, remove_empty_cols)
    merger_cleaner.process()
    print("Process completed. Please check the log for details.")


if __name__ == "__main__":
    main()
