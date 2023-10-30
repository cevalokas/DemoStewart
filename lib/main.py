import csv
import serial
import struct
import time

def send_servo_commands_from_csv(ser_port, csv_file_path):

    try:
        # 创建串口连接
        ser = serial.Serial(ser_port, 9600)  

        # 打开CSV文件
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # 跳过标题行

            # 定义协议格式
            instruction_format = '>BBI'  # 大端模式，两个字节 + 两个双字节

            # 从CSV文件读取数据并发送指令
            for row in csv_reader:
                pinNum, pulseWidth = int(row[0]), int(row[1])
                instruction = struct.pack(instruction_format, 0x01, pinNum, pulseWidth)
                ser.write(instruction)
                time.sleep(cmd[1]/1000)

        # 关闭串口连接
        ser.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == '__main__':
  csv_file_path = 'your_csv_file.csv'  # 替换为你的CSV文件路径
  ser_port = 'COMx'  # 替换为你的串口名称
  success = send_servo_commands_from_csv(ser_port, csv_file_path)
  if success:
      print("Commands sent successfully.")
  else:
      print("Failed to send commands.")