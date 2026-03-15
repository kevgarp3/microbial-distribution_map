import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import re
import glob
import os

def parse_location(loc_str):
    # Parses a location string like '32.89155 N 117.23836 W' into (lat, lon).
    if not isinstance(loc_str, str) or not loc_str.strip():
        return None, None
    pattern = r"([\d.]+)\s*([NS])\s+([\d.]+)\s*([EW])"
    match = re.match(pattern, loc_str.strip())
    if not match:
        return None, None
    lat = float(match.group(1)) * (1 if match.group(2) == "N" else -1)
    lon = float(match.group(3)) * (1 if match.group(4) == "E" else -1)
    return lat, lon

def load_krona_files(krona_dir: str) -> dict:
    # Returns {run_accession: html_content} for all *_krona.html files found in krona_dir
    krona_map = {}
    for path in glob.glob(os.path.join(krona_dir, "*_krona.html")):
        filename = os.path.basename(path)
        run_acc = filename.replace("_krona.html", "")
        with open(path, "r", encoding="utf-8") as f:
            krona_map[run_acc] = f.read()
    return krona_map

def render_map(df, krona_dir, map_theme):
    # Parsing the coordinates
    df_map = df.copy()
    df_map[["lat", "lon"]] = df_map["location"].apply(
        lambda x: pd.Series(parse_location(x))
        )

    # Extracting only those mappable records from the whole dataset 
    df_valid = df_map.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    if df_valid.empty:
        st.warning("No records with valid coordinates to display.")
        return

    # Getting duplicated (overlapping) coordinates
    coords = df_valid[["lat", "lon"]].values
    duplicated = df_valid.duplicated(subset=["lat", "lon"], keep=False)

    # Jittering overlapping coordinates slightly
    rng = np.random.default_rng(seed=42)  # Seed for reproducibility
    jitter_amount = 0.035
    coords[duplicated.values, 0] += rng.uniform(-jitter_amount, jitter_amount, duplicated.sum())
    coords[duplicated.values, 1] += rng.uniform(-jitter_amount, jitter_amount, duplicated.sum())
    df_valid[["lat", "lon"]] = coords

    # Showing a caption message for each of how many valid records are plotted in the map.
    n_dropped = len(df_map) - len(df_valid)
    if n_dropped:
        st.caption(f"⚠️ {n_dropped} record(s) excluded — missing or unparseable location.")
    elif len(df_map) != len(df_valid):
        st.caption(f"❌ All the requested records ({n_dropped}) were excluded — missing or unparseable location.")
    else:
        st.caption(f"✅ All the requested records are included - correct location format found.")

    # Getting all krona HTML files
    krona_files = load_krona_files(krona_dir)
    # Flaggint points that have a krona file
    df_valid["has_krona"] = df_valid["run_accession"].isin(krona_files)

    # Two colors: one for points with krona, one without
    df_valid["color"] = df_valid["has_krona"].apply(
        lambda x: [30, 144, 255, 180] if x else [120, 120, 120, 160]
    )
    # [120, 120, 120, 160]  # Gray
    # [220, 50, 50, 200]    # Red
    # [30, 144, 255, 180]   # Blue

    # Build HTML tooltip: all columns except lat/lon/color/has_krona.
    tooltip_cols = [c for c in df_valid.columns if c not in ("lat", "lon", "color", "has_krona")]
    # Per-point HTML tooltip — to conditionally include krona-related notes.
    df_valid["tooltip"] = df_valid.apply(
        lambda row: "".join(f"<b>{col}:</b> {row[col]}<br/>" for col in tooltip_cols) +
                    ("<br/><i style='color:1E90FFB4'>🔬 Available krona plot</i>" if row["has_krona"] else ""),
                    axis=1
    )
    # Setting the map style depending on the chosen map_theme (dark/light)
    # Using free CARTO basemaps (without any API key/token needed)
    if map_theme == 'dark':
        m_style = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json" # Dark background, white borders
    else:
        m_style = "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"  # Colorful and with visible borders.

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_valid,
        get_position="[lon, lat]",
        get_radius=8000,        # metres — adjust to taste
        radius_min_pixels=3,    # never smaller than 3px (zoomed out)
        radius_max_pixels=10,   # never larger than 10px (zoomed in)
        get_fill_color="color",
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
        pickable=True,
        auto_highlight=True)

    view_state = pdk.ViewState(
        latitude=df_valid["lat"].mean(),
        longitude=df_valid["lon"].mean(),
        zoom=5,
        pitch=0)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"html": "{tooltip}", 
                 "style": {"color": "white", "backgroundColor": "#1a1a2e"}},
        map_style = m_style)

    st.pydeck_chart(deck)
    
    # Getting the IDs of all records which have a krona plot.
    krona_points = df_valid[df_valid["has_krona"]]["run_accession"].tolist()
    # Only show selector for points that have a krona plot.
    if not krona_points:
        st.info("No Krona plots available for any mapped point.")
    else:
        run_acc_krona = st.selectbox("🔬 Select a run_accession ID to view its Krona plot:",
                                     options=[None] + krona_points,
                                     format_func=lambda x: "— select —" if x is None else x)
        # Render the krona plot for the selected run_accession ID.
        if run_acc_krona:
            st.markdown(f"### 🔬 Krona plot — `{run_acc_krona}`")
            st.components.v1.html(krona_files[run_acc_krona], height=600, scrolling=True)
    
    return df_valid