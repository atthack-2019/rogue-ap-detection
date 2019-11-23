from flask import Flask, request
from list_wifi_distances import center_of_gravity, Circle, DIST_MULTIPLIER, colors
from my_trilateration import get_trilateration_point
import matplotlib
import matplotlib.pyplot as plt
import requests

app = Flask(__name__, static_url_path='')
matplotlib.use('Agg')

class AP:
    type_to_color = {
        'rogue': 'ro',
        'no_threat': 'go',
        'unknown': 'bo'
    }

    def __init__(self, ssid, bssid, position, threat_type, distance=-1.0):
        self.ssid = ssid
        self.bssid = bssid
        self.position = position
        self.threat_type = threat_type
        self.distance = distance

    def __repr__(self):
        return f"{self.bssid}: {self.position}, {self.distance}"

    def color(self):
        return self.type_to_color[self.threat_type]

def get_circles():
    circles = []
    for ap in aps:
        print(ap)
        if ap.distance > 0.0:
            circles.append(Circle(ap.position[0], ap.position[1], ap.distance * DIST_MULTIPLIER))
    print(len(circles))

    return circles

def draw():
    fig, ax = plt.subplots()
    ax.set_xlim((0, 1000))
    ax.set_ylim((1000, 0))
    plt.grid(linestyle='--')
    print(aps)

    if aps[-1].threat_type == "rogue":
        print("threat")
        circles = get_circles()
        i = 0
        for circle in circles:
            ax.add_artist(plt.Circle((circle.x, circle.y), circle.radius, color = colors[i], alpha=0.5))
            i += 1
        center_intersections = get_trilateration_point(circles)
        if center_intersections is not None:
            centers.append(center_intersections)
            aps[-1].position = center_intersections
        else:
            aps[-1].position = center_of_gravity(circles)

    for ap in aps:        
        plt.plot(ap.position[0], ap.position[1], ap.color())

    fig.savefig('static/plotaps.png', transparent=True)
    plt.close(fig)

def try_get(bssid):
    for ap in aps:
        if ap.bssid.startswith(bssid):
            return value
    return None


def add_rogue_ap(ssid, bssid):
    print(f"Added rogue AP with SSID {ssid}, BSSID {bssid}.")
    if try_get(bssid) is None:
        aps.append(AP(ssid, bssid, (69, 69), 'rogue'))

aps = [
    AP('RaspberryPi-21', 'b8:27:eb:ba:cf:95', (281, 91), 'no_threat'),
    AP('RaspberryPi-4', 'b8:27:eb:25:0c:e5', (150, 96), 'no_threat'),
    AP('RaspberryPi-6', 'b8:27:eb:fb:1d:f6', (140, 200), 'no_threat'),
    AP('RaspberryPi-8', 'b8:27:eb:3a:ef:b7', (280, 200), 'no_threat'),
    AP('hackathon', 'B4:FB:E4:2B:B7:', (313, 65), 'unknown'),
    AP('hackathon', 'B4:FB:E4:CF:88:', (224, 288), 'unknown'),
    AP('hackathon', 'B4:FB:E4:2B:B1:', (111, 614), 'unknown'),
    AP('hackathon', '18:E8:29:E', (394, 162), 'unknown'),
    AP('hackathon', 'F0:9F:C2:F:', (372, 495), 'unknown'),
    AP('hackathon', '78:8A:20:8', (778, 65), 'unknown'),
    AP('hackathon', 'B4:FB:E4:21:38:', (877, 490), 'unknown')
]

@app.route('/')
def home():
    draw()
    return app.send_static_file("index.html")

@app.route('/report', methods=['POST'])
def report():
    form = request.form.to_dict(flat=False)
    print(form)
    if form.get('dist', None) is not None:
        for i in range(len(aps)):
            if aps[i].ssid.endswith(form['id'][0]):
                aps[i].distance = float(form['dist'][1])
                print(aps[i].distance)
    return "OK"

@app.route('/rogue', methods=['POST'])
def rogue_receive_threat():
    form = request.form.to_dict(flat=False)
    bssid = form.get('bssid')[0]
    ssid = form.get('ssid')[0]
    add_rogue_ap(ssid, bssid)
    
    for i in range(len(aps)):
        if aps[i].ssid.startswith("RaspberryPi"):
            name, id = aps[i].ssid.split('-')
            if id == "21":
                print("no")
                #requests.post(url='http://192.168.1.10:7777', data = {'bssid': bssid})
            else:
                print(f"POST 10.10.1.{id} with bssid {bssid}    ")
                requests.post(url='http://10.10.1.{0}:7777'.format(id), data = {'bssid': bssid})
    
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')