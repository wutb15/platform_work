#!/bin/bash
sudo docker build -t templeserver .
sudo docker run -p 5000:80 -d --name myflaskserver templeserver
