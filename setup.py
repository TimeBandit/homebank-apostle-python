from setuptools import setup, find_packages

setup(
    name="hba-python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'termcolor',
        'tabulate',
        # add other dependencies
    ],
    entry_points={
        'console_scripts': [
            'hba-python=src.main:main',
        ],
    },
)
