#!/bin/bash
docker build -t templeserver .
docker run -p 5000:80 -d --name myflaskserver --volumes-from mydatacontainer templeserver
