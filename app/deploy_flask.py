#!/usr/bin/env python

import os
import subprocess
import json

def get_config_dict(environment):
  conf_file=open("/app/docker_configs/"+environment+"/configs.json", 'r')
  conf_dict=json.load(conf_file)
  conf_file.close()
  return conf_dict

def get_environment():
  environment=os.environ['ENVIRONMENT']
  return environment

def get_app_name():
  environment = get_environment()
  conf_dict = get_config_dict(environment)
  app_name = conf_dict['flask_docker_configs']['APP_NAME']
  conf_file.close()
  return app_name

def get_flask_version():
  version=os.environ['VERSION']
  return version

def install_flask():
  app_name = get_app_name()
  version = get_flask_version()
  cmd="pip install "+app_name+"=="+version
  process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output, error

def get_port():
  flask_app_port = os.environ['APP_PORT']
  return flask_app_port

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

