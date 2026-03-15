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

## Links to Download Data

The databases used in this project can be downloaded by using `wget` with each of the following links:

* NCBI Taxonomy Database: ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
* SwissProt Database: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz

## Software Dependencies

The following list presents all software dependencies (and versions) required to execute this workflow:

* 
* 
* 
* 

The quickest way of installing all previously listed software dependencies is using the following command (all names in between "<>" can be replaced for the user's convenience).

```BASH
conda env create --prefix <workflow/envs/microbial-distribution-map> -f <workflow/envs/microbial-distribution-map.yaml>
```

Alternatively,

```BASH
conda env create -f <workflow/envs/microbial-distribution-map.yaml>
conda create --prefix <workflow/envs/microbial-distribution-map> --clone <microbial-distribution-map>
```

Then you can edit the <workflow/config/config.yaml> to update the <conda_env> to point to the <workflow/envs/microbial-distribution-map>.
After doing so, you can comfortably run the following command (just edit <N>, pertinently), without experimenting an unnecessary excessively time-consuming installation of software dependencies.

```BASH
snakemake --cores <N> --use-conda -n	# You may want to try a dry-run first.
snakemake --cores <N> --use-conda
```

## Useful Tips

* Backup all produced files.
* The related bug should have been fixed, but... if Snakemake gets stuck and tries to produce already existing files for any reason. Running the following commands may come in handy.

```BASH
rm -rf .snakemake/metadata/
snakemake --touch
snakemake -n
```

## Commands

All source code and Snakemake-enabled workflow can be cloned from the following GitHub repository: [https://github.com/kevgarp3/genome-based_phylogeny](https://github.com/kevgarp3/microbial-distribution_map)
