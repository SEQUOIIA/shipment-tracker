#!/usr/bin/env python

#from distutils.core import setup
from setuptools import find_packages, setup

setup(name='Shipment-tracker',
      version='1.0',
      description='Track shipments from various shipping companies',
      author='Emil H. Clausen <SEQUOIIA>',
      author_email='sequoiia@hummel.yt',
      url='https://github.com/sequoiia/shipment-tracker',
      packages=find_packages("src"),
      package_dir={
        '': 'src'
        },
      entry_points={
        "console_scripts": ["shipment-tracker=shipment_tracker.main:main"]
      },
      install_requires=[
        'requests',
        'click'
      ]
     )
