#!/bin/bash
db_dir=$1
indir=$2
run_accession=$3
#fastq1=$3
#fastq2=$4
outdir=$4 # sample_profile.txt



metaphlan --install \
  --input_type fastq \
  -1 $fastq1 \
  -2 $fastq2 \
  --bowtie2out sample.bowtie2.bz2 \
  -o "${outdir}/${run_accession}_profile.txt"

# metaphlan2krona.py --profile "${outdir}/${run_accession}_profile.txt" \
#    --krona "${outdir}/${run_accession}_krona.txt
# grep -v "^#" "${outdir}/${run_accession}_profile.txt" | \
#    cut -f1,3 > "${outdir}/${run_accession}_krona.txt

# ktImportText "${outdir}/${run_accession}_krona.txt \
#    -o "${outdir}/${run_accession}_krona.html

# merge_metaphlan_tables.py