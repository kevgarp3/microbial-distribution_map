########################################################################################################################################################
# Section 0: Importing Modules, Declaring Hard-Coded Paths and Initializing the App
########################################################################################################################################################
import streamlit as st
import os
import signal
import pandas as pd
from itertools import compress
from plot_histograms import rm_category, add_category, plot_singleCol_histogram, plot_twoCol_histogram
from prep_fastq_download import get_fastq_links, call_download_fastqs
from get_map_render import render_map
from streamlit_theme import st_theme
from pathlib import Path

project_dir = "results/skin-microbiome/" # To further be received by Snakemake
fastqs_dir = project_dir + "0_data/0-3_fastq_downloads/"
histograms_dir = project_dir + "1_plots/1-1_histograms/"
kronas_dir = project_dir + "1_plots/1-2_krona_plots/"
maps_dir = project_dir + "2_maps/"

st.title("Microbiome-Distribution Map")
if st.sidebar.button("Close app"):
    os.kill(os.getpid(), signal.SIGTERM)

########################################################################################################################################################
# Section 1: Getting the clean bio-projects metadata file from the user and checking it
########################################################################################################################################################
tsv_file = st.sidebar.file_uploader("Upload the clean bio-projects' metadata tab-delimited file", type=["tsv", "txt"])
if not (tsv_file):
    st.info("Please provide the clean bio-projects' metadata tab-delimited file in the side window to proceed...")
else:
    # Reading the provided tsv_file and making sure it contains all the expected columns.
    tsv_df = pd.read_csv(tsv_file, sep="\t")
    expected_cols = ["run_accession", "sample_accession", "location", "fastq_ftp", "fastq_md5", "study_title", "sample_description"]
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
            st.success("The provided file contains the right format. Thank you!")
            # Getting the columns for which to plot a histogram:
            singleCol_hists = st.sidebar.multiselect("Select the columns for which you want to plot a histogram: ", [rm_category(col) for col in category_cols])
            # Getting to know the user selection of columns for which to plot a histogram:
            if not (singleCol_hists):
                st.info("Please select the columns for which you want to plot a histogram to proceed...")
            else:
                st.header("Exploring the Data Distribution of the Sequencing Experiments")
                st.subheader("Per-Column Histograms")
                # Plotting the simple histograms:
                st.success("See the requested histograms below.")
                st.text("Currently showing the distribution per:\n" + "\n".join([col for col in singleCol_hists]))
                for col in singleCol_hists:
                    st.plotly_chart(plot_singleCol_histogram(tsv_df, col + "_category"))
                # Getting to know the user selection of columns for which to plot a 2-column co-dependent histogram:
                twoCol_hist = st.sidebar.multiselect("Select 2 columns for which to plot a 2-column co-dependent histogram: ", [rm_category(col) for col in category_cols], max_selections=2)
                if not (twoCol_hist) or len(twoCol_hist) < 2:
                    st.info("Please select 2 columns for which to plot a 2-column co-dependent histogram to proceed...")
                else:
                    st.subheader("2-Column Co-Dependent Histogram")
                    # Plotting the 2-column co-dependent histograms:
                    st.success("See the requested co-dependent histogram below.")
                    st.text("Currently showing the distribution for:\n" + "\n".join([col for col in twoCol_hist]))
                    st.plotly_chart(plot_twoCol_histogram(tsv_df, twoCol_hist[0] + "_category", twoCol_hist[1]  + "_category"))
                    Path(histograms_dir + ".app_histograms_viewed.txt").touch()

########################################################################################################################################################
# Section 3: Asking for a specific filter selection
########################################################################################################################################################
                    exp_filter1 = st.sidebar.multiselect("Filter the sequencing experiment IDs using " + rm_category(twoCol_hist[0]), set(tsv_df[add_category(twoCol_hist[0])]))
                    exp_filter2 = st.sidebar.multiselect("Filter the sequencing experiment IDs using " + rm_category(twoCol_hist[1]), set(tsv_df[add_category(twoCol_hist[1])]))
                    if not (exp_filter1 and exp_filter2):
                        st.info("Please select both of the required filters to proceed...")
                    else:
                        st.success("See information related to the filtered sequencing experiments below.")
                        st.text("Currently filtering sequencing experiments for:\n"
                                 + twoCol_hist[0] + ": " + ", ".join(map(str, (exp_filter1))) + "\n" 
                                 + twoCol_hist[1] + ": " + ", ".join(map(str, (exp_filter1)))
                        )
                        # Filtering the data frame using the user-defined filters.
                        twoCol_hist = [add_category(col) for col in twoCol_hist]
                        filtered_df = tsv_df[tsv_df[twoCol_hist[0]].isin(exp_filter1) & tsv_df[twoCol_hist[1]].isin(exp_filter2)]
                        # Filtering the data frame 
                        df_toShow = filtered_df[["run_accession", "study_title", "location"] + category_cols]
                        # Showing the details and distribution of the filtered sequencing experiments.
                        st.info("See the details of the filtered sequencing experiments below:")
                        st.text("Number of filtered records: " + str(len(df_toShow)))
                        st.dataframe(df_toShow, use_container_width=True)
                        st.info("See the distribution of the filtered sequencing experiments below:")
                        st.plotly_chart(plot_twoCol_histogram(filtered_df, twoCol_hist[0], twoCol_hist[1]))

########################################################################################################################################################
# Section 4: Downloading FASTQ files, if desired
########################################################################################################################################################
                        # Asking the user to pick some of the sequencing experiments which to focus on them.  
                        st.info("Please select the sequencing experiments whose FASTQ files you want to download.")
                        ids_of_interest = st.multiselect("Select the run_accession IDs: ", filtered_df["run_accession"])
                        if ids_of_interest:
                            # Implementing a button to download the FASTQ files of the selected Bio-Projects.
                            st.info("Click on \"Download FASTQ Files\" when ready.")
                            if st.button("⬇️ Download FASTQ Files"):
                                # From filtered_df, extracting the links to download the FASTQ files specific to the run_accession IDs selected by the user.
                                links = get_fastq_links(filtered_df, ids_of_interest)
                                st.text("Downloads requested from the following URLs:\n" + "\n".join(links))
                                with st.spinner("Downloading FASTQ files. This might take a while..."):
                                    # Downloading the FASTQ files using the extracted links.
                                    result = call_download_fastqs(fastqs_dir, links)
                                if result.returncode == 0:
                                    st.success("Download complete!")
                                    st.code(result.stdout)
                                else:
                                    st.error("Something went wrong!")
                                    st.code(result.stderr)

## Possibly include a "Get List of FASTQs" button
                        
########################################################################################################################################################
# Section 4: Exploring the geographical distribution of the sequencing experiments
########################################################################################################################################################
                        st.header("Exploring the Geographical Distribution of the Sequencing Experiments")
                        st.info("Please select the level of visualization for the map.")
                        
                        # Allow the user to choose the level of visualization for the map.
                        map_lvls = ["All Sequencing Experiments", "Filtered Sequencing Experiments", "Specifically Selected Run_Accession IDs"]
                        map_lvl_of_interest = st.selectbox("Select what you want to see:",
                                                           options = [None] + map_lvls,
                                                           format_func=lambda x: "— select —" if x is None else x)
                        # Get the current app theme used by the user.
                        theme = st_theme()
                        map_theme = theme['base'] if theme else 'light'

                        if map_lvl_of_interest:
                            if map_lvl_of_interest == map_lvls[0]:
                                df_to_map = tsv_df
                            elif map_lvl_of_interest == map_lvls[1]:
                                df_to_map = filtered_df
                            else:
                                df_to_map = filtered_df[filtered_df["run_accession"].isin(ids_of_interest)]
                            
                            df_to_map = df_to_map[["run_accession", "sample_accession", "study_title", "location"] + category_cols]
                            df_in_map = render_map(df_to_map, kronas_dir, map_theme)
                            Path(maps_dir + ".app_map_viewed.txt").touch()
                            st.info("Click on \"Dowload Map Data (CSV)\" when ready.")
                            # Export map data as CSV
                            if st.button(label="⬇️ Download Map Data (CSV)"):
                                map_filepath = os.path.join(maps_dir, "map_data.csv")
                                data=df_in_map.drop(columns=["color", "tooltip"]).to_csv(map_filepath, index=False)
                                st.success(f"Saved to '{map_filepath}'")
                                # END MESSAGE:
                                st.caption("Please click on the Close App button at the top of the sidebar, when you have finished exploring the data")