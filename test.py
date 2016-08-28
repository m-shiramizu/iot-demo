#!/usr/bin/python
# coding: utf-8

# GPIOモジュールインポート
import RPi.GPIO as GPIO
# timeモジュールインポート
import time



# GPIOモード設定
# GPIO番号指定をBCM(GPIO番号)に設定
GPIO.setmode(GPIO.BCM)

# GPIOの初期化(天気用LEDのみ)
GPIO.setup(21, GPIO.OUT)

GPIO.setup(18, GPIO.IN)


try:
  while True:
    if GPIO.input(18) == GPIO.HIGH:
      print "on"
      GPIO.output(21, 1)
    else:
      print "off"
      GPIO.output(21, 0)
      time.sleep(0.5)
except KeyboardInterrupt:
  GPIO.cleanup()

finally:
  GPIO.cleanup()
