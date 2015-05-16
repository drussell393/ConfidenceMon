#!/usr/bin.env python
# Rehash Command Module for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)


class CommandClass(object):

    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        self.main.reloadsettings()
