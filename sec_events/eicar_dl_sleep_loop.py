#Tested with Python 3.6.1 on macOS

import requests
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

#infinite loop, only writing ten total files and rewriting them as same name after 10 files
while True:
    local_filename = url.split('/')[-1]
    local_filename = local_filename + str(n % size_of_file_loop)
    download_file(url, local_filename)
    n += 1
    sleep(sleep_time)
