#!/usr/bin/env bash
for i in $(seq 1 3 100);
do echo $i ;
python new_mm1.py -M 1 -A $i -S 100 >> mm1.out
done

python clean_data.py -F 'mm1.out' >> mm1_cleaned.out

python plot_mmN.py -F 'mm5_cleaned.out'