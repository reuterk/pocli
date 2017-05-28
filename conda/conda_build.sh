#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for PACKAGE in pyocclient pocli
do
    conda build --no-anaconda-upload $DIR/$PACKAGE
done

