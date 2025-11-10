# AI Occupancy Sensor - Arduino Node

This README covers the setup for the Arduino sensor node. Its purpose is to read sensor data and publish it as a JSON payload to the Raspberry Pi broker over MQTT.

LIBRARIES
----------------
WiFiS3
ArduinoMqttClient

REQUIREMENTS
----------------
Arduino UNO R4 Wifi
PIR Motion Sensor (HC-SR501)
Light Sensor (Photoresistor)
Analog Sound Sensor (KY-038)
Breadboard & jumper wires
//Any additional sensors/modules


Setup and Wiring
----------------
PIR(OUT)-> Digital Pin 3
Light(A0)-> Analog Pin A0
Sound (A0)-> Analog Pin A1
All sensors get **5V** and **GND** from the Arduino.


## How to Use

1.  **Libraries:** Open the Arduino IDE and use the Library Manager to install the two libraries listed above.
2.  **Credentials and Config:** Open the `.ino` sketch and update the `WIFI_SSID` and `WIFI_PASSWORD` variables with your network info. You must also change the `BROKER_HOST` variable to match either the hostname or IP address of the Raspberry Pi (Hostname is better!)
3.  **Upload:** Connect the Arduino and upload the sketch.
