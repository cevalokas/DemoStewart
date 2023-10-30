import csv
import numpy as np

def read_platform_positions_from_csv(file_path):
    SP = []
    DP = []

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            position_type, x, y, z = row
            position = np.array([float(x), float(y), float(z)])
            if position_type == 'SP':
                SP.append(position)
            elif position_type == 'DP':
                DP.append(position)

    return SP, DP

B, P = read_platform_positions_from_csv('platform_positions.csv')
print(B,P)