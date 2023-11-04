import time
import math
import numpy as np
from stewart_ik_v4 import refresh, writePWM


def neckNod(file_path):
  max_pulse = 2000 
  min_pulse = 1000
  mid_pulse = 1500
  pos = 1500
  quickness = 10
  t = 25

  refresh(file_path)
  
  while (pos >= min_pulse):
    PWM_time = np.array([t, pos, 3000-pos, pos, 3000-pos, pos, 3000-pos])
    PWM = np.copy(PWM_time)
    PWM[1:] = PWM[1:]*4096/20000
    writePWM(file_path, PWM)
    pos = pos - quickness
  pos = pos + quickness
  while (pos <= max_pulse):
    PWM_time = np.array([t, pos, 3000-pos, pos, 3000-pos, pos, 3000-pos])
    PWM = np.copy(PWM_time)
    PWM[1:] = PWM[1:]*4096/20000
    writePWM(file_path, PWM)
    pos = pos + quickness
  pos = pos + quickness
  while (pos >= mid_pulse):
    PWM_time = np.array([t, pos, 3000-pos, pos, 3000-pos, pos, 3000-pos])
    PWM = np.copy(PWM_time)
    PWM[1:] = PWM[1:]*4096/20000
    writePWM(file_path, PWM)
    pos = pos - quickness






if __name__ == '__main__':
  neckNod("./lib/pwm_cmd.csv")
