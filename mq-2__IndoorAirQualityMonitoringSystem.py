import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the MQ-2 sensor
mq2_dpin = 5
mq2_apin = 6

# Set up GPIO pins
GPIO.setup(mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def detect_gas():
    if GPIO.input(mq2_dpin):
        return True
    else:
        return False

def play_audio():
   
    audio_file = '/home/art/Downloads/emergency-alarm-with-reverb-29431.mp3'
    subprocess.Popen(["omxplayer", audio_file])

if __name__ == '__main__':
    try:
        while True:
            if detect_gas():
                print("Gas detected!")
                play_audio()
            else:
                print("No gas detected.")
            time.sleep(1)  # Check every 1 second
    except KeyboardInterrupt:
        GPIO.cleanup()
