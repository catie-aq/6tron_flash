#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = []

test_requirements = []

setup(
    author="CATIE",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tool to flash 6TRON Boards",
    entry_points={
        'console_scripts': [
            'sixtron_flash=sixtron_flash.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sixtron_flash',
    name='sixtron_flash',
    packages=find_packages(include=['sixtron_flash', 'sixtron_flash.*']),
    setup_requires=setup_requirements,
    version='1.0.0'
)
