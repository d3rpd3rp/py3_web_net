#tested on Python 3.6.1 on macOS

import requests
from time import sleep

#vars
url = 'http://wrs41.winshipway.com/'
sleep_time = 60

#infinite loop
while True:
    r = requests.get(url, stream=True)
    sleep(sleep_time)
