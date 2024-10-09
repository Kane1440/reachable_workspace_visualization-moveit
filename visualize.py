import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 读取文件
points = np.loadtxt("points.txt")

# 提取 x, y, z 坐标
x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

# 创建 3D 图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 根据 z 坐标生成颜色渐变
norm = plt.Normalize(z.min(), z.max())
colors = cm.viridis(norm(z))  # 使用 Viridis 颜色映射

# 绘制点
ax.scatter(x, y, z, c=colors, marker='o')

# 设置坐标轴标签
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# 设置坐标轴尺度一致
max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
mid_x = (x.max()+x.min()) * 0.5
mid_y = (y.max()+y.min()) * 0.5
mid_z = (z.max()+z.min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# 添加坐标轴
ax.quiver(0, 0, 0, 1, 0, 0, color='r', arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, 0, 1, 0, color='g', arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, 0, 0, 1, color='b', arrow_length_ratio=0.1)

# 显示图形
plt.colorbar(ax.scatter(x, y, z, c=colors, marker='o'), ax=ax, label='Z value')  # 添加颜色条
plt.show()
