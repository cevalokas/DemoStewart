/**

 * 在ESP32上测试脖子
*/

#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>
#include <SPI.h>

#define CMD_LENGTH 4

#define PCA9685_ADDR_1 0x60
#define PCA9685_SERVO_FREQUENCY_1 50
#define PCA9685_OSCILLATOR_FREQUENCY_1 25300000


Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(PCA9685_ADDR_1); 
//Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(PCA9685_ADDR_2); 

void onRecv_sendServoCMD(); // 中断回调函数

void debbugingInfo(int boardNum, int pinNum, int pulseWidth);

void set_servo_pulseWidth(Adafruit_PWMServoDriver &pwmBoard, int pinNum, int pulseWidth);
void set_servo_angle(Adafruit_PWMServoDriver &pwmBoard, int pinNum, float angle);

void setup()
{
  Serial.begin(115200);
  Serial.setRxFIFOFull(CMD_LENGTH); // 设置串口接收缓冲区满的阈值，超过阈值会触发中断，发送舵机控制命令
  Serial.onReceive(onRecv_sendServoCMD, false); // 中断的方式处理来自串口的指令
  delay(500);

  Wire.begin();
  Serial.println("\nI2C Scanner");

  byte error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknown error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
  delay(1000);  
  Serial.print("i2c devices found:");
  Serial.println(nDevices);
  Wire.end();
  delay(3000); 

  pwm1.begin();
  pwm1.setOscillatorFrequency(PCA9685_OSCILLATOR_FREQUENCY_1); // Set the PWM oscillator frequency, used for fine calibration
  pwm1.setPWMFreq(PCA9685_SERVO_FREQUENCY_1);       // Set the servo operating frequency
  delay(100);

}

void loop()
{
  delay(100000);

}

void onRecv_sendServoCMD()
{
  // read cmd from serial
  uint8_t buff[CMD_LENGTH];
  int count = Serial.read(buff, CMD_LENGTH);

  // send vaild cmd to PCA9685
  if (count == CMD_LENGTH){
    if (buff[0] == 0x01){
      // set servo cammand
      u_int8_t pinNum = buff[1] & 0x0F;
      int boardNum = buff[1] >> 4;
      u_int16_t pulseWidth = buff[2]*256 + buff[3];
      
      debbugingInfo(boardNum, pinNum, pulseWidth); // For debugging

      if (boardNum == 0){
        set_servo_pulseWidth(pwm1, pinNum, pulseWidth);
      }

    } else if (buff[0] == 0x02){
      // to do: set_servo_angle
      Serial.printf("[To-do] set_servo_angle() ");

    } else {
      // invaild cmd
      Serial.printf("[CMD-ERROR] Invalid Command!");
    }

  } else {
    // Cmd length error
    Serial.printf("[CMD-ERROR] Command Length Error!");
  }
}


void debbugingInfo(int boardNum, int pinNum, int pulseWidth) {
  String value_info = "[SERVO-CMD] boardNum:";
  value_info = value_info + boardNum;

  value_info = value_info + " pinNum:";
  value_info = value_info + pinNum;

  value_info = value_info + " pulseWidth:";
  value_info = value_info + pulseWidth;
  Serial.println(value_info);
}

void set_servo_pulseWidth(Adafruit_PWMServoDriver &pwmBoard, int pinNum, int pulseWidth) {
  // send cmd by IIC
  pwmBoard.setPWM(pinNum, 0, pulseWidth);
}

void set_servo_angle(Adafruit_PWMServoDriver &pwmBoard, int pinNum, float angle, float minAngle=0.0, float maxAngle=180.0, float minPulseWidth=500, float maxPulseWidth=2500, int freq=PCA9685_SERVO_FREQUENCY_1){
  /* 调用set_servo_pulseWidth */
  // 确认角度范围
  angle = constrain(angle, minAngle, maxAngle);
  
  // 计算脉冲长度
  float pulseWidth_us = map(angle, minAngle, maxAngle, minPulseWidth, maxPulseWidth); 

  // Set the servo position
  pwmBoard.setPWM(pinNum, 0, int((pulseWidth_us * freq * 4096) / 1000000));
}


