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
    parser.add_argument(
        "-F",
        "--file_path",
        help="file_path",
        default='',
        type=str)
    parser.add_argument(
        "-A",
        "--arrival_rate",
        help="packet arrival rate [packets/s]; default is 1.0",
        default=1.0,
        type=float)
    parser.add_argument(
        "-S",
        "--service_rate",
        help="packet service rate [packets/s]; default is 10.0",
        default=0.1,
        type=float)

    args = parser.parse_args()

    file_path = args.file_path
    arrival_rate = args.arrival_rate
    service_rate = args.service_rate
    num_servers = args.num_servers

    file_prefix = file_path.split('.')[0]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Major ticks every 10, minor ticks every 5 for x axis
    x_major_ticks = np.arange(0, 101, 10)
    x_minor_ticks = np.arange(0, 101, 5)

    # Major ticks every 0.1, minor ticks every 0.1 for y axis
    y_major_ticks = np.arange(0, 1.1, 0.2)
    y_minor_ticks = np.arange(0, 1.1, 0.1)

    ax.set_xticks(x_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # calculate and plot analytical results

    # m/m/1 formula
    if num_servers == 1:
        x1 = np.arange(1, 100)
        y1 = 1 / (100 - x1)
        plt.plot(x1, y1, 'b-', label="Analysis", linewidth=1)

    else:

        # m/m/n formula
        m = num_servers

        x1 = np.arange(1, 100)
        p = x1 / service_rate / m

        n = np.arange(0, m)

        denominator = np.array([(m * p) ** num for num in n])

        division = np.array([math.factorial(num) for num in n])

        p0 = 1 / (sum(np.array([denominator[num] / division[num] for num in range(m)]))
                  + (m * p) ** m / math.factorial(m)
                  * 1 / (1 - p))

        pm = (m * p) ** m / (math.factorial(m) * (1 - p)) * p0

        y1 = p / (x1 * (1 - p)) * pm + 1 / service_rate

        plt.plot(x1, y1, 'b-', label="Analysis", linewidth=1)

    # load and plot simulation results
    # change delimiter '/t' into ','
    x2, y2 = np.loadtxt(file_path, delimiter='\t', unpack=True)
    plt.plot(x2, y2, 'rx', label="Simulation")

    # add labels, legend, and title
    plt.xlabel(r'$\lambda$ [pkts/s]')
    plt.ylabel(r'$E[T]$ [s]')
    plt.legend()
    plt.title(r'' + file_prefix + ' ($\mu=' + str(service_rate) + '$ [pkts/s])')

    plt.savefig(file_prefix + '.pdf')
    plt.show()
