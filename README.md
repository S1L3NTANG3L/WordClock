# Word Clock for Raspberry Pi Pico W

This project provides the code for a word clock implementation using a Raspberry Pi Pico W. The clock displays the current time in words by lighting up corresponding LEDs. It supports time synchronization using NTP (Network Time Protocol) and fallback to an RTC module (DS1302 or DS3231) for timekeeping. Have included the gerber file if you want to use a custom PCB and a schematic of how the pin connections should look.<br>
Link to the English 3D Files: https://www.printables.com/model/77997-word-clock<br>
Link to the Afrikaans 3d Files: https://www.printables.com/model/1125495-afrikaans-word-clock

## Features

- **Wi-Fi Connectivity**: Connects to a Wi-Fi network to synchronize time with an NTP server.
- **Timezone Support**: Adjusts the time to your local timezone.
- **Real-Time Clock (RTC)**: Fallback to DS1302 or DS3231 modules for timekeeping in case of Wi-Fi unavailability.
- **Word Clock Display**: Lights up words corresponding to the current time using GPIO pins connected to LEDs.
- **Periodic Updates**: Updates the clock every two minutes to keep time accurate.

## Hardware Requirements

1. **Raspberry Pi Pico W**: Can use the Pico 2 as well
2. **RTC Module**: DS1302 or DS3231
3. **LEDs**: Connected to GPIO pins to display words
4. **Wi-Fi Network**: Needed to sync the initial time via NTP
5. **I2C Communication**: SDA and SCL pins
6. **DS137 NPN Power Transistors**: Take the 5v GPIO signal and switch the LEDs
7. **150 Ohm Resistors**: Current limit the LEDs so they don't burn out
8. **Buck Convertor**: Depending on whether you plan to build this using 5, 12 or 24 volts, you'll need to pick up a buck converter to step down the voltage for the PICO

## GPIO Pin Configuration

The following GPIO pins are used to control the LEDs for the word clock:

Use the Clock.py code to figure out which pins your LEDs are connected to.

| Word        | GPIO Pin |
|-------------|----------|
| IT_IS       | 0        |
| FIVE (mins) | 1        |
| TEN (mins)  | 2        |
| QUARTER     | 3        |
| TWENTY      | 4        |
| HALF        | 5        |
| PAST        | 6        |
| TO          | 7        |
| ONE         | 8        |
| TWO         | 9        |
| THREE       | 10       |
| FOUR        | 11       |
| FIVE (hrs)  | 12       |
| SIX         | 13       |
| SEVEN       | 14       |
| EIGHT       | 15       |
| NINE        | 16       |
| TEN (hrs)   | 17       |
| ELEVEN      | 18       |
| TWELVE      | 19       |
| MINUTES     | 20       |
| OCLOCK      | 21       |

## Setup Instructions

1. **Connect RTC Module**:
   - DS1302 (Requires a chip select, so use gpio22) or DS3231 to the appropriate GPIO pins as specified in the code.
   - Configure SDA and SCL pins for I2C communication.

2. **Update Wi-Fi Credentials**:
   - Fill in your Wi-Fi SSID and password in the `SSID` and `PASSWORD` variables.

3. **Adjust Timezone**:
   - Set the `timezone_offset` variable to match your local timezone.

4. **Install Required Libraries**:
   - Ensure the `ntptime`, `ds1302`, and `ds3231` libraries are available in your MicroPython environment.

5. **Upload Code**:
   - Copy the provided script to your Pico W using an IDE like VSCode with the MicroPico Extension.

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
- `word_clock_updater(ds, i2c, wifiFlag, dsFlag)`: Background task periodically synchronising and updating the clock.
- `main()`: The main function is to initialize components and run the word clock updater.

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

