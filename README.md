# README: Microbial Species Distribution Map.

This workflow enables building a Microbial Species Distribution Map based on amplicon or shotgun sequencing data of samples containing sequenced genetic information of multiple organisms.

To run the whole workflow (including app launch run), but first read "Software Dependencies":
```BASH
snakemake --cores <N> --use-conda
```
Otherwise launch the app directly:
```BASH
streamlit run ./src/main.py
```

## Project's Tree Directory

```TEXT
├── README.md       # The README file for the project
├── data            # Contains the raw data for all projects using this workflow. 
│   └── databases
│       └── bowtie2_db
├── doc             # Contains the project report and the related presentation.
├── results             # Contains workflow-derived files, per run and stage.
│   └── skin-microbiome # Run (specific project)
│       ├── 0_data
│       │   ├── 0-1_raw_list
│       │   ├── 0-2_metadata
│       │   ├── 0-3_fastq_downloads
│       │   └── 0-4_bowtie2_db
│       ├── 1_plots
│       │   ├── 1-1_histograms
│       │   └── 1-2_krona_plots
│       │       └── prep-files
│       └── 2_maps
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

* python=3.13.12
* pandas=3.0.1
* metaphlan=4.2.4
* krona=2.8.1
* plotly=6.6.0
* pip
* streamlit==1.55.0
* st-theme==1.2.3

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

All source code and Snakemake-enabled workflow can be cloned from the following GitHub repository: [https://github.com/kevgarp3/microbial-distribution_map](https://github.com/kevgarp3/microbial-distribution_map)
