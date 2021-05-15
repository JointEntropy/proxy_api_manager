from setuptools import setup, find_packages
from os.path import join, dirname

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='proxy_api_manager',
    version='0.0.1',
    packages=find_packages(),
    install_requires=required,
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)

