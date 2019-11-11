#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     mm1.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2016-09-27
#
# @brief    Simulate M/M/1 queueing system
#
# @remarks  Copyright (C) 2016 Kyeong Soo (Joseph) Kim. All rights reserved.
#
# @remarks  This software is written and distributed under the GNU General
#           Public License Version 2 (http://www.gnu.org/licenses/gpl-2.0.html).
#           You must not remove this notice, or any other, from this software.
#

import argparse
import numpy as np
import random
import simpy
import sys


def source(env, mean_ia_time, mean_srv_time, server, wait_times, number, trace):
    """Generates packets with exponential interarrival time."""
    for i in range(number):
        ia_time = random.expovariate(1.0 / mean_ia_time)
        srv_time = random.expovariate(1.0 / mean_srv_time)
        pkt = packet(env, 'Packet-%d' % i, server, srv_time, wait_times, trace)
        env.process(pkt)
        yield env.timeout(ia_time)


def packet(env, name, server, service_time, wait_times, trace):
    """Requests a server, is served for a given service_time, and leaves the server."""
    arrv_time = env.now
    if trace:
        print('t=%.4Es: %s arrived' % (arrv_time, name))

    with server.request() as request:
        yield request

        wait_time = env.now - arrv_time
        wait_times.append(wait_time)
        if trace:
            print('t=%.4Es: %s waited for %.4Es' % (env.now, name, wait_time))
        yield env.timeout(service_time)
        if trace:
            print('t=%.4Es: %s served for %.4Es' %
                  (env.now, name, service_time))


def run_simulation(mean_ia_time, mean_srv_time, num_packets=1000, random_seed=1234, trace=True):
    """Runs a simulation and returns statistics."""
    print('M/M/1 queue\n')
    random.seed(random_seed)
    env = simpy.Environment()

    # start processes and run
    server = simpy.Resource(env, capacity=1)
    wait_times = []
    env.process(source(env, mean_ia_time,
                       mean_srv_time, server, wait_times, number=num_packets, trace=trace))
    env.run()

    # return statistics (i.e., mean waiting time)
    return np.mean(wait_times)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-A",
        "--mean_ia_time",
        help="mean packet interarrival time [s]; default is 1.0",
        default=1.0,
        type=float)
    parser.add_argument(
        "-S",
        "--mean_srv_time",
        help="mean packet service time [s]; default is 0.1",
        default=0.1,
        type=float)
    parser.add_argument(
        "-N",
        "--num_packets",
        help="number of packets to generate; default is 1000",
        default=1000,
        type=int)
    parser.add_argument(
        "-R",
        "--random_seed",
        help="seed for random number generation; default is 1234",
        default=1234,
        type=int)
    parser.add_argument('--trace', dest='trace', action='store_true')
    parser.add_argument('--no-trace', dest='trace', action='store_false')
    parser.set_defaults(trace=True)
    args = parser.parse_args()

    # set variables using command-line arguments
    mean_ia_time = args.mean_ia_time
    mean_srv_time = args.mean_srv_time
    num_packets = args.num_packets
    random_seed = args.random_seed
    trace = args.trace

    # run a simulation
    mean_waiting_time = run_simulation(
        mean_ia_time, mean_srv_time, num_packets, random_seed, trace)

    # print statistics from the simulation
    print("Average waiting time = %.4Es\n" % mean_waiting_time)
