import subprocess
import time
import importlib

importlib.import_module("scanner")
import scanner

template = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CZ

network={{
        bssid={1}
	ssid="{0}"
	key_mgmt=WPA-EAP
	pairwise=CCMP TKIP
	group=CCMP TKIP
	eap=PEAP
	identity="bob"
	password="hello"
	ca_cert="/home/pi/ca.pem"
	phase2="MSCHAPV2"
}}
"""

# BAD = "04:f0:21:42:1a:06"
GOOD = "04:f0:21:45:cd:f3"

def generate_wpasupplicant(ssid, bssid):
    filled = template.format(ssid, bssid)
    with open("/tmp/wpa_supplicant", "w") as f:
        f.write(filled)

def run_scan():
    cmd = "sudo rm /var/run/wpa_supplicant/wlan0"
    p = subprocess.Popen(cmd, shell=True)
    cmd = "sudo wpa_supplicant -c /tmp/wpa_supplicant -i wlan0 > /tmp/out"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(20)
    cmd = "sudo killall wpa_supplicant"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def check_result():
    with open("/tmp/out") as f:
        res = f.read()
        if "CTRL-EVENT-EAP-SUCCESS" in res and "CTRL-EVENT-EAP-FAILURE EAP" not in res:
            print("OK")
        else:
            print("FAIL")



invalid, to_check = scanner.control_AP('"turris-WPA2ent"', "", "")
print(invalid, to_check)
for tup in to_check:
    bssid = tup[0]
    generate_wpasupplicant('turris-WPA2ent', bssid)
    run_scan()
    print(tup)
    check_result()
