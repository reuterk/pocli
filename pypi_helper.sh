#!/bin/bash

python setup.py clean
/opt/apps/anaconda/3/4.2.0/bin/python3 setup.py sdist
/opt/apps/anaconda/3/4.2.0/bin/python3 setup.py bdist_wheel --universal
twine upload dist/*

