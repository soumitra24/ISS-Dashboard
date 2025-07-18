import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import time

# Set page configuration
st.set_page_config(
    page_title="ISS Real-Time Dashboard",
    page_icon="🛰️",
    layout="wide"
)

# --- API Functions ---

@st.cache_data(ttl=60) # Cache data for 60 seconds
def get_iss_position():
    """Fetches the current position of the ISS from Open-Notify API."""
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['message'] == 'success':
            lat = float(data['iss_position']['latitude'])
            lon = float(data['iss_position']['longitude'])
            return lat, lon
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching ISS position: {e}")
        return None, None
    return None, None

@st.cache_data(ttl=3600) # Cache for 1 hour
def get_astronauts():
    """Fetches the list of astronauts currently in space."""
    try:
        response = requests.get("http://api.open-notify.org/astros.json", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['message'] == 'success':
            return data['number'], data['people']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching astronaut data: {e}")
        return 0, []
    return 0, []

# --- Dashboard UI ---

st.title("🛰️ Real-Time ISS Dashboard")
st.markdown("This dashboard tracks the International Space Station's current position and crew.")

# --- Live Data Metrics ---
lat, lon = get_iss_position()
num_astros, astros_list = get_astronauts()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Latitude", f"{lat:.4f}°" if lat is not None else "N/A")
with col2:
    st.metric("Longitude", f"{lon:.4f}°" if lon is not None else "N/A")
with col3:
    st.metric("Astronauts Onboard", num_astros)

# --- Main Layout with Map and Info ---
map_col, info_col = st.columns([2, 1])

with map_col:
    st.header("Live Ground Track")
    if lat is not None and lon is not None:
        # Create a Folium map centered on the ISS
        m = folium.Map(location=[lat, lon], zoom_start=3)

        # Add a marker for the ISS
        tooltip = f"ISS Position: ({lat:.2f}, {lon:.2f})"
        folium.Marker(
            [lat, lon], 
            popup=f"<b>ISS</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}", 
            tooltip=tooltip,
            icon=folium.Icon(icon='rocket', prefix='fa', color='red')
        ).add_to(m)
        
        # Display the map
        st_folium(m, use_container_width=True, height=500)
    else:
        st.warning("Could not display map. Position data is unavailable.")

with info_col:
    st.header("👨‍🚀 Current Crew")
    
    # Add a manual refresh button here
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    if astros_list:
        # Create a DataFrame for better display
        df = pd.DataFrame(astros_list)
        df.rename(columns={'name': 'Name', 'craft': 'Spacecraft'}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, height=None)
    else:
        st.info("Astronaut data is currently unavailable.")

# --- Auto-refresh Settings ---
st.sidebar.title("Settings")
auto_refresh = st.sidebar.checkbox("Auto-refresh every 10 seconds", value=False)

if auto_refresh:
    # Use st.empty() placeholder for controlled refresh
    placeholder = st.empty()
    with placeholder.container():
        time.sleep(10)
        st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: left; color: #888; font-size: 0.8em; padding: 10px;'>"
    "Made by Soumitra Kumar"
    "</div>", 
    unsafe_allow_html=True
)
