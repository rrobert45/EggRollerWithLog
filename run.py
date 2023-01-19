import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import csv

# Set the sensor type (DHT22) and the GPIO pin number
sensor = Adafruit_DHT.DHT22
pin = 4

# Set the relay pin number
relay = 17

# Set the interval for logging data and turning on the relay (in seconds)
log_interval = 300 # 5 minutes
relay_interval = 14280 # 4 hours

# Initialize the GPIO pin for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)

# Open the CSV files for writing
temp_humidity_file = open('temp_humidity_data.csv', 'w', newline='')
temp_humidity_writer = csv.writer(temp_humidity_file)
temp_humidity_writer.writerow(['Time', 'Temperature', 'Humidity'])

relay_file = open('relay_data.csv', 'w', newline='')
relay_writer = csv.writer(relay_file)
relay_writer.writerow(['Time', 'Relay Status'])

try:
    while True:
        # Read the humidity and temperature
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Log the temperature and humidity data
        if humidity is not None and temperature is not None:
            temp_humidity_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity])
            temp_humidity_file.flush()
        else:
            print('Failed to read data from sensor')

        # Check if it's time to turn on the relay
        if time.time() % relay_interval < 2:
            # Turn on the relay for 2 minutes
            GPIO.output(relay, GPIO.HIGH)
            relay_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "ON"])
            relay_file.flush()
            time.sleep(120)
            GPIO.output(relay, GPIO.LOW)
            relay_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "OFF"])
            relay_file.flush()
            print("relay has been turned on")
        else:
            relay_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "OFF"])
            relay_file.flush()
        # Wait for the next log interval
        time.sleep(log_interval)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    # Close the CSV files
    temp_humidity_file.close()
    relay_file.close()