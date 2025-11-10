Welcome to the readme for the raspberry pi setup

//include raspberry pi setup instructions, mqtt, etc.



listen.py
------------
Used to collect raw sensor data to create and train ai model
Data is saved to sensor_data.csv, once data is properly labeled it can be uploaded to py as labeled_data.csv



AITrain.py
------------
Used to create AI model based of collected data, run this file once labeled_data.csv is loaded onto pi, will create a model.pki used for predict.py to make predictions


predict.py
------------
Uses labeled_data.csv AI model to make predictions

