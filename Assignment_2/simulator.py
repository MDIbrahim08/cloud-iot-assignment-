import json
import random
import time
import paho.mqtt.client as mqtt

# -------------------------------
# Identity Details (IMPORTANT)
# Name: Ibrahim
# Use Case: Industrial Boiler
# -------------------------------

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/boiler/ibrahim_fa"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker:", BROKER)

while True:
    # Normal operation values
    temperature = round(random.uniform(2.0, 6.0), 2)
    humidity = random.randint(60, 80)

    # Stress test condition (Anomaly)
    # Randomly inject extreme temperature
    if random.randint(1, 20) == 10:
        temperature = 100.0

    # Status logic
    if temperature < 5:
        status = "OK"
    elif temperature < 8:
        status = "Warning"
    else:
        status = "Critical"

    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "status": status
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Published:", payload)

    time.sleep(5)
