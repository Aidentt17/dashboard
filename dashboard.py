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

#############title####################

# Header
st.markdown("""
    <h1 style='text-align: center; font-weight: 600;'>
        Basketball Victoria Statistic Display
    </h1>
    """, unsafe_allow_html=True)    

###############################Header labels########################

header_meanings = {
    "FIBA ID Number": "International Basketball Federation Number",
    "First Name": "Player's first name",
    "Family Name": "Player's last name",
    "Gender": "Player's gender",
    "Club Name": "Name of basketball club",
    "Competition Name": "Name of competition",
    "Season": "Basketball season year",
    "GP": "Games played",
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
    "2PM": "Two-point goals made",
    "2PA": "Two-point goal attempted",
    "3PM": "Three-point goals made",
    "3PA": "Three-point goal attempted",
    "FTM": "Free throws made",
    "FTA": "Free throws attempted"
}

############################# pop up legend ##############################
def show_legend_popup():
    with st.modal("Column Definitions Legend"):
        st.subheader("Basketball Statistics Column Definitions")
        
        # Create a scrollable container for the definitions
        legend_container = st.container()
        with legend_container:
            # Use columns to create a nicer layout
            col1, col2 = st.columns(2)
            
            # Split definitions between columns for better readability
            cols = list(df.columns)
            half = len(cols) // 2
            
            for i, col in enumerate(cols):
                # Determine which column to place this definition
                display_col = col1 if i < half else col2
                
                with display_col:
                    if col in header_meanings:
                        st.markdown(f"**{col}**: {header_meanings[col]}")
                    else:
                        st.markdown(f"**{col}**: No definition available")
        
        # Add a button to close the modal
        st.button("Close", key="close_legend")


# Initialize session state for legend visibility if it doesn't exist
if 'show_legend' not in st.session_state:
    st.session_state.show_legend = False

# Function to toggle legend visibility
def toggle_legend():
    st.session_state.show_legend = not st.session_state.show_legend

# Toggle button for showing/hiding the legend with consistent text
button_text = "✗ Hide Scrollable Column Legend" if st.session_state.show_legend else "✓ Show Scrollable Column Legend"
st.button(button_text, on_click=toggle_legend)

# Show legend if state is True
if st.session_state.show_legend:
    # Create scrollable legend for main area with hardcoded entries
    legend_html = """
    <div style="height:300px; overflow-y:scroll; padding:10px; border:1px solid #e6e6e6; border-radius:5px; background-color:#f8f9fa;">
    """
    # Use the hardcoded dictionary directly without referencing df.columns
    for header, meaning in header_meanings.items():
        legend_html += f"<p><strong>{header}</strong>: {meaning}</p>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)



##################################################################
################## user decided data set ########################
##################################################################

################# Load dataset #################

available_datasets = [
    "df.csv",
    "dfavgcareer.csv",
    "dfavgsbs.csv",
    "dfscaledavgcareer.csv",
    "dfscaledavgsbs.csv",
    "dfscaledthirtyavgcareer.csv",
    "dfscaledthirtyavgsbs.csv",
    "dftotalscareer.csv"
]
dataset_name_map = {
    "df.csv": "Total Season by Season",
    "dfavgcareer.csv": "Average Career Stats",
    "dfavgsbs.csv": "Average Season by Season Stats",
    "dfscaledavgcareer.csv": "Adjusted 40-Minutes Avg Career Stats",
    "dfscaledavgsbs.csv": "Adjusted 40-Minutes Avg Season by season Stats",
    "dfscaledthirtyavgcareer.csv": "Adjusted 30-Minutes Avg Career Stats",
    "dfscaledthirtyavgsbs.csv": "Adjusted 30-Minutes Avg Season by Season Stats",
    "dftotalscareer.csv": "Total Career Stats"
}

readable_to_filename = {v: k for k, v in dataset_name_map.items()}

readable_names = list(readable_to_filename.keys())
selected_readable_name = st.sidebar.selectbox("Choose a Dataset", readable_names)
selected_dataset = readable_to_filename[selected_readable_name]

try:
    df = pd.read_csv(selected_dataset)
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()


############################ Filters ############################

# UI separator
st.sidebar.markdown("### **_________ Filter Options ___________**")

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
        df["full_name"] = ""  # fallback to prevent errors

# Player search
search_term = st.sidebar.text_input("Search Player Name")
if search_term:
    matches = df["full_name"].astype(str).str.contains(search_term.strip(), case=False, na=False)
    if matches.any():
        df = df[matches]
    else:
        st.warning(f"No matches found for: '{search_term}'")


# Only apply search if a valid name column exists
if search_term:
    if "full_name" in df.columns:
        df = df[df["full_name"].astype(str).str.contains(search_term, case=False, na=False)]
    else:
        st.warning("No 'full_name' column found. Player name search is not available for this dataset.")

# Club filter
if "Club Name" in df.columns:
    clubs = st.sidebar.multiselect("Select Club Name(s)", df["Club Name"].dropna().unique())
    if clubs:
        df = df[df["Club Name"].isin(clubs)]

# Gender filter
if "Gender" in df.columns:
    genders = st.sidebar.multiselect("Select Gender(s)", df["Gender"].dropna().unique())
    if genders:
        df = df[df["Gender"].isin(genders)]

# Season filter
if "Season" in df.columns and df["Season"].dtype in ['int64', 'float64']:
    min_season, max_season = int(df["Season"].min()), int(df["Season"].max())
    season_range = st.sidebar.slider("Select Season Range", min_season, max_season, (min_season, max_season))
    df = df[(df["Season"] >= season_range[0]) & (df["Season"] <= season_range[1])]

# Level filter
if "Level" in df.columns:
    levels = st.sidebar.multiselect("Select Level(s)", df["Level"].dropna().unique())
    if levels:
        df = df[df["Level"].isin(levels)]

# Equivalent Competition
if "Equivalent Competition" in df.columns:
    eq_comps = st.sidebar.multiselect("Select Equivalent Competition(s)", df["Equivalent Competition"].dropna().unique())
    if eq_comps:
        df = df[df["Equivalent Competition"].isin(eq_comps)]

# Competition Name
if "Competition Name" in df.columns:
    comps = st.sidebar.multiselect("Select Competition Name(s)", df["Competition Name"].dropna().unique())
    if comps:
        df = df[df["Competition Name"].isin(comps)]

############################ Highlighting ############################

st.sidebar.markdown("### **________ Highlight Options _________**")

highlight_mode = st.sidebar.radio("Highlight Specific Rows?", ["No", "Yes"])

highlight_column = None
highlight_type = None
highlight_value = None

if highlight_mode == "Yes":
    highlight_column = st.sidebar.selectbox("Highlight by Column", df.columns)
    highlight_type = st.sidebar.radio("Condition", ["Equals", "Greater Than", "Less Than"])
    highlight_value = st.sidebar.text_input("Value to Match")
#warning
    if len(df) > 500:
        st.warning("Warning: The dataset is quite large, please consider reducing the size of the dataset through thre filters.")

    def highlight_filtered_rows(row):
        try:
            cell = row[highlight_column]
            if highlight_type == "Equals" and str(cell) == highlight_value:
                return ['background-color: orange'] * len(row)
            elif highlight_type == "Greater Than" and pd.to_numeric(cell, errors='coerce') > float(highlight_value):
                return ['background-color: orange'] * len(row)
            elif highlight_type == "Less Than" and pd.to_numeric(cell, errors='coerce') < float(highlight_value):
                return ['background-color: orange'] * len(row)
        except:
            pass
        return [''] * len(row)

############################ Display/ math ############################

info_columns = [
    "Name", "First Name", "Family Name", "Club Name", "Competition Name",
    "Equivalent Competition", "Level", "Gender", "Season", "GP"
]

stat_columns = [col for col in df.columns if col not in info_columns]
final_columns = [col for col in info_columns + stat_columns if col in df.columns]

readable_name = dataset_name_map.get(selected_dataset, selected_dataset)
st.write(f"### Displaying: {readable_name}")

if highlight_mode == "Yes":
    st.dataframe(df[final_columns].style.apply(highlight_filtered_rows, axis=1))
else:
    st.dataframe(df[final_columns])

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