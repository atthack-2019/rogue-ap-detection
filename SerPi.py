from flask import Flask
from flask import request
import reporter
from time import sleep


app = Flask('SerPi')


@app.route('/', methods=['POST'])
def measure():
    bssid = request.form.get('bssid')
    for i in range(4):
        reporter.report(bssid)
        sleep(1)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
