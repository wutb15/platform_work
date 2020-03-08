import queue
import threading
import contextlib
import time
import requests
import sys, getopt
import json
from concurrent.futures import ThreadPoolExecutor, as_completed



def img_req(imgfile, uri):
    ts = time.time()
    payload = {'ts': ts, 'url': imgfile}
    resp = requests.post(uri, data=payload)
    return resp


def main(argv):
    threadnumber = 5
    imgfile = ''
    logfilename = 'time.json'
    fp = open(logfilename, 'w')
    fp.close()
    try:
        opts, args = getopt.getopt(argv, "ht:i:", ["threadnumber=", "imgfile="])
    except getopt.GetoptError:
        print('client.py -t <threadnumber> -i <imgfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-t", "--threadnumber"):
            threadnumber = int(arg)
        elif opt in ("-i", "--imgfile"):
            imgfile = arg
    pool = ThreadPoolExecutor(threadnumber)
    endpoint = '/testB'
    url = 'http://127.0.0.1:5000'
    uri = url+endpoint
    all_task = []
    for i in range(threadnumber):
        all_task.append(pool.submit(img_req, imgfile, uri))
    for future in as_completed(all_task):
        data = future.result()
        data = str(data)
        with open(logfilename, 'a') as fp:
            fp.write(data)


if __name__ == "__main__":
    main(sys.argv[1:])
