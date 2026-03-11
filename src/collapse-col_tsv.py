#!/usr/bin/python3
"""
Title: collapse-col_tsv.py

Description:
This script processes a tab-delimited file to collapse a specified field into given
categories as specified by the user.

Usage:
'''BASH
python collapse-col_tsv.py <tsv_file> <target_col> \
    -i <id_col (optional)> \
    -O <output_dir (optional)> \
    -C <categories (optional)> \
'''

Input:
A tab-delimited file; the column name to be processed; a column name to be tracked as an
ID; an output directory; and a text file listing category names and the corresponding list
of patterns to be used to extract all fields from the target_col matching the patterns to
classify the fields in the corresponding category. The required format to list categories 
in the text file is the following (one category per line):
    
    '''example file for --categories
    category-1: pattern-1.1, pattern-1.2, ..., pattern-1.N
    ...          ... 
    category-n: pattern-n.1, ..., pattern-n.M
    '''

Output:
A collapsed tab-delimited file only containig the id and target columns, as well as the collapsed
category column, as applicable.

Procedure:
    Section 0.1: Importing the necessary modules.
    Section 0.2: Collecting the user-entered parameters (from the command line).
    Section 1: Validating the user-defined paramaters and reading the tsv file.
    Section 2: Processing the tsv-file according to the user specifications.
    Section 3: Writing an output collapsed file.

Version: 2.0
Date: 11-Mar-2026
Author: Kevin García Prado
"""

######################################################################################
#%% Section 0.1 Importing the required libraries.
######################################################################################
import argparse
from pathlib import Path
import fnmatch

######################################################################################
#%% Section 0.2 Collecting the user-entered parameters (from the command line).
######################################################################################
# Declaring the argument parser.
argParser = argparse.ArgumentParser(
            prog="collapse-col_tsv.py", 
            usage="python collapse-col_tsv.py <tsv_file> <target_col> -i <id_col> "
                  "-O <output_dir> -C <categories>",
            description="TThis script processes a tab-delimited file to collapse a specified "
                  "field into given categories as specified by the user.",
            epilog="Version: 1.0 (11-Mar-2026); Author: Kevin García Prado")

# Adding positional arguments to the argument parser.
argParser.add_argument('tsv_file', help="File name of the tab-delimited file to be used.")
argParser.add_argument('target_col', help="Column name of the target column.")

# Adding optional arguments to the argument parser.
argParser.add_argument('-i', '--id_col', default=False, help="Extra column to be tracked "
                       "as an ID column (to print out a tab-separated file) with the collapsed data.")
argParser.add_argument('-O', '--output_dir', default="./", help="Output directory")
argParser.add_argument('-C', '--categories', default=False, help="A text file listing category names and "
                       "the corresponding list of patterns to be used to extract all fields from the "
                       "target_col matching the patterns to classify the fields in the corresponding "
                       "category. The required format to list categories in the text file is the following "
                       "(one category per line): \"category-A: pattern-1, pattern-2, ..., pattern-N\"")

# Collecting the arguments from the user.
args = argParser.parse_args()

######################################################################################
#%% Section 1. Validating the user-defined arguments and reading the tsv file.
######################################################################################
# Checking that all arguments are valid.
print("")
# Checking that the tsv_file exists.
if not Path(args.tsv_file).is_file():
    print("The provided tsv_file does not exist: " + args.tsv_file); exit()
# Checking that the output_dir exists.
if not Path(args.output_dir).is_dir():
    print("The provided output_dir does not exist: " + args.output_dir); exit()
# Checking that the categories file exists.
if not Path(args.categories).is_file():
    print("The provided categories text file does not exist: " + args.categories); exit()

# Obtaining the categories from the categories text file, if applicable.
category_dict = {}
if args.categories:
    with open(args.categories, "r") as categories_file:
        all_patterns = []
        for line in categories_file:
            line = line.strip().split(": ")
            # Checking that a list of patterns was provided for each defined category.
            if len(line) != 2:
                print(line)
                print("Formatting error: " + str(Path(args.categories).name) + "\n Please ensure "
                "there are only tab-separated columns (one for the categories; another for the "
                "corresponding patterns."); exit()
            
            category = line[0]
            # Checking if categories are repeated.
            if category in category_dict:
                print("The list of categories contains repeated elements. Please revise it."); exit()
            else:
                patterns = line[1].lower().split(", ")
                all_patterns.extend(patterns)
                # Saving the category with its corresponding list of patterns.
                category_dict[category] = patterns

        # Checking if patterns were repeated.
        if len(set(all_patterns)) != len(all_patterns):
            print("At least one pattern is repeated within the categories-tsv file. Please revise it."); exit()
        else:
            del all_patterns

# Reading the input tsv_file...
with open(args.tsv_file, "r") as file:
    header = file.readline().strip().split("\t")
    # Checking that the target_col exists in the tsv_file.
    if not args.target_col in header:
        print("The provided target_col (" + args.target_col + ") does not exist. "
              "Valid options are:\n" + ", ".join(header)); exit()
    # Checking that the id_col (if provided) exists in the tsv file.
    if args.id_col and args.id_col not in header:
        print("The provided id_col (" + args.id_col + ") does not exist. "
              "Valid options are:\n" + ", ".join(header)); exit()
            
    # Saving the fields of the target column and id, as applicable.
    record_dict = {}
    id=0
    for record in file:
        record = record.strip().split("\t")
        raw_field = record[header.index(args.target_col)]
        field = raw_field.lower().replace("gaz:", "").split(":")[0].split(";")[0]
        if args.id_col:
            id = record[header.index(args.id_col)]
        else:
            id += 1
         
        if field not in record_dict:
            record_dict[field] = {id: raw_field}
        elif id not in record_dict[field]:
            record_dict[field][id] = raw_field

######################################################################################
#%% Section 2: Processing the tsv-file according to the user specifications.
######################################################################################
# If there is a category_dict set up...  
if category_dict:
    # Create a final_dict with category keys, each containing an empty dictionary.
    final_dict = {category: {} for category in category_dict.keys()}
    # Iterating through categories and the corresponding patterns.
    for category in category_dict:
        for pattern in category_dict[category]:
            # Iterating through the record_dict to save those field-IDs pairs matching
            # the patterns for the specific category.
            matched_fields = []
            for field in record_dict.keys():
                # print(category + " (" + pattern + "): " + field + " ... " + str(fnmatch.fnmatch(field, pattern)))
                if fnmatch.fnmatch(field, pattern):
                    matched_fields.append(field)
                    # print(category + " (" + pattern + ")" + ": " + field)
                    final_dict[category][field] = record_dict[field]
            # Deleting all the matched_fields keys from the record_dict.
            for field in matched_fields:
                del record_dict[field]

    # Adding all remaining field-IDs pairs to the final_dict in a None category.
    if record_dict:
        for field in record_dict:
            cap_field = [f.capitalize() for f in field.split()]
            cap_field = " ".join(cap_field)
            final_dict[cap_field] = {cap_field: record_dict[field]}
    
    record_dict = dict(final_dict); del final_dict

    id_count = 0
    for category in record_dict:
        for field in record_dict[category]:
            id_count += len(record_dict[category][field])
    print("Unique IDs: " + str(id_count))
    
######################################################################################
#%% Section 3: Writing an output collapsed file.
######################################################################################
outfile_name = args.output_dir + str(args.target_col + "-" + "collapsed_" + Path(args.tsv_file).stem + ".tsv")
with open(outfile_name, "w") as outfile:
    # If there is a category_dict set up...
    if category_dict:
        outfile.write("\t".join([args.id_col, args.target_col+"_category", args.target_col]) + "\n")
        for category in record_dict:
            for field in record_dict[category]:
                for id in record_dict[category][field]:
                    outfile.write("\t".join([id, str(category), record_dict[category][field][id]]) + "\n")
    # Otherwise...
    else:
        outfile.write("\t".join(["id", args.target_col]) + "\n")
        for field in record_dict:
            for id in record_dict[field]:
                outfile.write("\t".join([id, record_dict[field][id]]))