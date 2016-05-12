#!/bin/sh
/usr/bin/pkill -f nai.py
rm /var/log/nai/u555fc199b2f588047d59e9068b77b1b9.pid 
python nai.py &
ps -ax | grep nai.py
