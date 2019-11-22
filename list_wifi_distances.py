#!/usr/bin/python3

import numpy as np
from wifi import Cell
import matplotlib.pyplot as plt

DIST_MULTIPLIER = 20.0

positions = {
    'B4:FB:E4:2B:B7:': (631, 312),
    'B4:FB:E4:CF:88:': (407, 222),
    'B4:FB:E4:2B:B1:': (83, 110),
    '18:E8:29:E1:76:': (546, 395),
    'F0:9F:C2:FE:26:': (200, 371),
    '78:8A:20:80:4A:': (629, 779),
    'B4:FB:E4:21:38:': (206, 877)
}

def get_freq(frequency):
    return float(frequency.split()[0]) * 1000

def get_networks():
    result = []
    nets = list(Cell.all('wlan0'))
    for net in nets:
        freq = get_freq(net.frequency)
        print(net.address, freq)
        result.append((net.address, dist(net.signal, freq)))

    return result


def dist(sig, freq=2412):
    return 10 ** ((27.55 - (20 * np.log10(freq)) - sig) / 20.0)

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.radius})"

def get_circles(nets, positions):
    circles = []
    for (mac, dist) in nets:
        print(mac)
        pos = positions.get(mac[:-2], None)
        if pos is not None:
            circles.append(Circle(pos[0], pos[1], dist * DIST_MULTIPLIER))
    return circles

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
def print_circles(circles_ls):
    plt_circles = []
    for i in range (len(circles_ls)):
        circle = circles_ls[i]
        plt_circles.append(plt.Circle((circle.x, circle.y), circle.radius, color = colors[i], alpha=0.5))
    fig, ax = plt.subplots()
    plt.grid(linestyle='--')
    ax.set_xlim((-1000, 1000))
    ax.set_ylim((-1000, 1000))
    for c in plt_circles:
        ax.add_artist(c)
    fig.savefig('plotcircles.png')
    plt.show()

if __name__ == '__main__':
    nets = get_networks()

    circles = get_circles(nets, positions)
    print(circles)
    print_circles(circles)