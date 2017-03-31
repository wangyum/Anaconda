#!/bin/bash

set -ex

# git pull

ANACONDA_SOURCE_DIR=`pwd`
ANACONDA_DEPLOP_DIR=/var/www/html/anaconda/deploy
VERSION="d$(date '+%Y%m%d-%H.%M.%S')-$(git rev-parse --short HEAD)"
PARCEL_NAME="Anaconda-${VERSION}"
PARCEL_PATH=${ANACONDA_DEPLOP_DIR}/${PARCEL_NAME}

rm -rf ${ANACONDA_DEPLOP_DIR}/*

rsync -av --exclude='.git/' --exclude='cm_ext/' --exclude='Examples/' --exclude='.github/' --exclude='*.tar.bz2'  ${ANACONDA_SOURCE_DIR}/*  ${PARCEL_PATH}

sed -i "s/__VERSION__/${VERSION}/g"     ${PARCEL_PATH}/meta/parcel.json

cd ${ANACONDA_DEPLOP_DIR}

tar -zcf ${PARCEL_NAME}-el6.parcel ${PARCEL_NAME} --remove-files 

sha1sum ${PARCEL_PATH}-el6.parcel | awk -F" " '{print $1}' > ${PARCEL_PATH}-el6.parcel.sha
/opt/cloudera/parcels/Anaconda/bin/python2.7 ${ANACONDA_SOURCE_DIR}/cm_ext/make_manifest/make_manifest.py ${ANACONDA_DEPLOP_DIR}
