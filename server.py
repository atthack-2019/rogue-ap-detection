from flask import Flask, request
from list_wifi_distances import get_circles, print_circles, center_of_gravity
from my_trilateration import get_trilateration_point

app = Flask(__name__, static_url_path='')

nets = [
    ('21', 15),
    ('4', 15),
    ('6', 15),
    ('8', 15)
]

positions = {
    '21': (0, 0),
    '4': (0, 500),
    '6': (500, 500),
    '8': (500, 0)
}

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