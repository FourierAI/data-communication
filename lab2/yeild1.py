#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: yeild1.py
# @time: 2019-12-09 12:34
# @desc:


def sum_my(Max):
    sum = 0
    while sum < Max:
        sum = sum + 1
        yield sum


for i in sum_my(100):
    print(i)
