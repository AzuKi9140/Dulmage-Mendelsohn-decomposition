import numpy as np
from mip import BINARY, Model, OptimizationStatus, maximize, xsum


class MaximumFlow:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.n, self.m = matrix.shape
        self.matching: list[tuple[int, int]] = []

    def solve(self):
        # MIPモデルの作成
        model = Model("Maximum Flow")

        # 変数の作成（行と列のペアに対するバイナリ変数）
        x = [
            [model.add_var(var_type=BINARY) for _ in range(self.m)]
            for _ in range(self.n)
        ]

        # 始点から各行への流入量を表す変数
        flow_from_source = [
            model.add_var(var_type=BINARY, name=f"flow_from_source_{i}")
            for i in range(self.n)
        ]

        # 各列から終点への流出量を表す変数
        flow_to_sink = [
            model.add_var(var_type=BINARY, name=f"flow_to_sink_{j}")
            for j in range(self.m)
        ]

        # 行ノードから列ノードへの制約
        for i in range(self.n):
            for j in range(self.m):
                if self.matrix[i, j] == 0:  # エッジが存在しない場合
                    model.add_constr(x[i][j] == 0)  # 枝が存在しない

        # 始点と終点を除いた各ノードの流出入は0
        for i in range(self.n):
            model.add_constr(
                flow_from_source[i] - xsum(x[i][j] for j in range(self.m)) == 0
            )
        for j in range(self.m):
            model.add_constr(
                xsum(x[i][j] for i in range(self.n)) - flow_to_sink[j] == 0
            )

        objective_function = xsum(x[i][j] for i in range(self.n) for j in range(self.m))

        model.add_constr(
            xsum(flow_from_source[i] for i in range(self.n)) == objective_function
        )

        model.objective = maximize(objective_function)

        # 最適化の実行
        model.optimize()

        # 結果の表示
        if model.status == OptimizationStatus.OPTIMAL:
            print("最適解:")
            for i in range(self.n):
                for j in range(self.m):
                    if x[i][j].x >= 0.99:  # バイナリ変数の値が1に近い場合
                        print(f"行 {i + 1} と列 {j + 1} がマッチングされています。")
                        self.matching.append((i, j))
        else:
            print("最適解が見つかりませんでした。")
