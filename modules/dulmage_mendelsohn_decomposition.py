from typing import List, Set, Tuple

import numpy as np

from .strongly_connected_components import StronglyConnectedComponents


class DulmageMendelsohnDecomposition:
    def __init__(self, matrix: np.ndarray, matching: List[Tuple[int, int]]):
        self.matrix = matrix
        self.matching = matching
        self.n = matrix.shape[0]
        self.m = matrix.shape[1]
        self.dM_rows = set(r for r, _ in matching)
        self.dM_cols = set(c for _, c in matching)
        self.decomposition = None
        self.has_v0 = False
        self.has_vinf = False

    def _find_Vinf(self) -> Tuple[Set[int], Set[int]]:
        unmatched_rows = set(range(self.n)) - self.dM_rows

        vinf_rows = set()
        vinf_cols = set()
        stack = list(unmatched_rows)

        while stack:
            v = stack.pop()
            if v not in vinf_rows:
                vinf_rows.add(v)
                for c in range(self.m):
                    if (
                        self.matrix[v, c] != 0
                        and (v, c) not in self.matching
                        and c not in vinf_cols
                    ):
                        vinf_cols.add(c)
                        for r, mc in self.matching:
                            if mc == c and r not in vinf_rows:
                                stack.append(r)

        return vinf_rows, vinf_cols

    def _find_V0(self) -> Tuple[Set[int], Set[int]]:
        unmatched_cols = set(range(self.m)) - self.dM_cols

        v0_rows = set()
        v0_cols = set()
        stack = list(unmatched_cols)

        while stack:
            c = stack.pop()
            if c not in v0_cols:
                v0_cols.add(c)
                for r in range(self.n):
                    if (
                        self.matrix[r, c] != 0
                        and (r, c) not in self.matching
                        and r not in v0_rows
                    ):
                        v0_rows.add(r)
                        for mr, c2 in self.matching:
                            if mr == r and c2 not in v0_cols:
                                stack.append(c2)

        return v0_rows, v0_cols

    def solve(self) -> List[List[List[int]]]:
        v0_rows, v0_cols = self._find_V0()
        vinf_rows, vinf_cols = self._find_Vinf()

        self.has_v0 = bool(v0_rows or v0_cols)
        self.has_vinf = bool(vinf_rows or vinf_cols)

        remove_rows = v0_rows.union(vinf_rows)
        remove_cols = v0_cols.union(vinf_cols)

        remaining_rows = sorted(set(range(self.n)) - remove_rows)
        remaining_cols = sorted(set(range(self.m)) - remove_cols)
        row_map = {old: new for new, old in enumerate(remaining_rows)}
        col_map = {old: new for new, old in enumerate(remaining_cols)}

        remaining_matrix = self.matrix[np.ix_(remaining_rows, remaining_cols)]

        remaining_matching = []
        for r, c in self.matching:
            if r not in remove_rows and c not in remove_cols:
                remaining_matching.append((row_map[r], col_map[c]))

        scc_components = []
        if remaining_matching:
            scc = StronglyConnectedComponents(remaining_matrix, remaining_matching)
            scc_components = scc.find_sccs()

            scc_components = [
                [
                    [remaining_rows[r] for r in comp_rows],
                    [remaining_cols[c] for c in comp_cols],
                ]
                for comp_rows, comp_cols in scc_components
            ]

        decomposition = []

        if self.has_v0:
            decomposition.append([sorted(list(v0_rows)), sorted(list(v0_cols))])

        decomposition.extend(scc_components)

        if self.has_vinf:
            decomposition.append([sorted(list(vinf_rows)), sorted(list(vinf_cols))])

        self.decomposition = decomposition
        return decomposition

    def print_summary(self):
        """DM分解の結果を綺麗に出力"""
        if self.decomposition is None:
            print("まだDM分解が実行されていません。solve()を先に実行してください。")
            return

        print("\nDulmage-Mendelsohn分解の結果:")
        print("=" * 50)

        for i, [rows, cols] in enumerate(self.decomposition):
            if i == 0 and self.has_v0:
                component_type = "V0 (垂直成分)"
            elif i == len(self.decomposition) - 1 and self.has_vinf:
                component_type = "Vinf (無限成分)"
            else:
                # V0がない場合は強連結成分の番号をV1から開始
                scc_number = i if self.has_v0 else i + 1
                component_type = f"V{scc_number} (強連結成分)"

            print(f"\n{component_type}:")
            print("-" * 30)
            print(f"行集合 R = {[r + 1 for r in rows]}")
            print(f"列集合 C = {[c + 1 for c in cols]}")
            if rows or cols:
                print(f"サイズ  : |R| = {len(rows)}, |C| = {len(cols)}")

        print("\n" + "=" * 50)

        total_rows = sum(len(rows) for rows, _ in self.decomposition)
        total_cols = sum(len(cols) for _, cols in self.decomposition)
        print("\n統計情報:")
        print(f"総頂点数: {total_rows + total_cols}")
        print(f"総成分数: {len(self.decomposition)}")
        print(f"マッチングサイズ: {len(self.matching)}")

    def print_compact(self):
        """DM分解の結果をコンパクトに出力"""
        if self.decomposition is None:
            print("まだDM分解が実行されていません。solve()を先に実行してください。")
            return

        print("\nDM分解:")
        for i, [rows, cols] in enumerate(self.decomposition):
            if i == 0 and self.has_v0:
                component_type = "V0"
            elif i == len(self.decomposition) - 1 and self.has_vinf:
                component_type = "Vinf"
            else:
                # V0がない場合は強連結成分の番号をV1から開始
                scc_number = i if self.has_v0 else i + 1
                component_type = f"V{scc_number}"
            print(
                f"{component_type}: R={[r + 1 for r in rows]}, C={[c + 1 for c in cols]}"
            )
