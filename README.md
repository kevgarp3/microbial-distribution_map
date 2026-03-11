# README: Microbial Species Distribution Map.

This workflow enables building a Microbial Species Distribution Map based on amplicon or shotgun sequencing data of samples containing sequenced genetic information of multiple organisms.

To achieve this the following steps are performed:

1. 
2. 
3. 
4. 
5. 

## Project's Tree Directory

```TEXT
├── README.md       # The README file for the project
├── data            # Contains the raw data for all projects using this workflow. 
│
├── results             # Contains workflow-derived files, per run and stage.
│   └── skin-microbiome # Run (specific project)
│       ├── 0_data      # Contains the data used throughout the workflow.
│       │   ├── bio-projects.txt    # All bio-project IDs of interest.
│       │   ├── metadata_seq-data   # Contains all the metadata of the FASTQ files.
│       │   └── seq-data            # Contains all related FASTQ files.
│       ├── 1_
│       │   ├── 
│
├── src             # Contains the project's code.
└── workflow        # Contains files ensuring reproducibility with Snakemake
    ├── Snakefile   # Contains all Snakemake rules ensuring the workflow execution.
    ├── config      # Contains configuration files editable for each run (project).
    └── envs        # Contains a YAML specifying the workflow's software dependencies. 
```

## Filters Choice

* Maximum GC content (%): 35
* Minimum scaffold length (bp): 3,000

## Links to Download Data

The databases used in this project can be downloaded by using `wget` with each of the following links:

* NCBI Taxonomy Database: ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
* SwissProt Database: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz

## Software Dependencies

The following list presents all software dependencies (and versions) required to execute this workflow:

* python=3.12.12
* blast=2.17.0
* proteinortho=6.3.6
* busco=6.0.0
* clustalo=1.2.4
* raxml=8.2.13
* phylip=3.69.7

All the previous dependencies can be easily installed within a conda environment by running the following command:

```BASH
conda env create -f workflow/envs/genome-based_phylogeny.yaml
conda activate genome-based_phylogeny
```

(ONCE THE WORKFLOW IS IMPLEMENTED IN SNAKEMAKE!)
Alternatively, the following command should trigger the pipeline:

```BASH
snakemake -n --use-conda
```

## Commands

All source code and workflow implementation (via Snakemake) can be cloned from the following GitHub repository: [https://github.com/kevgarp3/genome-based_phylogeny](https://github.com/kevgarp3/genome-based_phylogeny)