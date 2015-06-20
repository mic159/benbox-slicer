from setuptools import setup, find_packages

setup(
    name='benbox-slicer',
    version='1.0.0',
    packages=find_packages(),
    license='MIT',
    author='mic159',
    description='Slice PNGs into Benbox flavour GCODE',

    entry_points={
        'console_scripts': [
            'benbox-slicer = benbox_slicer.main:cli'
        ]
    }
)
