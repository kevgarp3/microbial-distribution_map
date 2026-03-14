#!/usr/bin/python3
"""
Title: prep_fastq_download.py

Description:
This module contains functions used to prepare fastq downloads and should be used only
in presence of an appropriate complementary BASH script using wget, hereafter referred
as download_fastqs.sh

Usage:
'''PYTHON
from prep_fastq_download import get_fastq_links, call_download_fastqs
'''

Version: 1.0
Date: 13-Mar-2026
Author: Kevin García Prado
"""
######################################################################################
#%% Section 0: Importing the necessary modules.
######################################################################################
import pandas as pd
import subprocess

######################################################################################
#%% Section 1: Declaring the functions.
######################################################################################
def get_fastq_links(df, ids_list):
    # Get the "fastq_ftp" fields from those rows matching the "run_accesion" IDs in 
    # ids_of_interest.
    raw_links = df.loc[df["run_accession"].isin(ids_list), "fastq_ftp"]
    # Extract the actual links.
    links = [link.strip() for raw_link in raw_links for link in raw_link.strip().split(";")]
    return(links)

def call_download_fastqs(outdir_fastqs, links):
    result = subprocess.run(["bash", "src/download_fastqs.sh", outdir_fastqs] + links, 
                            capture_output=True, text=True)
    return result