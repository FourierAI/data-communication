#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: plot_each_delay.py
# @time: 2019-12-19 23:00
# @desc:

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x_major_locator = MultipleLocator(1)

    ax.xaxis.set_major_locator(x_major_locator)

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # calculate and plot analytical results

    # load and plot simulation results
    # change delimiter '/t' into ','
    x, y = np.loadtxt('eachpacket_waitingtime_data200.out', delimiter=',', unpack=True)

    data_frame = {}

    for i in range(len(x)):
        data_frame[x[i]] = y[i]

    xlab = np.arange(min(x), max(x) + 0.01, 0.01).tolist()

    ylab = []

    for x in xlab:

        y_value = data_frame.get(round(x,5))
        if y_value == None:
            ylab.append(0)
        else:
            ylab.append(y_value)

    plt.plot(xlab, ylab)
    plt.xlabel('each packet generation timestamp ms')
    plt.ylabel('waiting time ms')

    # add labels, legend, and title
    plt.legend()
    plt.title(r'each packet waiting time')

    plt.savefig('each packet waiting time.pdf')
    plt.show()
