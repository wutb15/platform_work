#!/bin/bash
b=${1:-10}
p=${2:-5000}
docker run -p ${p}:80 -d --name myflaskserver --volumes-from mydatacontainer templeserver -b ${b}

