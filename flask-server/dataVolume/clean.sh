#!/bin/bash
docker container stop mydatacontainer
docker container rm mydatacontainer
docker image rm serverdata
