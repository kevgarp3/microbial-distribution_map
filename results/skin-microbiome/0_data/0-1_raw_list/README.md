# README: Raw List

As per the Snakemake-enabled workflow, the results/skin-microbiome/0_data/0-1_raw_list/ directory should eventually contain
a soft link to the raw list available in the data/ directory. However, this file is not being publicly shared as the list containing 93,690 different identifiers of skin microbiome-related sequencing Bio-Projects from ENA is currently (March 2026) under active research (please refer to the README under the data/ directory).

## Expected content of results/skin-microbiome/0_data/0-1_raw_list/

```TEXT
└── results
    └── skin-microbiome
        └── 0_data
            └── 0-1_raw_list    
                ├── README.md   # This README file regarding the raw list      
                └── bio-projects.txt -> ../../../../data/ncbi_skin-metagenome_sampleIDs.txt  
```