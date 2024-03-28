import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the PPD42 sensor
dust_sensor_pin = 17

def setup_sensor():
    GPIO.setup(dust_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_sensor():
    try:
        # Function to read the sensor data
        def callback(channel):
            global low_pulse_count, total_pulse_count
            if GPIO.input(channel):  # If rising edge (low pulse)
                low_pulse_count += 1
            total_pulse_count += 1

        GPIO.add_event_detect(dust_sensor_pin, GPIO.BOTH, callback=callback)

        # Initialize counts
        low_pulse_count = 0
        total_pulse_count = 0

        # Wait for 30 seconds to count pulses
        time.sleep(30)

        # Calculate low pulse occupancy and ratio
        low_pulse_occupancy = low_pulse_count / total_pulse_count * 100  # Percentage
        ratio = low_pulse_occupancy / 30  # Ratio based on 30 seconds

        print("Low Pulse Occupancy: {:.2f}%".format(low_pulse_occupancy))
        print("Ratio: {:.2f}".format(ratio))

        # Detect cigarette smoke based on ratio (example threshold)
        if ratio > 0.1:  # Adjust threshold as needed
            print("Cigarette smoke detected!")
        else:
            print("No cigarette smoke detected.")

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    setup_sensor()
    try:
        while True:
            read_sensor()
            time.sleep(30)  # Read every 60 seconds
    except KeyboardInterrupt:
        GPIO.cleanup()
