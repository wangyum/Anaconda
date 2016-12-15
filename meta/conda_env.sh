#!/bin/bash

if [ -z "${CDH_PYTHON}" ]; then
    export CDH_PYTHON=${PARCELS_ROOT}/${PARCEL_DIRNAME}/bin/python
fi
