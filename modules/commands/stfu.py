#!/usr/bin/env python

class CommandClass(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        self.main.sched.shutdown()
        self.main.msg(channel, 'STFU\'d by {username}'.format(username = user))

