# Word Clock for Raspberry Pi Pico W

This project provides the code for a word clock implementation using a Raspberry Pi Pico W. The clock displays the current time in words by lighting up corresponding LEDs. It supports time synchronization using NTP (Network Time Protocol) and fallback to an RTC module (DS1302 or DS3231) for timekeeping.

## Features

- **Wi-Fi Connectivity**: Connects to a Wi-Fi network to synchronize time with an NTP server.
- **Timezone Support**: Adjusts the time to your local timezone.
- **Real-Time Clock (RTC)**: Fallback to DS1302 or DS3231 modules for timekeeping in case of Wi-Fi unavailability.
- **Word Clock Display**: Lights up words corresponding to the current time using GPIO pins connected to LEDs.
- **Periodic Updates**: Updates the clock every two minutes to keep time accurate.

## Hardware Requirements

1. **Raspberry Pi Pico W**
2. **RTC Module**: DS1302 or DS3231
3. **LEDs**: Connected to GPIO pins to display words
4. **Wi-Fi Network**
5. **I2C Communication**: SDA and SCL pins

## GPIO Pin Configuration

The following GPIO pins are used to control the LEDs for the word clock:

Use the Clock.py code to figure out which pins you have your leds connected to.

| Word        | GPIO Pin |
|-------------|----------|
| IT_IS       | 0        |
| FIVE (mins) | 3        |
| TEN (mins)  | 7        |
| QUARTER     | 21       |
| TWENTY      | 17       |
| HALF        | 5        |
| PAST        | 1        |
| TO          | 8        |
| ONE         | 10       |
| TWO         | 2        |
| THREE       | 9        |
| FOUR        | 11       |
| FIVE (hrs)  | 12       |
| SIX         | 16       |
| SEVEN       | 6        |
| EIGHT       | 13       |
| NINE        | 4        |
| TEN (hrs)   | 14       |
| ELEVEN      | 15       |
| TWELVE      | 19       |
| MINUTES     | 20       |
| OCLOCK      | 18       |

## Setup Instructions

1. **Connect RTC Module**:
   - DS1302 or DS3231 to the appropriate GPIO pins as specified in the code.
   - Configure SDA and SCL pins for I2C communication.

2. **Update Wi-Fi Credentials**:
   - Fill in your Wi-Fi SSID and password in the `SSID` and `PASSWORD` variables.

3. **Adjust Timezone**:
   - Set the `timezone_offset` variable to match your local timezone.

4. **Install Required Libraries**:
   - Ensure the `ntptime`, `ds1302`, and `ds3231` libraries are available in your MicroPython environment.

5. **Upload Code**:
   - Copy the provided script to your Pico W using an IDE like Thonny.

6. **Run the Program**:
   - Execute the script on your Pico W.

## How It Works

1. **Wi-Fi Connection**:
   - The Pico W attempts to connect to the specified Wi-Fi network. If successful, it synchronizes the time using an NTP server.

2. **Time Synchronization**:
   - Time is adjusted to the local timezone and set on the RTC module.

3. **Word Clock Update**:
   - The clock updates the displayed time every two minutes by lighting up the appropriate LEDs based on the current time.

4. **Fallback to RTC**:
   - If Wi-Fi is unavailable, the clock uses the RTC module to retrieve the time.

## Code Overview

### Functions

- `connect_to_wifi(ssid, password, hostname)`: Connects to the Wi-Fi network.
- `sync_time_ntp(ds, dsFlag)`: Synchronizes time with an NTP server and updates the RTC.
- `update_word_clock(ds, wifiFlag, dsFlag)`: Updates the word clock display based on the current time.
- `word_clock_updater(ds, i2c, wifiFlag, dsFlag)`: Background task to periodically synchronize and update the clock.
- `main()`: Main function to initialize components and run the word clock updater.

## Customization

- **Hostname**: Change the `HOSTNAME` variable to give your Pico W a custom network name.
- **RTC Module**: Set the `dsFlag` variable to `True` for DS3231 or `False` for DS1302.
- **Word Pin Mapping**: Modify the `word_pins` dictionary to adjust GPIO pin assignments.

## Troubleshooting

- **Wi-Fi Connection Issues**:
  - Ensure the SSID and password are correct.
  - Verify the Wi-Fi network is active and within range.

- **RTC Module Not Detected**:
  - Check the wiring and ensure proper I2C configuration.

- **Incorrect Time**:
  - Verify the `timezone_offset` and ensure NTP synchronization is successful.

