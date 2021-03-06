import flask
from flask import Flask
from flask import request
import numpy as np
import urllib.request
import cv2
import time
import threading
import queue
from concurrent.futures import Future, ProcessPoolExecutor,ThreadPoolExecutor
import json
import argparse

request_queue = queue.Queue()

app = Flask(__name__)


@app.route('/testB', methods=['POST'])
def test():
    future = Future()
    ts = request.form['ts']
    img_url = request.form['url']
    request_queue.put((future, img_url, ts), block=True, timeout=10)
    rsp = future.result(timeout=10)
    print('receive rsp\n')  # debug information
    return json.dumps(rsp)




class workerThread(threading.Thread):
    def __init__(self, _batch_size, request_queue):
        threading.Thread.__init__(self)
        self._batch_size = _batch_size
        self._is_started = 0
        self._req_queue = request_queue
        self._executor = ThreadPoolExecutor()

    def run(self):
        self._is_started = 1
        print('worker running\n')  # debug information
        self._worker()

    def stop(self):
        self._is_started = 0

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
                        n = n - 1

                    model_result_list = self._do_business(img_url_list, recieve_ts_list)
                    for i in range(len(model_result_list)):
                        future_list[i].set_result(model_result_list[i])
                        print('set results\n')  # debug information
                except queue.Empty:
                    if len(future_list) == 0:
                        time.sleep(0.1)
                    else:# early processing
                        model_result_list = self._do_business(img_url_list, recieve_ts_list)
                        for i in range(len(model_result_list)):
                            future_list[i].set_result(model_result_list[i])
                            print('set results\n')  # debug information
                    continue
            except Exception as e:
                continue
        self._executor.shutdown(wait=True)

    def _do_business(self, img_url_list, recieve_ts_list):
        result_list = []
        executor = self._executor
        print('do business\n')
        #with ProcessPoolExecutor() as executor:
        for result in executor.map(self.img_decode, img_url_list, recieve_ts_list):  # multithread process
            result_list.append(result)

        '''
        for i in range(len(img_url_list)):
            img_url = img_url_list[i]
            rec_ts = recieve_ts_list[i]
            result = self._img_decode(img_url, rec_ts)
            result_list.append(result)
        '''
        return result_list
    @staticmethod
    def img_decode(img_url, rec_ts):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batchsize', type=int, help='input batchsize', default=14)
    args = parser.parse_args()
    batchsize = args.batchsize
    worker = workerThread(batchsize, request_queue)
    worker.daemon = True
    worker.start()
    print('begins\n')
    app.run(threaded=True, port=80, host='0.0.0.0')
