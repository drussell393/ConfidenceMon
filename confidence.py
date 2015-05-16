#!/usr/bin/env python
# Confidence Monitoring Bot Core
# Author: Dave Russell Jr (drussell393)

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor, ssl
from twisted.python import log
from datetime import datetime
from modules import *
from apscheduler.schedulers.background import BackgroundScheduler
import imp
import os
import redis


class ConfidenceMonitor(irc.IRCClient):
    nickname = 'ConfidenceMon'
    realname = 'Confidence by Dave Russell'
    fingerReply = 'Don\'t FINGER me!'
    userinfo = 'Dave Russell\'s Bot'
    versionName = 'Confidence Monitoring Bot'
    versionNum = 1.01

    def __init__(self):
        self.factory = ConfidenceMonitorFactory()
        self.reloadSettings()

    def logging(self, loglevel, message):
        prefix = '[' + loglevel.upper() + '] '
        return log.msg(prefix + message)

    def signedOn(self):
        self.logging('info', 'Confidence Monitor has signed on {network} as {username}'.format(
            network=self.settingsdb.get('server'), username=self.nickname))
        if (self.settingsdb.get('nspassword')):
            self.logging('info', 'Attempting to authenticate to NickServ for {username}'.format(
                username=self.nickname))
            self.msg(
                'NickServ', 'IDENTIFY ' + self.settingsdb.get('nspassword'))

        for channel in self.settingsdb.smembers('channels'):
            self.join(channel)

    def joined(self, channel):
        self.logging(
            'info', 'Confidence Monitor has joined {channel}'.format(channel=channel))
        if (hasattr(self, 'loggingchannel') == False):
            self.loggingchannel = channel
            self.startScheduler()

    def privmsg(self, user, channel, msg):
        if (channel == self.nickname):
            self.logging('info', '{username} has PM\'d me with: {message}'.format(
                username=user, message=msg))
            self.pmhandler = pmhandler.PMHandler()
            self.pmhandler.init(self, msg, user)
        else:
            for trigger in self.settingsdb.smembers('triggers'):
                if (msg.startswith(trigger)):
                    reload(commandhandler)
                    self.commandhandler = commandhandler.CommandHandler(self)
                    self.commandhandler.init(channel, msg, user)

    def kickedFrom(self, channel, kicker, message):
        self.logging('crit', 'Confidence Monitor was kicked from {channel} by {kicker} with reason: {reason}'.format(
            channel=channel, kicker=kicker, reason=message))
        self.join(channel)
        self.msg(channel, 'I know you didn\'t mean to kick me.')

    def reloadSettings(self):
        self.settingsdb = redis.StrictRedis(host='localhost', port=6379, db=0)

    def startScheduler(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.sched.add_job(self.getZabEvents, trigger='interval', minutes=2)

    def getZabEvents(self):
        zabapi = zabbix.ZabbixAPI(url=self.settingsdb.get('zaburl'), user=self.settingsdb.get(
            'zabid'), password=self.settingsdb.get('zabpass'))
        events = zabapi.trigger.get(
            maintenance=False, withUnacknowledgedEvents=True, selectHosts='extend', output='extend')
        prefixes = {'0': 'Undefined',
                    '1': 'INFO',
                    '2': 'WARNING',
                    '3': 'CAUTION',
                    '4': 'CRITICAL',
                    '5': 'CRITICAL'}
        for event in events:
            for host in event['hosts']:
                if (len(host['maintenances']) == 0):
                    eventdb = str(event['triggerid']) + \
                        '-' + str(host['hostid'])
                    if (self.settingsdb.exists(eventdb)):
                        if (self.settingsdb.get(eventdb) != str(event['lastchange'])):
                            self.msg(self.loggingchannel, prefixes[str(event['priority'])] + ': ' + str(
                                host['name']) + ' -- ' + str(event['description'] + ' -- Hostname: ' + str(host['host'])))
                            self.settingsdb.delete(eventdb)
                            self.settingsdb.append(
                                eventdb, str(event['lastchange']))
                    else:
                        self.msg(self.loggingchannel, prefixes[str(event['priority'])] + ': ' + str(
                            host['name']) + ' -- ' + str(event['description'] + ' -- Hostname: ' + str(host['host'])))
                        self.settingsdb.append(
                            eventdb, str(event['lastchange']))


class ConfidenceMonitorFactory(protocol.ClientFactory):
    protocol = ConfidenceMonitor

    def clientConnectionLost(self, connector, reason):
        self.main = ConfidenceMonitor()
        self.main.logging('crit', 'Lost Connection: ' + str(reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.main.logging('crit' 'Connection Failed: ' + str(reason))
        reactor.stop()

if __name__ == "__main__":
    log.startLogging(open(os.path.dirname(os.path.abspath(
        __file__)) + '/logging/log-' + datetime.now().isoformat() + '.txt', 'w'))
    factory = ConfidenceMonitorFactory()
    confidence = ConfidenceMonitor()
    hostname = confidence.settingsdb.get('server')
    port = confidence.settingsdb.get('port')
    reactor.connectSSL(
        hostname, int(port), factory, ssl.ClientContextFactory())
    reactor.run()
