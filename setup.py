import os.path
from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt") as req:
        return req.read().split("\n")
setup(
    name="auto_trans",
    version="0.0.1-alpha",
    url="https://github.com/geofferyj/auto_trans",
    author="auto_trans",
    author_email="geofferyjoseph1@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={"console_scripts": ["auto_trans=auto_trans.auto_trans:start"]},
)