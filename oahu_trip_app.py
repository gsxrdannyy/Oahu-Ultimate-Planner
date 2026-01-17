import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Oahu Ultimate Planner", page_icon="🌺", layout="centered")

# --- 1. SETUP DATA ---
zones = ['Waikiki', 'Airport', 'West', 'Haleiwa', 'Waimea', 'Kahuku', 'Kualoa', 'Kaneohe', 'Kailua', 'Waimanalo', 'HawaiiKai']

# Travel Time Matrix (Minutes)
time_df = pd.DataFrame([
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

# Distance Matrix (Miles)
dist_df = pd.DataFrame([
    [2,  9,  25, 30, 35, 40, 22, 12, 15, 18, 10], # Waikiki
    [9,  0,  18, 25, 30, 38, 20, 12, 18, 22, 18], # Airport
    [25, 18, 0,  25, 30, 40, 35, 28, 32, 38, 35], # West
    [30, 25, 25, 0,  5,  12, 22, 30, 35, 42, 50], # Haleiwa
    [35, 30, 30, 5,  0,  8,  18, 35, 40, 48, 55], # Waimea
    [40, 38, 40, 12, 8,  0,  12, 25, 30, 38, 50], # Kahuku
    [22, 20, 35, 22, 18, 12, 0,  10, 18, 25, 35], # Kualoa
    [12, 12, 28, 30, 35, 25, 10, 0,  8,  15, 20], # Kaneohe
    [15, 18, 32, 35, 40, 30, 18, 8,  0,  6,  15], # Kailua
    [18, 22, 38, 42, 48, 38, 25, 15, 6,  0,  8],  # Waimanalo
    [10, 18, 35, 50, 55, 50, 35, 20, 15, 8,  0]   # HawaiiKai
], index=zones, columns=zones)

# Master Database
data = [
    {"Cat": "Act", "Name": "Hotel: Hyatt Place (Rest)", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": "https://www.hyatt.com"},
    {"Cat": "Act", "Name": "Start: Depart Hotel", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Travel: Flight to Oahu", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Travel: Flight Home", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Relax: Waikiki Beach", "Zone": "Waikiki", "GPS": "Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Swim: Ala Moana Beach", "Zone": "Waikiki", "GPS": "Ala Moana Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Hike: Diamond Head", "Zone": "Waikiki", "GPS": "Diamond Head State Monument", "Adult": 10, "Child": 0, "Link": "https://gostateparks.hawaii.gov/diamondhead"},
    {"Cat": "Act", "Name": "Kualoa: Jurassic Adv", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 150, "Child": 75, "Link": "https://www.kualoa.com"},
    {"Cat": "Act", "Name": "Snorkel: Hanauma Bay", "Zone": "HawaiiKai", "GPS": "Hanauma Bay", "Adult": 25, "Child": 0, "Link": "https://pros9.hnl.info/"},
    {"Cat": "Act", "Name": "Adventure: Waimea Bay", "Zone": "Waimea", "GPS": "Waimea Bay Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Beach: Lanikai Beach", "Zone": "Kailua", "GPS": "Lanikai Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Explore: Dole Plantation", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 7, "Link": "https://doleplantation.com"},
    {"Cat": "Act", "Name": "Snorkel: Kuilima Cove", "Zone": "Kahuku", "GPS": "Kuilima Cove", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Snorkel: Shark's Cove", "Zone": "Waimea", "GPS": "Shark's Cove", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Sunset: Ko Olina Lagoons", "Zone": "West", "GPS": "Ko Olina Lagoons", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Hike: Lanikai Pillbox", "Zone": "Kailua", "GPS": "Lanikai Pillbox", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Beach: Kailua Beach Park", "Zone": "Kailua", "GPS": "Kailua Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Beach: Ka'a'awa Beach", "Zone": "Kualoa", "GPS": "Kaaawa Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Beach: Waimanalo Bay", "Zone": "Waimanalo", "GPS": "Waimanalo Bay Beach Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Beach: Makapu'u Tidepools", "Zone": "Waimanalo", "GPS": "Makapuu Tidepools", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Kualoa: UTV Raptor", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 165, "Child": 75, "Link": ""},
    {"Cat": "Act", "Name": "Park: Kualoa Regional", "Zone": "Kualoa", "GPS": "Kualoa Regional Park", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Garden: Ho'omaluhia", "Zone": "Kaneohe", "GPS": "Hoomaluhia Botanical Garden", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Lookout: Halona Blowhole", "Zone": "HawaiiKai", "GPS": "Halona Blowhole Lookout", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Statue: King Kamehameha", "Zone": "Waikiki", "GPS": "King Kamehameha Statue", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Hike: Waimea Falls", "Zone": "Waimea", "GPS": "Waimea Valley", "Adult": 25, "Child": 14, "Link": ""},
    {"Cat": "Act", "Name": "Culture: Byodo-In Temple", "Zone": "Kaneohe", "GPS": "Byodo-In Temple", "Adult": 5, "Child": 3, "Link": ""},
    {"Cat": "Act", "Name": "Museum: Bishop Museum", "Zone": "Waikiki", "GPS": "Bishop Museum", "Adult": 25, "Child": 15, "Link": ""},
    {"Cat": "Act", "Name": "Zoo: Honolulu Zoo", "Zone": "Waikiki", "GPS": "Honolulu Zoo", "Adult": 19, "Child": 11, "Link": ""},
    {"Cat": "Act", "Name": "Show: Free Hula Show", "Zone": "Waikiki", "GPS": "Kuhio Beach Hula Mound", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "Night: Stargazing", "Zone": "Haleiwa", "GPS": "Waialua", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Act", "Name": "(Select Activity)", "Zone": "Waikiki", "GPS": "Waikiki", "Adult": 0, "Child": 0, "Link": ""},
    
    {"Cat": "Food", "Name": "Breakfast: Hotel Buffet", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": ""},
    {"Cat": "Food", "Name": "Breakfast: Leonard's Bakery", "Zone": "Waikiki", "GPS": "Leonard's Bakery", "Adult": 10, "Child": 10, "Link": ""},
    {"Cat": "Food", "Name": "Breakfast: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 29, "Child": 16, "Link": "https://www.dukeswaikiki.com"},
    {"Cat": "Food", "Name": "Breakfast: Eggs 'n Things", "Zone": "Waikiki", "GPS": "Eggs 'n Things Saratoga", "Adult": 25, "Child": 15, "Link": "https://eggsnthings.com"},
    {"Cat": "Food", "Name": "Breakfast: Musubi Cafe Iyasume", "Zone": "Waikiki", "GPS": "Musubi Cafe Iyasume", "Adult": 8, "Child": 8, "Link": ""},
    {"Cat": "Food", "Name": "Breakfast: Kono's North Shore", "Zone": "Haleiwa", "GPS": "Kono's North Shore", "Adult": 18, "Child": 18, "Link": "https://www.konosnorthshore.com"},
    {"Cat": "Food", "Name": "Breakfast: Liliha Bakery", "Zone": "Waikiki", "GPS": "Liliha Bakery", "Adult": 22, "Child": 15, "Link": "https://www.lilihabakery.com"},
    {"Cat": "Food", "Name": "Breakfast: Cinnamon's (Ilikai)", "Zone": "Waikiki", "GPS": "Cinnmaon's at the Ilikai", "Adult": 25, "Child": 15, "Link": "https://cinnamons808.com"},
    {"Cat": "Food", "Name": "Lunch: McDonald's (Kaneohe)", "Zone": "Kaneohe", "GPS": "McDonald's Kaneohe", "Adult": 12, "Child": 10, "Link": ""},
    {"Cat": "Food", "Name": "Lunch: Giovanni's Shrimp Truck", "Zone": "Kahuku", "GPS": "Giovanni's Shrimp Truck", "Adult": 20, "Child": 15, "Link": "https://giovannisshrimptruck.com"},
    {"Cat": "Food", "Name": "Lunch: Seven Brothers Burgers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Link": "https://www.sevenbrothersburgers.com"},
    {"Cat": "Food", "Name": "Dinner: Hale Koa Luau", "Zone": "Waikiki", "GPS": "Hale Koa Hotel", "Adult": 86, "Child": 45, "Link": "https://www.halekoa.com"},
    {"Cat": "Food", "Name": "Dinner: Paradise Cove Luau", "Zone": "West", "GPS": "Paradise Cove Luau", "Adult": 140, "Child": 110, "Link": "https://www.paradisecove.com"},
    {"Cat": "Food", "Name": "Dinner: Chief's Luau", "Zone": "West", "GPS": "Chief's Luau", "Adult": 155, "Child": 135, "Link": "https://www.chiefsluau.com"},
    {"Cat": "Food", "Name": "Dinner: Toa Luau", "Zone": "Waimea", "GPS": "Toa Luau", "Adult": 135, "Child": 105, "Link": "https://www.toaluau.com"},
    {"Cat": "Food", "Name": "Dinner: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 50, "Child": 25, "Link": "https://www.dukeswaikiki.com"},
    {"Cat": "Food", "Name": "Dinner: Yard House", "Zone": "Waikiki", "GPS": "Yard House Waikiki", "Adult": 40, "Child": 20, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Marukame Udon", "Zone": "Waikiki", "GPS": "Marukame Udon Waikiki", "Adult": 18, "Child": 12, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Rainbow Drive-In", "Zone": "Waikiki", "GPS": "Rainbow Drive-In", "Adult": 18, "Child": 14, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Maui Brewing Co.", "Zone": "Waikiki", "GPS": "Maui Brewing Co Waikiki", "Adult": 35, "Child": 18, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Paia Fish Market", "Zone": "Waikiki", "GPS": "Paia Fish Market Waikiki", "Adult": 28, "Child": 18, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Cheesecake Factory", "Zone": "Waikiki", "GPS": "The Cheesecake Factory Honolulu", "Adult": 35, "Child": 18, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Zippy's", "Zone": "Waikiki", "GPS": "Zippy's Kapahulu", "Adult": 20, "Child": 14, "Link": ""},
    {"Cat": "Food", "Name": "Snack: Matsumoto Shave Ice", "Zone": "Haleiwa", "GPS": "Matsumoto Shave Ice", "Adult": 8, "Child": 8, "Link": ""},
    {"Cat": "Food", "Name": "Snack: Dole Whip", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 9, "Link": ""},
    {"Cat": "Food", "Name": "Dinner: Seven Brothers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Link": ""}
]
df = pd.DataFrame(data)

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Trip Settings")
adults = st.sidebar.number_input("Adults", 1, 10, 2)
kids = st.sidebar.number_input("Kids", 0, 10, 3)
base_cost = st.sidebar.number_input("Fixed Package (Air/Hotel/Car)", value=5344)

# --- 3. MAIN APP INTERFACE ---
st.title("🌺 Oahu Trip App")
st.caption("Live GPS • Split Budget • 11 Zones")

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

# Trackers
total_food_fun = 0
prev_zone = "Waikiki"
slot_counter = 0

for day, slots in days:
    st.markdown(f"### 📅 {day}")
    
    for slot_name in slots:
        # Determine default value
        def_val = defaults[slot_counter] if slot_counter < len(defaults) else data[0]['Name']
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
        
        # Calc Cost (Variable only)
        cost = (row['Adult'] * adults) + (row['Child'] * kids)
        total_food_fun += cost
        
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

# --- 4. TOTALS (SPLIT VIEW) ---
st.header("💰 Trip Budget")

col1, col2, col3 = st.columns(3)

grand_total = base_cost + total_food_fun

with col1:
    st.metric("Food & Fun", f"${total_food_fun:,.0f}", help="Combined Meals & Activities")

with col2:
    st.metric("Package", f"${base_cost:,.0f}", help="Fixed Cost: Flight/Hotel/Car")

with col3:
    st.metric("Grand Total", f"${grand_total:,.0f}", delta="Final")
