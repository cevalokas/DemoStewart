import numpy as np
import time
from scipy.spatial.transform import Rotation as R
from math import *
from vpython import *

def covert_status2Cmd(statusFilePath, savePath=None, csvHeader="ServoIndex, targetPulseWidth"):
    statuses = np.genfromtxt(statusFilePath, delimiter=',')[1:]
    cmdlist = []
    lastStatus = np.full((22,), 1500.0)
    
    for status in statuses:
        # figure out the servo changed
        for idx, state in enumerate(status): 
            if (lastStatus[idx]!=state and idx != 0):
                cmdlist.append([idx,state])

        cmdlist.append([0,status[0]]) # get delay

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
    print("###### HumanoidController Demo Started #######")

    covert_status2Cmd(statusFilePath="Demo1Status.csv", savePath="Demo1CMD.csv")

    type_cmds = "pulseWidth"
    arr_cmds = loadCmd("Demo1CMD.csv")

    humanoidRobot = HumanoidController.HumanoidServoController(USBPort='/dev/ttyUSB0', servoInfoPath="Demo1ServoInfo.csv")

    for cmd in arr_cmds:
        if cmd[0]!=0:
            if type_cmds == "pulseWidth":
                humanoidRobot.sendcmd_PulseWidth(cmd[0],cmd[1])
        else:
            time.sleep(cmd[1]/1000) # servoIndex = 0 是停顿间隔,单位s

    print("##### HumanoidController Demo Terminated #####")