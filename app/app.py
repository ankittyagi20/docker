#!/usr/bin/env python

import sys
from flask import Flask

sys.path.append(".")
from deploy_flask import get_port, get_environment, get_flask_version

app = Flask('__name__')
@app.route('/')
def hello_world():
    env = get_environment()
    ver = get_flask_version()
    ret_val = "Welcome to the sample flask app, this is {} environment and the flask version is: {}".format(env,ver)
    return ret_val

if __name__ == '__main__':
    PORT = get_port()
    #PORT = 9090
    app.run(debug=True,host='0.0.0.0', port=int(PORT))
