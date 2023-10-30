import csv
import serial
import time

def send_servo_commands_from_csv(ser_port, file_path):
  try:
    # 创建串口连接
    ser = serial.Serial(ser_port, 9600)  

    # 打开CSV文件
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)        
        next(csv_reader)# 跳过标题行
        
        for row in csv_reader:
            cmd = [int(cell) for cell in row]             
            byte_array = bytearray()
            
            for i in range(1, len(cmd)):
                byte_array.append(0x01)
                byte_array.append(i & 0xFF)
                low_byte = cmd[i] & 0xFF
                high_byte = (cmd[i] >> 8) & 0xFF
                byte_array.append(high_byte)
                byte_array.append(low_byte)
            print(byte_array)#测试用
            ser.write(byte_array)
            time.sleep(cmd[0]/1000)

        # 关闭串口连接
        ser.close()
        return True
  except Exception as e:
      print(f"Error: {e}")
      return False


if __name__ == '__main__':
  file_path = './lib/pwm_cmd.csv'  
  ser_port = 'COM3'  
  success = send_servo_commands_from_csv(ser_port, file_path)
  if success:
      print("Commands sent successfully.")
  else:
      print("Failed to send commands.")