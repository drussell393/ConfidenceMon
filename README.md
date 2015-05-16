Confidence Monitoring Bot v1.01
-------------------------------

### Changelog

Version 1.01 provides the following changes:

- Introduce a global access list for commands
- Fix broken 'arise' command
- Fix broken 'ack' command
- Create a new method in the core for the scheduler
- Add PEP8 styling

All known issues have been fixed at this point. This is the final release until
I decide to add something else to it.

Older release notes can still be found below.

<hr />

### Confidence Monitoring Bot v1.0

The idea of this bot is purely to provide me with real-time or near real-time
updates of my Zabbix monitoring events/triggers via IRC. The bot will also have
key features such as:

- ack (acknowledge events)
- stfu (stop telling me things are happening)
- arise (resume telling me things are happening)
- restart (mostly for dev work, restarting to core)

There will likely be more additions as time goes on. However, it uses the Zabbix API,
which was not coded by me. The rest of the bot (outside of `modules/zabbix.py`) was
entirely coded by me. 

It also uses the Twisted framework to connect to IRC, handle SSL connections, and
APScheduler for the timer. While I could have made my own timer, I decided that the
bot would benefit from such an advanced scheduler like APScheduler.


#### Known Issues

I am currently aware of a few issues:

- The bot randomly restarts

This issue is most likely due to the amount of errors it's getting from Zabbix and
I will likely have to introduce some sort of rate limiting and/or threading for that.
The reason I say that is because it looks like the problem is around the fact that
the bot doesn't reply to "PING"s from the server fast enough. It comes right back,
and the log file for the bot is unaffected, but that causes a lot of contention on
the VPS that it's running on... So there's that.

- Performance issues

This is likely related to the above issue, but there are dozens of processes running
for the bot at once. This will likely be changed when we move to a more reasonable 
set up (rate limiting, PING responses, and not leaving around our process mess).

- Acking doesn't exactly work... erm

So basically, I need to learn how Zabbix's API is doing the search that runs the
whole process of 'ack'. It gets the host fine, but the event gets a little lost. I
think it'd probably be better to use `trigger.get` anyways. I may change it to that.

- Arise sorta works... erm

So, arise works in the sense it starts the timer but not the job. I'm looking into
this one actively, but the problem with the BackgroundScheduler object in APScheduler
is that there's no pause\_job() method. It's just start() and stop(). I was hoping that
starting it again and just re-adding the job would fix it, but thus far it looks like a
no-go.

#### The End

That's really it thus far. Version 1.01 coming soon, woo. I'll actually include setuptools
stuff next time.. Whoops.
