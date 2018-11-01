#!/usr/bin/env python

from flask import Flask
app = Flask('__name__')
@app.route('/')
def hello_world():
    return 'Welcome to the Flask App'

if __name__ == '__main__':
    install_flask()
    PORT = get_port()
    install_flask(version)
    app.run(debug=True,host='0.0.0.0', port=int(PORT))
