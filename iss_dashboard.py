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

# --- API Functions with Fallback ---

@st.cache_data(ttl=60)
def get_iss_position():
    """Fetches the current position of the ISS with multiple API fallbacks."""
    apis = [
        "http://api.open-notify.org/iss-now.json",
        "https://api.wheretheiss.at/v1/satellites/25544",
        "https://api.n2yo.com/rest/v1/satellite/positions/25544/0/0/0/1/&apiKey=demo"
    ]
    
    for api_url in apis:
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Handle different API response formats
            if api_url.startswith("http://api.open-notify.org"):
                if data.get('message') == 'success':
                    lat = float(data['iss_position']['latitude'])
                    lon = float(data['iss_position']['longitude'])
                    return lat, lon
            elif api_url.startswith("https://api.wheretheiss.at"):
                lat = float(data['latitude'])
                lon = float(data['longitude'])
                return lat, lon
                
        except requests.exceptions.RequestException as e:
            st.warning(f"API {api_url} failed: {e}")
            continue
        except (KeyError, ValueError) as e:
            st.warning(f"Invalid response from {api_url}: {e}")
            continue
    
    # If all APIs fail, return demo coordinates
    st.error("All ISS position APIs are unavailable. Showing demo position.")
    return 28.6139, 77.2090  # Demo coordinates (Delhi, India)

@st.cache_data(ttl=3600)
def get_astronauts():
    """Fetches the list of astronauts with fallback data."""
    try:
        response = requests.get("http://api.open-notify.org/astros.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('message') == 'success':
            return data['number'], data['people']
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching astronaut data: {e}")
        
    # Fallback demo data
    st.info("Using demo astronaut data due to API unavailability.")
    demo_astronauts = [
        {"name": "Demo Astronaut 1", "craft": "ISS"},
        {"name": "Demo Astronaut 2", "craft": "ISS"},
        {"name": "Demo Astronaut 3", "craft": "ISS"}
    ]
    return len(demo_astronauts), demo_astronauts

# --- Dashboard UI ---

st.title("🛰️ Real-Time ISS Dashboard")
st.markdown("This dashboard tracks the International Space Station's current position and crew.")

# Add network status indicator
with st.container():
    try:
        test_response = requests.get("https://httpbin.org/status/200", timeout=3)
        if test_response.status_code == 200:
            st.success("✅ Network connection active")
        else:
            st.warning("⚠️ Network issues detected")
    except:
        st.error("❌ No internet connection - Try refreshing or check your internet connection")

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
        m = folium.Map(location=[lat, lon], zoom_start=3)
        tooltip = f"ISS Position: ({lat:.2f}, {lon:.2f})"
        folium.Marker(
            [lat, lon], 
            popup=f"<b>ISS</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}", 
            tooltip=tooltip,
            icon=folium.Icon(icon='rocket', prefix='fa', color='red')
        ).add_to(m)
        st_folium(m, use_container_width=True, height=500)
    else:
        st.warning("Could not display map. Position data is unavailable.")

with info_col:
    st.header("👨‍🚀 Current Crew")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    if astros_list:
        df = pd.DataFrame(astros_list)
        df.rename(columns={'name': 'Name', 'craft': 'Spacecraft'}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, height=None)
    else:
        st.info("Astronaut data is currently unavailable.")


# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='display: flex; flex-direction: row; justify-content: space-between; color: #888; font-size: 0.8em; padding: 10px;'>"
    "<p>Made by Soumitra Kumar</p>"
    "<p>Network issues? Try refreshing or check your internet connection</p>"
    "</div>",
    unsafe_allow_html=True
)
