# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='mw',
    version='0.0.1',
    description='Multiagent systems  - Ethnocentrism Model by Robert Axelrod and Ross A. Hammond',
    long_description=readme,
    author='Katarzyna Kondzielnik, Przemysław Przybyszewski',
    author_email='katarzyna.kondzielnik@gmail.com, przybyszewski.przemyslaw@gmail.com',
    url='https://github.com/Przybyszo/MW_SGH',
    packages=find_packages(exclude=('tests', 'docs'))
)