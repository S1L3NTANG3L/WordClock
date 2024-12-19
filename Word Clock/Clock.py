from machine import Pin
from time import sleep

gpio1 = Pin(0,Pin.OUT)

while True:
    gpio1.value(1)  # Turn on the pin
    print(f"GPIO {pin} is now ON")  # Optional: print the status
    sleep(10)  # Wait for 1 second
    gpio1.value(0)  # Turn off the pin
