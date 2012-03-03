#!/usr/bin/python

import argparse
from bitbucket import Bitbucket
from ditz import Ditz

def bitd(user, repo, email):
    bb = Bitbucket(user, repo)
    d = Ditz(user, repo, email)
    d.init()
    for component in bb.components:
        d.add_component(component)
    for issue in bb.issues:
        title = issue['title']
        content = issue['content']
        kind = 'f'
        if issue['metadata']['kind'] == 'bug':
            kind = 'b'
        if issue['metadata']['kind'] == 'task':
            kind = 't'
        component = issue['component']
        user = issue['reported_by']['first_name'] + " " + \
                issue['reported_by']['last_name']
        email = ''
        date = issue['created_on']
        issue_number = d.add_issue(title, content, kind,
                component, user, email, date)
        for comment in issue['comments']:
            content = comment['content']
            user = issue['author_info']['first_name'] + " " + \
                    issue['author_info']['last_name']
            email = ''
            date = comment['utc_created_on']
            d.add_comment(component, issue_number, content, user, email, date)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-u', '--user', required=True, help="Bitbucket user name")
    p.add_argument('-r', '--repo', required=True, help="Bitbucket repo name")
    p.add_argument('-e', '--email', required=True, help="Your e-mail")
    args = p.parse_args()
    bitd(user=args.user, repo=args.repo, email=args.email)

if __name__ == '__main__':
    main()

