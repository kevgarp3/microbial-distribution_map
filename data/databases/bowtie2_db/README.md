# README: BowTie2 Database

As per the Snakemake-enabled workflow, the database from BowTie2 used by MetaPhlAn 4.0 should be located in the data/databases/bowtie2_db/ directory. The expected contents of the before mentioned directory (once the database is downloaded) are described below.

## Expected content of data/databases/bowtie2_db/

```TEXT
└── data
    └── databases
        └── bowtie2_db
            ├── README.md       # This README file regarding the BowTie2 Database
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.1.bt2l       
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.2.bt2l       
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.3.bt2l       
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.4.bt2l       
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.rev.1.bt2l   
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.rev.2.bt2l   
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.nwk          
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.pkl          
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103.fna          
            ├── mpa_vJan21_CHOCOPhlAnSGB_202103_SGB.fna      
            └── mpa_vJan21_CHOCOPhlAnSGB_202103_VINFO.csa    
```

## Database Download

The Snakemake workflow ensures the database is found in the referred directory by first checking if it already exists and downloading all necessary files if they are missing or are corrupted (see "rule get_bowtie2_db" in config/Snakefile).