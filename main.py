# Thanks to https://github.com/triplepoint/micropython_bme280_i2c

import machine
import bme280_i2c
import time
import ssd1306

display_i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
# confirmed with i2c_scanner, display address is 0x3C, which is the default
display = ssd1306.SSD1306_I2C(128, 64, display_i2c)


# Create a Micropython I2C object with the appropriate device pins
sensor_i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

# Create a sensor object to represent the BME280
# Note that this will throw error if the device can't be reached over I2C.
sensor = bme280_i2c.BME280_I2C(address=bme280_i2c.BME280_I2C_ADDR_PRIM, i2c=sensor_i2c)

# Configure the sensor for the application in question.
sensor.set_measurement_settings({
    'filter': bme280_i2c.BME280_FILTER_COEFF_16,
    'standby_time': bme280_i2c.BME280_STANDBY_TIME_500_US,
    'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_p': bme280_i2c.BME280_OVERSAMPLING_16X,
    'osr_t': bme280_i2c.BME280_OVERSAMPLING_2X})

# Start the sensor automatically sensing
sensor.set_power_mode(bme280_i2c.BME280_NORMAL_MODE)

# Wait for the measurement settle time, print the measurement, and repeat
while 1:
    display.fill(0) # clear screen
    temperature = 'Temp:{}'.format(sensor.get_measurement()["temperature"])
    print(temperature)
    display.text(temperature, 0, 0)

    humidity = 'Humidity:{}'.format(sensor.get_measurement()["humidity"])
    print(humidity)
    display.text(humidity, 0, 8)

    pressure = 'Pressure:{}'.format(sensor.get_measurement()["pressure"])
    print(pressure)
    display.text(pressure, 0, 16)
    display.show()
    print('========================')
    time.sleep_ms(1000)

# The above code repeatedly prints a line like:
# {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}