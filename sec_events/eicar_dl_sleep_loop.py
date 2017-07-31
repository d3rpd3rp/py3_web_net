#Tested with Python 3.6.1 on macOS

import requests, random
from time import sleep

#used https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
#writes into same directory as python file, use os module to define unique path
def download_file(url, local_filename):
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

#vars
url = 'https://www.eicar.org/download/eicar_com.zip'
size_of_file_loop = 10
sleep_time = 60
n=0

#seed pseudo-random number generator
#no argument to seed uses system time as default
random.seed()

#infinite loop, only writing ten total files and rewriting them as same name after 10 files
while True:
    local_filename = url.split('/')[-1]
    local_filename = local_filename + str(n % size_of_file_loop)
    download_file(url, local_filename)
    n += 1
    sleep(sleep_time)
    #modify sleep time
    sleep_time = sleep_time + random.randint(1, 60)
    #don't sleep too much, if over thirty minutes
    if sleep_time > 1800:
        sleep_time = 60
