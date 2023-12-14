import open3d as o3d
import numpy as np
# 创建可视化窗口
vis = o3d.visualization.Visualizer()
vis.create_window()

# 加载模型
mesh = o3d.io.read_triangle_mesh("/home/zoratt/SHINE_mapping/experiments/r3lived_incre_reg_2023-12-08_15-01-21/mesh/mesh_frame_350.ply")

# 计算顶点法向量
mesh.compute_vertex_normals()

# 将顶点法向量转换为NumPy数组
vertex_normals = np.asarray(mesh.vertex_normals)

# 将顶点法向量的值映射到[0, 1]的范围，并设置为顶点颜色
vertex_colors = (vertex_normals + 1) / 2
mesh.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

# 可视化mesh
o3d.visualization.draw_geometries([mesh])