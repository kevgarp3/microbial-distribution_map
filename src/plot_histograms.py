#!/usr/bin/python3
"""
Title: plot_histograms.py

Description:
This module contains functions plot histograms for each column specified by the
Histograms derived of co-dependent columns are enabled as well.

Usage:
'''PYTHON
from plot_histograms import plot_singleCol_histogram, plot_twoCol_histogram
'''

Version: 1.0
Date: 12-Mar-2026
Author: Kevin García Prado
"""
######################################################################################
#%% Section 0: Importing the necessary modules.
######################################################################################
import plotly.express as px

######################################################################################
#%% Section 1: Declaring the functions.
######################################################################################
def rm_category(colname) -> str:
    return colname.strip().replace("_category", "").replace("_", " ").title()

def add_category(colname) -> str:
    return colname.lower().replace(" ", "_") + "_category"

# Declaring a function for plotting single-column histograms.
def plot_singleCol_histogram(df, col):
    fig = px.histogram(df, x=add_category(rm_category(col)), title="Distribution of " + rm_category(col))
    return fig

# Declaring a function for plotting a two-column co-dependent histogram.
def plot_twoCol_histogram(df, col1, col2):
    fig = px.histogram(df, x=add_category(rm_category(col1)),
                       color=add_category(rm_category(col2)),
                       barmode="overlay", 
                       title="Distribution of " + rm_category(col1) + " per " + rm_category(col2))
    return fig