import os
import sys
import glob
from setuptools import setup

entry_points = {
    'console_scripts': ['poc=poc.cli:main']
}

# copy the template files to the same relative location in the installation directory
# data_files = [('perflog/data', glob.glob('perflog/data/*'))]

setup(name='poc',
      version='0.1',
      description='OwnCloud client',
      author='Florian Kaiser, Klaus Reuter',
      author_email='khr@mpcdf.mpg.de',
      packages=['poc'],
      install_requires=['pyocclient'],
      entry_points=entry_points,
      zip_safe=False)

    #   data_files=data_files,

