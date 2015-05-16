#!/usr/bin/env python
# Restart Command for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

import os


class CommandClass(object):

    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        self.main.logging(
            'info', '{username} has requested I restart...'.format(username=user))
        self.main.msg(channel, 'Restarting now...')
        os.execv('/home/dev/confidence/confidence.py', [''])
