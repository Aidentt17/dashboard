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
df = pd.read_excel("all.xlsx", engine="openpyxl")
# Remove whitespace if any
df.columns = df.columns.str.strip()

################## UI for type of data ##################

# options for the different scaleing
scale_options = ["Raw", "Scaled (Per Minute)", "Scaled (to 40 Minutes)"]
selected_scale = st.sidebar.selectbox("Select Stats View", scale_options)

# Map to column prefixes
if selected_scale == "Raw":
    prefix = ""
elif selected_scale == "Scaled (Per Minute)":
    prefix = "scaled"
elif selected_scale == "Scaled (to 40 Minutes)":
    prefix = "adjusted"

# Display mode state
if "display_mode" not in st.session_state:
    st.session_state.display_mode = "averages"

#markdown display for each user choice
st.sidebar.markdown("### **Display Options**")
if st.sidebar.button("Show Averages"):
    st.session_state.display_mode = "averages"
if st.sidebar.button("Show Season-by-Season"):
    st.session_state.display_mode = "season"
if st.sidebar.button("Show Totals"):
    st.session_state.display_mode = "totals"

############################ Filters ############################

# UI separator
st.sidebar.markdown("### **_________ Filter Options ___________**")

# Add full_name column
if "First Name" in df.columns and "Family Name" in df.columns:
    df["full_name"] = df["First Name"] + " " + df["Family Name"]

# Player search
search_term = st.sidebar.text_input("Search Player Name")
if search_term:
    df = df[df["full_name"].str.contains(search_term, case=False, na=False)]

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
        st.warning("Warning: The dataset is quite large. Highlighting may cause performance issues. Consider narrowing your filter criteria or the dataset size.")

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
#coloumns to keep
info_columns = [
    "First Name", "Family Name", "Club Name", "Competition Name",
    "Equivalent Competition", "Level", "Gender", "Season", "GP"
]
#coloumns to do compututations
stat_suffixes = [
    "MIN", "PTS", "DR", "OR", "REB", "AST", "STL", "BLK", "BLKON",
    "FOUL", "FOULON", "TO", "FGM", "FGA", "2PM", "2PA", "3PM", "3PA", "FTM", "FTA"
]
selected_columns = [f"{prefix}{s}" if prefix else s for s in stat_suffixes]
existing_selected_columns = [col for col in selected_columns if col in df.columns]
missing_columns = [col for col in selected_columns if col not in df.columns]

if missing_columns:
    st.warning(f"Missing columns for this scale: {missing_columns}")

if len(existing_selected_columns) == 0:
    st.warning("No matching stat columns found to display.")
else:
    if st.session_state.display_mode == "averages":
        avg_stats = df.groupby("full_name")[existing_selected_columns].mean()
        first_info = df.groupby("full_name")[info_columns].first()
        result = avg_stats.join(first_info).reset_index()
        final_columns = ["full_name"] + info_columns + existing_selected_columns

        st.write(f"### Player Averaged Stats ({selected_scale})")
        if highlight_mode == "Yes":
            st.dataframe(result[final_columns].style.apply(highlight_filtered_rows, axis=1))
        else:
            st.dataframe(result[final_columns])

    elif st.session_state.display_mode == "totals":
        total_stats = df.groupby("full_name")[existing_selected_columns].sum()
        first_info = df.groupby("full_name")[info_columns].first()
        result = total_stats.join(first_info).reset_index()
        final_columns = ["full_name"] + info_columns + existing_selected_columns

        st.write(f"### Player Total Stats ({selected_scale})")
        if highlight_mode == "Yes":
            st.dataframe(result[final_columns].style.apply(highlight_filtered_rows, axis=1))
        else:
            st.dataframe(result[final_columns])

    else:  # season-by-season
        display_columns = info_columns + existing_selected_columns
        st.write(f"### Player Season Stats ({selected_scale})")
        if highlight_mode == "Yes":
            st.dataframe(df[display_columns].style.apply(highlight_filtered_rows, axis=1))
        else:
            st.dataframe(df[display_columns])
