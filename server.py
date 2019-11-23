from flask import Flask, request
from list_wifi_distances import get_circles, print_circles, center_of_gravity
from my_trilateration import get_trilateration_point

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
        self.type = threat_type

    def color(self):
        return type_to_color[self.threat_type]

def draw(aps):
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
    if try_get(bssid) is None:
        
        aps.append(AP(ssid, bssid, (), 'rogue'))
    pass

nets = [
    AP('RaspberryPi-21' 'b8:27:eb:ba:cf:95', (0, 0), 'no_threat'),
    AP('RaspberryPi-4', 'b8:27:eb:25:0c:e5', (0, 500), 'no_threat'),
    AP('RaspberryPi-6', 'b8:27:eb:fb:1d:f6', (500, 500), 'no_threat'),
    AP('RaspberryPi-8', 'b8:27:eb:3a:ef:b7', (500, 0), 'no_threat'),
    AP('hackathon', 'B4:FB:E4:2B:B7:': (313, 65), 'unknown'),
    AP('hackathon', 'B4:FB:E4:CF:88:': (224, 288), 'unknown'),
    AP('hackathon', 'B4:FB:E4:2B:B1:': (111, 614), 'unknown'),
    AP('hackathon', '18:E8:29:E': (394, 162), 'unknown'),
    AP('hackathon', 'F0:9F:C2:F:': (372, 495), 'unknown'),
    AP('hackathon', '78:8A:20:8': (778, 65), 'unknown'),
    AP('hackathon', 'B4:FB:E4:21:38:': (877, 490), 'unknown')
]

@app.route('/')
def home():
    return app.send_static_file("index.html")

@app.route('/report', methods=['POST'])
def report():
    form = request.form.to_dict(flat=False)
    print(form)
    if form.get('dist', None) is not None:
        for i in range(len(nets)):
            if nets[i][0] == form['id'][0]:
                nets[i] = (nets[i][0], float(form['dist'][1]))
    circles = get_circles(nets, positions)
    center_kukly = get_trilateration_point(circles)
    center_gravity = center_of_gravity(circles)
    if center_kukly is None:
        print("fail")
        center_kukly = (-500, -500)
    print_circles(circles, [center_gravity, center_kukly])
    return str(nets)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')