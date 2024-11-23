import numpy as np
from mip import BINARY, Model, OptimizationStatus, xsum, maximize


class BipartiteMatching:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.n, self.m = matrix.shape

    def solve(self):
        # MIPモデルの作成
        model = Model("Bipartite Matching")

        # 変数の作成（行と列のペアに対するバイナリ変数）
        x = [
            [model.add_var(var_type=BINARY) for _ in range(self.m)]
            for _ in range(self.n)
        ]

        # 行ノードから列ノードへの制約
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i, j] != 0:  # エッジが存在する場合
                    model.add_constr(x[i][j] <= 1)  # 容量1の制約
                else:
                    model.add_constr(x[i][j] == 0)

        # 各行ノードに対する制約（1つの列ノードにしか接続できない）
        for i in range(self.n):
            model.add_constr(xsum(x[i][j] for j in range(self.m)) <= 1)

        # 各列ノードに対する制約（1つの行ノードにしか接続できない）
        for j in range(self.m):
            model.add_constr(xsum(x[i][j] for i in range(self.n)) <= 1)

        # 目的関数の設定
        model.objective = maximize(
            xsum(x[i][j] for i in range(self.n) for j in range(self.m))
        )

        # 最適化の実行
        model.optimize()

        # 結果の表示
        if model.status == OptimizationStatus.OPTIMAL:
            print("最適解:")
            for i in range(self.n):
                for j in range(self.m):
                    if x[i][j].x >= 0.99:  # バイナリ変数の値が1に近い場合
                        print(f"行 {i + 1} と列 {j + 1} がマッチングされています。")
        else:
            print("最適解が見つかりませんでした。")
