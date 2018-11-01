#!/usr/bin/env python

from git import Repo
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="url of the git repo", dest="u")
parser.add_argument("-d",help="local directory where to clone, the directory should be empty if already exists",
                   dest="d")

args = parser.parse_args()

git_url=args.u
repo_dir=args.d

try:

    cloned_repo = Repo.clone_from(git_url, repo_dir)
    if cloned_repo.git_dir:
        print("{}".format("True"))

except RuntimeError as e:
    print("Error occurred: {}".format(e))
