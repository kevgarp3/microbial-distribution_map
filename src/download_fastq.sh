#!/bin/bash
outdir="$1"
shift
links=("$@")

for url in "${links[@]}"; do
    wget -c -P "$outdir" "$url" || curl -C - -O --output-dir "$outdir" "$url"
done
echo "All FASTQ files were saved to $outdir"