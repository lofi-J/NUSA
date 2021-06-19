import os
import requests
from configparser import ConfigParser
from datetime import datetime, timedelta
import time

serial = 111111

urlstr = "http://nero666.dothome.co.kr/" + str(serial) + '.ini'
data = requests.get(urlstr)
data.encoding = 'utf-8'

with open(str(serial) + ".ini", 'w', encoding='utf-8') as f:
    f.write(str(data.text))

    
parser = ConfigParser()
parser.read("111111.ini")

stream_mode = parser.get('settings', 'StreamMode')
stream_key = parser.get('settings', 'StreamKey')

if stream_mode == 'on':
    tm = time.localtime(time.time())
    stime = datetime(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)
    print(os.system("ffmpeg -re -i /dev/video0 -f lavfi -i anullsrc -vb 2500k -s 1280x720 -f flv rtmp://a.rtmp.youtube.com/live2/{0}".format(stream_key)))
