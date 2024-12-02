import numpy as np
import pandas as pd


class IOTable:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path, header=2, index_col=1)
        self.intermediate_df = self._extract_intermediate()
        self.filtered_intermediate_df = None

    def _extract_intermediate(self):
        rows = slice(1, 53)
        cols = slice(1, 53)
        intermediate_df = self.df.iloc[rows, cols].astype(float)

        # すべての値が0の行を除外
        zero_rows = intermediate_df.index[intermediate_df.sum(axis=1) == 0]
        intermediate_df = intermediate_df.drop(index=zero_rows)

        # 同じインデックスを持つ列も削除
        intermediate_df = intermediate_df.drop(columns=zero_rows, errors="ignore")
        print(intermediate_df.shape)

        return intermediate_df

    def print_intermediate_table_summary(self):
        """
        中間投入表全体の統計情報を表示します
        """
        # 全ての値を1次元配列として扱う
        all_values = self.intermediate_df.values.flatten()
        print("=== 全体の統計情報 ===")
        print(f"データ数: {len(all_values)}")
        print(f"平均値: {all_values.mean():.2f}")
        print(f"標準偏差: {all_values.std():.2f}")
        print(f"最小値: {all_values.min():.2f}")
        print(f"最大値: {all_values.max():.2f}")
        print(f"中央値: {np.median(all_values):.2f}")

        # パーセンタイルの情報も表示
        percentiles = [10, 25, 50, 75, 90]
        print("\n=== パーセンタイル ===")
        for p in percentiles:
            value = np.percentile(all_values, p)
            print(f"{p}パーセンタイル: {value:.2f}")

    def get_filtered_intermediate(self, percentile=10, by_row=False):
        """
        intermediate_dfの値のうち、下位n%(デフォルトは10%)未満の値を0に置き換えます

        Parameters:
        -----------
        percentile : int
            カットオフするパーセンタイル（デフォルト: 10）
        by_row : bool
            行ごとに個別のパーセンテイルを適用するかどうか（デフォルト: False）
        """
        filtered_df = self.intermediate_df.copy()

        if by_row:
            # 行ごとに個別のパーセンタイルを適用
            for row in filtered_df.index:
                threshold = filtered_df.loc[row].quantile(percentile / 100)
                filtered_df.loc[row, filtered_df.loc[row] < threshold] = 0
        else:
            # 列ごとに個別のパーセンタイルを適用
            for col in filtered_df.columns:
                threshold = filtered_df[col].quantile(percentile / 100)
                filtered_df.loc[filtered_df[col] < threshold, col] = 0

        self.filtered_intermediate_df = filtered_df

    def get_filtered_intermediate_by_percent(self, percentile=10, by_row=False):
        """
        intermediate_dfの各行または列に対して、下位n%の値を0に置き換えます

        Parameters:
        -----------
        percentile : int
            置き換える値のパーセンテージ（デフォルト: 10）
        by_row : bool
            行ごとに個別のパーセンテイルを適用するかどうか（デフォルト: False）
        """
        filtered_df = self.intermediate_df.copy()

        if by_row:
            # 行ごとに個別のパーセンテイルを適用
            for row in filtered_df.index:
                count = int(len(filtered_df.columns) * (percentile / 100))
                threshold_indices = filtered_df.loc[row].nsmallest(count).index
                filtered_df.loc[row, threshold_indices] = 0
        else:
            # 列ごとに個別のパーセンテイルを適用
            for col in filtered_df.columns:
                count = int(len(filtered_df) * (percentile / 100))
                threshold_indices = filtered_df[col].nsmallest(count).index
                filtered_df.loc[threshold_indices, col] = 0

        self.filtered_intermediate_df = filtered_df

    def filter_by_count(self, count: int, by_row: bool = False):
        """
        各行または各列の指定された数だけ残し、それ以外を0にします

        Parameters:
        -----------
        count : int
            残す値の数
        by_row : bool
            行ごとに個別のカウントを適用するかどうか（デフォルト: False）
        """
        filtered_df = self.intermediate_df.copy()

        if by_row:
            # 行ごとに指定された数だけ残す
            for row in filtered_df.index:
                # 各行の上位count個のインデックスを取得
                top_indices = filtered_df.loc[row].nlargest(count).index
                filtered_df.loc[
                    row, filtered_df.loc[row] < filtered_df.loc[row, top_indices].min()
                ] = 0
        else:
            # 列ごとに指定された数だけ残す
            for col in filtered_df.columns:
                # 各列の上位count個のインデックスを取得
                top_indices = filtered_df[col].nlargest(count).index
                filtered_df.loc[
                    filtered_df[col] < filtered_df.loc[top_indices, col].min(), col
                ] = 0

        self.filtered_intermediate_df = filtered_df

    def save_filtered_intermediate(self, output_path):
        """
        フィルタリング済みの中間投入表（self.filtered_intermediate_df）をExcelファイルとして保存します

            Parameters:
        -----------
        output_path : str
            出力するExcelファイルのパス（例: 'output/filtered_table.xlsx'）
        """

        if self.filtered_intermediate_df is None:
            raise ValueError(
                "フィルタリングされたデータがありません。先にget_filtered_intermediateを実行してください。"
            )

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            self.filtered_intermediate_df.to_excel(
                writer, sheet_name="filtered_intermediate", index=True
            )

    def print_intermediate_table(self):
        print(self.intermediate_df)


if __name__ == "__main__":
    io_table = IOTable("data/io_table.xlsx")
    io_table.print_intermediate_table()
    io_table.print_intermediate_table_summary()
    # io_table.get_filtered_intermediate(30)
    io_table.filter_by_count(20, by_row=True)
    io_table.save_filtered_intermediate("output/filtered_table.xlsx")
