import paho.mqtt.client as mqtt
import json
import csv
import time

TOPIC = "home/room/sensors"
BROKER_ADDRESS = "localhost"
CSV_FILE = "sensor_data.csv"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected! Subscribing to topic: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    light_value = data["light"]
    sound_value = data["sound"]
    motion_value = data["motion"]
    print(f"Light: {light_value}, Sound: {sound_value}, Motion: {motion_value}")

    timestamp = int(time.time())
    row = [timestamp, light_value, sound_value, motion_value]

    try:
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    except Exception as e:
        print(f"Error writing to CSV: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    print("Connecting to broker...")
    client.connect(BROKER_ADDRESS, 1883)
    client.loop_forever() 
except KeyboardInterrupt:
    print("\nStopping.")
    client.disconnect()