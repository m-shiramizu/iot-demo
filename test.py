#!/usr/bin/python
# coding: utf-8

# GPIOモジュールインポート
import RPi.GPIO as GPIO
# timeモジュールインポート
import time

# LED点滅パターン
ledPat = {
  "on":     (1, 1, 1, 1),
  "off":    (0, 0, 0, 0),
  "blink1": (0, 1, 0, 1),
  "blink2": (0, 0, 0, 1)
}


# GPIOモード設定
# GPIO番号指定をBCM(GPIO番号)に設定
GPIO.setmode(GPIO.BCM)

# GPIOの初期化(天気用LEDのみ)
GPIO.setup(21, GPIO.OUT)

#   LED点滅処理
try:

  while True:
    for var in range(0, 4):
      for num in range(0, len(ledPat)):
        GPIO.output(21, ledPat['blink2'][num])
        time.sleep(0.25)
    for var in range(0, 4):
      for num in range(0, len(ledPat)):
        GPIO.output(21, ledPat['blink1'][num])
        time.sleep(0.10)
      
  
finally:

  GPIO.cleanup()
