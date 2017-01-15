# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pip.req import parse_requirements
import pip

with open('README.rst') as f:
    readme = f.read()

install_reqs = parse_requirements("requirements.txt", session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='mw',
    version='0.0.1',
    description='Multiagent systems - Modification of wolf-rabbit-grass model from Netlogo',
    long_description=readme,
    author='Katarzyna Kondzielnik, Przemysław Przybyszewski',
    author_email='katarzyna.kondzielnik@gmail.com, przybyszewski.przemyslaw@gmail.com',
    url='https://github.com/Przybyszo/MW_SGH',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=reqs
)