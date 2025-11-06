//Code to read data from all the sensors and publish them to the Rasberry pi
#include <WiFiS3.h>
#include <ArduinoMqttClient.h>

//---GLOBAL--//
const char* WIFI_SSID = "WhiteSky-Boulevard98";
const char* WIFI_PASSWORD = "97p3gucy";
const char* BROKER_HOST = "pi-broker.local"; //retrieve ip address regardless of if its different than last connection
const int BROKER_PORT = 1883; //mqtt port
const char* SENSOR_TOPIC = "home/room/sensors";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

unsigned long lastPublishTime = 0; //time since last publish
const long PUBLISH_INTERVAL = 3500; //publish every 5 seconds


//Setup sensor variables
#define PIR_PIN 3 //Digital pin 3
#define LIGHT_PIN A0 //Analog pin 0
#define SOUND_PIN A1 //Analog pin 1
//Add any extra variables here if new sensors added

void setup() {
  Serial.begin(9600);
  while(!Serial); //Do not run until serial monitor has been opened
  pinMode(PIR_PIN, INPUT); //Set PIR as input
  connectWiFi();
  connectMQTT();
}


void loop() {  
  if(!mqttClient.connected()) {
    Serial.println("MQTT connection lost, attempting to reconnect");
    connectMQTT();
  }
  mqttClient.poll();

  //Read sensor data and print to serial plotter if connected
  int lightLevel = readLightSensor();
  int soundLevel = readSoundSensor();
  int motion     = readMotionSensor();
  //Easier reading on graph
  int motionDisplay = motion * 200; 

  //Comma-separated format for the Serial Plotter
  Serial.print(lightLevel);
  Serial.print(",");
  Serial.print(soundLevel);
  Serial.print(",");
  Serial.println(motionDisplay); // Use println on the last one

  //If been 5 seconds publish data
  unsigned long currentTime = millis();
  if (currentTime - lastPublishTime > PUBLISH_INTERVAL) {
    lastPublishTime = currentTime;
    PublishSensorData(lightLevel, soundLevel, motion);
  }
  // 200ms delay between readings
  delay(200);
}

//---HELPER FUNCTIONS---//
void PublishSensorData(int light, int sound, int motion) {
    Serial.println("Publishing to MQTT");
    //format as JSON string
    char jsonBuffer[256];
    sprintf(jsonBuffer,
          "{\"light\": %d, \"sound\": %d, \"motion\": %d}", light, sound, motion);
    Serial.print("Publishing JSON: ");
    Serial.println(jsonBuffer);
    mqttClient.beginMessage(SENSOR_TOPIC);
    mqttClient.print(jsonBuffer);
    mqttClient.endMessage();  
  } 


int readLightSensor() {
  return analogRead(LIGHT_PIN); //Return light value
}

int readMotionSensor() {
  return digitalRead(PIR_PIN); //Returns 1(HIGH) or 0(LOW)
}

int readSoundSensor() { 
  unsigned long startTime = millis(); // Get the current time
  unsigned int sample;
  
  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;

  // Collect data for 50 milliseconds
  while (millis() - startTime < 50) {
    sample = analogRead(SOUND_PIN); // Read a sample
    
    if (sample < 1024) { // Ignore any bad readings
      if (sample > signalMax) {
        signalMax = sample; // Save as the new highest
      } else if (sample < signalMin) {
        signalMin = sample; // Save as the new lowest
      }
    }                  
  }
  
  // Return the difference between the highest and lowest
  return signalMax - signalMin; 
}
//add any extra sensor helper functions here if new sensors added

//---Connection functions---//
void connectWiFi() {
  Serial.print("Connecting to wifi: ");
  Serial.println(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("."); //indicated connection attempts
    delay(5000);
  }
  Serial.println("\nWifi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  Serial.print("Connecting to MQTT Broker: ");
  Serial.println(BROKER_HOST);


  while (!mqttClient.connect(BROKER_HOST, BROKER_PORT)) {
    Serial.print("MQTT connection failed (Code ");
    Serial.print(mqttClient.connectError());
    Serial.println("). Retrying in 5 seconds...");
    delay(5000);
  }
  Serial.println("\nMQTT Connected!");
}



