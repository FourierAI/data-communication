#!/usr/bin/env bash
for i in $(seq 1 3 100);
do echo $i ;
python new_mm1.py -M 1 -A $i -S 100 >> mm1.out