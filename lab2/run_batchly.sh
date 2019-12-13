#!/usr/bin/env bash

for i in $(seq 100 100 8000);
do echo $i ;
python queue_onoff_traffic.py -S $i -T 2 --no-trace >> wait_time.out
done