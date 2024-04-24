#!/bin/bash
set -e

if [ $# -eq 0 ]; then
    codon build --release rtow/__main__.py
    mv rtow/__main__ r
    time ./r
    echo
    imgcat main.ppm
else
    time codon run --release "$1"
fi
