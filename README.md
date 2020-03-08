# platform_work
homework for cloud platform

## 第一阶段
### 简介
本阶段的作业是在本地实现响应高并发的访问的服务器。本次作业我采用的是单独使用python flask来作为服务端的架构。由于flask在默认的设置下是单线程的，这意味着如果处理大规模的耗时较多的请求时会有明显的阻塞，所以选择利用BlockingQueue存储请求数据，ThreadPoolExecutor批量多线程执行请求的计算任务的方式来实现异步的处理多线程。
### 程序简介
client.py可以使用命令行的形式更改参数，有'client.py -t <threadnumber> -i <imgfile>'来更改线程数量以及处理图片的来源
  
server.py则是通过更改代码中的batchsize参数来更改批量处理的请求数量，并将feed_back预存在test.json文件下
### 简单观察的结果
通过增大线程数以及batchsize可以使得cpu负载不断提高，当cpu负载达到上限时会观察到ts_diff明显增加，同时访问频率也变缓慢
### 存在的问题
由于本次实现的结果是异步的，所以client.py中每个线程并不能及时得到请求的结果，只能获得一个提交成功的信息。feed_back只在服务端保存，还没有一个优雅的方法使其返回给用户
