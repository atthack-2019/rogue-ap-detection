#!/usr/bin/python3

import numpy as np
from wifi import Cell
import matplotlib.pyplot as plt
from my_trilateration import get_center_kukly

DIST_MULTIPLIER = 15.55555555

positions = {
    'B4:FB:E4:2B:B7:': (313, 65),
    'B4:FB:E4:CF:88:': (224, 288),
    'B4:FB:E4:2B:B1:': (111, 614),
    '18:E8:29:E': (394, 162),
    'F0:9F:C2:F:': (372, 495),
    '78:8A:20:8': (778, 65),
    'B4:FB:E4:21:38:': (877, 490)
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
        return f"Circle({self.x}, {self.y}, {self.radius})"

def try_get(positions, mac):
    for key, value in positions.items():
        if mac.startswith(key):
            return value
    return None

def get_circles(nets, positions):
    circles = []
    for (mac, dist) in nets:
        print(mac)
        pos = try_get(positions, mac)
        if pos is not None:
            circles.append(Circle(pos[0], pos[1], dist * DIST_MULTIPLIER))
    return circles

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] * 2
def print_circles(circles_ls, centers):
    plt_circles = []
    for i in range (len(circles_ls)):
        circle = circles_ls[i]
        plt_circles.append(plt.Circle((circle.x, circle.y), circle.radius, color = colors[i], alpha=0.5))
    fig, ax = plt.subplots()
    plt.grid(linestyle='--')
    ax.set_xlim((0, 650))
    ax.set_ylim((0, 650))
    for c in plt_circles:
        ax.add_artist(c)
    center_colors = ['r', 'b']
    i = True
    for center in centers:
        plt.plot(center[0], center[1], center_colors[i] + 'o')
        i = ~i
    fig.savefig('plotcircles.png')

def center_of_gravity(circles):
    mean_x = 0.0
    mean_y = 0.0
    mass_sum = 0.0

    for circle in circles:
        mass = 1.0 / (circle.radius)
        mass_sum += mass
        mean_x += mass * circle.x
        mean_y += mass * circle.y
    
    mean_x /= mass_sum
    mean_y /= mass_sum
    return (mean_x, mean_y)

if __name__ == '__main__':
    nets = get_networks()

    #circles = [Circle(224, 288, 98.30908117508503), Circle(111, 614, 530.7598666118824), Circle(313, 65, 9.36606857087998), Circle(877, 490, 869.9444473308448)]

    circles = get_circles(nets, positions)
    print(circles)
    center_gravity = center_of_gravity(circles)
    center_kukly = get_center_kukly(circles)
    
    print_circles(circles, [center_gravity, center_kukly])

