#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include "Wire.h"
#endif

MPU6050 mpu(0x68);
MPU6050 mpu2(0x69);


// MPU control/status vars
bool dmpReady = false; // set true if DMP init was successful
uint8_t mpuIntStatus; // holds actual interrupt status byte from MPU
uint8_t devStatus; // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize; // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount; // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

bool dmpReady2 = false; // set true if DMP init was successful
uint8_t mpuIntStatus2; // holds actual interrupt status byte from MPU
uint8_t devStatus2; // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize2; // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount2; // count of all bytes currently in FIFO
uint8_t fifoBuffer2[64]; // FIFO storage buffer


// orientation/motion vars
Quaternion q; // [w, x, y, z] quaternion container
VectorFloat gravity; // [x, y, z] gravity vector
float ypr[3]; // [yaw, pitch, roll] yaw/pitch/roll container and gravity vector

Quaternion q2; // [w, x, y, z] quaternion container
VectorFloat gravity2; // [x, y, z] gravity vector
float ypr2[3]; // [yaw, pitch, roll] yaw/pitch/roll container and gravity vector

volatile bool mpuInterrupt = false; // indicates whether MPU interrupt pin has gone high
void dmpDataReady()
{
  mpuInterrupt = true;
  //Serial.println("ready");
}

volatile bool mpuInterrupt2 = false; // indicates whether MPU interrupt pin has gone high
void dmpDataReady2()
{
  mpuInterrupt2 = true;
  //Serial.println("ready2");
}

void setup()
{
// join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
  TWBR = 12; // 400kHz I2C clock (200kHz if CPU is 8MHz)
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

mpu.initialize();
mpu2.initialize();
Serial.begin(115200);
devStatus = mpu.dmpInitialize();
devStatus2 = mpu2.dmpInitialize();

// supply your own gyro offsets here, scaled for min sensitivity
mpu.setXGyroOffset(220);
mpu.setYGyroOffset(76);
mpu.setZGyroOffset(-85);
mpu.setZAccelOffset(1788); // 1688 factory default for my test chip

mpu2.setXGyroOffset(220);
mpu2.setYGyroOffset(76);
mpu2.setZGyroOffset(-85);
mpu2.setZAccelOffset(1788); // 1688 factory default for my test chip

// make sure it worked (returns 0 if so)
  if (devStatus == 0)
  {
    // turn on the DMP, now that it's ready
    mpu.setDMPEnabled(true);

    // enable Arduino interrupt detection
    attachInterrupt(0, dmpDataReady, RISING);
    mpuIntStatus = mpu.getIntStatus();

    // set our DMP Ready flag so the main loop() function knows it's okay to use it
    dmpReady = true;

    // get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize();

  }
  else
  {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    Serial.print(F("DMP Initialization failed (code "));
    Serial.print(devStatus);
    Serial.println(F(")"));
  }

  if (devStatus2 == 0)
  {
    // turn on the DMP, now that it's ready
    mpu2.setDMPEnabled(true);

    // enable Arduino interrupt detection
    attachInterrupt(1, dmpDataReady2, RISING);
    mpuIntStatus2 = mpu2.getIntStatus();

    // set our DMP Ready flag so the main loop() function knows it's okay to use it
    dmpReady2 = true;

    // get expected DMP packet size for later comparison
    packetSize2 = mpu2.dmpGetFIFOPacketSize();

  }
  else
  {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    Serial.print(F("DMP Initialization failed 2 (code "));
    Serial.print(devStatus2);
    Serial.println(F(")"));
  }
}


void loop()
{
  // if programming failed, don't try to do anything
  if (!dmpReady) return;
  if (!dmpReady2) return;

  // wait for MPU interrupt or extra packet(s) available
  while ((!mpuInterrupt && fifoCount < packetSize) || (!mpuInterrupt2 && fifoCount2 < packetSize2));

  // reset interrupt flag and get INT_STATUS byte
  mpuInterrupt = false;
  mpuIntStatus = mpu.getIntStatus();

  mpuInterrupt2 = false;
  mpuIntStatus2 = mpu2.getIntStatus();

  // get current FIFO count
  fifoCount = mpu.getFIFOCount();
  fifoCount2 = mpu2.getFIFOCount();

  // check for overflow (this should never happen unless our code is too inefficient)
  if ((mpuIntStatus & 0x10) || fifoCount == 1024)
  {
    // reset so we can continue cleanly
    mpu.resetFIFO();
    //Serial.println(F("FIFO overflow!"));

  // otherwise, check for DMP data ready interrupt (this should happen frequently)
  }
  else if (mpuIntStatus & 0x02)
  {
    // wait for correct available data length, should be a VERY short wait
    while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();
    // read a packet from FIFO
    mpu.getFIFOBytes(fifoBuffer, packetSize);
    // track FIFO count here in case there is > 1 packet available
    // (this lets us immediately read more without waiting for an interrupt)
    fifoCount -= packetSize;

    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
    Serial.print("uarm:");
    Serial.print(ypr[0] * 180/M_PI);
    Serial.print(":");
    Serial.print(ypr[1] * 180/M_PI);
    Serial.print(":");
    Serial.println(ypr[2] * 180/M_PI);
  }

  if ((mpuIntStatus2 & 0x10) || fifoCount2 == 1024)
  {
    // reset so we can continue cleanly
    mpu2.resetFIFO();
    //Serial.println(F("FIFO overflow! 2"));

  // otherwise, check for DMP data ready interrupt (this should happen frequently)
  }
  else if (mpuIntStatus2 & 0x02)
  {
    // wait for correct available data length, should be a VERY short wait
    while (fifoCount2 < packetSize2) fifoCount2 = mpu2.getFIFOCount();
    // read a packet from FIFO
    mpu2.getFIFOBytes(fifoBuffer2, packetSize2);
    // track FIFO count here in case there is > 1 packet available
    // (this lets us immediately read more without waiting for an interrupt)
    fifoCount2 -= packetSize2;

    mpu2.dmpGetQuaternion(&q2, fifoBuffer2);
    mpu2.dmpGetGravity(&gravity2, &q2);
    mpu2.dmpGetYawPitchRoll(ypr2, &q2, &gravity2);
    Serial.print("farm:");
    Serial.print(ypr2[0] * 180/M_PI);
    Serial.print(":");
    Serial.print(ypr2[1] * 180/M_PI);
    Serial.print(":");
    Serial.println(ypr2[2] * 180/M_PI);
  }
  delay(10);
}