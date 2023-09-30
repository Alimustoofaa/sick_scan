from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'sick_scan_tcp',
    version = '1.0.1',
    description = 'Library for interacting with SICK LIDAR sensors with TCP Connection',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Ali Mustofa',
    author_email = 'hai.alimustofa@gmail.com',
    url = 'https://github.com/Alimustoofaa/sick_scan',
    keywords = ['Sick Scan', 'Sick Lidar', 'LMS511', 'LMS111'],
    packages = find_packages(),
    install_requires = requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
