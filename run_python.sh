#!/bin/bash
set -e

python preprocess.py python
time python3 -m rtow_python
