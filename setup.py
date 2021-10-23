from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

setup(
    name='pythonsql',
    description='Python utility tool for interacting with SQL.',
    url='https://github.com/raynardfung/python-sql',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pg8000>=1.21.0',
        'pandas>=1.3.2',
    ]
)