#!/usr/bin/python3

import numpy as np
from wifi import Cell

def get_freq(frequency):
    return float(frequency.split()[0]) * 1000

def is_2_4(freq):
    return freq > 2000 and freq < 3000

def get_networks():
    nets = list(Cell.all('wlan0'))
    for net in nets:
        freq = get_freq(net.frequency)
        if is_2_4(freq):
            print(net.address, dist(net.signal, freq))

def dist(sig, freq=2412):
    return 10**((27.55-(20*np.log10(freq)) - sig)/20.0)

get_networks()
