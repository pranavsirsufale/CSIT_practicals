import random, time, sys, json
from flask import Flask, jsonify
from threading import Thread

try:
    from smbus2 import SMBus
    import RPi.GPIO as GPIO
    print("Detected Raspberry Pi environment. Using hardware sensor drivers.")
    IS_RPI = True
except ImportError:
    print("Raspberry Pi libraries not found. Using mock sensors for simulation.")
    IS_RPI = False

if IS_RPI:
    class BME280Sensor:
        def __init__(self, i2c_bus=1, i2c_addr=0x76):
            self.bus = SMBus(i2c_bus)
            self.i2c_addr = i2c_addr
            self.chip_id = 0x60
            self.bus.write_byte_data(self.i2c_addr, 0xf2, 0x01)
            self.bus.write_byte_data(self.i2c_addr, 0xf4, 0x27)
        def read_value(self, sensor_type):
            try:
                data = self.bus.read_i2c_block_data(self.i2c_addr, 0xf7, 8)
                raw_temp = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
                raw_humidity = (data[7] << 8) | data[8]
                if sensor_type == 'temperature':
                    return round((raw_temp / 1000) - 10, 2)
                elif sensor_type == 'humidity':
                    return round(raw_humidity / 1000, 2)
                else:
                    return None
            except Exception as e:
                return None

    class GpioSensor:
        def __init__(self, pin=17):
            self.pin = pin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
        def read_value(self):
            try:
                return GPIO.input(self.pin)
            except Exception as e:
                return None
else:
    class TemperatureSensor:
        def read_value(self):
            return round(random.uniform(15.0, 30.0), 2)
    class HumiditySensor:
        def read_value(self):
            return random.randint(40, 80)
    class LightSensor:
        def read_value(self):
            return random.randint(100, 1000)

sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "wind_speed": 0.0,
    "precipitation": 0.0
}

app = Flask(__name__)

def read_sensors_loop():
    if IS_RPI:
        bme280 = BME280Sensor()

        while True:
            sensor_data["temperature"] = bme280.read_value("temperature")
            sensor_data["humidity"] = bme280.read_value("humidity")
            sensor_data["wind_speed"] = round(random.uniform(0.0, 20.0), 2)
            sensor_data["precipitation"] = round(random.uniform(0.0, 5.0), 2)
            time.sleep(3)
    else:
        temp_sensor = TemperatureSensor()
        humidity_sensor = HumiditySensor()

        while True:
            sensor_data["temperature"] = temp_sensor.read_value()
            sensor_data["humidity"] = humidity_sensor.read_value()
            sensor_data["wind_speed"] = round(random.uniform(0.0, 20.0), 2)
            sensor_data["precipitation"] = round(random.uniform(0.0, 5.0), 2)
            time.sleep(3)


@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

if __name__ == "__main__":
    sensor_thread = Thread(target=read_sensors_loop, daemon=True)
    sensor_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
