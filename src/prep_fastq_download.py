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
import os
import hashlib
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
    return links

################################################################## To be further polished....
#def get_fastq_md5s(df, ids_list):
#    # Get the "fastq_ftp" fields from those rows matching the "run_accesion" IDs in 
#    # ids_of_interest.
#    raw_links = df.loc[df["run_accession"].isin(ids_list), "fastq_md5"]
#    # Extract the actual links.
#    links = [link.strip() for raw_link in raw_links for link in raw_link.strip().split(";")]
#    return links

def md5sum(fastq_file, chunk_size=8192):
    md5 = hashlib.md5()
    with open(fastq_file, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()

def check_existing_fastqs(fastqs_dir, links):
    # Check whether each expected FASTQ file, as per the link names exists in the
    # expected fastqs-containing directory.
    missing_links = []
    for link in links:
        fname = os.path.basename(link)
        if not os.path.exists(os.path.join(fastqs_dir, fname)):
            missing_links.append(link)
    # To be further developed to check for md5.
    return missing_links

def call_download_fastqs(outdir_fastqs, links, f=False):
    bash_args = ["bash", "src/download_fastqs.sh", outdir_fastqs] + links
    if f:
        bash_args.append("-f")
    result = subprocess.run(bash_args, capture_output=True, text=True)
    return result