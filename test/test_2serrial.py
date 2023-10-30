import csv

import time
file_path = './lib/pwm_cmd.csv' 


with open(file_path, 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    # 跳过标题行
    next(csv_reader)
    
    for row in csv_reader:
        cmd = [int(cell) for cell in row]  # 将每个单元格的内容转换为整数
        
        byte_array = bytearray()
        
        for i in range(1, len(cmd)):
            byte_array.append(0x01)
            byte_array.append(i & 0xFF)
            low_byte = cmd[i] & 0xFF
            high_byte = (cmd[i] >> 8) & 0xFF
            byte_array.append(high_byte)
            byte_array.append(low_byte)
        
        print(byte_array)

        time.sleep(cmd[0]/1000)