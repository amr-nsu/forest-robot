#!/bin/sh

sudo pigpiod

BASE_PATH=/home/ubuntu/work/fores-robot/server
cd $BASE_PATH

python3 server.py
