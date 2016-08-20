# coding: utf-8

import sys
import ConfigParser
import signal
import time
import httplib
import json
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
from gcloud import storage
from gcloud.storage import Blob

configfile = ConfigParser.SafeConfigParser()
configfile.read("./config/config.ini")

UPLOAD_BUCKET = configfile.get("gcs","upload_bucket") 
PROJECT_ID = configfile.get("gcs","project_id")
UPLOAD_FILE = configfile.get("gcs","upload_file")
OUTPUT_FILE = configfile.get("gcs","output_file")

SENSOR_PIN = int(configfile.get("sensor","pin"))
INTERVAL = float(configfile.get("sensor","interval"))
SHUTTER_DISTANCE = int(configfile.get("sensor","shutter_distance"))

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

class Sensor_SEN136B5B:
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

        value = {
          "type": "sensor_data",
          "attributes": {
            "jst": now_jst,
            "time": now_unixtime,
            "distance": distance_val
          }
        }
        return value

sensor = Sensor_SEN136B5B()
client = storage.Client(project=PROJECT_ID)
bucket = client.get_bucket(UPLOAD_BUCKET)

with picamera.PiCamera() as camera:
  camera.resolution = (2592, 1944)
  camera.start_preview()

  while True:
    value = sensor.readValue()
    distance = int(value['attributes']['distance'])
    print distance
    ## 閾値を超えたら
    if distance <= SHUTTER_DISTANCE:
      #time.sleep(5)
      camera.capture(UPLOAD_FILE)
      print "ok  %d" % distance
      time.sleep(5)
      outputfile = OUTPUT_FILE + datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
      print outputfile
      blob = Blob(outputfile, bucket)
      with open(UPLOAD_FILE, 'rb') as my_file:
        blob.upload_from_file(my_file)
        
    time.sleep(INTERVAL)
