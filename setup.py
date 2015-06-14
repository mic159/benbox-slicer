from setuptools import setup, find_packages

setup(
    name='benbox-slicer',
    version='1.0.0',
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'benbox-slicer = benbox_slicer.main:cli'
        ]
    }
)
