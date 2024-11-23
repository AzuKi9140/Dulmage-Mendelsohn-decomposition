from collections import defaultdict
from typing import Dict, List, Set, Tuple

import numpy as np


class StronglyConnectedComponents:
    def __init__(self, matrix: np.ndarray, valid_edges: List[Tuple[int, int]]):
        self.matrix = matrix
        self.valid_edges = valid_edges
        self.n = matrix.shape[0]
        self.m = matrix.shape[1]
        self.total_vertices = self.n + self.m

        self.index = 0
        self.stack = []
        self.on_stack = [False] * self.total_vertices
        self.indices = [-1] * self.total_vertices
        self.lowlink = [-1] * self.total_vertices
        self.sccs = []

        self.graph = self._create_adjacency_list()

    def _create_adjacency_list(self) -> Dict[int, List[int]]:
        """二部グラフの有向グラフ表現の隣接リストを作成"""
        adj_list = {i: [] for i in range(self.total_vertices)}

        # マッチング辺（双方向）
        for r, c in self.valid_edges:
            adj_list[r].append(c + self.n)
            adj_list[c + self.n].append(r)

        # マッチングに含まれない辺（RからCへの一方向）
        matched_edges = set(self.valid_edges)
        for r in range(self.n):
            for c in range(self.m):
                if self.matrix[r, c] != 0 and (r, c) not in matched_edges:
                    adj_list[r].append(c + self.n)

        return adj_list

    def _create_scc_graph(self) -> Dict[int, Set[int]]:
        """強連結成分間の到達可能性グラフを作成"""
        # 各頂点がどの強連結成分に属しているかのマップを作成
        vertex_to_scc = {}
        for scc_id, [rows, cols] in enumerate(self.sccs):
            for r in rows:
                vertex_to_scc[r] = scc_id
            for c in cols:
                vertex_to_scc[c + self.n] = scc_id

        # 強連結成分間の辺を見つける
        scc_graph = defaultdict(set)

        # 元のグラフの各辺について、異なる強連結成分を結ぶ辺を探す
        for v in range(self.total_vertices):
            if v in self.graph and v in vertex_to_scc:
                for u in self.graph[v]:
                    if u in vertex_to_scc:
                        v_scc = vertex_to_scc[v]
                        u_scc = vertex_to_scc[u]
                        if v_scc != u_scc:
                            # 小さい番号から大きい番号への辺となるように向きを設定
                            scc_graph[v_scc].add(u_scc)

        return scc_graph

    def _topological_sort_sccs(self):
        """強連結成分を半順序関係に基づいてソート"""
        scc_graph = self._create_scc_graph()

        # 入次数を計算
        in_degree = defaultdict(int)
        for u in range(len(self.sccs)):
            for v in scc_graph[u]:
                in_degree[v] += 1

        # 入次数0の頂点から始める
        queue = [i for i in range(len(self.sccs)) if in_degree[i] == 0]
        sorted_sccs = []

        while queue:
            u = queue.pop(0)
            sorted_sccs.append(u)

            for v in scc_graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        # SCCsを並び替える（トポロジカル順序そのままで、小さい番号から大きい番号への有向道があるようにする）
        self.sccs = [self.sccs[i] for i in sorted_sccs]

    def _strong_connect(self, v: int):
        """Tarjanのアルゴリズムのメインロジック"""
        self.indices[v] = self.index
        self.lowlink[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack[v] = True

        for w in self.graph[v]:
            if self.indices[w] == -1:
                self._strong_connect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
            elif self.on_stack[w]:
                self.lowlink[v] = min(self.lowlink[v], self.indices[w])

        if self.lowlink[v] == self.indices[v]:
            scc_rows = set()
            scc_cols = set()
            while True:
                w = self.stack.pop()
                self.on_stack[w] = False
                if w < self.n:
                    scc_rows.add(w)
                else:
                    scc_cols.add(w - self.n)
                if w == v:
                    break
            if scc_rows or scc_cols:
                self.sccs.append([sorted(list(scc_rows)), sorted(list(scc_cols))])

    def find_sccs(self) -> List[List[List[int]]]:
        """グラフの強連結成分を見つける"""
        for v in range(self.total_vertices):
            if self.indices[v] == -1:
                self._strong_connect(v)

        # 強連結成分間の半順序関係に基づいてソート
        self._topological_sort_sccs()
        return self.sccs

    def print_sccs(self):
        """強連結成分を1-indexedで表示"""
        print("強連結成分:")
        for i, [rows, cols] in enumerate(self.sccs):
            print(
                f"Component {i}: R={[r + 1 for r in rows]}, C={[c + 1 for c in cols]}"
            )
