#!/usr/bin/env python
# PM Handler for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

class PMHandler(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, message, user):
        self.main.logging('info', '{username} has PM\'d me with: {message}'.format(username = user, message = message))
        self.main.msg(user, 'Please do not PM me. I am a bot, not your friend.')

