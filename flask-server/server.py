import flask
from flask import Flask
from flask import request
import numpy as np
import urllib.request
import cv2
import time
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import requests
import json
count = 0
batchsize = 200
request_queue = queue.Queue()
executing_queue = queue.Queue(batchsize)
executor = ThreadPoolExecutor(batchsize)
logfilename = 'time.json'
mu = threading.Lock()

app = Flask(__name__)


@app.route('/testB', methods=['POST'])
def test():
    if request.method == 'POST':
        request_queue.put(request.form)
        print('receive data\n')
    return 'OK'
@app.route('/')
def index():
    return 'Hello world'

@app.route('/do',methods=['POST'])
def do():
    if request.method == 'POST':
        if executing_queue.qsize() >= batchsize:
            return 'The executing queue is full'
        if request_queue.qsize() == 0:
            return 'The request queue is empty'
        while executing_queue.qsize() < batchsize and request_queue.qsize() > 0:
            reqform = request_queue.get()
            executing_queue.put(reqform)
        return 'OK'
def consumer():
    print('consumer process running')
    logfilename = 'time.json'
    fp = open(logfilename, 'w')
    fp.close()
    while True:
        if executing_queue.qsize() < batchsize and request_queue.qsize() > 0:
            requests.post("http://127.0.0.1:5000/do")

        if executing_queue.qsize() == batchsize:
            print('begin decoding')
            for i in range(batchsize):
                reqform = executing_queue.get()
                executor.submit(img_decode, reqform)
        time.sleep(0.001)
def img_decode(reqform):
    print('enter img_decode function\n')
    dataform = reqform.to_dict()
    rec_ts = dataform['ts']
    rec_ts = float(rec_ts)

    img_url = dataform['url']

    resp = urllib.request.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    resp_ts = time.time()
    ts_diff = resp_ts - rec_ts
    feed_back = {'rec_ts': rec_ts, 'resp_ts': resp_ts, 'ts_diff': ts_diff}
    logfilename = 'time.json'
    if mu.acquire(True):
        with open(logfilename, 'a') as logfile:
            json.dump(feed_back, logfile)
            logfile.write('\n')
        mu.release()
    print('decode complete\n')
    return feed_back


if __name__ == '__main__':
    t = threading.Thread(target=consumer)
    t.start()

    app.run()
