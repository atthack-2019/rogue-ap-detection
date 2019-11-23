import list_wifi_distances
import requests

rogue_mac = '04:F0:21:42:1A:06'
rogue_mac = '04:f0:21:45:cd:f3'
pi_id = 8


distance = list_wifi_distances.get_network(rogue_mac)
print(distance)
requests.post("http://10.10.10.93:8000/report", data={'id':pi_id, 'dist': distance})
