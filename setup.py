from asyncio import subprocess
from setuptools import setup, find_packages

setup(
    name='thesis_scripts',
    version='0.1.0',
    packages=find_packages(),
    author='Anno Knierim',
    install_requires=[
        'numpy',
        'matplotlib',
        'astropy',
        'ctapipe',
        'pandas',
        'joblib',
        'colour'
    ]
)