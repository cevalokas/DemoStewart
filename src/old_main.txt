#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>                           
#include <SPI.h>
#include <HardwareSerial.h>
#include <pthread.h>


Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x60); // Create an object of board 1
int servoFrequency = 50;
int orders[21] = {307}; // 初始化保证安全

// Put function declarations here:
void readSerial();
// int t2t(int); // 让上位机干

void setup() {
  Wire.begin(21, 22); // Initialize I2C on ESP32 (SDA on GPIO21, SCL on GPIO22)

  pwm1.begin();
  pwm1.setOscillatorFrequency(25300000); // Set the PWM oscillator frequency, used for fine calibration
  pwm1.setPWMFreq(servoFrequency);       // Set the servo operating frequency

  Serial.begin(9600); // Initialize serial communication
  for (int i = 0; i < 6; i++) {
    pwm1.setPWM(i, 0, orders[i]);
  }

  delay(1000);
}

void loop() {
  // Put your main code here, to run repeatedly:
  
  readSerial();
  // 向两块板发信号
  for (int i = 0; i < 11; i++) {
    pwm1.setPWM(i, 0, orders[i]);
  }

  delay(10);
}

// 接收串口数据（单字节），转化为整型
void readSerial() {
  if (Serial.available()) { // 确保至少有字节可用
    byte byteArray[6]; // 创建一个存储字节的数组

    // 从串行端口读取12个字节
    Serial.readBytes(byteArray, 12);

    // 将字节数组中的数据转换为整数数组
    for (int i = 0; i < 21; i++) {
      orders[i] = (byteArray[i * 2 + 1] << 8) | byteArray[i * 2];
    }
  }
}

/*
int t2t(int time){
  float tick = time/20000*4096 ;
  return tick;
}
*/
