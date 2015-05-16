#!/us/bin/env python
# Resume Monitoring Command for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

class CommandClass(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        self.main.startScheduler()
        self.main.msg(self.main.loggingchannel, 'I\'m awake, go away.')
