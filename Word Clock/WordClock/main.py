import network
import time
import uasyncio as asyncio
from machine import RTC, Pin, I2C
import ntptime  # NTP time synchronization
from ds1302 import *
from ds3231 import *

# Wi-Fi
SSID = ""  #Fill in your wifi SSID
PASSWORD = ""  #Fill in your wifi Password
HOSTNAME = "WordClockPico"  #Change if you want to give it a custom network hostname

# Timezone Offset (in hours)
timezone_offset = 2  # Adjust to your local timezone (e.g., 1 for UTC+1, -5 for UTC-5)

# RTC (Real-Time Clock)
rtc = RTC()

#I2C Pins
# Initialize the SDA (Serial Data Line) pin for I2C communication
sdaPIN = Pin(26)
# Initialize the SCL (Serial Clock Line) pin for I2C communication
sclPIN = (27)
csPIN = (22)
#Flag to check if wifi is available
wifiFlag = True

# GPIO Pins for Word Clock (Set based on the outputs of running the loop code)
word_pins = {
    "IT_IS": Pin(0, Pin.OUT),
    "FIVE": Pin(3, Pin.OUT),    # First "FIVE" GPIO
    "TEN_1": Pin(7, Pin.OUT),  # First "TEN" GPIO
    "QUARTER": Pin(21, Pin.OUT),
    "TWENTY": Pin(17, Pin.OUT),
    "HALF": Pin(5, Pin.OUT),
    "PAST": Pin(1, Pin.OUT),
    "TO": Pin(8, Pin.OUT),
    "ONE": Pin(10, Pin.OUT),
    "TWO": Pin(2, Pin.OUT),
    "THREE": Pin(9, Pin.OUT),
    "FOUR": Pin(11, Pin.OUT),
    "FIVE_H": Pin(12, Pin.OUT),  # "FIVE" for hours aka The Lower FIVE
    "SIX": Pin(16, Pin.OUT),
    "SEVEN": Pin(6, Pin.OUT),
    "EIGHT": Pin(13, Pin.OUT),
    "NINE": Pin(4, Pin.OUT),
    "TEN_2": Pin(14, Pin.OUT),  # Second "TEN" GPIO aka The Lower TEN
    "ELEVEN": Pin(15, Pin.OUT),
    "TWELVE": Pin(19, Pin.OUT),
    "MINUTES": Pin(20, Pin.OUT),
    "OCLOCK": Pin(18, Pin.OUT),
}

# Connect to Wi-Fi
def connect_to_wifi(ssid, password, hostname):
    # Initialize the Wi-Fi connection in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Set the hostname
    try:
        wlan.config(hostname=hostname)
    except AttributeError:
        print("Hostname configuration not supported on this device.")
    # Attempt to connect to the Wi-Fi network
    print(f"Connecting to {ssid}...")
    wlan.connect(ssid, password)
    # Wi-Fi timeout counter
    timeout = 60
    for i in range(timeout):
        if wlan.isconnected():
            # Connection successful
            print("Connected!")
            print("IP Address:", wlan.ifconfig()[0])
            return True
        print("Waiting for connection...")
        time.sleep(1)

    # Connection failed
    print("Failed to connect to Wi-Fi within the timeout period.")
    wlan.active(False)
    return False

# Synchronize Time with NTP Server and Adjust for Timezone
def sync_time_ntp(ds, dsFlag):
    try:
        print("Synchronizing time with NTP server...")
        ntptime.settime()
        print("Time synchronized!")
        # Adjust time for timezone offset
        current_time = time.localtime(time.time() + timezone_offset * 3600)
        #print("Current Time:",current_time)
        rtc.datetime((
            current_time[0], current_time[1], current_time[2], current_time[6],  # Year, Month, Day, Weekday
            current_time[3], current_time[4], current_time[5], 0  # Hour, Minute, Second, Subsecond
        ))
        # Set the DS3231 RTC to current system time
        if (dsFlag):
            ds.set_time() #DS3231
        else:
            ds.year(current_time[0])  # Set the year to 2085
            ds.month(current_time[1])    # Set the month to January
            ds.day(current_time[2])     # Set the day to 17th
            ds.hour(current_time[3])    # Set the hour to midnight (00)
            ds.minute(current_time[4])  # Set the minute to 17
            ds.second(current_time[5])  # Set the second to 30

        #print("DS Time:",ds.get_time())
    except Exception as e:
        print(f"Failed to synchronize time: {e}")

def update_word_clock(ds, wifiFlag, dsFlag):
    if (wifiFlag):
        # Get the current time
        current_time = time.localtime()
        hour = current_time[3]  # Current hour (24-hour format)
        minute = current_time[4]  # Current minute
    else:
        if (dsFlag):
            current_time = ds.get_time() #DS3231
            hour = current_time[3]  # Current hour (24-hour format) #DS3231
            minute = current_time[4]  # Current minute #DS3231
        else:
            hour = ds.hour()
            minute = ds.minute()
    print(hour,":",minute)
    # Round the minutes to the nearest 5
    rounded_minute = 5 * round(minute / 5)

    # Clear all pins
    for pin in word_pins.values():
        pin.value(0)

    # Always light up "IT IS"
    word_pins["IT_IS"].value(1)

    # Determine the words to light up based on the rounded minutes
    if rounded_minute == 0:
        word_pins["OCLOCK"].value(1)
    elif minute >= 55:
        word_pins["OCLOCK"].value(1)
        hour += 1
    elif rounded_minute <= 30:
        # "PAST" logic
        word_pins["PAST"].value(1)
        if rounded_minute == 5:
            word_pins["FIVE"].value(1)
        elif rounded_minute == 10:
            word_pins["TEN_1"].value(1)
        elif rounded_minute == 15:
            word_pins["QUARTER"].value(1)
        elif rounded_minute == 20:
            word_pins["TWENTY"].value(1)
        elif rounded_minute == 25:
            word_pins["TWENTY"].value(1)
            word_pins["FIVE"].value(1)
        elif rounded_minute == 30:
            word_pins["HALF"].value(1)
    else:
        # "TO" logic
        word_pins["TO"].value(1)
        rounded_minute = 60 - rounded_minute  # Calculate remaining minutes to the next hour
        if rounded_minute == 5:
            word_pins["FIVE"].value(1)
        elif rounded_minute == 10:
            word_pins["TEN_1"].value(1)
        elif rounded_minute == 15:
            word_pins["QUARTER"].value(1)
        elif rounded_minute == 20:
            word_pins["TWENTY"].value(1)
        elif rounded_minute == 25:
            word_pins["TWENTY"].value(1)
            word_pins["FIVE"].value(1)
        # Increment the hour for "TO"
        hour += 1        

    # Ensure the hour wraps around to a 12-hour format
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12

    # Light up the corresponding hour word
    hour_words = [
        "ONE", "TWO", "THREE", "FOUR", "FIVE_H", "SIX",
        "SEVEN", "EIGHT", "NINE", "TEN_2", "ELEVEN", "TWELVE"
    ]
    word_pins[hour_words[hour - 1]].value(1)


# Background Task to Update Word Clock
async def word_clock_updater(ds, i2c, wifiFlag, dsFlag):
    while True:
        if (wifiFlag):
            sync_time_ntp(ds, dsFlag)
        update_word_clock(ds, wifiFlag, dsFlag)
        await asyncio.sleep(120)  # Update every two minutes

# Main Function
async def main():
    dsFlag = False #DS3231 = True
    # Initialize the I2C interface with the specified pins and frequency
    i2c = I2C(1, sda=sdaPIN, scl=sclPIN, freq=400000) 
    #Connect to wifi
    wifiFlag = connect_to_wifi(SSID, PASSWORD, HOSTNAME)    
    # Create an instance of the DS3231 class for interfacing with the DS3231 RTC
    if (dsFlag):
        ds = DS3231(i2c) #DS3231
    else:
        ds = DS1302(Pin(sclPIN),Pin(sdaPIN),Pin(csPIN))
    print("Word clock is running...")
    await word_clock_updater(ds, i2c, wifiFlag, dsFlag)

# Run the program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")