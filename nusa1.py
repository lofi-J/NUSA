import os
import requests
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time

global detected_time_s
global detected_time_m
global a_shock
global a_motion
global cool_time_m
global cool_time_s

cool_time_m = 0
cool_time_s = 0

tm = time.localtime(time.time())
stime = datetime(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)

# serial number
serial = 111111

# sensor
GPIO.setmode(GPIO.BOARD)
shock_pin = 23
motion_pin = 26
GPIO.setup(shock_pin, GPIO.IN)
GPIO.setup(motion_pin, GPIO.IN)

# define sms
account_sid = "ACfe4fe02aa2e5f6f016be99af85fa2a92"
auth_token = "e4213e8a06137a32f8e0de668517a687"
client = Client(account_sid, auth_token)

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
    global a_motion
    global a_shock
    # arr = ["[nusa알림]\n", "스트리밍 시작", a, "후 모션이 감지되었습니다.\n", detected_time]
    if email == 'email@example.com' or "":
        print("email_address is none")
    else:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls() # 암호화 함수
        smtp.login("jsj2505@gmail.com", 'tvikvimnitxkhqve')
        if s == 'motion_m':
            msg = MIMEText('스트리밍 시작{0} 후 모션이 감지되었습니다.'.format(a_motion))
            print("메일을 전송했습니다._motion")
        else:
            msg = MIMEText('스트리밍 시작{0} 후 충격이 감지되었습니다.'.format(a_shock))
            print("메일을 전송했습니다._shock")

        msg['Subject'] = "NUSA에서 보낸 메일"
        msg['To'] = email
        smtp.sendmail("jsj2505@gmail.com", email, msg.as_string())
        smtp.quit()
        

def send_sms_(str):
    s = str
    global phone
    global a_motion
    global a_shock
    
    if phone == "01012345678" or "":
        print("phone_ number is none")
    else:
        if s == 'motion_m':
            arr_m = ["[nusa알림]\n", "스트리밍 시작", a_motion, "후 모션이 감지되었습니다.\n"]
            message = client.messages.create(
                body = "{0}{1}{2}{3}".format(arr_m[0], arr_m[1], arr_m[2], arr_m[3]),
                from_ = '(256) 826-0711',
                to = phone
            )
            print("메세지를 보냈습니다_motion")
        else:
            arr_s = ["[nusa알림]\n", "스트리밍 시작", a_shock, "후 충격이 감지되었습니다.\n"]
            message = client.messages.create(
                body = "{0}{1}{2}{3}".format(arr_s[0], arr_s[1], arr_s[2], arr_s[3]),
                from_ = '(256) 826-0711',
                to = phone
            )
            print("메세지를 보냈습니다_shock")
        

"""sensor shock"""
def shock():
   global a_shock
   global detected_time_s
   global stime
   global cool_time_s
   time_now = int(time.time()) 
   if time_now - cool_time_s >= 0:
       if GPIO.input(shock_pin) == True:
                tm_s = time.localtime(time.time())
                detected_time_s = datetime(tm_s.tm_year, tm_s.tm_mon, tm_s.tm_mday, tm_s.tm_hour, tm_s.tm_min, tm_s.tm_sec)
                a_shock = detected_time_s - stime
                send_sms_('shock_s')
                send_mail_('shock_s')
                cool_time_s = time_now + 300 


def motion():
    global a_motion
    global detected_time_m
    global stime
    global cool_time_m
    time_now = int(time.time())
    if time_now - cool_time_m >= 0:
        if GPIO.input(motion_pin) == True:
                tm2 = time.localtime(time.time())
                detected_time_m = datetime(tm2.tm_year, tm2.tm_mon, tm2.tm_mday, tm2.tm_hour, tm2.tm_min, tm2.tm_sec)
                a_motion = detected_time_m - stime
                send_sms_('motion_m')
                send_mail_('motion_m')
                cool_time_m = time_now + 300 
                
def sm():
   while True: 
      if shock_check == "on":
          shock()
      if motion_check == "on":
          motion()

if stream_mode == "on":
    sm()
