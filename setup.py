from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name = 'sick_scan_tcp',
    version = '1.0.0',
    description = 'Library for interacting with SICK LIDAR sensors with TCP Connection',
    author = 'Ali Mustofa',
    author_email = 'hai.alimustofa@gmail.com',
    packages = find_packages(),
    install_requires = requirements
)
