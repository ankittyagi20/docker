#!/usr/bin/env python

import os
import subprocess
import json
from git import Repo

def get_git_repo(repo_url, repo_dir):
  try:
    cloned_repo = Repo.clone_from(repo_url, repo_dir)
    if cloned_repo.git_dir:
      print("{}".format("True"))

  except RuntimeError as e:
    print("Error occurred: {}".format(e))

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

if __name__ == '__main__':
    repo_url = os.environ['REPO_URL']
    repo_dir = os.environ['REPO_DIR']
    get_git_repo(repo_url=repo_url, repo_dir=repo_dir)
    install_flask()
    version = get_flask_version()
    install_flask(version)
