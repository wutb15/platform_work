FROM python:3.6
WORKDIR /app
COPY . /app
RUN pip install -U pip
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install -r requirements.txt
ENV NAME World
ENTRYPOINT ["python3","server.py"]
