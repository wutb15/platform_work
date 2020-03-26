#!/bin/bash
sudo docker container stop myflaskserver
sudo docker container rm myflaskserver
sudo docker image rm templeserver
