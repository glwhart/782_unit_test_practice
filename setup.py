#!/usr/bin/env python
try:
    from setuptools import setup
    args = {}
except ImportError:
    from distutils.core import setup
    print("""\
*** WARNING: setuptools is not found.  Using distutils...
""")

from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

from os import path
setup(name='basis',
      version='0.0.2',
      description='Solve particle-in-box and Kronig-Penney type problems with a basis',
      long_description= "" if not path.isfile("README.md") else read_md('README.md'),
      author='Gus L. W. Hart',
      author_email='gus.hart@gmail.com',
      url='https://github.com/glwhart/782_unit_test_practice',
      license='MIT',
      setup_requires=['pytest-runner',],
      tests_require=['pytest', 'python-coveralls'],
      install_requires=[
          "argparse",
          "termcolor",
          "numpy",
          "matplotlib",
#          "pyserial",
      ],
      packages=['basis'],
      scripts=['basis/solve.py'],
      package_data={'liveserial': []},
      include_package_data=True,
      classifiers=[
          'Development Status :: 1 - Pre-Alpha',
          'Intended Audience :: Students/Researchers',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
     )
