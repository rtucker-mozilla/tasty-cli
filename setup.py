#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mozapi',
    version='0.14',
    description='CLI Interface to Mozilla REST Api',
    author='Rob Tucker',
    author_email='rtucker@mozilla.com',
    url='https://github.com/rtucker-mozilla/tasty-cli',
    license='MPL-1.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    extras_require = {
        'argparse':  ["argparse"]
    },
    entry_points = {
        'console_scripts': [
            'api.py = mozapi.api:main'
        ],
    },

    )
