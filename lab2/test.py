#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: test.py
# @time: 2019-12-10 19:23
# @desc:

import simpy
import time

if __name__ == "__main__":

    for i in range(10):
       time.sleep(0.1)
       print("The order is ", i)