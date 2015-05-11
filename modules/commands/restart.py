#!/usr/bin/env python
# Restart Command for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

import os 

class CommandClass(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        user = user.split('!', 1)[0]
        print user
        if (user in self.main.settingsdb.smembers('accesslist')):
            self.main.logging('info', '{username} has requested I restart...'.format(username = user))
            self.main.msg(channel, 'Restarting now...')
            os.execv('/home/dev/confidence/confidence.py', [''])
        else:
            self.main.logging('crit', '{username} has issued the restart command, but does not have access.'.format(username = user))
            self.main.msg(channel, 'Access Denied')
