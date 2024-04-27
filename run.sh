#!/bin/bash
set -e

python preprocess.py codon
codon build --release rtow_codon/__main__.py 2> >(grep -v '^ld: warning')
time ./rtow_codon/__main__
