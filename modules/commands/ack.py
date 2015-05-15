#!/usr/bin/env python
# Acknowledgement Command Module for Confidence Monitoring Bot
# Author: Dave Russell Jr (drussell393)

import imp
import os
import json

class CommandClass(object):
    def __init__(self, confidence):
        self.main = confidence

    def init(self, channel, msg, user):
        user = user.split('!', 1)[0]
        if (len(msg.split()) >= 3):
            mod = imp.load_source('Confidence_Monitor_Bot_Zabbix', os.path.dirname(os.path.abspath(__file__)) + '/../zabbix.py')
            self.zabapi = mod.ZabbixAPI(url = self.main.settingsdb.get('zaburl'), user = self.main.settingsdb.get('zabid'), password = self.main.settingsdb.get('zabpass'))
            host = self.zabapi.host.get(search = msg.split()[2], limit = 1)
            if (len(host) >= 1):
                event = self.zabapi.event.get(search = msg.split()[3], hostids = int(host[0]['hostid']), acknowledged = False)
                if (len(event) >= 1):
                    self.ack(host, event, user)
                else:
                    self.main.msg(channel, 'I cannot find an event for that server that matches {event}'.format(event = msg.split()[3]))
            else:
                self.main.msg(channel, 'I cannot find a server called {server}'.format(server = msg.split()[2]))
        else:
            self.main.msg(channel, 'I\'m sorry Dave, I cannot let you do that.')
            self.main.msg(channel, 'Insufficient number of arguments for \'ack\'.')

    def ack(self, host, events, user):
        for event in events:
            self.zabapi.event.acknowledge(eventids = event['eventid'], message = 'Acknowledged by {username} on IRC.'.format(username = user))
            self.main.msg(self.main.loggingchannel, '{event} on {server} acknowledged by {username}.'.format(event = event['eventid'], server = host[0]['hostid'], username = user))
            self.main.logging('info', '{event} on {server} acknowledged by {username}.'.format(event = event['eventid'], server = host[0]['hostid'], username = user))
