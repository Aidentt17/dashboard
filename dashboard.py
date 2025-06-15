###############imports#####################

import streamlit as st
import pandas as pd
import altair as alt

#################################################################
#################################UI##############################
#################################################################

# Set page layout to wide so tables can fill the width
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"  
)


# Change font theme to Manrope, Sans-Serif
st.markdown("""
    <style> 
        html, body, [class*="st-"] {font-family: 'Manrope', sans-serif !important; font-weight: 400;}
    </style>
""", unsafe_allow_html=True)

# Simple fix for dataframe menu icons
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        [data-testid="stIconMaterial"] {
            font-family: 'Material Icons' !important;
            font-feature-settings: 'liga' !important;
        }
    </style>
""", unsafe_allow_html=True)

# Hide link icons from headers
st.markdown("""
    <style>
        /* Hide all link icons */
        .stMarkdown a[href^="#"],
        .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a,
        .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

#############title####################

# Header
st.markdown("""
    <h1 style='text-align: center; font-weight: 600;'>
        Basketball Victoria Leagues - Statistics
    </h1>
    """, unsafe_allow_html=True)    

###############################Header labels########################
# Career-specific legend columns
career_header_meanings = {
    "Gender": "Player's gender",
    "GP": "Games played",
    "Name": "Player's name",
    "MIN": "Minutes played",
    "PTS": "Points scored",
    "DR": "Defensive rebounds",
    "OR": "Offensive rebounds",
    "REB": "Rebounds",
    "AST": "Assists",
    "STL": "Steals",
    "BLK": "Blocks",
    "BLKON": "Blocks received",
    "FOUL": "Fouls committed",
    "FOULON": "Fouls received",
    "TO": "Turnovers",
    "FGM": "Field goals made",
    "FGA": "Field goal attempted",
    "FG%": "Field goal percentage",
    "2PM": "Two-point goals made",
    "2PA": "Two-point goal attempted",
    "2P%": "Two-point goal percentage",
    "3PM": "Three-point goals made",
    "3PA": "Three-point goal attempted",
    "3P%": "Three-point goal percentage",
    "FTM": "Free throws made",
    "FTA": "Free throws attempted",
    "FT%": "Free throw percentage"
}

# Season-specific legend columns
season_header_meanings = {
    "Club Name": "Name of basketball club",
    "Competition Name": "Name of competition during that specific season",
    "Equivalent Competition": "Equivalent competitions have had various names over the years",
    "Level": "Competition level",
    "Gender": "Player's gender",
    "Season": "Basketball season year",
    "GP": "Games played (in season)",
    "Name": "Player's name",
    "Factor": "Factor applied to average",
    "MIN": "Minutes played",
    "PTS": "Points scored",
    "DR": "Defensive rebounds",
    "OR": "Offensive rebounds",
    "REB": "Rebounds",
    "AST": "Assists",
    "STL": "Steals",
    "BLK": "Blocks",
    "BLKON": "Blocks received",
    "FOUL": "Fouls committed",
    "FOULON": "Fouls received",
    "TO": "Turnovers",
    "FGM": "Field goals made",
    "FGA": "Field goal attempted",
    "FG%": "Field goal percentage",
    "2PM": "Two-point goals made",
    "2PA": "Two-point goal attempted",
    "2P%": "Two-point goal percentage",
    "3PM": "Three-point goals made",
    "3PA": "Three-point goal attempted",
    "3P%": "Three-point goal percentage",
    "FTM": "Free throws made",
    "FTA": "Free throws attempted",
    "FT%": "Free throw percentage"
}

############################# pop up legend ##############################
# Initialize session state for legend visibility if it doesn't exist
if 'show_legend' not in st.session_state:
    st.session_state.show_legend = False

# Function to toggle legend visibility
def toggle_legend():
    st.session_state.show_legend = not st.session_state.show_legend

# Toggle button for showing/hiding the legend with consistent text
button_text = "✗ Hide Legend" if st.session_state.show_legend else "✓ Show Legend"
st.button(button_text, on_click=toggle_legend)


##################################################################
################## user decided data set ########################
##################################################################

################# Load dataset #################

# Define dataset mappings
career_datasets = {
    "Totals": "dftotalscareer.csv",
    "Averages": "dfavgcareer.csv",
    "Averages (Adjusted to 40 minute games)": "dfscaledavgcareer.csv",
    "Averages (Per 30 minutes played)": "dfscaledthirtyavgcareer.csv"

}

seasons_datasets = {
    "Totals": "df.csv",
    "Averages": "dfavgsbs.csv",
    "Averages (Adjusted to 40 minute games)": "dfscaledavgsbs.csv",
    "Averages (Per 30 minutes played)": "dfscaledthirtyavgsbs.csv"
}

st.sidebar.markdown("## Settings")

# Main dataset type selection
dataset_type = st.sidebar.selectbox("Select Display Option", ["Career", "Seasons"])

# Based on selection, show appropriate options
if dataset_type == "Career":
    selected_readable_name = st.sidebar.radio("Select Metric Option", list(career_datasets.keys()))
    selected_dataset = career_datasets[selected_readable_name]
    current_header_meanings = career_header_meanings
    legend_title = "Career Statistics Column Definitions"
else:  # Seasons
    selected_readable_name = st.sidebar.radio("Select Metric Option", list(seasons_datasets.keys()))
    selected_dataset = seasons_datasets[selected_readable_name]
    current_header_meanings = season_header_meanings
    legend_title = "Season Statistics Column Definitions"

try:
    df = pd.read_csv(selected_dataset)
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# Converting Season to integer
if "Season" in df.columns:
    df["Season"] = df["Season"].astype(int)

############################# pop up legend ##############################
# Show legend if state is True
if st.session_state.show_legend:
    # Create scrollable legend for main area with dynamic entries based on dataset type
    legend_html = f"""
    <div style="height:300px; overflow-y:scroll; padding:10px; border:1px solid #e6e6e6; border-radius:5px; background-color:#f8f9fa;">
    <h4>{legend_title}</h4>
    """
    # Use the appropriate dictionary based on dataset type
    for header, meaning in current_header_meanings.items():
        legend_html += f"<p><strong>{header}</strong>: {meaning}</p>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)


############################ Filters ############################
# UI separator
st.sidebar.markdown("## Filters")
# reset feature
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# Button with unique key that changes on each reset
if st.sidebar.button("Reset Filters", key=f"reset_btn_{st.session_state.reset_counter}"):
    # Clear ALL session state except essential ones
    keys_to_keep = ["reset_counter", "show_legend"]
    keys_to_clear = [key for key in st.session_state.keys() if key not in keys_to_keep]
    
    for key in keys_to_clear:
        del st.session_state[key]
    
    # Force reset of all filter components by setting them to empty/default values
    filter_keys = ["search_term", "clubs", "genders", "season_range", "levels", "eq_comps", "comps"]
    for key in filter_keys:
        if key == "search_term":
            st.session_state[key] = ""
        elif key == "season_range":
            # Will be reset when component recreates
            pass
        else:
            st.session_state[key] = []
    
    # Increment counter to force component re-creation
    st.session_state.reset_counter += 1
    
    # Force rerun
    st.rerun()


# Standardize to full_name column for filtering and display
if "full_name" not in df.columns:
    if "Name" in df.columns:
        df["full_name"] = df["Name"].astype(str).str.strip()
    elif "First Name" in df.columns and "Family Name" in df.columns:
        df["full_name"] = (
            df["First Name"].astype(str).str.strip() + " " +
            df["Family Name"].astype(str).str.strip()
        )
    else:
        st.warning("No suitable player name columns found in this dataset.")
        df["full_name"] = ""  # fallback

# Player search
search_term = st.sidebar.text_input(
    "Search Player Name",
    key=f"search_term_{st.session_state.reset_counter}",
    value=st.session_state.get("search_term", "")
)
if search_term:
    matches = df["full_name"].astype(str).str.contains(search_term.strip(), case=False, na=False)
    if matches.any():
        df = df[matches]
    else:
        st.warning(f"No matches found for: '{search_term}'")

# Club filter
if "Club Name" in df.columns:
    club_options = sorted(df["Club Name"].dropna().unique())
    clubs = st.sidebar.multiselect(
    "Select Club Name(s)", 
    club_options, 
    key=f"clubs_{st.session_state.reset_counter}",
    default=st.session_state.get("clubs", [])
)
    if clubs:
        df = df[df["Club Name"].isin(clubs)]

# Gender filter
if "Gender" in df.columns:
    gender_options = sorted(df["Gender"].dropna().unique())
    genders = st.sidebar.multiselect(
    "Select Gender(s)", 
    gender_options, 
    key=f"genders_{st.session_state.reset_counter}",
    default=st.session_state.get("genders", [])
)
    if genders:
        df = df[df["Gender"].isin(genders)]
#SEASON FILTER ERROR HANDLING WITH SMIN AND MAX BEING THE SAME
if "Season" in df.columns and df["Season"].dtype in ['int64', 'float64']:
    min_season, max_season = int(df["Season"].min()), int(df["Season"].max())

    # If min and max are equal, bump max by 1 to avoid Streamlit error
    if min_season == max_season:
        max_season = min_season + 1

    season_range = st.sidebar.slider(
    "Select Season Range",
    min_value=min_season,
    max_value=max_season,
    value=(min_season, max_season if max_season != min_season else min_season),
    key=f"season_range_{st.session_state.reset_counter}"
)

    # Clamp filter to actual min_season and max_season
    # If user picks the fake max_season (min_season + 1), treat it as min_season
    start_season = season_range[0]
    end_season = season_range[1]
    if end_season > df["Season"].max():
        end_season = start_season

    df = df[(df["Season"] >= start_season) & (df["Season"] <= end_season)]

# Level filter
if "Level" in df.columns:
    level_options = sorted(df["Level"].dropna().unique())
    levels = st.sidebar.multiselect(
    "Select Level(s)", 
    level_options, 
    key=f"levels_{st.session_state.reset_counter}",
    default=st.session_state.get("levels", [])
)
    if levels:
        df = df[df["Level"].isin(levels)]

# Equivalent Competition
if "Equivalent Competition" in df.columns:
    eq_options = sorted(df["Equivalent Competition"].dropna().unique())
    eq_comps = st.sidebar.multiselect(
    "Select Equivalent Competition(s)", 
    eq_options, 
    key=f"eq_comps_{st.session_state.reset_counter}",
    default=st.session_state.get("eq_comps", [])
)
    if eq_comps:
        df = df[df["Equivalent Competition"].isin(eq_comps)]

# Competition Name
if "Competition Name" in df.columns:
    comp_options = sorted(df["Competition Name"].dropna().unique())
    comps = st.sidebar.multiselect(
    "Select Competition Name(s)", 
    comp_options, 
    key=f"comps_{st.session_state.reset_counter}",
    default=st.session_state.get("comps", [])
)
    if comps:
        df = df[df["Competition Name"].isin(comps)]



############################ Highlighting ############################
#
#st.sidebar.markdown("### **________ Highlight Options _________**")
#
#highlight_mode = st.sidebar.radio("Highlight Specific Rows?", ["No", "Yes"])
#
#highlight_column = None
#highlight_type = None
#highlight_value = None
#
#if highlight_mode == "Yes":
#    highlight_column = st.sidebar.selectbox("Highlight by Column", df.columns)
#    highlight_type = st.sidebar.radio("Condition", ["Equals", "Greater Than", "Less Than"])
#    highlight_value = st.sidebar.text_input("Value to Match")
#warning
#    if len(df) > 500:
#        st.warning("Warning: The dataset is quite large, please consider reducing the size of the dataset through thre filters.")
#
#    def highlight_filtered_rows(row):
#        try:
#            cell = row[highlight_column]
#            if highlight_type == "Equals" and str(cell) == highlight_value:
#                return ['background-color: orange'] * len(row)
#            elif highlight_type == "Greater Than" and pd.to_numeric(cell, errors='coerce') > float(highlight_value):
#            elif highlight_type == "Less Than" and pd.to_numeric(cell, errors='coerce') < float(highlight_value):
#                return ['background-color: orange'] * len(row)
#        except:
#            pass
#        return [''] * len(row)

############################ Display/ math ############################
# Remove the row index and keep the result in df
df = df.reset_index(drop=True)


info_columns = [
    "Name","First Name", "Family Name", "Gender", "Season", "Club Name", "Competition Name",
    "Equivalent Competition", "Level", "GP", "full_name"
]

# Columns to show (exclude 'full_name')
display_info_columns = [col for col in info_columns if col != "full_name"]

# Define stat columns (exclude full_name too, just in case it's not info)
stat_columns = [
    col for col in df.columns 
    if col not in info_columns and col != "full_name"
]

# Final displayed columns
final_columns = [
    col for col in display_info_columns + stat_columns 
    if col in df.columns
]

############################ Column Hiding Logic ############################
# Define columns to hide based on dataset type and metric option
columns_to_hide = []

# Hide Level and Factor columns for all Seasons datasets
if dataset_type == "Seasons":
    columns_to_hide.extend(["Level", "Factor"])

# Hide Minutes column for "Per 30 minutes played" options
if "Per 30 minutes played" in selected_readable_name:
    columns_to_hide.append("MIN")

# Remove hidden columns from final_columns
final_columns = [col for col in final_columns if col not in columns_to_hide]

st.write(f"### Displaying: {selected_readable_name}")

############################ Dataset Descriptions ############################
# Add descriptions for specific metric options
if "Adjusted to 40 minute games" in selected_readable_name:
    st.write("*Stats from 48 minute games in earlier seasons (where applicable) are adjusted down to 40 minutes worth*")
elif "Per 30 minutes played" in selected_readable_name:
    st.write("*Stats adjusted based on everyone playing 30 minutes per game (average starter minutes)*")

# Identify numeric columns for formatting
numeric_cols = df[final_columns].select_dtypes(include='number').columns

# Check if current dataset is an averaged dataset
is_averaged_dataset = any(keyword in selected_readable_name for keyword in ["Averages", "Per 30 minutes played"])

# Custom format: 1 decimal point for averaged datasets, smart format for totals
def smart_format(x, col_name=None):
    if pd.isna(x):
        return ""
    elif isinstance(x, (int, float)):
        # Always show Season as whole number
        if col_name == "Season":
            return f"{int(x)}"
        elif is_averaged_dataset:
            return f"{x:.1f}"  # Always 1 decimal for averaged datasets
        else:
            return f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}"  # Smart format for totals
    return x

# Function to convert columns to appropriate numeric types
def convert_to_numeric(df, columns):
    """Convert specified columns to numeric, handling errors gracefully"""
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
    return df_copy

# Display the dataframe
df_for_display = convert_to_numeric(df[final_columns], numeric_cols)

# Configure formatting for numeric columns
column_config = {}
for col in numeric_cols:
    if col in df_for_display.columns:
        if col == "Season":
            column_config[col] = st.column_config.NumberColumn(col, format="%d")
        elif is_averaged_dataset:
            column_config[col] = st.column_config.NumberColumn(col, format="%.1f")
        else:
            column_config[col] = st.column_config.NumberColumn(col, format="%.0f")

# Pin Name column to left
column_config["Name"] = st.column_config.Column("Name", pinned="left")

st.dataframe(
    df_for_display,
    hide_index=True,
    use_container_width=True,
    column_config=column_config
)


#if highlight_mode == "Yes":
#    st.dataframe(
#        df[final_columns]
#        .style
#        .format(format_dict)
#        .apply(highlight_filtered_rows, axis=1)
#    )
#else:
#    st.dataframe(
#        df[final_columns]
#        .style
#        .format(format_dict)
#    )




########################################        
# extra U/I
########################################

# White fixed header
st.markdown("""
    <style>
        .header-white {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            color: #000000;
            text-align: center;
            padding: 15px 0;
            font-size: 20px;
            font-weight: bold;
            z-index: 1000;
            border-bottom: 1px solid #ddd;
        }

        /* Push content down so it's not hidden behind the header */
        .main > div {
            padding-top: 70px;
        }
    </style>

    <div class="header-white">
        My Streamlit App Header
    </div>
""", unsafe_allow_html=True)

# Double footer with dark grey and black
st.markdown("""
    <style>
        .footer-darkgrey {
            position: fixed;
            left: 0;
            bottom: 30px; /* Height of the black footer */
            width: 100%;
            background-color: #333333;
            color: #ffffff;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
        }

        .footer-black {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #000000;
            color: #ffffff;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
        }
    </style>

    <div class="footer-darkgrey">
        Subscribe
    </div>
    <div class="footer-black">
        About
    </div>
""", unsafe_allow_html=True)

#streamlit css
st.markdown("""
<style>
[data-testid="stElementToolbar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
