#include <Wire.h>
#include <SFE_BMP180.h>

SFE_BMP180 bmp180;

void setup() {
  Serial.begin(9600);
  bool baglanti = bmp180.begin();

  if (baglanti) {
    Serial.println("BMP180 baglanti saglandi");
  }
}

void loop() {

  char status;
  double T, P;
  bool baglanti = false;

  status = bmp180.startTemperature();

  if (status != 0) {
    delay(1000);
    status = bmp180.getTemperature(T);

    if (status != 0) {
      status = bmp180.startPressure(3);

      if (status != 0) {
        delay(status);
        status = bmp180.getPressure(P, T);

        if (status != 0) {
          Serial.print("Basınc: ");
          Serial.print(P);
          Serial.println(" hPa");

          Serial.print("Sıcaklık: ");
          Serial.print(T);
          Serial.println(" C");
        }
      }
    }
  }
}
