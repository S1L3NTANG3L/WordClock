from machine import Pin
import time

# Initialize GPIO pins 0 to 22 as outputs
pins = [Pin(i, Pin.OUT) for i in range(23)]  # Create a list of Pin objects

while True:
    for i, pin in enumerate(pins):
        print(f"Toggling pin {i}")  # Print the current pin number
        pin.value(1)  # Set pin high
        time.sleep(10)  # Wait 10s
        pin.value(0)  # Set pin low
        time.sleep(0.1)  # Wait 100ms
