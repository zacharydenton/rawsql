#!/usr/bin/env python
import rawsql

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='rawsql',
    version=rawsql.__version__,
    description="A library for using plain SQL.",
    long_description=readme,
    author=rawsql.__author__,
    author_email='z@chdenton.com',
    url='https://github.com/zacharydenton/rawsql',
    packages=[
        'rawsql',
    ],
    package_dir={'rawsql': 'rawsql'},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='rawsql',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: SQL',
        'Topic :: Database'
    ],
    test_suite='tests'
)
