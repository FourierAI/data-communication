#!/usr/bin/env bash

for i in $(seq 100 100 5000);
do echo $i ;
python queue_onoff_traffic.py -S $i -T 2 --no-trace >> test.out
done