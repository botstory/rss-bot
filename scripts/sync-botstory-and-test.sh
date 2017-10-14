#!/usr/bin/env bash

echo "====================================================="
echo ""
echo " Install botstory"
echo ""
echo "====================================================="

pip install --editable /usr/src/botstory

echo "====================================================="
echo ""
echo " pytest"
echo ""
echo "====================================================="

py.test
