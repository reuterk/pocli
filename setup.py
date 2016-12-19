"""pocli (Python OwnCloud Client) setup script
"""

import os
from setuptools import setup, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    # https://stackoverflow.com/questions/3779915/why-does-python-setup-py-sdist-create-unwanted-project-egg-info-in-project-r
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf build')
        os.system('rm -vrf dist')
        os.system('rm -vrf pocli.egg-info')
        os.system('rm -vrf pocli/__pycache__')
        os.system("find . -name '*.pyc' -delete -print")

entry_points = {
    'console_scripts': ['poc=pocli.cli:main']
}

setup(name='pocli',
      version='0.1',
      description='Python-based minimal command-line client for OwnCloud',
      author='Florian Kaiser, Klaus Reuter',
      author_email='khr@mpcdf.mpg.de',
      packages=['pocli'],
      install_requires=['requests', 'pyocclient'],
      cmdclass={'clean': CleanCommand},
      entry_points=entry_points,
      zip_safe=False)
