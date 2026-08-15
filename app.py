import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ⚙️ Page Configuration
st.set_page_config(page_title="Matthew Ryan's Travel Tracker", layout="wide")
st.title("🌍 Matthew Ryan's Travel Tracker")

# 💾 Initialize Session State (acts as our database for the session)
if 'world_data' not in st.session_state:
    st.session_state['world_data'] = pd.DataFrame(columns=['Country', 'Date Visited', 'Notes'])

if 'us_data' not in st.session_state:
    st.session_state['us_data'] = pd.DataFrame(columns=['State Name', 'State Code', 'Date Visited', 'Notes'])

# 🗂️ Create Tabs for World and U.S. tracking
tab1, tab2 = st.tabs(["🌎 Rest of the World", "🇺🇸 United States"])

# ==========================================
# 🌎 TAB 1: REST OF THE WORLD
# ==========================================
with tab1:
    st.header("World Travels")
    
    # 📝 Input Form
    with st.form("world_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            country = st.text_input("Country (e.g., Japan, France)")
        with col2:
            date_vis = st.date_input("Date Visited")
        with col3:
            notes = st.text_input("Notes / Memories")
        
        submit_world = st.form_submit_button("➕ Add Country")
        
        if submit_world and country:
            new_row = pd.DataFrame([{'Country': country, 'Date Visited': date_vis, 'Notes': notes}])
            st.session_state['world_data'] = pd.concat([st.session_state['world_data'], new_row], ignore_index=True)
            st.success(f"Added {country} to your map!")

    # 📊 Metrics
    total_countries = len(st.session_state['world_data']['Country'].unique())
    percent_world = (total_countries / 195) * 100
    st.metric(label="Total Countries Visited", value=f"{total_countries} / 195", delta=f"{percent_world:.2f}% of the World")
    
    # 🗺️ Shaded Map
    if not st.session_state['world_data'].empty:
        fig_world = px.choropleth(
            st.session_state['world_data'],
            locations="Country",
            locationmode="country names",
            color="Country",
            hover_name="Country",
            hover_data=["Date Visited", "Notes"],
            scope="world",
            title="Countries Visited"
        )
        st.plotly_chart(fig_world, use_container_width=True)
    
    # ✏️ Editable Data Table
    st.subheader("Manage Your Entries")
    st.info("💡 You can edit or delete rows directly in the table below.")
    edited_world = st.data_editor(st.session_state['world_data'], num_rows="dynamic", key="world_editor")
    st.session_state['world_data'] = edited_world

# ==========================================
# 🇺🇸 TAB 2: UNITED STATES
# ==========================================
with tab2:
    st.header("U.S. Travels")
    
    # 📝 Input Form
    with st.form("us_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            state_name = st.text_input("State Name (e.g., New York)")
        with col2:
            state_code = st.text_input("State Code (e.g., NY)")
        with col3:
            date_vis_us = st.date_input("Date Visited")
        with col4:
            notes_us = st.text_input("Notes / Memories")
            
        submit_us = st.form_submit_button("➕ Add State")
        
        if submit_us and state_name and state_code:
            new_row_us = pd.DataFrame([{
                'State Name': state_name, 
                'State Code': state_code.upper(), 
                'Date Visited': date_vis_us, 
                'Notes': notes_us
            }])
            st.session_state['us_data'] = pd.concat([st.session_state['us_data'], new_row_us], ignore_index=True)
            st.success(f"Added {state_name} to your map!")

    # 📊 Metrics
    total_states = len(st.session_state['us_data']['State Name'].unique())
    percent_us = (total_states / 50) * 100
    st.metric(label="Total States Visited", value=f"{total_states} / 50", delta=f"{percent_us:.2f}% of the U.S.")
    
    # 🗺️ Shaded Map
    if not st.session_state['us_data'].empty:
        fig_us = px.choropleth(
            st.session_state['us_data'],
            locations="State Code",
            locationmode="USA-states",
            color="State Name",
            hover_name="State Name",
            hover_data=["Date Visited", "Notes"],
            scope="usa",
            title="U.S. States Visited"
        )
        st.plotly_chart(fig_us, use_container_width=True)
        
    # ✏️ Editable Data Table
    st.subheader("Manage Your Entries")
    st.info("💡 You can edit or delete rows directly in the table below.")
    edited_us = st.data_editor(st.session_state['us_data'], num_rows="dynamic", key="us_editor")
    st.session_state['us_data'] = edited_us