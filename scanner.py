
from wifi import Cell, Scheme


def get_ssid(interface, valid_ssid, valid_encryption):
    aps = Cell.all(interface)
    invalid_AP = []
    sub_valid_AP = []

    for e in aps:
        if e.ssid != valid_ssid:
                invalid_AP.append((e.address, e.ssid))
        else:
            sub_valid_AP.append((e.address, e.ssid))
    return invalid_AP, sub_valid_AP


def control_AP(interface, valid_ssid, valid_sec):
    return get_ssid(interface, valid_ssid, valid_sec)





