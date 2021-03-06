import os
import requests
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
# from twilio.rest import Client
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time
from background import stime

global detected_time
b_stime = stime
global a

# serial number
serial = 111111

# sensor
GPIO.setmode(GPIO.BOARD)
shock_pin = 23
motion_pin = 26
GPIO.setup(shock_pin, GPIO.IN)
GPIO.setup(motion_pin, GPIO.IN)

# define sms
# account_sid = "ACd3629a5ddec39f71bb9754cd11e3cb8c"
# auth_token = "ded2e1b7129859a4eb65ed4d37e09656"
# client = Client(account_sid, auth_token)

# ini file crawling
urlstr = "http://nero666.dothome.co.kr/" + str(serial) + '.ini'
data = requests.get(urlstr)
data.encoding = 'utf-8'

with open(str(serial) + ".ini", 'w', encoding='utf-8') as f:
    f.write(str(data.text))

parser = ConfigParser()
parser.read("111111.ini")

# read ini  parser.get('settings', )
stream_mode = parser.get('settings', 'StreamMode')
stream_key = parser.get('settings', 'StreamKey')
motion_check = parser.get('settings', 'MotionCheck')
shock_check = parser.get('settings', 'ShockCheck')
email = parser.get('settings', 'EmailAddress')
phone = parser.get('settings', 'PhoneNumber')
phone = phone.replace('0', '+82', 1)

"def"
def send_mail_(str):
    s = str
    global email
    arr = ["[nusa알림]\n", "스트리밍 시작", a, "후 모션이 감지되었습니다.\n", detected_time]
    if email == 'email@example.com' or "":
        print("email_address is none")
    else:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls() # 암호화 함수
        smtp.login("jsj2505@gmail.com", 'tvikvimnitxkhqve')
        if s == 'motion_m':
            msg = MIMEText('웹캠에 모션이 감지되었습니다.')
        else:
            msg = MIMEText("웹캠에 충격이 감지되었습니다.")

        msg['Subject'] = "NUSA에서 보낸 메일"
        msg['To'] = "jsj2505@naver.com"
        smtp.sendmail(email, "jsj2505@naver.com", msg.as_string())
        smtp.quit()
        print("메일을 전송했습니다.")
"""
def send_sms_(str):
    s = str
    global phone
    global a
    arr_m = ["[nusa알림]\n", "스트리밍 시작", a, "후 모션이 감지되었습니다.\n", detected_time]
    arr_s = ["[nusa알림]\n", "스트리밍 시작", a, "후 충격이 감지되었습니다.\n", detected_time]
    if phone == "01012345678" or "":
        print("phone_ number is none")
    else:
        if s == 'motion_m':
            message = client.messages.create(
                body = "{0}{1}{2}{3}{4}".format(arr_m[0], arr_m[1], arr_m[2], arr_m[3], arr_m[4]),
                from_ = '(812) 577-9045',
                to = phone
            )
        else:
            message = client.messages.create(
                body = "{0}{1}{2}{3}{4}".format(arr_s[0], arr_s[1], arr_s[2], arr_s[3], arr_s[4]),
                from_ = '(812) 577-9045',
                to = phone
            )
    print("메세지를 보냈습니다")
"""

"""sensor shock"""
def shock():
   global a
   global detected_time
   global b_stime
   while True:
      if GPIO.input(shock_pin) == True:
         if shock_check == "on":
            tm2 = time.localtime(time.time())
            detected_time = datetime(tm2.tm_year, tm2.tm_mon, tm2.tm_mday, tm2.tm_hour, tm2.tm_min, tm2.tm_sec)
            a = detected_time - b_stime
            send_sms_('shock_s')
            send_mail_('shcok_s')
            break


def motion():
   global a
   global detected_time
   global b_stime
   while True:
      if GPIO.input(motion_pin) == True:
         if motion_check == "on":
            tm2 = time.localtime(time.time())
            detected_time = datetime(tm2.tm_year, tm2.tm_mon, tm2.tm_mday,tm2.tm_hour, tm2.tm_min, tm2.tm_sec)
            a = detected_time - b_stime
            send_sms_('motion_m')
            send_mail_('motion_m')
            break

def sm():
   while True:
      shock()
      time.sleep(0.5)
      print("shocked")
      motion()
      print("motion")
      time.sleep(300)

"""define"""

try:
   #작업들
   if stream_mode == 'on':
       sm()
   else:
      print("stream mode is off")
except KeyboardInterrupt:
   print("Ctrl+c 입력됨 프로그램을 종료")
