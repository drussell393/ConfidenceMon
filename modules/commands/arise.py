#!/us/bin/env python
# Resume Monitoring Command for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

class CommandClass(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        self.main.sched.start()
        self.main.sched.add_job(self.main.getZabEvents, trigger = 'interval', minutes = 2)
        self.main.msg(self.main.loggingchannel, 'I\'m awake, go away.')
