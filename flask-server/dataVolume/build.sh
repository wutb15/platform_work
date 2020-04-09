#!/bin/bash
docker build -t serverdata .
docker run  -itd --name mydatacontainer serverdata
