#!/bin/bash
foo () {
    local flag=false
    OPTIND=1

    while getopts 'f' opt; do
        case $opt in
            f) flag=true ;;
            *) echo 'Error in command line parsing' >&2
               exit 1
        esac
    done
    shift "$(( OPTIND - 1 ))"

    local param1="$1"
    local param2="$2"

    if "$flag"; then
        echo_per_download=true
    else
        echo_per_download=false
    fi
}

outdir="$1"
links=("$@")

for url in "${links[@]}"; do
    if $echo_per_download; then
        echo "Downloading from: $url"
    fi
    wget -c -P "$outdir" "$url" || curl -C - -O --output-dir "$outdir" "$url"
done
echo "All FASTQ files were saved to $outdir"