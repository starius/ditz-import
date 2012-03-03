#!/usr/bin/python

import argparse
import json
from bitbucket import Bitbucket

def bitbucket_issues(user, repo, out):
    bb = Bitbucket(user, repo)
    json.dump(bb.issues, out, indent=2)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-u', '--user', required=True, help="Bitbucket user name")
    p.add_argument('-r', '--repo', required=True, help="Bitbucket repo name")
    p.add_argument('-o', '--out', default='-', help="Output file",
            type= argparse.FileType('w'))
    args = p.parse_args()
    bitbucket_issues(user=args.user, repo=args.repo, out=args.out)

if __name__ == '__main__':
    main()

