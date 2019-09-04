#!/bin/bash

PKG_DIR="lib"
rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}
docker run --rm -v $(pwd):/foo -w /foo amazonlinux:latest \
    yum install -y python37 && curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user &&  ~/.local/bin/pip install -r requirements.txt -t ${PKG_DIR}
cp git-2.4.3.tar ${PKG_DIR}