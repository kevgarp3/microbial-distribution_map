#!/usr/bin/python3
"""
Title: plot_histograms.py

Description:
This script processes a tab-delimited file to plot a histogram for each column specified
by the user. Histograms derived of co-dependent columns is enabled as an option.

Usage:
'''PYTHON
'''

Version: 1.0
Date: 12-Mar-2026
Author: Kevin García Prado
"""
######################################################################################
#%% Section 0: Importing the necessary modules.
######################################################################################
import plotly.express as px
#import matplotlib.pyplot as plt

######################################################################################
#%% Section 1: Declaring the functions.
######################################################################################
# Declaring a function for plotting single-column histograms.
def plot_singleCol_histogram(df, col):
    fig = px.histogram(df, x=col, title="Distribution of " + col)
    return fig

# Declaring a function for plotting a two-column co-dependent histogram.
def plot_twoCol_histogram(df, col1, col2):
    fig = px.histogram(df, x=col1, color=col2, barmode="overlay", 
                        title="Distribution of " + col1 + " by " + col2)
    return fig