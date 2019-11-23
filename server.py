from flask import Flask, request
from list_wifi_distances import get_circles, print_circles
from my_trilateration import get_trilateration_point

app = Flask(__name__, static_url_path='')

nets = [
    ('21', 5),
    ('4', 5),
    ('6', 5),
    ('8', 5)
]

positions = {
    '21': (0, 0),
    '4': (0, 233),
    '6': (233, 233),
    '8': (233, 0)
}

@app.route('/')
def home():
    circles = get_circles(nets, positions)
    center_kukly = get_trilateration_point(circles)
    if center_kukly is None:
        print("fail")
        center_kukly = (-500, -500)
    print_circles(circles, [center_kukly])
    return app.send_static_file("index.html")

@app.route('/report', methods=['POST'])
def report():
    form = request.form.to_dict(flat=False)
    print(form)
    if form.get('dist', None) is not None:
        for i in range(len(nets)):
            if nets[i][0] == form['id'][0]:
                nets[i] = (nets[i][0], float(form['dist'][1]))
    return str(nets)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')