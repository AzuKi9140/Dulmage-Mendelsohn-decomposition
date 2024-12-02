from modules import BipartiteMatching, IOTable, MaximumFlow
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
# matrix = np.array(
#     [
#         [0, 1, 0, 0, 0],  # 頂点1からの辺（6-10への接続）
#         [0, 1, 0, 0, 0],  # 頂点2からの辺
#         [0, 1, 0, 0, 0],  # 頂点3からの辺
#         [0, 0, 1, 1, 1],  # 頂点4からの辺
#         [1, 1, 0, 0, 0],  # 頂点5からの辺
#     ]
# )

# matrix = np.array(
#     [
#         [1, 1, 1, 0, 0, 0, 0],  # 頂点1からの辺（6-10への接続）
#         [0, 0, 1, 1, 0, 1, 0],  # 頂点2からの辺
#         [0, 0, 0, 1, 1, 0, 0],  # 頂点3からの辺
#         [0, 0, 0, 1, 1, 0, 1],  # 頂点4からの辺
#         [0, 0, 0, 0, 0, 1, 1],  # 頂点5からの辺
#         [0, 0, 0, 0, 0, 0, 1],  # 頂点6からの辺
#         [0, 0, 0, 0, 0, 0, 1],  # 頂点7からの辺
#     ]
# )

io_table = IOTable("data/io_table.xlsx")
# io_table.get_filtered_intermediate(90)
# io_table.get_filtered_intermediate(30, by_row=True)
io_table.filter_by_count(20, by_row=True)
matrix = io_table.filtered_intermediate_df.to_numpy()
matrix = io_table.filtered_intermediate_df.to_numpy()
matrix[matrix != 0] = 1  # 0以外の値をすべて1に置き換え
print(matrix)

bipartite_matching = BipartiteMatching(matrix)
# bipartite_matching.solve()

maximum_flow = MaximumFlow(matrix)
maximum_flow.solve()
print(len(maximum_flow.matching))

dm_decomposition = DMDecomp(matrix, maximum_flow.matching)
dm_decomposition.solve()
dm_decomposition.print_summary()
