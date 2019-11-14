#!/usr/bin/env bash

for i in $(seq 5 5 95);
do echo $i ;
python new_mmN.py -M 1 -A $i -S 100 -N 10000 --no-trace >> mm1.out
done

for i in $(seq 5 5 95);
do echo $i ;
python new_mmN.py -M 2 -A $i -S 50 -N 10000 --no-trace >> mm2.out
done

for i in $(seq 5 5 95);
do echo $i ;
python new_mmN.py -M 5 -A $i -S 20 -N 10000 --no-trace >> mm5.out
done

python plot_mmN.py -F 'mm1.out'
python plot_mmN.py -F 'mm2.out'
python plot_mmN.py -F 'mm5.out'