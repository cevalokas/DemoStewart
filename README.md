# Demo_Stewart

# 1. 硬件结构
使用ESP32驱动单个PCA9685芯片驱动6个舵机

# 2. 数据
数据以csv格式存储，主要有三部分：
- platform_positions.csv: 硬件状态信息，包括
  - "SP, X, Y, Z" 六个马达的坐标
  - "DP, X, Y, Z" 动平面上六个连动点坐标
- state_cmd.csv: 目标姿态指令
  - "DelayTime, x, y, z, a, b, c" 延时，三维坐标和绕三个坐标轴旋转的角度
- pwm_cmd.csv: 对每个舵机的pwm信号指令
  - "DelayTime, S0, S1, S2, S3, S4, S5"


# 3. 软件结构
## 接口协议
使用 `pyserial` 库，通过USB向ESP32发送指令。单条指令 4Bytes（指令位(1Byte)+数据位(3Bytes)），协议如下：

| 指令 Instruction         | 指令位 Code | 数据位 Data                                     |
| ------------------------ | ----------- | ----------------------------------------------- |
| 复原                     | 0x00        | to do                                           |
| 控制舵机角度(pulseWidth) | 0x01        | boardNum(4bits)+pinNum(4bits)+pulseWidth(8bits) |0

## stewart_ik.py
逆运动学变换，读硬件状态和目标姿态，解出对应PWM信号，存到“pwm_cmd.csv”

## main.py
读取pwm_cmd.csv, 转换协议发送到serrial

## main.cpp
通过串口，接受来自上位机（python）的命令。串口中断，执行回调函数 `onRecv_sendServoCMD()`，实现向 PCA9685 芯片发送 IIC 的指令。