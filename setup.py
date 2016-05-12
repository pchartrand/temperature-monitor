import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

test_requirements = ['nose']

setup(
    name='temperature-monitor',
    version='0.2.6',
    tests_require = test_requirements,
    install_requires = [
        'python_memcached', 'pyserial', 'matplotlib'
    ],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Temperature reading and graphing from an arduino device.',
    long_description=README,
    url='https://github.com/pchartrand/temperature-monitor',
    author='Philippe Chartrand',
    author_email='philippe.chartrand@videotron.ca',
    classifiers=[
        'Environment :: X11 Environment',
        'Intended Audience :: Tinkerers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
          'Topic :: Home automation :: Arduino',
        'Topic :: Home automation :: Temperature measurement',
    ],
    test_suite="temperature_monitor.tests.libs",
    entry_points={
            'console_scripts': [
                'tempgraph = temperature_monitor.bin.tempgraph:main_func',
                'templast = temperature_monitor.bin.templast:main_func',
                'tempread = temperature_monitor.bin.tempread:main_func',
                'tempstore = temperature_monitor.bin.tempstore:main_func',
                'tempgraphsaver = temperature_monitor.bin.tempgraphsaver:main_func',

            ],
            'gui_scripts': [
                'tempgraph = temperature_monitor.bin.tempgraph:main_func',
            ]
        }

)
