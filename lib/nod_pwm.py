import time
import math
from stewart_ik_v4 import refresh, writePWM


def neckNod(file_path):
  max_pulse = 2500 
  min_pulse = 500
  mid_pulse = 1500
  pos = 1500
  quickness = 10

  refresh(file_path)
  
  while (pos >= min_pulse):
    PWM = [50, pos, 1500, pos, 3000 - pos, 1500, 3000 - pos]
    writePWM(file_path, PWM)
    pos = pos - quickness
  pos = pos + quickness
  while (pos <= max_pulse):
    PWM = [50, pos, 1500, pos, 3000 - pos, 1500, 3000 - pos]
    writePWM(file_path, PWM)
    pos = pos + quickness
  pos = pos + quickness
  while (pos >= mid_pulse):
    PWM = [50, pos, 1500, pos, 3000 - pos, 1500, 3000 - pos]
    writePWM(file_path, PWM)
    pos = pos - quickness

  writePWM(file_path, PWM)




if __name__ == '__main__':
  neckNod("./lib/pwm_cmd.csv")
