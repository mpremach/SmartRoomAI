# AI Occupancy Sensor - Raspberry Pi Setup

This README covers the setup for the Raspberry Pi. This device acts as the central MQTT Broker, the Data Logger, the AI Model Trainer, and the Live Predictor for the system.


Pi Setup & Configuration
------------ 
1. Raspberry Pi OS Lite (64-bit)
2. Install MQTT BROKER 
(Run these commands on the Pi)
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
*Make sure host name of pi matches whatever was used for the BROKER_HOST variable for the arduino*
3. Install necessary libraries
python3 -m pip install paho-mqtt pandas scikit-learn joblib --break-system-packages

listen.py
------------
Purpose: Used to collect raw sensor data to create and train the AI model.

Action: Run python3 listen.py.

Result: Data is saved to sensor_data.csv. Once enough data is collected, it must be labeled (see next step).


AITrain.py
------------
Purpose: Used to create the AI model ("brain") from the labeled data.

Action: Run python3 AITrain.py after labeled_data.csv is on the Pi.

Result: This script reads labeled_data.csv and creates the model.pkl file.


predict.py
------------
Purpose: Uses the model.pkl "brain" to make live predictions.

Action: Run python3 predict.py.

Result: The script loads the model and prints real-time occupancy predictions as new sensor data arrives from the Arduino.


## How to Use

1. Start the Arduino: Ensure the Arduino is powered on and publishing to the MQTT broker.
2. Run python3 listen.py to allow data collection, once a large enough sample is saved (saved to sensor_data.csv) data must be downloaded
3. Label data is csv file to match goal (in this case occupancy) and then save the new labeled data as labeled_data.csv
4. Transfer labeled_data.csv to Pi
5. Run python3 AITrain.py
6. Run python3 predict.py


