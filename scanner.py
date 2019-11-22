
from wifi import Cell, Scheme


def get_ssid(interface, valid_ssid, valid_encryption):
    aps = Cell.all(interface)
    invalid_AP = []
    sub_valid_AP = []

    for e in aps:
        if e.ssid != valid_ssid or  not e.encrypted or valid_encryption != e.encryption_type:
                invalid_AP.append((e.address, e.ssid))
        else:
            sub_valid_AP.append((e.address, e.ssid))
    return invalid_AP, sub_valid_AP


def control_AP(interface, valid_ssid, valid_sec):
    invalid, sub_valid = get_ssid(interface, valid_ssid, valid_sec)
    return invalid, sub_valid

print(control_AP("wlp5s0", "hackathon", "wpa2"))




