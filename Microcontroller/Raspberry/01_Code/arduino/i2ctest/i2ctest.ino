#include <Wire.h>
#include "MPU9250.h"
#include <Wire.h>
#include <SPI.h>


MPU9250 mpu;


void setup() {
  Wire.setSDA(20);
  Wire.setSCL(21);
  Wire1.setSDA(2);
  Wire1.setSCL(3);

  Wire.begin();
  Wire1.begin();

  Serial.begin(9600);
  Wire1.beginTransmission(0x68);
  mpu.setup(0x68);
  while(!Serial);
  if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
  }
  // put your setup code here, to run once:

}


void loop() {
  // put your main code here, to run repeatedly:
    Scani2c(1);
    if (mpu.update()) {
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 25) {
            print_roll_pitch_yaw();
            prev_ms = millis();
        }
    }
    delay(5000);
}
void Scani2c(int wireSelection){
  byte errorCode;
  byte deviceAddress;
  int totalDevices=0;

  Serial.printf("Now Scannig I2c port %d\n", wireSelection);

  for(deviceAddress=8; deviceAddress<120; deviceAddress++){
    if(wireSelection==1){
      Wire1.beginTransmission(deviceAddress);
      errorCode = Wire1.endTransmission();
    }
    else{
      Wire.beginTransmission(deviceAddress);
      errorCode = Wire.endTransmission();
    }

    if(errorCode==0){
      Serial.print("I2C device found at address 0x");
      if(deviceAddress <16){
        Serial.print("0");
      }
      Serial.println(deviceAddress,HEX);
      if(deviceAddress == 0x68){
        mpu.setup(deviceAddress);
        Wire1.beginTransmission(deviceAddress);
        return;
      }
      totalDevices++;
    }
    else if (errorCode ==4){
      Serial.print("Error at address 0x");
      if(deviceAddress<16){
        Serial.print("0");
      }
      Serial.println(deviceAddress,HEX);
    }
    if(totalDevices == 0)
    Serial.println("No I2C devies found");
    else
    Serial.printf("\n%d", totalDevices);
    if(totalDevices >0){
      if(totalDevices <2){
        Serial.println(" I2C device found");
      }
      else{
        Serial.println( " I2c devices found");
      }
      Serial.println("done\n");
    }

  }
}

void print_roll_pitch_yaw() {
    Serial.print("Yaw, Pitch, Roll: ");
    Serial.print(mpu.getYaw(), 2);
    Serial.print(", ");
    Serial.print(mpu.getPitch(), 2);
    Serial.print(", ");
    Serial.println(mpu.getRoll(), 2);
}


