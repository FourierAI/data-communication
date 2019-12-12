import argparse

import numpy as np
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-M",
        "--num_servers",
        help="number of servers; default is 1",
        default=1,
        type=int)

    args = parser.parse_args()

    num_servers = args.num_servers

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Major ticks every 10, minor ticks every 5 for x axis
    # x_major_ticks = np.arange(0, 101, 10)
    # x_minor_ticks = np.arange(0, 101, 5)
    #
    # # Major ticks every 0.1, minor ticks every 0.1 for y axis
    # y_major_ticks = np.arange(0, 1.1, 0.2)
    # y_minor_ticks = np.arange(0, 1.1, 0.1)

    # ax.set_xticks(x_major_ticks)
    # ax.set_xticks(x_minor_ticks, minor=True)
    # ax.set_yticks(y_major_ticks)
    # ax.set_yticks(y_minor_ticks, minor=True)

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # calculate and plot analytical results

    # load and plot simulation results
    # change delimiter '/t' into ','
    y1 = np.loadtxt('token2.out', unpack=True)
    x1 = list(range(len(y1)))

    plt.plot(x1, y1, label="Simulation")

    # add labels, legend, and title
    plt.legend()
    plt.title(r'$ [pkts/s])')

    plt.savefig('token.pdf')
    plt.show()
