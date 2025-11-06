import paho.mqtt.client as mqtt
import json

TOPIC = "home/room/sensors"
BROKER_ADDRESS = "localhost"

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