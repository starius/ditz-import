#!/usr/bin/python

from tempfile import NamedTemporaryFile as Temp
import os

def sh(cmd):
    print(cmd)
    os.system(cmd)

class Ditz:
    def __init__(self, user, repo, email):
        self.user = user
        self.email = email
        self.repo = repo
        self.components = []
        self.issue_number = {} # component : max issue number

    def add_headers(self, file, user=None, email=None):
        file.write((user or self.user) + "\n")
        file.write((email or self.email) + "\n")
        file.write("bugs" + "\n")

    def init(self):
        sh("rm .ditz-config")
        t = Temp()
        self.add_headers(t)
        t.write(self.repo + "\n")
        t.write("y\n")
        t.write("d\n")
        t.flush()
        sh("ditz init < " + t.name)

    def add_component(self, component):
        sh("rm .ditz-config")
        self.components.append(component)
        t = Temp()
        self.add_headers(t)
        t.write(component + "\n")
        t.flush()
        sh("ditz add-component < " + t.name)

    def add_issue(self, title, content, kind, component, user, email, date):
        sh("date -s '%s'" % date)
        sh("rm .ditz-config")
        if not component:
            component = self.repo
        issue_number = self.issue_number.get(component, 0) + 1
        self.issue_number[component] = issue_number
        t = Temp()
        self.add_headers(t, user=user, email=email)
        t.write(title + "\n")
        t.write(content + "\n" + "/stop\n")
        t.write(kind + "\n")
        component_number = 1
        if component in self.components:
            component_number = self.components.index(component) + 2
        t.write(component_number + "\n")
        t.write("" + "/stop\n")
        t.flush()
        sh("ditz add < " + t.name)
        return issue_number

    def close_issue(self, component, issue_number):
        sh("ditz close " + comment + "-" + issue_number)

    def add_comment(self, component, issue_number, content, user, email, date):
        sh("date -s '%s'" % date)
        sh("rm .ditz-config")
        t = Temp()
        self.add_headers(t, user=user, email=email)
        t.write(content + "\n" + "/stop\n")
        t.flush()
        sh("ditz comment " + component + "-" + issue_number + " < " + t.name)

