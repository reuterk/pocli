"""
"""

from setuptools import setup

entry_points = {
    'console_scripts': ['poc=poc.cli:main']
}

setup(name='poc',
      version='0.1',
      description='Python based command line client for OwnCloud',
      author='Florian Kaiser, Klaus Reuter',
      author_email='khr@mpcdf.mpg.de',
      packages=['poc'],
      install_requires=['pyocclient'],
      entry_points=entry_points,
      zip_safe=False)
