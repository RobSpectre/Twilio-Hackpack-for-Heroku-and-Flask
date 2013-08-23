#!/usr/bin/env python

from setuptools import setup
setup(name='hackpack',
      version='1.0',
      author='twilio',
      author_email='help@twilio.com',
      description='twilio heroku hackpack',
      include_package_data=True,
      zip_safe=False,
      packages=['hackpack'],
      install_requires=[
        'flask>=0.9',
        'twilio>=3.4.3',
        'mock>=0.8.0',
        'nose>=1.1.2',
      ])
