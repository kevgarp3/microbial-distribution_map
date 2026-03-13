#!/bin/bash

metaphlan file.1.fastq.gz,file.2.fastq.gz \
  --input_type fastq \
  --bowtie2out sample.bowtie2.bz2 \
  -o sample_profile.txt