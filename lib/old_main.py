import serial
import csv
import time

# ser为串口对象，后续调用均用点运算符
ser = serial.Serial('COM4', 9600, 8, 'N', 1) # 接口, 波特率, bytesize=8, parity='N', stopbits=1
flag = ser.is_open
file = "./lib/pwm_cmd.csv"

def print_hex_array(byte_array):#调试用
    for byte in byte_array:
        hex_value = hex(byte)[2:]  # 将byte转换为十六进制表示（去掉前缀'0x'）
        if len(hex_value) == 1:
            hex_value = '0' + hex_value  # 确保十六进制值始终是两位数
        print(hex_value, end=' ')

# 打开txt文件，按行读取整数并发送
with open(file, 'r', newline='') as csvfile:
    #time.sleep(2)
    fire = csv.reader(csvfile)
    next(file)
    for line in file:
        # 将每一行的内容分割成整数列表
        int_array = [int(x) for x in line.split()]
        print(int_array)#调试用

        # 将时间转换成12位指令
        for i in range(1, 7):
          int_array[i] = int(int_array[i]*4096/20000)

        #print(int_array)#调试用
        
        # 创建一个字节数组来存储截取的最小两个字节
        byte_array = bytearray()

        # 截取数组中每个整数的最小两个字节并添加到字节数组中
        for i in range(1, len(int_array)):  # 从第二个元素开始（int_array[1]）
          num = int_array[i]
          low_byte = num & 0xFF
          high_byte = (num >> 8) & 0xFF
          byte_array.append(low_byte)
          byte_array.append(high_byte)
          print_hex_array(byte_array)#调试用
          print(byte_array)#调试用

        
        #print_hex_array("\n")#调试用

        # 发送整个字节数组到串口
        ser.write(byte_array)

        # 持续时间内暂停
        time.sleep(int_array[0]/1000)

# 关闭串口连接
ser.close()