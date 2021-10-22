from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pythonsql',
    description='Python utility tool for interacting with SQL.',
    url='https://github.com/raynardfung/python-sql',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements
)