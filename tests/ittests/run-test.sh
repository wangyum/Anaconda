#!/bin/bash

export PATH=/opt/cloudera/parcels/Anaconda/bin:${PATH}

tests=$(find /opt/cloudera/parcels/Anaconda/tests/ittests/  -name "*.py")

for test in ${tests}
do
  echo "DEBUG: test "${test}
  python ${test}
done
