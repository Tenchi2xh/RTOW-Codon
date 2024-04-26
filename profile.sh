#!/bin/bash
set -e

python preprocess.py codon
codon build --debug rtow_codon/__main__.py
sudo dtrace -c './rtow_codon/__main__ large-file' -o out.stacks -n 'profile-997 /execname == "__main__"/ { @[ustack(100)] = count(); }'
./flamegraph/stackcollapse.pl out.stacks |
    ./flamegraph/flamegraph.pl \
        --title "Ray Tracing in One Weekend" \
        --subtitle "Codon build flame graph" \
        --width 1536 \
        --height 32 \
        --fonttype monospace \
        > rtow_codon.svg
python -c "import webbrowser as w; b = w.get('chrome'); b.open_new('file://$(pwd)/rtow_codon.svg')"
