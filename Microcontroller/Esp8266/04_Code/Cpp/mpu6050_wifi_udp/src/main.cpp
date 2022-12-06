#include <Wire.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_HMC5883_U.h>
#include <ArduinoJson.h>
#include <Kalman.h>

// Sensor Configuring
Adafruit_MPU6050 mpu6050;
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
#define RESTRICT_PITCH

Kalman kalmanX, kalmanY, kalmanZ; // Create the Kalman instances
const uint8_t HMC5883L = 0x1E;    // Address of magnetometer
/* IMU Data */
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;
double magX, magY, magZ;
int16_t tempRaw;

double roll, pitch, yaw;

double gyroXangle, gyroYangle, gyroZangle; // Angle calculate using the gyro only
double compAngleX, compAngleY, compAngleZ; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY, kalAngleZ;    // Calculated angle using a Kalman filter
uint32_t timer;
uint8_t i2cData[14]; // Buffer for I2C data

#define MAG0MAX 603
#define MAG0MIN -578

#define MAG1MAX 542
#define MAG1MIN -701

#define MAG2MAX 547
#define MAG2MIN -556

float magOffset[3] = {(MAG0MAX + MAG0MIN) / 2, (MAG1MAX + MAG1MIN) / 2, (MAG2MAX + MAG2MIN) / 2};
double magGain[3];

// Wifi Configuration
char const *ssid = "Ergo-Proxy";
char const *password = "Mayer-Re-l";

// Udp Configuration
WiFiUDP Udp;
char const *udp_ip = "10.10.10.10";
int udp_port = 4455;
bool send_json = true;

// Prototype defination
void wifiSetup(char const *_ssid = ssid, char const *_password = password);
void udpSetup(int _udp_port = udp_port, bool test = false);
void udpSend(String _message = "test", int _delay_ms = 10);
void calibrateMag();
void sensorSetup(int _loop_delay = 10);
void updateSensor();
void updateYaw();
void updatePitchRoll();
void updateMPU6050();
void updateHMC5883L();

String sensorGetJson();

// Setup  event
void setup()
{
    Serial.begin(115200);
    Wire.begin();

    calibrateMag();

    sensorSetup();
    wifiSetup();
    udpSetup();
}
// Loop event
void loop()
{
    udpSend(sensorGetJson());
    delay(100);
}
// Configuration of wireless
void wifiSetup(char const *_ssid, char const *_password)
{
    Serial.printf("Connecting to %s ", _ssid);
    WiFi.begin(_ssid, _password);         // wifi ap configuring
    while (WiFi.status() != WL_CONNECTED) // wifi connection status check
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected.");
}
// Configuration of Udp socket
void udpSetup(int _udp_port, bool test)
{
    Udp.begin(_udp_port); // Udp port configuring
    Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), udp_port);
    if (test)
        udpSend(); // Udp test packed
}
// Udp send message
void udpSend(String message, int delay_ms)
{
    Udp.beginPacket(udp_ip, udp_port);
    Udp.write(message.c_str());
    Udp.endPacket();
    // Serial.printf("Sending packet: %s\n", message.c_str());
    delay(delay_ms);
}

String sensorGetJson()
{
    updateSensor();
    StaticJsonDocument<1024> static_json_document;

    // Get acceleration values
    static_json_document["roll"] = roll;
    static_json_document["pitch"] = pitch;
    static_json_document["yaw"] = yaw;

    char doc_buffer[1024];
    serializeJson(static_json_document, doc_buffer);

    return String(doc_buffer);
}

void sensorSetup(int _loop_delay)
{
    Serial.printf("Mpu6050 starting\n");
    while (!mpu6050.begin())
    {
        delay(_loop_delay);
    }
    Serial.printf("Mpu6050 found.\n");

    Serial.printf("HMC5883 starting\n");
    while (!mag.begin())
    {
        delay(_loop_delay);
    }
    Serial.printf("HMC5883 found.\n");

    mpu6050.setHighPassFilter(MPU6050_HIGHPASS_0_63_HZ);
    mpu6050.setMotionDetectionThreshold(1);
    mpu6050.setMotionDetectionDuration(20);
    mpu6050.setInterruptPinLatch(true);
    mpu6050.setInterruptPinPolarity(true);
    mpu6050.setMotionInterrupt(true);

    calibrateMag();
    delay(100); // Wait for sensors to stabilize

    /* Set Kalman and gyro starting angle */
    updateMPU6050();
    updateHMC5883L();
    updatePitchRoll();
    updateYaw();

    kalmanX.setAngle(roll); // First set roll starting angle
    gyroXangle = roll;
    compAngleX = roll;

    kalmanY.setAngle(pitch); // Then pitch
    gyroYangle = pitch;
    compAngleY = pitch;

    kalmanZ.setAngle(yaw); // And finally yaw
    gyroZangle = yaw;
    compAngleZ = yaw;

    timer = micros(); // Initialize the timer

    Serial.print("Mpu6050 configured.\n");
}

void updateSensor()
{
    /* Update all the IMU values */
    updateMPU6050();
    updateHMC5883L();

    double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
    timer = micros();

    /* Roll and pitch estimation */
    updatePitchRoll();
    double gyroXrate = gyroX / 131.0; // Convert to deg/s
    double gyroYrate = gyroY / 131.0; // Convert to deg/s

    // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
    if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90))
    {
        kalmanX.setAngle(roll);
        compAngleX = roll;
        kalAngleX = roll;
        gyroXangle = roll;
    }
    else
        kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter

    if (abs(kalAngleX) > 90)
        gyroYrate = -gyroYrate; // Invert rate, so it fits the restricted accelerometer reading
    kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt);

    /* Yaw estimation */
    updateYaw();
    double gyroZrate = gyroZ / 131.0; // Convert to deg/s
    // This fixes the transition problem when the yaw angle jumps between -180 and 180 degrees
    if ((yaw < -90 && kalAngleZ > 90) || (yaw > 90 && kalAngleZ < -90))
    {
        kalmanZ.setAngle(yaw);
        compAngleZ = yaw;
        kalAngleZ = yaw;
        gyroZangle = yaw;
    }
    else
        kalAngleZ = kalmanZ.getAngle(yaw, gyroZrate, dt); // Calculate the angle using a Kalman filter

    /* Estimate angles using gyro only */
    gyroXangle += gyroXrate * dt; // Calculate gyro angle without any filter
    gyroYangle += gyroYrate * dt;
    gyroZangle += gyroZrate * dt;

    gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate from the Kalman filter
    gyroYangle += kalmanY.getRate() * dt;
    gyroZangle += kalmanZ.getRate() * dt;

    /* Estimate angles using complimentary filter */
    compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll; // Calculate the angle using a Complimentary filter
    compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;
    compAngleZ = 0.93 * (compAngleZ + gyroZrate * dt) + 0.07 * yaw;

    // Reset the gyro angles when they has drifted too much
    if (gyroXangle < -180 || gyroXangle > 180)
        gyroXangle = kalAngleX;
    if (gyroYangle < -180 || gyroYangle > 180)
        gyroYangle = kalAngleY;
    if (gyroZangle < -180 || gyroZangle > 180)
        gyroZangle = kalAngleZ;

    /*   Serial.print(roll);
        Serial.print("\t");
        Serial.print(gyroXangle);
        Serial.print("\t");
        Serial.print(compAngleX);
        Serial.print("\t");
        Serial.print(kalAngleX);
        Serial.print("\t");

        Serial.print("\t");

        Serial.print(pitch);
        Serial.print("\t");
        Serial.print(gyroYangle);
        Serial.print("\t");
        Serial.print(compAngleY);
        Serial.print("\t");
        Serial.print(kalAngleY);
        Serial.print("\t");

        Serial.print("\t");

        Serial.print(yaw);
        Serial.print("\t");
        Serial.print(gyroZangle);
        Serial.print("\t");
        Serial.print(compAngleZ);
        Serial.print("\t");
        Serial.print(kalAngleZ);
        Serial.print("\t");

        Serial.println();*/
}

void updateMPU6050()
{
    sensors_event_t a, g, temp;
    mpu6050.getEvent(&a, &g, &temp);

    accX = a.acceleration.x;
    accY = a.acceleration.y;
    accZ = a.acceleration.z;
    Serial.print(accX);
    Serial.print("\t");

    Serial.print(accY);
    Serial.print("\t");

    Serial.print(accZ);
    Serial.print("\n");

    tempRaw = temp.temperature;

    gyroX = g.gyro.x;
    gyroY = g.gyro.y;
    gyroZ = g.gyro.z;
}

void updateHMC5883L()
{
    sensors_event_t event;
    mag.getEvent(&event);

    magX = event.magnetic.x;
    magY = event.magnetic.y;
    magZ = event.magnetic.z;

    /* Serial.print(magX);
     Serial.print("\t");
     Serial.print(magY);
     Serial.print("\t");
     Serial.println(magZ);*/
}

void updatePitchRoll()
{
    roll = atan2(accY, accZ) * RAD_TO_DEG;
    pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
}

void updateYaw()
{
    magX *= -1; // Invert axis - this it done here, as it should be done after the calibration
    magZ *= -1;

    magX *= magGain[0];
    magY *= magGain[1];
    magZ *= magGain[2];

    magX -= magOffset[0];
    magY -= magOffset[1];
    magZ -= magOffset[2];

    double rollAngle = kalAngleX * DEG_TO_RAD;
    double pitchAngle = kalAngleY * DEG_TO_RAD;

    double Bfy = magZ * sin(rollAngle) - magY * cos(rollAngle);
    double Bfx = magX * cos(pitchAngle) + magY * sin(pitchAngle) * sin(rollAngle) + magZ * sin(pitchAngle) * cos(rollAngle);
    yaw = atan2(-Bfy, Bfx) * RAD_TO_DEG;

    yaw *= -1;
}

void calibrateMag()
{
    updateHMC5883L(); // Read positive bias values

    double magPosOff[3] = {magX, magY, magZ};

    delay(100);       // Wait for sensor to get ready
    updateHMC5883L(); // Read negative bias values

    double magNegOff[3] = {magX, magY, magZ};

    magGain[0] = -2500 / float(magNegOff[0] - magPosOff[0]);
    magGain[1] = -2500 / float(magNegOff[1] - magPosOff[1]);
    magGain[2] = -2500 / float(magNegOff[2] - magPosOff[2]);
}