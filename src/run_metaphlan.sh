#!/bin/bash
db_dir=$1
outdir=$2
shift 2
fastq_files=("$@")

echo $(echo "${fastq_files[@]}" | tr " " ",")

#metaphlan ${fastq_files[@]} \ #comma-separated
# --nproc 15 \
# --input_type fastq \
# --mapout ${outdir}/${run_accession}.bowtie2.bz2 \
# --ignore_eukaryotes \
# --ignore_archaea \
# -o "${outdir}/${run_accession}_profile.txt"

# metaphlan2krona.py --profile "${outdir}/${run_accession}_profile.txt" \
#    --krona "${outdir}/${run_accession}_krona.txt
# grep -v "^#" "${outdir}/${run_accession}_profile.txt" | \
#    cut -f1,3 > "${outdir}/${run_accession}_krona.txt

# ktImportText "${outdir}/${run_accession}_krona.txt \
#    -o "${outdir}/${run_accession}_krona.html

# merge_metaphlan_tables.py