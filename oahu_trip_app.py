import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oahu Ultimate Planner", page_icon="🌺", layout="centered")

# --- 1. DATA SETUP ---
zones = ['Waikiki', 'Airport', 'West', 'Haleiwa', 'Waimea', 'Kahuku', 'Kualoa', 'Kaneohe', 'Kailua', 'Waimanalo', 'HawaiiKai']

# Static Estimates (For planning reference only)
time_matrix = pd.DataFrame([
    [15, 20, 45, 50, 60, 70, 50, 30, 35, 40, 25], # Waikiki
    [20, 0,  25, 40, 50, 60, 40, 25, 30, 40, 35], # Airport
    [45, 25, 0,  40, 50, 65, 50, 45, 50, 60, 55], # West
    [50, 40, 40, 0,  15, 30, 45, 55, 60, 75, 80], # Haleiwa
    [60, 50, 50, 15, 0,  15, 35, 60, 70, 80, 90], # Waimea
    [70, 60, 65, 30, 15, 0,  20, 45, 55, 65, 80], # Kahuku
    [50, 40, 50, 45, 35, 20, 0,  25, 35, 45, 60], # Kualoa
    [30, 25, 45, 55, 60, 45, 25, 0,  20, 30, 40], # Kaneohe
    [35, 30, 50, 60, 70, 55, 35, 20, 0,  15, 30], # Kailua
    [40, 40, 60, 75, 80, 65, 45, 30, 15, 0,  15], # Waimanalo
    [25, 35, 55, 80, 90, 80, 60, 40, 30, 15, 0]   # HawaiiKai
], index=zones, columns=zones)

# Master Database with precise GPS search terms
data = [
    {"Name": "Hotel: Hyatt Place (Rest)", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": "https://www.hyatt.com"},
    {"Name": "Start: Depart Hotel", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Travel: Flight to Oahu", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Travel: Flight Home", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Relax: Waikiki Beach", "Zone": "Waikiki", "GPS": "Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Swim: Ala Moana Beach", "Zone": "Waikiki", "GPS": "Ala Moana Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Hike: Diamond Head", "Zone": "Waikiki", "GPS": "Diamond Head State Monument", "Adult": 10, "Child": 0, "Link": "https://gostateparks.hawaii.gov/diamondhead"},
    {"Name": "Kualoa: Jurassic Adv", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 150, "Child": 75, "Link": "https://www.kualoa.com"},
    {"Name": "Snorkel: Hanauma Bay", "Zone": "HawaiiKai", "GPS": "Hanauma Bay", "Adult": 25, "Child": 0, "Link": "https://pros9.hnl.info/"},
    {"Name": "Adventure: Waimea Bay", "Zone": "Waimea", "GPS": "Waimea Bay Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Beach: Lanikai Beach", "Zone": "Kailua", "GPS": "Lanikai Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Explore: Dole Plantation", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 7, "Link": "https://doleplantation.com"},
    {"Name": "Breakfast: Hotel Buffet", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Name": "Breakfast: Leonard's Bakery", "Zone": "Waikiki", "GPS": "Leonard's Bakery", "Adult": 10, "Child": 10, "Link": ""},
    {"Name": "Breakfast: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 29, "Child": 16, "Link": "https://www.dukeswaikiki.com"},
    {"Name": "Lunch: McDonald's (Kaneohe)", "Zone": "Kaneohe", "GPS": "McDonald's Kaneohe", "Adult": 12, "Child": 10, "Link": ""},
    {"Name": "Dinner: Hale Koa Luau", "Zone": "Waikiki", "GPS": "Hale Koa Hotel", "Adult": 86, "Child": 45, "Link": "https://www.halekoa.com"},
    {"Name": "Dinner: Yard House", "Zone": "Waikiki", "GPS": "Yard House Waikiki", "Adult": 40, "Child": 20, "Link": ""},
    {"Name": "Dinner: Seven Brothers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Link": ""},
    {"Name": "Dinner: Marukame Udon", "Zone": "Waikiki", "GPS": "Marukame Udon Waikiki", "Adult": 18, "Child": 12, "Link": ""}
]
df = pd.DataFrame(data)

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Trip Settings")
adults = st.sidebar.number_input("Adults", 1, 10, 2)
kids = st.sidebar.number_input("Kids", 0, 10, 3)
base_cost = st.sidebar.number_input("Fixed Costs (Hotel/Air)", value=5344)

# --- 3. MAIN APP INTERFACE ---
st.title("🌺 Oahu Trip App")
st.caption("Live GPS • Auto-Budgeting • Itinerary")

days = [
    ("Mon 20", ["Morning (Travel)", "Afternoon (Arr)", "Dinner"]),
    ("Tue 21", ["Morning", "Afternoon", "Dinner"]),
    ("Wed 22", ["Morning", "Lunch", "Afternoon", "Dinner"]),
    ("Thu 23", ["Morning", "Afternoon", "Dinner"]),
    ("Fri 24", ["Morning", "Afternoon (Depart)"])
]

defaults = [
    "Travel: Flight to Oahu", "Hotel: Hyatt Place (Rest)", "Dinner: Hale Koa Luau",
    "Hike: Diamond Head", "Swim: Ala Moana Beach", "Dinner: Yard House",
    "Kualoa: Jurassic Adv", "Lunch: McDonald's (Kaneohe)", "Beach: Lanikai Beach", "Dinner: Seven Brothers",
    "Snorkel: Hanauma Bay", "Adventure: Waimea Bay", "Dinner: Marukame Udon",
    "Relax: Waikiki Beach", "Travel: Flight Home"
]

total_cost = base_cost
prev_zone = "Waikiki"
slot_counter = 0

for day, slots in days:
    st.markdown(f"### 📅 {day}")
    
    for slot_name in slots:
        # Determine default value
        def_val = defaults[slot_counter] if slot_counter < len(defaults) else data[0]['Name']
        
        # 1. FIXED LOGIC: Get list of names and find integer index
        # This prevents the StreamlitAPIException (int64 error)
        all_options = df['Name'].tolist()
        try:
            default_idx = all_options.index(def_val)
        except ValueError:
            default_idx = 0
            
        # UI Layout
        c1, c2 = st.columns([3, 1])
        with c1:
            selected = st.selectbox(f"{slot_name}", all_options, index=default_idx, key=slot_counter, label_visibility="collapsed")
        
        # Logic
        row = df[df['Name'] == selected].iloc[0]
        curr_zone = row['Zone']
        gps_target = row['GPS'].replace(" ", "+")
        
        # Static Calc
        minutes = time_matrix.loc[prev_zone, curr_zone]
        
        # Calc Cost
        cost = (row['Adult'] * adults) + (row['Child'] * kids)
        total_cost += cost
        
        # LIVE GPS LINK
        live_map_url = f"https://www.google.com/maps/dir/?api=1&origin=?q={gps_target}+Hawaii"
        
        # Display Stats
        with c2:
            st.link_button("📍 GO", live_map_url, type="primary")

        s1, s2, s3 = st.columns(3)
        s1.caption(f"📍 {curr_zone}")
        s2.caption(f"Est. Drive: {minutes} min")
        s3.caption(f"Cost: ${cost}")
        
        prev_zone = curr_zone
        slot_counter += 1
    
    st.divider()

# --- 4. TOTALS ---
st.success(f"### 💰 Grand Total: ${total_cost:,.2f}")
