#!/usr/bin/env python
# Command Handler Module for Confidence Monitor
# Author: Dave Russell Jr (drussell393)

import glob
import os
import imp


class CommandHandler(object):

    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, message, user):
        self.messageParts = message.split()
        if (len(self.messageParts) >= 2):
            self.command = message.split()[1]
            self.commands = list()
            for command in glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/commands/*.py'):
                self.commands.append(command[38:-3])
            if (self.command in self.commands):
                self.handle(channel, message, user)
            else:
                self.main.logging('info', '{username} provided unknown command: {command}'.format(
                    username=user, command=self.command))
                self.main.msg(channel, 'That command does not exist.')
        else:
            self.main.msg(channel, 'Not enough arguments to be a command.')

    def handle(self, channel, message, user):
        try:
            mod = imp.load_source('Confidence_Monitoring_Module_' + self.command, os.path.dirname(
                os.path.abspath(__file__)) + '/commands/' + self.command + '.py')
            mod = mod.CommandClass(self.main)
            mod = mod.init(channel, message, user)
        except Exception as e:
            self.main.msg(channel, 'Module failed to load: ' + str(e))
            self.main.logging('crit', 'Module failed to load: ' + str(e))
