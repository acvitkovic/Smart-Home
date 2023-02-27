#include <Wire.h>
#include <Artekit_TMP116.h>
#include <ClosedCube_OPT3001.h>
#include <Dps310.h>
#include <sSense-HDC2010.h>

#define OPT3001_ADDRESS 0x44
#define HDC_ADDRESS 0x40
Dps310 Dps310PressureSensor = Dps310();
Artekit_TMP116 temp_sensor(0x48);
ClosedCube_OPT3001 opt3001;
HDC2010 hdc(HDC_ADDRESS); 



float humidity = 0;
float pressure =0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  temp_sensor.begin();

  hdc.begin();
  hdc.reset();

  opt3001.begin(OPT3001_ADDRESS);
  
  //DPS sensor
  int16_t pin_cs = SS;
  Serial.begin(9600);
  Dps310PressureSensor.begin(SPI, pin_cs);
  configureSensor();
  
  hdc.setHighHumidity(55);     // High humidity of 55%
  hdc.setLowHumidity(40);      // Low humidity of 40%
  
  // Configure Measurements
  hdc.setMeasurementMode(HUMID_ONLY);  // Set measurements to temperature and humidity
  hdc.setRate(ONE_HZ);                     // Set measurement frequency to 1 Hz
  hdc.setTempRes(FOURTEEN_BIT);
  hdc.setHumidRes(FOURTEEN_BIT);
  
  //begin measuring
  hdc.triggerMeasurement();
}

void loop() {

  float temp;
  temp_sensor.readTemperature(&temp);
  Serial.print(temp);
  
  //DPS 
    uint8_t oversampling = 7;
  
    Dps310PressureSensor.measurePressureOnce(pressure, oversampling);
  
    Serial.print("x");

    Serial.print(pressure/100);
    Serial.print("x");
 
  //OPT code
  OPT3001 result = opt3001.readResult();
  printResult("OPT3001", result);
  Serial.print("x");

  //HDC code
  humidity = hdc.readHumidity();
  Serial.print(humidity);
  
  Serial.println();
  delay(1000);
  
}

void configureSensor() {
  OPT3001_Config newConfig;
  
  newConfig.RangeNumber = B1100;  
  newConfig.ConvertionTime = B0;
  newConfig.Latch = B1;
  newConfig.ModeOfConversionOperation = B11;

  OPT3001_ErrorCode errorConfig = opt3001.writeConfig(newConfig);
  if (errorConfig != NO_ERROR)
    printError("OPT3001 configuration", errorConfig);
  else {
    OPT3001_Config sensorConfig = opt3001.readConfig();
  }
  
}

void printResult(String text, OPT3001 result) {
  if (result.error == NO_ERROR) {
    Serial.print(result.lux);
  }
  else {
    printError(text,result.error);
  }
}

void printError(String text, OPT3001_ErrorCode error) {
  Serial.print(text);
  Serial.print(": [ERROR] Code #");
  Serial.println(error);
}
