import csv
import numpy as np

# 零初始位置时静平台位置
SP = [np.array([12, -14, 0]), np.array([12, 14, 0]), np.array([6.12435565, 17.39230485, 0]),
     np.array([-18.12435565, 3.39230485, 0]), np.array([-18.12435565, -3.39230485, 0]),
     np.array([6.12435565, -17.39230485, 0])]

# 零初始位置时动平台位置
DP = [np.array([12, -2, 0]), np.array([12, 2, 0]), np.array([-4.26794919, 11.39230485, 0]),
     np.array([-7.73205081, 9.39230485, 0]), np.array([-7.73205081, -9.39230485, 0]),
     np.array([-4.26794919, -11.39230485, 0])]

# 将数据保存到CSV文件
with open('platform_positions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['PositionType', 'X', 'Y', 'Z'])
    for b in SP:
        writer.writerow(['SP'] + list(b))
    for p in DP:
        writer.writerow(['DP'] + list(p))