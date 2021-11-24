#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=8.0",
    "requests>=2.26.0",
    "parsel>=1.6.0",
    "python-dateutil>=2.8.2",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Daniel Ndegwa",
    author_email="daniendegwa@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="AsianBookie.com python api",
    entry_points={
        "console_scripts": [
            "asianbookie=asianbookie.cli:asianbookie_cli",
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="asianbookie",
    name="asianbookie",
    packages=find_packages(include=["asianbookie", "asianbookie.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/kbgro/asianbookie",
    version="2.0.0",
    zip_safe=False,
)
