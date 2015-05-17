#!/usr/bin/env python
# Setup Script for Confidence Monitor
# Author: Dave Russell Jr (drussell393)

from setuptools import setup, find_packages

setup(name = 'ConfidenceMon',
      version = 1.01,
      description = 'IRC Monitoring Bot for Zabbix',
      author = 'Dave Russell Jr',
      url = 'https://github.com/drussell393/ConfidenceMon',
      license = 'MIT',
      packages = find_packages(),
      install_requires = ['twisted', 'apscheduler']
      )
