########################################################################################################################################################
# Section 0: Importing Modules, Declaring Hard-Coded Paths and Initializing the App
########################################################################################################################################################
import streamlit as st
import pandas as pd
from itertools import compress
from plot_histograms import plot_singleCol_histogram, plot_twoCol_histogram
import subprocess
import os
import signal

project_dir = "results/skin-microbiome/" # To further be received by Snakemake
outdir_hists = project_dir + "2_histograms"
outdir_fastqs = project_dir + "3_fastq_downloads"
outdir_kronas = project_dir + "4_krona_plots"

st.title("Microbiome-Distribution Map")
if st.button("Close app"):
    os.kill(os.getpid(), signal.SIGTERM)
########################################################################################################################################################
# Section 1: Getting the clean bio-projects metadata file from the user and checking it
########################################################################################################################################################
tsv_file = st.sidebar.file_uploader("Upload the clean bio-projects' metadata tab-delimited file", type=["tsv", "txt"])
if not (tsv_file):
    st.info("Please provide the clean bio-projects' metadata tab-delimited file to proceed...")
else:
    # Reading the provided tsv_file and making sure it contains all the expected columns.
    tsv_df = pd.read_csv(tsv_file, sep="\t")
    expected_cols = ["run_accession", "sample_accession", "location", "fastq_ftp", "study_title", "sample_description"]
    if not all([col in tsv_df.columns for col in expected_cols]):
        st.warning("You have provided an invalid tab-delimited file. Please validate your input and upload the clean bio-projects'"
                   "metadata file. You can obtain it using this app's pre-processing pipeline.")
    else:
        # Checking if the provided tsv_file contains any columns processed by the pre-processing pipeline.
        col_is_category = ["_category" in col for col in tsv_df.columns]
        category_cols = list(compress(tsv_df.columns, col_is_category))
        if not category_cols:
            st.warning("The tab-delimited file you have provided seems not to be properly cleaned as it is missing categorized columns. "
                       "Please validate your input and upload the clean bio-projects's metadata file. You can obtain it using this app's "
                       "pre-processing pipeline.")
        elif len(category_cols) < 2:
            st.warning("The tab-delimited file only contains one categorized column. Please make sure at least two columns are "
                       "categorized using this app's pre-processing pipeline.")    
            
########################################################################################################################################################
# Section 2: Plotting Histograms
########################################################################################################################################################
        else:
            # Getting the columns for which to plot a histogram:
            singleCol_hists = st.sidebar.multiselect("Select the columns for which you want to plot a histogram: ", category_cols)
            # Getting to know the user selection of columns for which to plot a histogram:
            if not (singleCol_hists):
                st.info("Please select the columns for which you want to plot a histogram to proceed...")
            else:
                st.header("Exploring the Distribution of Sequencing Experiments...")
                st.subheader("Per-Column Histograms")
                # Plotting the simple histograms:
                st.success("See the requested histograms below.")
                st.text("Currently showing the distribution per:\n" + "\n".join(singleCol_hists))
                for col in singleCol_hists:
                    st.plotly_chart(plot_singleCol_histogram(tsv_df, col))
                # Getting to know the user selection of columns for which to plot a 2-column co-dependent histogram:
                twoCol_hist = st.sidebar.multiselect("Select 2 columns for which to plot a 2-column co-dependent histogram: ", category_cols, max_selections=2)
                if not (twoCol_hist) or len(twoCol_hist) < 2:
                    st.info("Please select 2 columns for which to plot a 2-column co-dependent histogram to proceed...")
                else:
                    st.subheader("2-Column Co-Dependent Histogram")
                    # Plotting the 2-column co-dependent histograms:
                    st.success("See the requested co-dependent histogram below.")
                    st.text("Currently showing the distribution per:\n" + " and ".join(twoCol_hist))
                    st.plotly_chart(plot_twoCol_histogram(tsv_df, twoCol_hist[0], twoCol_hist[1]))

########################################################################################################################################################
# Section 3: Asking for a specific filter selection
########################################################################################################################################################
                    exp_filter1 = st.sidebar.multiselect("Filter the sequencing experiment IDs using " + twoCol_hist[0], set(tsv_df[twoCol_hist[0]]))
                    exp_filter2 = st.sidebar.multiselect("Filter the sequencing experiment IDs using " + twoCol_hist[1], set(tsv_df[twoCol_hist[1]]))
                    if not (exp_filter1 and exp_filter2):
                        st.info("Please select both of the required filters to proceed...")
                    else:
                        st.success("See information related to the filtered sequencing experiments below.")
                        st.text("Currently filtering sequencing experiments for:\n"
                                 + twoCol_hist[0] + ": " + ", ".join(exp_filter1) + "\n" + twoCol_hist[1] + ": " + ", ".join(exp_filter2))
                        # Filtering the data frame using the user-defined filters.
                        filtered_df = tsv_df[tsv_df[twoCol_hist[0]].isin(exp_filter1) & tsv_df[twoCol_hist[1]].isin(exp_filter2)]
                        # Filtering the data frame 
                        df_toShow = filtered_df[["run_accession", "sample_accession", "study_title", "fastq_ftp"]]
                        # Showing the details and distribution of the filtered sequencing experiments.
                        st.info("See the details of the filtered sequencing experiments below:")
                        st.dataframe(df_toShow, use_container_width=True)
                        st.info("See the distribution of the filtered sequencing experiments below:")
                        st.plotly_chart(plot_twoCol_histogram(filtered_df, twoCol_hist[0], twoCol_hist[1]))
                        # Asking the user to pick some of the sequencing experiments which to focus on them.  
                        st.info("Please select the sequencing experiments whose FASTQ files you want to download.")
                        id_of_interest = st.multiselect("Select the run_accession IDs: ", filtered_df["run_accession"])
                        if id_of_interest:
                            # Implementing a button to download the FASTQ files of the selected Bio-Projects.
                            st.info("Click on \"Download FASTQ Files\" when ready.")
                            if st.button("Download FASTQ Files"):
                                # Get all fields from the "fastq_ftp" column of the filtered df whose "sample_accession" was selected by the user.
                                raw_links = filtered_df.loc[filtered_df["run_accession"].isin(id_of_interest), "fastq_ftp"]
                                # Extract the actual links.
                                links = [link.strip() for raw_link in raw_links for link in raw_link.strip().split(";")]
                                st.text("Downloads requested from the following URLs:\n" + "\n".join(links))
                                with st.spinner("Downloading FASTQ files. This might take a while..."):
                                    result = subprocess.run(["bash", "src/download_fastq.sh", outdir_fastqs] + links, 
                                        capture_output=True, text=True)
                                if result.returncode == 0:
                                    st.success("Download complete!")
                                    st.code(result.stdout)
                                else:
                                    st.error("Something went wrong!")
                                    st.code(result.stderr)

                        st.success("All fine!")