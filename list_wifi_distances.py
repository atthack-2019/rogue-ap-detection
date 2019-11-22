#!/usr/bin/python3

import numpy as np
from wifi import Cell

def get_freq(frequency):
    return float(frequency.split()[0]) * 1000

def get_networks():
    nets = list(Cell.all('wlan0'))
    for net in nets:
        print(net.address, dist(net.signal, get_freq(net.frequency)))

def dist(sig, freq=2412):
    return 10**((27.55-(20*np.log10(freq)) - sig)/20.0)

get_networks()
