

# EEE413-Data Communication-lab2

####Author: Zhipeng Ye

#### Student ID: 1926908

#### Faculty: MSc Multimedia Telecommunications

#### Date: 18 December 2019



### Introduction

In the class, we have studied leaky bucket and token bucket theory which is a theory about controling flux passing through the system and promoting the quality of service. 

Leaky bucket controls the burst size [Figure 1]. This means the packet will be cut down when burst size is larger than the size of leaky bucket.

Moreover, token bucket controls the peak rate {Figure 2}. When the token bucket has enough token, the packet can pass through system.

<img src="/Users/geekye/Documents/Courses/Data communication/lab/lab2/leaky_bucket.png" alt="image-20191218074309210" style="zoom:50%;" />

<center>Figure 1</center>

![image-20191218074437114](/Users/geekye/Documents/Courses/Data communication/lab/lab2/figure2.png)

<center>Figure 2</center>

---

##### In this assignment, we focus on the Token bucket filter (TBF) [Figure 3].

![image-20191218085348653](/Users/geekye/Documents/Courses/Data communication/lab/lab2/figure3.png)

<center>Figure 3</center>

Here are the Token Bucket Filter parameters:

- Token generation rate: $\rho $ MB/s.
- Token bucket capacity: $C$ MB (full when the first burst arrives)
- Peak output rate: 10 MB/s (same as the input rate)

For designing the parameters of Token bucket Filter, we must do threes steps to do experiments correctly, using a fluid model (In a fluid model, traffic arrivals are assumed to be continuous like liquid flows rather than discrete ).

First of all, as we discussed in the lecture, the burst length S is given by $S = \frac{C}{M-\rho}$.

Because of $\rho = 10 MB/s$ , $S = \frac{C}{10-\rho}$.

As shown in Figure 3, the duration of burst is 0.001s (i.e., 1ms). we must make sure the first burst can pass through without no shaping.
$$
S = \frac{C}{10-\rho} \geq 0.001 \\
C \geq 0.01 - 0.001\rho
$$
So we get the minimum token bucket capacity $0.01-0.001\rho$ MB.

Secondly, for avoiding burst generation rate is larger than token bucket generation rate. We must make the amount tokens generated during the off period should be equal to or greater than the token bucket capacity.
$$
0.001\rho \geq 0.01-0.001\rho \\
\rho \geq 5
$$
Therefore, we get the minimum token generation rate is $5 MB/s$.

Finally, we obtain the minimum token bucket capacity $5kB$.

---

Simulation

In this simulation, we use simpy to simulate token bucket filter. 

Here is my python code (change the file supported by teacher), I convert uint from MB/s into b/s for conveniency.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     queue_onoff_traffic.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2018-11-23
#
# @brief    Simulate a queueing system with an on-off packet generator.
#


import argparse

import numpy as np
import simpy


class Packet(object):
    """
    Parameters:
    - ctime: packet creation time
    - size: packet size in bytes
    """

    def __init__(self, ctime, size):
        self.ctime = ctime
        self.size = size


class OnoffPacketGenerator(object):
    """Generate fixed-size packets back to back based on on-off status.

    Parameters:
    - env: simpy.Environment
    - pkt_size: packet size in bytes
    - pkt_ia_time: packet interarrival time in second
    - on_period: ON period in second
    - off_period: OFF period in second
    """

    def __init__(self, env, pkt_size, pkt_ia_time, on_period, off_period,
                 trace=False):
        self.env = env
        self.pkt_size = pkt_size
        self.pkt_ia_time = pkt_ia_time
        self.on_period = on_period
        self.off_period = off_period
        self.trace = trace
        self.out = None
        self.on = True
        self.gen_permission = simpy.Resource(env, capacity=1)
        self.action = env.process(self.run())  # start the run process when an instance is created

    def run(self):
        env.process(self.update_status())
        while True:
            with self.gen_permission.request() as req:
                yield req
                p = Packet(self.env.now, self.pkt_size)
                self.out.put(p)
                if self.trace:
                    print("t={0:.4E} [s]: packet generated with size={1:.4E} [B]".format(self.env.now, self.pkt_size))
            yield self.env.timeout(self.pkt_ia_time)

    def update_status(self):
        while True:
            now = self.env.now
            if self.on:
                if self.trace:
                    print("t={:.4E} [s]: OFF->ON".format(now))
                yield env.timeout(self.on_period)
            else:
                if self.trace:
                    print("t={:.4E} [s]: ON->OFF".format(now))
                req = self.gen_permission.request()
                yield env.timeout(self.off_period)
                self.gen_permission.release(req)
            self.on = not self.on  # toggle the status


class FifoQueue(object):
    """Receive, process, and send out packets.

    Parameters:
    - env : simpy.Environment
    """

    def __init__(self, env, trace=False):
        self.trace = trace
        self.store = simpy.Store(env)
        self.env = env
        self.out = None
        self.action = env.process(self.run())

        # unit b/ms
        self.transmission_rate = 10 * 10 ** 3
        self.token_rate = 5 * 10 ** 3
        self.capacity = 5 * 10 ** 3
        self.token_amount = self.capacity
        self.current_time = env.now

    def run(self):

        while True:
            msg = (yield self.store.get())

            # if msg.size <= self.capacity put packet into FIFO queue
            if msg.size <= self.capacity:
                now = env.now
                time_passed = now - self.current_time

                self.token_amount = self.token_amount + self.token_rate * time_passed

                if self.token_amount > self.capacity:
                    self.token_amount = self.capacity

                if msg.size > self.token_amount:

                    token_difference = msg.size - self.token_amount
                    yield self.env.timeout(token_difference / self.token_rate)
                    self.token_amount = 0
                else:
                    self.token_amount = self.token_amount - msg.size

                self.current_time = env.now

                delay_time = msg.size / self.transmission_rate
                yield self.env.timeout(delay_time)

                self.out.put(msg)

    def put(self, pkt):
        self.store.put(pkt)


class PacketSink(object):
    """Receives packets and display delay information.

    Parameters:
    - env : simpy.Environment
    - trace: Boolean

    """

    def __init__(self, env, trace=False):
        self.store = simpy.Store(env)
        self.env = env
        self.trace = trace
        self.wait_times = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            msg = (yield self.store.get())
            now = self.env.now
            self.wait_times.append(now - msg.ctime)
            if self.trace:
                print("t={0:.4E} [s]: packet arrived with size={1:.4E} [B]".format(now, msg.size))

    def put(self, pkt):
        self.store.put(pkt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-S",
        "--pkt_size",
        help="packet size [byte]; default is 100",
        default=100,
        type=int)
    parser.add_argument(
        "-A",
        "--pkt_ia_time",
        help="packet interarrival time [second]; default is 10 * 10 ** (-3)",
        default=10 * 10 ** (-3),
        type=float)
    parser.add_argument(
        "--on_period",
        help="on period [m second]; default is 1.0",
        default=1,
        type=float)
    parser.add_argument(
        "--off_period",
        help="off period [m second]; default is 1.0",
        default=1,
        type=float)
    parser.add_argument(
        "-T",
        "--sim_time",
        help="time to end the simulation [m second]; default is 2",
        default=2,
        type=float)
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
    pkt_size = args.pkt_size
    pkt_ia_time = args.pkt_ia_time
    on_period = args.on_period
    off_period = args.off_period
    sim_time = args.sim_time
    random_seed = args.random_seed
    trace = args.trace

    env = simpy.Environment()
    pg = OnoffPacketGenerator(env, pkt_size, pkt_ia_time, on_period, off_period,
                              trace)
    fifo = FifoQueue(env, trace)
    ps = PacketSink(env, trace)
    pg.out = fifo
    fifo.out = ps
    env.run(until=sim_time)

    print("{:.4E} = {:.4E}\n".format(pkt_size, np.mean(ps.wait_times)))
```

The main change implementing token bucket filter is 

```python
    def __init__(self, env, trace=False):
        self.trace = trace
        self.store = simpy.Store(env)
        self.env = env
        self.out = None
        self.action = env.process(self.run())

        # unit b/ms
        self.transmission_rate = 10 * 10 ** 3
        self.token_rate = 5 * 10 ** 3
        self.capacity = 5 * 10 ** 3
        self.token_amount = self.capacity
        self.current_time = env.now

    def run(self):

        while True:
            msg = (yield self.store.get())

            # if msg.size <= self.capacity put packet into FIFO queue
            if msg.size <= self.capacity:
                now = env.now
                time_passed = now - self.current_time

                self.token_amount = self.token_amount + self.token_rate * time_passed

                if self.token_amount > self.capacity:
                    self.token_amount = self.capacity

                if msg.size > self.token_amount:

                    token_difference = msg.size - self.token_amount
                    yield self.env.timeout(token_difference / self.token_rate)
                    self.token_amount = 0
                else:
                    self.token_amount = self.token_amount - msg.size

                self.current_time = env.now

                delay_time = msg.size / self.transmission_rate
                yield self.env.timeout(delay_time)

                self.out.put(msg)
```

I use the simpy.store to implement FIFO queue. According to the parameters I have calculated, I design a token bucket filter. 

Firstly, packet size can't be larger than the amount of capacity, therefore, I add the judgement statement.

Secondly, I compute the amount of token by passed time and token generation rate and if token amount larger than the capacity, the buffer will discard some token. 

Thirdly, if packet.size is larger than the amount of token, the packet will wait for token generation. If the pakcet size is samller than the amount of token, the packet don't need to wait for generating token.

Finally, I add the time costing in transmission.

Make packet size constant and change time.

