#!/bin/bash

# Run some basic tests of the `oc' command line client.
# Requires manual confirmation of file deletion.

set -e

export OC_UNIT_TEST_COOKIE=ON
OC_TESTDIR=/tmp/$USER/oc_tests

CMD='ds'
#CMD='oc'

JUNK_FILE="junk.dat"
JUNK_DIR="oc_test_directory"
JUNK_SIZE_MB=16

COUNTER=0

source ocpasswd.bash

function print_green() {
    echo -n -e "\033[1;32m"
    echo "$1"
    echo -n -e "\033[1;m"
}

function run_test() {
    COUNTER=$((COUNTER + 1))
    print_green "TEST $COUNTER: \`$1'"
    $1
}


echo "Running basic tests of the pocli command line interface." 
echo Installation: `which ${CMD}`
echo "Press enter to continue or Ctrl-c to abort."
read

ocpasswd

echo
echo

mkdir -p $OC_TESTDIR
cd $OC_TESTDIR

dd if=/dev/zero of=${JUNK_FILE} bs=1M count=${JUNK_SIZE_MB} status=none

run_test "${CMD} --help"

run_test "${CMD} check"
run_test "${CMD} ls"

# upload test file
run_test "${CMD} mkdir ${JUNK_DIR}"
run_test "${CMD} put --directory=${JUNK_DIR} ${JUNK_FILE}"

# download test file
mkdir -p ${JUNK_DIR}
run_test "${CMD} get --directory=${JUNK_DIR} ${JUNK_DIR}/${JUNK_FILE}"

run_test "${CMD} rm --yes ${JUNK_DIR}/${JUNK_FILE}"
run_test "${CMD} rm --yes ${JUNK_DIR}"

rm ${JUNK_DIR}/${JUNK_FILE}
rmdir ${JUNK_DIR}
rm ${JUNK_FILE}
cd ..
rmdir $OC_TESTDIR

echo
echo
