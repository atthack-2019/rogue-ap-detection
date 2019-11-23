import list_wifi_distances
import requests


def report(rogue_mac):
    pi_id = 8
    distance = list_wifi_distances.get_network(rogue_mac.upper())
    print(distance)
    requests.post("http://10.10.10.93:8000/report", data={'id':pi_id, 'dist': distance})
