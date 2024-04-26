#!/bin/bash
set -e

python preprocess.py python
time pypy3 -m rtow_python
