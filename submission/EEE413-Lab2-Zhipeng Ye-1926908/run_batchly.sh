#!/usr/bin/env bash

for i in $(seq 100 10 5000);
do echo $i ;
python queue_onoff_traffic.py -S $i -T 2 --no-trace >> wait_time.out
done



python queue_onoff_traffic.py -S 3000 -T 2 >> wait_time_trace.out

python queue_onoff_traffic.py -S 200 -T 10 --no-trace >> eachpacket_waitingtime_data.out

python queue_onoff_traffic.py -S 200 -T 10 --on_period 0.3 --off_period 1 --no-trace >> eachpacket_waitingtime_data200.out

python queue_onoff_traffic.py -S 20 -T 2 --no-trace >> eachpacket_waitingtime_data200.out