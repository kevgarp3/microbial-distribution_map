######################################################################################
# Section 0: Importing Modules and Initializing the App
######################################################################################
import streamlit as st
import pandas as pd
from plot_histograms import plot_singleCol_histogram, plot_twoCol_histogram

st.title("Microbiome-Distribution Map")

######################################################################################
# Section 1: Getting the bio-projects metadata file from the user and checking it
######################################################################################

tsv_file = st.sidebar.file_uploader("Upload the clean bio-projects' metadata tab-delimited file", type=["tsv", "txt"])
if not (tsv_file):
    st.info("Please provide the clean bio-projects' metadata tab-delimited file to proceed...")

######################################################################################
# Section 2: Plotting Histograms
######################################################################################

# Getting the columns for which to plot a histogram:
else:
    tsv_df = pd.read_csv(tsv_file, sep="\t")
    singleCol_hists = st.sidebar.multiselect("Select the columns for which you want to plot a histogram: ", tsv_df.columns)
    # Getting to know the user selection of columns for which to plot a histogram:
    if not (singleCol_hists):
        st.info("Please select the columns for which you want to plot a histogram to proceed...")
    else:
        # Plotting the simple histograms:
        st.success("See the requested histograms below. Currently showing: " + ", ".join(singleCol_hists))
        for col in singleCol_hists:
            st.plotly_chart(plot_singleCol_histogram(tsv_df, col))
        # Getting to know the user selection of columns for which to plot a 2-column co-dependent histogram:
        twoCol_hist = st.sidebar.multiselect("Select 2 columns for which to plot a 2-column co-dependent histogram: ", tsv_df.columns, max_selections=2)
        if not (twoCol_hist) or len(twoCol_hist) < 2:
            st.info("Please select 2 columns for which to plot a 2-column co-dependent histogram to proceed...")
        else:
            # Plotting the 2-column co-dependent histograms:
            st.success("See the requested co-dependent histogram below. Currently showing: " + " and ".join(twoCol_hist))
            st.plotly_chart(plot_twoCol_histogram(tsv_df, twoCol_hist[0], twoCol_hist[1]))

######################################################################################
#%% Section 3: Asking for a specific filter selection
######################################################################################

            biop_filter1 = st.sidebar.multiselect("Filter the Bio-Project ID's using " + twoCol_hist[0], set(tsv_df[twoCol_hist[0]]))
            biop_filter2 = st.sidebar.multiselect("Filter the Bio-Project ID's using " + twoCol_hist[1], set(tsv_df[twoCol_hist[1]]))
            if not (biop_filter1 and biop_filter2):
                st.info("Please select each of the required filters to proceed...")
            else:
                st.success("See the filtered records and choose those Bio-Project ID's which you want to focus on: ")
                filtered_records = tsv_df[tsv_df[twoCol_hist[0]].isin(biop_filter1) & tsv_df[twoCol_hist[1]].isin(biop_filter2)]
                filtered_records["sample_accession", "study_title", "sample_description"]
                filtered_biops = filtered_records["sample_accession"]
                bp_of_interest = st.multiselect("Select those Bio-Project ID's which you want to focus on: ", filtered_biops)