from flask import Flask, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
from DFRobot_DHT20 import DFRobot_DHT20
import time
import pygame

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Initialize DHT20 sensor
I2C_BUS = 0x01  # default use I2C1 bus
I2C_ADDRESS = 0x38  # default I2C device address
dht20 = DFRobot_DHT20(I2C_BUS, I2C_ADDRESS)

# Initialize Pygame for sound
pygame.init()
sound = pygame.mixer.Sound('/home/art/Downloads/emergency-alarm-with-reverb-29431.mp3')

# Pin configuration for MQ2 sensor
mq2_dpin = 5

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

@app.route('/')
def index():
    return "Gas Leakage Detection and DHT20 Sensor Data"

@app.route('/sensor', methods=['GET'])
def get_sensor_data():
    if not dht20.begin():
        return jsonify({'error': 'DHT20 sensor initialization failed'})

    T_celsius, humidity, crc_error = dht20.get_temperature_and_humidity()

    if crc_error:
        return jsonify({'error': 'CRC error'})

    T_fahrenheit = T_celsius * 9/5 + 32
    return jsonify({
        'temperature_celsius': T_celsius,
        'temperature_fahrenheit': T_fahrenheit,
        'humidity': humidity
    })

@app.route('/gas', methods=['GET'])
def get_gas_status():
    if GPIO.input(mq2_dpin):
        return "Gas not leaking"
    else:
        return "Gas leakage."

@app.route('/alarm/start')
def start_alarm():
    sound.play()
    return "Alarm started."

@app.route('/alarm/stop')
def stop_alarm():
    sound.stop()
    return "Alarm stopped."

def main():
    init()
    print("Please wait...")
    time.sleep(5)

    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
