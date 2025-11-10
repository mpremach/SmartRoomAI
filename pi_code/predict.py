import paho.mqtt.client as mqtt
import json
import joblib
import pandas as pd
import time


print("Loading (model.pkl)")
model = joblib.load("model.pkl")


MQTT_BROKER = "localhost" 
MQTT_TOPIC = "home/room/sensors"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected to broker at {MQTT_BROKER}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"\nRaw data received: {payload}")
    
    try:
        data = json.loads(payload)
        light = data.get("light")
        sound = data.get("sound")
        motion = data.get("motion")

        if all(v is not None for v in [light, sound, motion]):
            

            live_data = pd.DataFrame(
                [[light, sound, motion]],  
                columns=['light', 'sound', 'motion']  
            )

            
            prediction_probabilities = model.predict_proba(live_data)
            probabilities = prediction_probabilities[0]

            prob_empty = probabilities[0] * 100
            prob_occupied = probabilities[1] * 100

            print(f"AI PREDICTION: {prob_occupied:.1f}% Occupied / {prob_empty:.1f}% Empty")

        else:
            print("Error: JSON message is missing one or more keys.")
            
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from payload: {payload}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Note: Using VERSION 1 here for broader compatibility
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()
except ConnectionRefusedError:
    print(f"Connection refused. Is the MQTT broker running?")
except KeyboardInterrupt:
    print("\nDisconnecting from broker...")
    client.disconnect()
    print("Script stopped.")