# platform_work
homework for cloud platform

## 第一阶段
### 简介
本阶段的作业是在本地实现响应高并发的访问的服务器。本次作业我采用的是单独使用python flask来作为服务端的架构。由于flask在默认的设置下是单线程的，这意味着如果处理大规模的耗时较多的请求时会有明显的阻塞。解决方案是首先利用flask软件中的threaded选项使得处理请求可以多线程处理,再利用BlockingQueue存储请求数据,并利用future为每个请求记录处理结果。ThreadPoolExecutor批量多线程执行请求的计算任务并得到结果，将结果存储到对应的future之中来实现异步的处理多线程请求。
### 程序简介
client.py可以使用命令行的形式更改参数，有'client.py -t <threadnumber> -i <imgfile>'来更改线程数量以及处理图片的来源，各个请求线程将收到到的feedback存储在time.json当中。
  
server.py则是通过更改代码中的batchsize参数来更改批量处理的请求数量，并将feed_back返回给各自的请求线程
### 简单观察的结果
通过增大线程数以及batchsize可以使得cpu负载不断提高，当cpu负载达到上限时会观察到ts_diff明显增加，同时访问频率也变缓慢
### 存在的问题
没有能够在服务器上运行,无法准确的测试真正高并发下的表现。同时本地机器上客户端与服务端并存，两者的表现容易混淆。

## 第二阶段
本阶段的作业是利用docker将服务封装起来，使其可以无
