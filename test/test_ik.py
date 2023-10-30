import numpy as np
import math

def stewart_ik_algebra(a, b, g): #逆运动学解舵机PWM
  L = np.zeros(6)
  RX = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
  RY = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
  RZ = np.array([[np.cos(g), -np.sin(g), 0], [np.sin(g), np.cos(g), 0], [0, 0, 1]])
  R = np.dot(RZ, np.dot(RY, RX))

  print(RX, RY, RZ)

if __name__ == '__main__':
  stewart_ik_algebra(math.pi/4,math.pi/4,math.pi/4)
  #stewart_ik_algebra(30,60,45)