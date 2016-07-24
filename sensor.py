# coding: utf-8

import sys
import signal
import time
import httplib
import json
import RPi.GPIO as GPIO
from datetime import datetime

param = sys.argv
SUBDOMAIN = param[1]  # URL
API_TOKEN = param[2]  # APIトークン
SENSOR_PIN = int(param[3])  # センサーのGPIO番号
INTERVAL = float(param[4])  # 測定間隔（秒）

# マイクロ秒sleep
usleep = lambda x: time.sleep(x / 1000000.0)


def signalhandler(num, frame):
    """
    UNIXシグナルのハンドラ
    引数は2つ・番号とフレームオブジェクト
    """
    print 'func(): %d, %s' % (num, str(frame))  # ここではSIGINTの数値がnumに入る
    sys.exit()


signal.signal(signal.SIGINT, signalhandler)


class Sensor:
    """ 
    センサー  
    """

    def readValue(self):

        now = 0
        # GPIO指定をGPIO番号で行う
        GPIO.setmode(GPIO.BCM)

        try:
            GPIO.setup(SENSOR_PIN, GPIO.OUT)   # 出力指定
            GPIO.output(SENSOR_PIN, 0)   # ピンの出力を0Vにする
            usleep(2)
            GPIO.output(SENSOR_PIN, 1)   # ピンの出力を3.3Vにする
            usleep(5)
            GPIO.output(SENSOR_PIN, 0)   # ピンの出力を0Vにする

            now = datetime.now()

            # ピンの電圧状態読み取る
            GPIO.setup(SENSOR_PIN, GPIO.IN)  # 入力指定
            while GPIO.input(SENSOR_PIN) == 0:
                continue
            start = time.time()

            cnt = 0
            while GPIO.input(SENSOR_PIN) == 1:
                # cnt = cnt + 1
                continue
            end = time.time()
        except KeyboardInterrupt:
            print "keyboardInterrupt"
        finally:
            GPIO.cleanup()

        distance = ((end - start) * 1000000) / 29 / 2
        distance = distance > 400 and 400 or distance  # 最大距離
        distance_val = int(round(distance, 0))
#        print "cnt %s  distance  %.3f cm" % (cnt, distance)

        now_jst = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        now_unixtime = now.strftime("%s.%f")

        logs = [
            {
                "type": "sensor_data",
                "attributes": {
                    "jst": now_jst,
                    "time": now_unixtime,
                    "distance": distance_val
                }
            }
        ]
        return logs

    # IotボードへへのPOST
    def registToKintone(self, subdomain, logs, apiToken):
        request = {"api_token": apiToken, "logs": logs}
        requestJson = json.dumps(request)
        headers = {"Content-Type": "application/json"}

        try:
            connect = httplib.HTTPSConnection(subdomain + ":443")
            connect.request("POST", "", requestJson, headers)
            response = connect.getresponse()
            print response
            return response
        except Exception as e:
            print(e)
            return None

sensor = Sensor()

while True:
    values = sensor.readValue()
    print values
    resp = sensor.registToKintone(SUBDOMAIN, values, API_TOKEN)
# print "status : %s msg : %s reason : %s " % (resp.status, resp.msg,
# resp.reason)
    print "result: %s distance: %s cm" % (rsp.reason, values[0]['attributes']['distance'])
    time.sleep(INTERVAL)
