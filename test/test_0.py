import numpy as np

# 创建一个示例NumPy数组
array = np.array([1, 2, 3, 4, 5])

# 选择要乘以的因子
factor = 2

# 使用NumPy进行数组乘法，从第二个元素开始
result = np.copy(array)
result[1:] = result[1:] * factor

print(result)