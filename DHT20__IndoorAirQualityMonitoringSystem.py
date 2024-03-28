from time import sleep
from DFRobot_DHT20 import DFRobot_DHT20

# The first parameter is to select i2c0 or i2c1
# The second parameter is the i2c device address
I2C_BUS = 0x01  # default use I2C1 bus
I2C_ADDRESS = 0x38  # default I2C device address
dht20 = DFRobot_DHT20(I2C_BUS, I2C_ADDRESS)

# Initialize sensor
if not dht20.begin():
    print("DHT20 sensor initialization failed")
else:
    while True:
        # Read ambient temperature and relative humidity
        T_celsius, humidity, crc_error = dht20.get_temperature_and_humidity()
        if crc_error:
            print("CRC               : Error\n")
        else:
            T_fahrenheit = T_celsius * 9/5 + 32
            print("Temperature       : {:.2f}°C / {:.2f}°F".format(T_celsius, T_fahrenheit))
            print("Relative Humidity : {:.2f} %".format(humidity))
            print("CRC               : OK\n")
            print("------------------------------------------------")
        sleep(2)
