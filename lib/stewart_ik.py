import numpy as np
import csv
import math


def readPlatform(file_path): # 读初始位置
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

def readState(file_path): #读位置状态指令
    X = []
    V = []

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            position_type, x, y, z = row
            position = np.array([float(x), float(y), float(z)])
            if position_type == 'SP':
                X.append(position)
            elif position_type == 'DP':
                V.append(position)

    return X, V

def stewart_ik_algebra(X, a, b, g, DP, SP): #逆运动学解舵机PWM
  L = np.zeros(6)
  RX = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
  RY = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
  RZ = np.array([[np.cos(g), -np.sin(g), 0], [np.sin(g), np.cos(g), 0], [0, 0, 1]])
  R = np.dot(RZ, np.dot(RY, RX))

  for i in range(6): #计算对应两点距离
    L[i] = np.linalg.norm(X + np.dot(R, DP[i]) - SP[i])

  a = 5.0  # 替换为长边（螺杆）的长度
  b = 4.0  # 替换为短边（转角）的长度
  cos_angle_A = np.zeros(6)
  angle_A = np.zeros(6)

  for i in range(6): # 使用余弦定理计算每个角的余弦值
    cos_angle_A[i] = (b**2 + L[i]**2 - a**2) / (2 * b * L[i])

  for i in range(6):# 使用反余弦函数计算每个角的度数
    angle_A[i] = math.degrees(math.acos(cos_angle_A[i]))

  PWM = degree2PWM(angle_A)

  return PWM

def degree2PWM(angles):
  PWM = np.zeros(6)
  for i in range(6):
    PWM[i] = 500 + angles[i]*2000/180
  return PWM


def covert_status2Cmd(statusFilePath, savePath=None, csvHeader="ServoIndex, targetPulseWidth"):
    statuses = np.genfromtxt(statusFilePath, delimiter=',')[1:]
    cmdlist = []
    lastStatus = np.full((22,), 1500.0)
    
    for status in statuses:
        # figure out the servo changed
        for idx, state in enumerate(status): 
            if (lastStatus[idx]!=state and idx != 0):
                cmdlist.append([idx-1,state])

        cmdlist.append([-1,status[0]]) # get delay

        lastStatus = status

    if savePath != None:
        np.savetxt(savePath, np.array(cmdlist), 
                   fmt="%d", 
                   delimiter=",",
                   newline="\n", 
                   header=csvHeader, 
                   comments='')

    return np.array(cmdlist)
    
def loadCmd(cmdFilePath):
    return np.genfromtxt(cmdFilePath, delimiter=',')[1:]



if __name__ == '__main__':
  SP, DP = readPlatform("platform_positions.csv")
  X, V = readState("state_cmd.csv")
  PWM = stewart_ik_algebra(X, V[0], V[1], V[2], DP, SP)  
  
  covert_status2Cmd(statusFilePath="Demo1Status.csv", savePath="Demo1CMD.csv")
  type_cmds = "pulseWidth"
  arr_cmds = loadCmd("Demo1CMD.csv")


"[12. 12. 12. 12. 12. 12.]"
"[12.16552506 12.16552506 10.31652948 13.76841382 13.76841382 10.31652948]"
"[12.16552506 12.16552506 13.76841382 10.31652948 10.31652948 13.76841382]"
"[14.         10.         11.13552872 13.11487704 11.13552872 13.11487704]"
"[12.16552506 12.16552506 12.16552506 12.16552506 12.16552506 12.16552506]"