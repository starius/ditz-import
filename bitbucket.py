#!/usr/bin/python

import urllib
import json

API_URL = "https://api.bitbucket.org/1.0/repositories/"

def get_url(url):
    return urllib.urlopen(url).read()

def user_repo(user, repo):
    return user + "/" + repo

class Bitbucket:
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.load_issues()
        self.build_components()

    def load_issues(self):
        url = API_URL + user_repo(self.user, self.repo) + "/issues/"
        self.overview = json.loads(get_url(url))
        self.issues = []
        for i in range(1, self.overview['count'] + 1):
            self.issues.append(json.loads(get_url(url + str(i))))

    def build_components(self):
        self.components = set()
        for issue in self.issues:
            component = issue['metadata']['component']
            if component:
                self.components.add(component)

