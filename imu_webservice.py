# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import web
import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
#        return 'Hello, ' + name + '!'
        accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
        acceleration = '"acceleration":[%0.6f,%0.6f,%0.6f]'% (accel_x, accel_y, accel_z)
        gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
        gyro  = '"gyro":[%0.6f,%0.6f,%0.6f]'% (gyro_x, gyro_y, gyro_z)
        mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
        magnetometer  = '"magnetometer":[%0.6f,%0.6f,%0.6f]'% (mag_x, mag_y, mag_z)
        quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
        quaternione  = '"quaternione":[%0.6f,%0.6f,%0.6f]'% (quat_i, quat_j, quat_k)
        quaternione_real  = '"quaternione_real":%0.6f'%  quat_real

        return '{%s,%s,%s,%s,%s}' % (acceleration,gyro,magnetometer,quaternione,quaternione_real)
        #return '{"quaternione":[%f,%f,%f]}'%(1.0,1.0,1.0)

if __name__ == "__main__":
    app.run()
