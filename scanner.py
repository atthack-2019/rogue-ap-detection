
import os
import threading
from argparse import ArgumentParser
import subprocess


def get_ssid(valid_ssid):
    p = \
        subprocess.Popen(
            'iwlist scan | grep "ESSID\nAddress"',
            shell=True, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    out = out.decode("utf-8")
    values = out.split("\n")[:-1]
#    print(values)
    for i in range(0, len(values)):
        if i % 2 == 0:
            print(values[i])
            values[i] = values[i].strip().split("-")[1][10:]
        else:
            values[i] = values[i].strip().split(":")[1].strip()
    invalid_AP = []
    sub_valid_AP = []

    for i in range(0, len(values), 2):
        if values[i+1] != valid_ssid:
            invalid_AP.append((values[i], values[i + 1]))
        else:
            sub_valid_AP.append((values[i], values[i+1]))

    return invalid_AP, sub_valid_AP


def check_same_encryption(networks, valid_sec, valid_type):
    pass


def control_AP(valid_ssid, valid_sec, valid_type):
    invalid, sub_valid = get_ssid(valid_ssid)
    #signature_check, new_invalids = check_same_encryption(sub_valid, valid_sec, valid_type)
    return invalid, sub_valid










