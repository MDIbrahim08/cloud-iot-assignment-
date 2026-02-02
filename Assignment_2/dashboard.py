import streamlit as st
import pandas as pd
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# -------------------------------
# Identity Details
# Name: Ibrahim
# Use Case: Industrial Boiler
# -------------------------------

BROKER = "broker.emqx.io"
TOPIC = "iot/boiler/ibrahim_fa"

st.set_page_config(page_title="Industrial Boiler Digital Twin", layout="wide")
st.title("Industrial Boiler Digital Twin Dashboard")
st.caption("Real-time IoT data visualization using MQTT and Streamlit")

data = pd.DataFrame(columns=["Time", "Temperature", "Humidity", "Status"])
placeholder = st.empty()

def on_message(client, userdata, msg):
    global data
    payload = json.loads(msg.payload.decode())
    new_row = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Temperature": payload["temperature"],
        "Humidity": payload["humidity"],
        "Status": payload["status"]
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)
client.loop_start()

while True:
    with placeholder.container():
        if not data.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature (°C)", data.iloc[-1]["Temperature"])
            col2.metric("Humidity (%)", data.iloc[-1]["Humidity"])
            col3.metric("Status", data.iloc[-1]["Status"])

            st.line_chart(data.set_index("Time")[["Temperature", "Humidity"]])
