import argparse

import numpy as np
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # calculate and plot analytical results

    # load and plot simulation results
    # change delimiter '/t' into ','
    x, y = np.loadtxt('wait_time.out', delimiter=' = ', unpack=True)

    plt.plot(x, y)
    plt.xlabel('packet size B')
    plt.ylabel('waiting time ms')

    # add labels, legend, and title
    plt.legend()
    plt.title(r'variation of waiting time with the packet size')

    plt.savefig('waiting time.pdf')
    plt.show()
