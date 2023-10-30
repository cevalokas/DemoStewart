
import csv

def read_csv_to_array(file_path):
    data = []

    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 跳过第一行（标题行）

        for row in csvreader:
            data.append(row)

    return data

# 使用示例
file_path = './lib/platform_positions.csv'  # 将文件路径替换为你的CSV文件路径
result = read_csv_to_array(file_path)


for row in result:
    print("fuck")
    print(row)