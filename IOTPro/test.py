import paho.mqtt.client as mqtt
import json
import threading
from flask import Flask, jsonify

# --- Global Sensor Data and Flask App ---
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "air_quality": 0,
    "light_level": 0
}

app = Flask(__name__)

# MQTT settings
MQTT_BROKER = 'localhost' # Use 'localhost' if the broker is on the same Pi
MQTT_PORT = 1883
# The topic must match what Zigbee2MQTT publishes. Check your Zigbee2MQTT logs.
# For example, if your sensor is named "scientech_kit", the topic might be `zigbee2mqtt/scientech_kit`.
MQTT_TOPIC = "zigbee2mqtt/your_scientech_kit_id"

def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the broker."""
    print("Connected to MQTT Broker with result code: " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """Callback function for when a message is received."""
    global sensor_data
    print("Received message: " + msg.topic)
    try:
        # The message payload is a JSON string from Zigbee2MQTT
        payload = json.loads(msg.payload.decode('utf-8'))

        # Update the global sensor_data dictionary
        # The key names here should match the data sent by the Scientech kit
        if "temperature" in payload:
            sensor_data["temperature"] = payload["temperature"]
        if "humidity" in payload:
            sensor_data["humidity"] = payload["humidity"]
        if "air_quality" in payload:
            sensor_data["air_quality"] = payload["air_quality"]
        if "light_level" in payload:
            sensor_data["light_level"] = payload["light_level"]

        print("Updated sensor data:", sensor_data)
    except Exception as e:
        print(f"Error parsing MQTT message: {e}")

# This function runs in a separate thread to handle MQTT communication
def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    # The loop_forever() function is blocking, so it must be in a thread.
    client.loop_forever()

# Define an API endpoint to serve the sensor data
@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    """Returns the latest sensor data as a JSON object."""
    return jsonify(sensor_data)

# Main entry point for the application
if __name__ == "__main__":
    # Start the MQTT communication in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()

    # Run the Flask web server in the main thread
    app.run(host='0.0.0.0', port=5000)
