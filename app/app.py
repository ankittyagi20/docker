#!/usr/bin/env python

import os
from flask import Flask
from deploy_flask import get_port

app = Flask('__name__')
@app.route('/')
def hello_world():
    return 'Welcome to the Flask App'

if __name__ == '__main__':
    PORT = get_port()
    app.run(debug=True,host='0.0.0.0', port=int(PORT))
