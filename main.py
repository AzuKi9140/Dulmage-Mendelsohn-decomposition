import numpy as np

from modules import BipartiteMatching, MaximumFlow
from modules import DulmageMendelsohnDecomposition as DMDecomp

# matrix = np.array(
#     [
#         [1, 1, 1, 0, 0, 0, 1, 0],
#         [1, 0, 1, -1, 0, 1, 0, -2],
#         [0, 1, 0, 0, 0, 0, 2, 0],
#         [0, 3, 0, 1, -1, 0, 0, 0],
#         [0, 1, 1, 0, 0, 0, 0, 0],
#         [-2, 0, 0, -3, 2, -1, 0, 3],
#         [0, 0, 1, 0, 0, 0, -1, 0],
#         [0, 0, 2, -1, 3, 0, 2, 0],
#     ]
# )

# 5x5の隣接行列を作成
matrix = np.array(
    [
        [0, 1, 0, 0, 0],  # 頂点1からの辺（6-10への接続）
        [0, 1, 0, 0, 0],  # 頂点2からの辺
        [0, 1, 0, 0, 0],  # 頂点3からの辺
        [0, 0, 1, 1, 1],  # 頂点4からの辺
        [1, 1, 0, 0, 0],  # 頂点5からの辺
    ]
)

print(matrix)

bipartite_matching = BipartiteMatching(matrix)
bipartite_matching.solve()

maximum_flow = MaximumFlow(matrix)
maximum_flow.solve()
print(maximum_flow.matching)

dm_decomposition = DMDecomp(matrix, maximum_flow.matching)
dm_decomposition.solve()
dm_decomposition.print_summary()
