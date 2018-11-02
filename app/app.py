#!/usr/bin/env python

import sys
from flask import Flask
import flask

sys.path.append(".")
from deploy_flask import get_port, get_environment, get_flask_version

app = Flask('__name__')
@app.route('/')
def hello_world():
    env = get_environment()
    ver = flask.__version__
    ret_val = "<h2 style='color:blue'>Welcome to the sample flask app, this is{} environment</h2> <h2 style='color:green'> and the flask version is: {}</h2>".format(env,ver)
    return ret_val

if __name__ == '__main__':
    try:
        PORT = get_port()
    except:
        PORT = "9090"
    if PORT == "":
        PORT = "9090"
    app.run(debug=True,host='0.0.0.0', port=int(PORT))
