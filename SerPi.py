from flask import Flask
from flask import request
import reporter

app = Flask('SerPi')


@app.route('/', methods=['POST'])
def measure():
    bssid = request.args.get('bssid')
    reporter.report(bssid)
    return


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7777)
