from flask import Flask, request
from list_wifi_distances import get_circles, print_circles, center_of_gravity
from my_trilateration import get_trilateration_point
import matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='')
matplotlib.use('Agg')

class AP:
    type_to_color = {
        'rogue': 'ro',
        'no_threat': 'go',
        'unknown': 'bo'
    }

    def __init__(self, ssid, bssid, position, threat_type):
        self.ssid = ssid
        self.bssid = bssid
        self.position = position
        self.threat_type = threat_type

    def color(self):
        return self.type_to_color[self.threat_type]

def draw():
    fig, ax = plt.subplots()
    ax.set_xlim((-1000, 1000))
    ax.set_ylim((-1000, 1000))
    plt.grid(linestyle='--')

    for ap in aps:
        plt.plot(ap.position[0], ap.position[1], ap.color())

    fig.savefig('static/plotaps.png', transparent=True)
    plt.close(fig)

def try_get(bssid):
    for ap in aps:
        if ap.bssid.startswith(key):
            return value
    return None

def get_circles():
    circles = []
    for (mac, dist) in nets:
        pos = try_get(positions, mac)
        if pos is not None:
            circles.append(Circle(pos[0], pos[1], dist * DIST_MULTIPLIER))
    return circles

def add_rogue_ap(ssid, bssid):
    print(f"Added rogue AP with SSID {ssid}, BSSID {bssid}.")
    if try_get(bssid) is None:
        aps.append(AP(ssid, bssid, (0, 0), 'rogue'))

rogue_ap = None
aps = [
    AP('RaspberryPi-21', 'b8:27:eb:ba:cf:95', (0, 0), 'no_threat'),
    AP('RaspberryPi-4', 'b8:27:eb:25:0c:e5', (0, 500), 'no_threat'),
    AP('RaspberryPi-6', 'b8:27:eb:fb:1d:f6', (500, 500), 'no_threat'),
    AP('RaspberryPi-8', 'b8:27:eb:3a:ef:b7', (500, 0), 'no_threat'),
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
    return app.send_static_file("index.html")

@app.route('/report', methods=['POST'])
def report():
    form = request.form.to_dict(flat=False)
    print(form)
    if form.get('dist', None) is not None:
        for i in range(len(aps)):
            if form['id'][0].startswith(aps[i].bssid):
                circles = get_circles()
                center_intersections = get_trilateration_point(circles)
                if center_intersections is not None:
                    centers.append(center_intersections)
                    aps[i].position = center_intersections
                else:
                    aps[i].position = center_of_gravity(circles)
    draw()
    return "OK"

@app.route('/rogue', methods=['POST'])
def rogue_receive_threat():
    form = request.form.to_dict(flat=False)
    if form.get['bssid'] and form.get['ssid'] is not None:
        bssid = form.get['bssid']
        ssid = form.get['ssid']
    for i in range(len(nets)):
        request.post('10.10.1.{0}'.format(nets[i][0]), data = {'bssid': bssid})
    add_rogue_ap(ssid, bssid, (0, 0), 'threat')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')
    draw()