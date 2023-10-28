import numpy as np
import math

# 运动学参数
# 零初始位置时静平台位置（相对于静平台坐标系）
B1 = np.array([12, -14, 0])
B2 = np.array([12, 14, 0])
B3 = np.array([6.12435565, 17.39230485, 0])
B4 = np.array([-18.12435565, 3.39230485, 0])
B5 = np.array([-18.12435565, -3.39230485, 0])
B6 = np.array([6.12435565, -17.39230485, 0])

# 零初始位置时动平台位置（相对于动平台坐标系）
P1 = np.array([12, -2, 0])
P2 = np.array([12, 2, 0])
P3 = np.array([-4.26794919, 11.39230485, 0])
P4 = np.array([-7.73205081, 9.39230485, 0])
P5 = np.array([-7.73205081, -9.39230485, 0])
P6 = np.array([-4.26794919, -11.39230485, 0])

def stewart_ik_algebra(x, y, z, a, b, g):
    L = np.zeros(6)
    X = np.array([x, y, z])
    RX = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    RY = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    RZ = np.array([[np.cos(g), -np.sin(g), 0], [np.sin(g), np.cos(g), 0], [0, 0, 1]])
    R = np.dot(RZ, np.dot(RY, RX))

    l1 = np.linalg.norm(X + np.dot(R, P1) - B1)
    l2 = np.linalg.norm(X + np.dot(R, P2) - B2)
    l3 = np.linalg.norm(X + np.dot(R, P3) - B3)
    l4 = np.linalg.norm(X + np.dot(R, P4) - B4)
    l5 = np.linalg.norm(X + np.dot(R, P5) - B5)
    l6 = np.linalg.norm(X + np.dot(R, P6) - B6)
    L = np.array([l1, l2, l3, l4, l5, l6])

    return L

# 测试示例
'''
x = -2
y = 0
z = 0
a = 0
b = 0
g = 0
result = stewart_ik_algebra(x, y, z, a, b, g)
print(result)
'''

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
    

"[12. 12. 12. 12. 12. 12.]"
"[12.16552506 12.16552506 10.31652948 13.76841382 13.76841382 10.31652948]"
"[12.16552506 12.16552506 13.76841382 10.31652948 10.31652948 13.76841382]"
"[14.         10.         11.13552872 13.11487704 11.13552872 13.11487704]"
"[12.16552506 12.16552506 12.16552506 12.16552506 12.16552506 12.16552506]"