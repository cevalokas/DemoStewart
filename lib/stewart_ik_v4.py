import numpy as np
import csv
import math
from stewart_algorithm import Stewart_Platform

def readPlatform(file_path): # 读初始坐标, 中心不对称
    SP = []
    DP = []

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            position_type, x, y, z = row
            position = np.array([float(x), float(y), float(z)])
            if position_type == 'SP':
                SP.append(position)
            elif position_type == 'DP':
                DP.append(position)

    return SP, DP

def readStateCMD(file_path): #读位置状态指令
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        line_count = 0
        for row in reader:
            line_count += 1
        T = np.zeros(line_count)
        X = np.zeros([line_count,3])
        V = np.zeros([line_count,3])
        csvfile.seek(0)  # 重置文件指针到文件开头
        next(reader)  # 跳过第一行
        for i, row in enumerate(reader):
            T[i] = float(row[0])  
            X[i] = [float(row[1]), float(row[2]), float(row[3])]
            V[i] = [float(row[4]), float(row[5]), float(row[6])]
            
    return T, X, V, line_count

def refresh(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        new_rows = [rows[0]]  # 保留CSV文件的第一行
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_rows)
    except FileNotFoundError:
        print(f"CSV file '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def stewart_ideal(X, V, lc, T): #平台中心对称，逆运动学

  L1 = 85.0  # 长边（螺杆）的长度mm
  L2 = 20.0  # 短边（转角）的长度mm
  r_S = 50  #底座半径
  r_D = 35  #平台半径
  Psi_S = np.pi/6  #底座上两个锚点之间角度的一半
  Psi_D = np.pi/6  #平台上两个锚点之间角度的一半
  ref_rotation = 0 #平台相对旋转

  PWM = np.zeros([lc,7])
  for k in range(lc):
    platform = Stewart_Platform(r_S, r_D, L2, L1, Psi_S, Psi_D, ref_rotation)
    servo_angles = platform.calculate( np.array([X[k,0],X[k,1],X[k,2]]), np.array([V[k,0], V[k,1], V[k,2]]) )
    PWM[k,0] = T[k]
    for i in range(1, 6):
        num = (500 + servo_angles[i]*2000/math.pi).astype(int)
        PWM[k, i] = int(num)

  return PWM


def stewart_odd(X, V, DP, SP,lc): #平台不中心对称，逆运动学
  L1 = 80.0  # 长边（螺杆）的长度
  L2 = 20.0  # 短边（转角）的长度
  PWM = np.zeros([lc,7])

  for k in range(lc):
    a, b, g = V[k,0], V[k,1], V[k,2]
    L = np.zeros(6)
    RX = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    RY = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    RZ = np.array([[np.cos(g), -np.sin(g), 0], [np.sin(g), np.cos(g), 0], [0, 0, 1]])
    R = np.dot(RZ, np.dot(RY, RX))

    for i in range(6): #计算对应两点距离
        #print(X[k] + np.dot(R, DP[i]) - SP[i])#test
        L[i] = np.linalg.norm(X[k] + np.dot(R, DP[i]) - SP[i])
    #print(L)#test

    cos_angle = np.zeros(6)
    angle = np.zeros(6)

    for i in range(6): # 使用余弦定理计算每个角的余弦值
        cos_angle[i] = (L2**2 + L[i]**2 - L1**2) / (2 * L2 * L[i])
        print(cos_angle[i])#test

    for i in range(6):# 使用反余弦函数计算每个角的弧度
        angle[i] = math.acos(cos_angle[i])
    #to do 有三个是反过来的

    for i in range(1, 6):
        PWM[k, i] = int(500 + angle[i]*2000/math.pi)

  return PWM

def writePWM(file_path, PWM):  #输出PWN信号
    with open(file_path, 'a', newline='') as csvfile:  # 'a' 模式以附加
        writer = csv.writer(csvfile)
        writer.writerow(PWM) #注意是单行还是多行




if __name__ == '__main__':
    SP, DP = readPlatform("./lib/platform_positions.csv")
    T, X, V, lc = readStateCMD("./lib/state_cmd.csv")
    PWM = stewart_odd(X, V, DP, SP, lc)
    #PWM = stewart_ideal(X, V, lc, T)  
    refresh("./lib/pwm_cmd.csv")
    writePWM("./lib/pwm_cmd.csv",PWM)

