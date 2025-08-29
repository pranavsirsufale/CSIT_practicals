import random, time, sys

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
        """
        A class to read temperature and humidity from a BME280 sensor
        connected via I2C to a Raspberry Pi.
        Requires the `smbus2` library.
        """
        def __init__(self, i2c_bus=1, i2c_addr=0x76):
            self.bus = SMBus(i2c_bus)
            self.i2c_addr = i2c_addr
            self.chip_id = 0x60
            self.name = "BME280 Sensor"

            self.bus.write_byte_data(self.i2c_addr, 0xf2, 0x01)
            self.bus.write_byte_data(self.i2c_addr, 0xf4, 0x27)

        def read_value(self, sensor_type):
            """Reads a specific value (e.g., 'temperature' or 'humidity')."""
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
            except FileNotFoundError:
                print("Could not connect to I2C device. Check your wiring and configuration.")
                return None
            except Exception as e:
                print(f"Error reading from BME280 sensor: {e}")
                return None

    class GpioSensor:
        """
        A class to read a digital signal from a simple GPIO pin.
        Requires the `RPi.GPIO` library.
        """
        def __init__(self, pin=17, name="GPIO Sensor"):
            self.pin = pin
            self.name = name
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)

        def read_value(self):
            """Reads the digital value (high/low) from the GPIO pin."""
            try:
                return GPIO.input(self.pin)
            except Exception as e:
                print(f"Error reading from GPIO pin {self.pin}: {e}")
                return None
else:
    class TemperatureSensor:
        """A mock sensor that generates random temperature data."""
        def __init__(self, name="Temperature Sensor"):
            self.name = name
        def read_value(self):
            return round(random.uniform(15.0, 30.0), 2)

    class HumiditySensor:
        """A mock sensor that generates random humidity data."""
        def __init__(self, name="Humidity Sensor"):
            self.name = name
        def read_value(self):
            return random.randint(40, 80)

    class LightSensor:
        """A mock sensor that generates random light level data."""
        def __init__(self, name="Light Sensor"):
            self.name = name
        def read_value(self):
            return random.randint(100, 1000)

def main():
    """
    Initializes sensors and continuously reads their data,
    printing the values to the console.
    """
    print("Initializing sensor reading program...")

    if IS_RPI:
        bme280 = BME280Sensor()
        gpio_sensor = GpioSensor()
        sensors_to_read = [
            ("Temperature", lambda: bme280.read_value("temperature"), "°C"),
            ("Humidity", lambda: bme280.read_value("humidity"), "%"),
            ("GPIO Signal", gpio_sensor.read_value, " (1=High, 0=Low)")
        ]

    else:
        sensors_to_read = [
            ("Temperature", TemperatureSensor().read_value, "°C"),
            ("Humidity", HumiditySensor().read_value, "%"),
            ("Light", LightSensor().read_value, " lux")
        ]
    try:
        while True:
            print("-" * 30)
            print("Reading sensor data...")
            for name, reader_func, unit in sensors_to_read:
                value = reader_func()
                print(f"{name}: {value}{unit}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        if IS_RPI:
            GPIO.cleanup()
            print("GPIO resources cleaned up.")
if __name__ == "__main__":
    main()

