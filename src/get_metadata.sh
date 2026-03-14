#!/bin/bash
bp_list=$1  # bio-projects list text file
metadata=$2 # output directory for the metadata file
cols="run_accession,sample_accession,library_strategy,country,location,fastq_ftp,fastq_md5,study_title,sample_description"

tmp_dir="${metadata}.tmp_bp-list_chunks/"
mkdir -p "$tmp_dir"
tmp_prefix="${tmp_dir}.chunk_"
split -l 215 "$bp_list" "$tmp_prefix"

metadata="${metadata}raw_metadata.tsv"

echo $cols | tr "," "\t" > $metadata
for f in ${tmp_prefix}*; do
    query=$(awk '{printf "%s%s", (NR==1?"":" OR "), "sample_accession="$1}' "$f")
    curl -s --get "https://www.ebi.ac.uk/ena/portal/api/search" \
        --data-urlencode "result=read_run" \
        --data-urlencode "query=${query}" \
        --data-urlencode "fields=${cols}" \
        --data-urlencode "format=tsv" \
        | tail -n +2 >> "$metadata"
done
rm -r "$tmp_dir"

#curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=${bio_proj}&fields=${cols}&format=tsv"