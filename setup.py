#!/usr/bin/env python

from setuptools import setup
setup(name='hackpack',
      version='2.0',
      author='Rob Spectre',
      author_email='help@twilio.com',
      description='A sample project for deploying Twilio to Heroku with Flask',
      include_package_data=True,
      zip_safe=False,
      packages=['hackpack', 'tests'],
      license='MIT',
      install_requires=[
          'flask>=0.10',
          'twilio>=3.6',
          'tox>=1.7'
      ])
