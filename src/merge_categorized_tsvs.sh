#!/bin/bash
raw_tsv=$1  # The raw TSV file to merge all other TSV files into.
outfile=$2  # The output filename.
shift 2
tsvs=("$@") # All input TSV files.
outdir="${outfile%%$(basename $outfile)}" # The output directory

# Starting header from raw_tsv
header=$(mktemp)
head -n1 "$raw_tsv" > "$header"
# Starting body from raw_tsv
body=$(mktemp)
tail -n +2 "$raw_tsv" > "$body"

# Iterating through all input TSV files:
for tsv in "${tsvs[@]}"; do
    # Creating temporary header and body files.
    h=$(mktemp)
    b=$(mktemp)
    # Adding only the second column headers.
    head -n1 "$tsv" | cut -d $'\t' -f2 > "$h"
    paste "$header" "$h" > "${header}.new"
    mv "${header}.new" "$header"
    # Adding only the second column body, joined by first column.
    tail -n +2 "$tsv" | cut -d $'\t' -f1,2 | sort -t $'\t' -k1,1 > "$b"

    # Get number of fields in body
    nfields=$(awk -F'\t' '{print NF; exit}' "$body")
    # Build output format: all fields of file 1 in original order, then field 2 of file 2
    o_format=$(seq 1 $nfields | sed 's/^/1./' | tr '\n' ',' | sed 's/,$//')
    o_format="${o_format},2.2"

    sort -t $'\t' -k2,2 "$body" > "${body}.sorted"
    join -t $'\t' -1 2 -2 1 -a 1 -o "$o_format" "${body}.sorted" "$b" > "${body}.new"
    
    #cut -d $'\t' -f2 "$body" | sort > /tmp/body_ids.txt
    #cut -d $'\t' -f1 "$b" | sort > /tmp/b_ids.txt
    # Check overlap
    #comm -12 /tmp/body_ids.txt /tmp/b_ids.txt | wc -l  # matching IDs
    #comm -23 /tmp/body_ids.txt /tmp/b_ids.txt | wc -l  # only in body
    #comm -13 /tmp/body_ids.txt /tmp/b_ids.txt | wc -l  # only in b
    #echo ""

    #cut -d $'\t' -f1 "$b" | head -15
    #echo ""
    #cut -d $'\t' -f1 "$body" | head -15
    #echo ""
    #cut -d $'\t' -f2 "$body" | head -15
    #echo ""

    mv "${body}.new" "$body"
    # Deleting the temporary header and body files
    rm "$h" "$b" ${body}.sorted
done

# Get the number of cols in raw_tsv.
ncols_raw=$(head -n1 "$raw_tsv" | awk -F "\t" '{print NF}')
# Remove rows with empty fields in the newly added columns.
body_filtered=$(mktemp)
awk -F "\t" -v start=$((ncols_raw+1)) '{
    empty=0
    for(i=start; i<=NF; i++) if($i=="") empty=1
    if(!empty) print
}' "$body" > "$body_filtered"

# Create the final output file and remove the remaining temporary files.
cat "$header" "$body_filtered" > "$outfile"
rm "$header" "$body" "$body_filtered"