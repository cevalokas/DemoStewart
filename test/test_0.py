import csv

def writePWM(file_path, PWM):  #输出PWN信号
    with open(file_path, 'a') as csvfile:  # 'a' 模式以附加
        writer = csv.writer(csvfile)
        writer.writerow(PWM)

writePWM("./lib/pwm_cmd.csv", [1,2,3,4,5])