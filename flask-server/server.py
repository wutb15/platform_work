import flask
from flask import Flask
from flask import request
import numpy as np
import urllib.request
import cv2
import time
import threading
import queue
from concurrent.futures import Future
import requests
import json
request_queue = queue.Queue()
mu = threading.Lock()

app = Flask(__name__)


@app.route('/testB', methods=['POST'])
def test():
    future = Future()
    ts = request.form['ts']
    img_url = request.form['url']
    request_queue.put((future, img_url, ts), block=True, timeout=5)
    rsp = future.result(timeout=5)
    print('receive rsp\n')
    print(rsp)
    return json.dumps(rsp)


class workerThread(threading.Thread):
    def __init__(self, _batch_size, request_queue):
        threading.Thread.__init__(self)
        self._batch_size = _batch_size
        self._is_started = 0
        self._req_queue = request_queue

    def run(self):
        self._is_started = 1
        print('worker running\n')
        self._worker()

    def _worker(self):
        while self._is_started:
            recieve_ts_list = []
            img_url_list = []
            future_list = []
            model_result_list = []
            try:
                try:
                    n = self._batch_size
                    while n > 0:
                        future, img_url, rec_ts = self._req_queue.get(block=False)
                        future_list.append(future)
                        img_url_list.append(img_url)
                        recieve_ts_list.append(rec_ts)
                        n = n-1

                    model_result_list = self._do_business(img_url_list, recieve_ts_list)
                    print('get results\n')
                    for i in range(len(model_result_list)):
                        future_list[i].set_result(model_result_list[i])
                        print('set results\n')
                except queue.Empty:
                    if len(future_list) == 0:
                        time.sleep(0.1)
                    continue
            except Exception as e:
                continue


    def _do_business(self,img_url_list, recieve_ts_list):
        result_list = []
        for i in range(len(img_url_list)):
            img_url = img_url_list[i]
            rec_ts = recieve_ts_list[i]
            result = self._img_decode(img_url, rec_ts)
            result_list.append(result)
        return result_list

    def _img_decode(self, img_url, rec_ts):
        print('enter img_decode function\n')
        rec_ts = float(rec_ts)
        resp = urllib.request.urlopen(img_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        resp_ts = time.time()
        ts_diff = resp_ts - rec_ts
        feed_back = {'rec_ts': rec_ts, 'resp_ts': resp_ts, 'ts_diff': ts_diff}
        return feed_back



if __name__ == '__main__':
    batchsize = 10
    worker = workerThread(batchsize, request_queue)
    worker.start()
    print('begins\n')
    app.run(host='0.0.0.0',port=80)
