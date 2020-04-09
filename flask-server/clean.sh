#!/bin/bash
docker container stop myflaskserver
docker container rm myflaskserver
docker image rm templeserver

