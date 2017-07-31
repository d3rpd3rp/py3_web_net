#tested on Python 3.6.1 on macOS

import requests, random
from time import sleep

#vars
url = 'http://wrs41.winshipway.com/'
sleep_time = 60

#seed pseudo-random number generator
#no argument to seed uses system time as default
random.seed()

#infinite loop
while True:
    r = requests.get(url, stream=True)
    sleep(sleep_time)
    sleep_time = sleep_time + random.randint(1, 60)
    #don't sleep too much, if over thirty minutes
    if sleep_time > 1800:
        sleep_time = 60
