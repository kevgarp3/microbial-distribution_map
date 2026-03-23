# README: Soft-Links to BowTie2 Database

As per the Snakemake-enabled workflow, the following FASTQ files are expected to be downloaded by the workflow into the results/skin-microbiome/0_data/0-3_fastq_downloads/ directory, by only using the back-end functionalities. Please refer to the "checkpoint get_fastqs" in workflow/Snakefile and to the workflow/skin-microbiome_config_fastq_downloads.tsv file for further understanding. These are not being provided in the repository only for the sake of not copying unnecessary information (as its download is already available) into the remote repository.

## Expected content of results/skin-microbiome/0_data/0-3_fastq_downloads/

```TEXT
└── results
    └── skin-microbiome
        └── 0_data
            └── 0-3_fastq_downloads
                ├── SRR9696273_1.fastq.gz
                ├── SRR9696273_2.fastq.gz
                ├── SRR9696276_1.fastq.gz
                ├── SRR9696276_2.fastq.gz
                ├── SRR9696282_1.fastq.gz
                └── SRR9696282_2.fastq.gz
```