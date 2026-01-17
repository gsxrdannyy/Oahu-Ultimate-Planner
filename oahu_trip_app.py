import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Oahu Ultimate Planner", page_icon="🌺", layout="centered")

# --- 1. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        df_budget = conn.read(worksheet="Sheet1", usecols=[0, 1], ttl=0)
        budget_dict = df_budget.set_index("Category")["Amount"].to_dict()
        try:
            df_itin = conn.read(worksheet="Itinerary", usecols=[0, 1], ttl=0)
            itin_dict = df_itin.set_index("ID")["Activity"].to_dict()
        except:
            itin_dict = {}
        return budget_dict, itin_dict
    except:
        return {}, {}

def save_all(pkg_val, fun_val, itinerary_snapshot):
    budget_data = pd.DataFrame([
        {"Category": "Package", "Amount": pkg_val},
        {"Category": "FoodFun", "Amount": fun_val}
    ])
    conn.update(worksheet="Sheet1", data=budget_data)
    
    itin_data = pd.DataFrame(itinerary_snapshot, columns=["ID", "Activity"])
    conn.update(worksheet="Itinerary", data=itin_data)
    st.cache_data.clear()

# --- 2. SETUP DATA ---
zones = ['Waikiki', 'Airport', 'West', 'Haleiwa', 'Waimea', 'Kahuku', 'Kualoa', 'Kaneohe', 'Kailua', 'Waimanalo', 'HawaiiKai']

time_data = [
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
]
time_df = pd.DataFrame(time_data, index=zones, columns=zones)

# --- MASTER DATABASE (Including New Groupons) ---
data_raw = [
    # --- NEW GROUPON ACTIVITIES ---
    {
        "Cat": "Act", 
        "Name": "Snorkel: Turtle Canyon (Groupon)", 
        "Zone": "Waikiki", 
        "GPS": "Kewalo Basin Harbor", 
        "Adult": 50, "Child": 40, # Est prices, check link for exact
        "Link": "https://www.groupon.com/deals/gl-waikiki-turtle-snorkeling-2",
        "Desc": "Swim with green sea turtles on a guided boat tour."
    },
    {
        "Cat": "Act", 
        "Name": "Adventure: E-Sea Scooters (Groupon)", 
        "Zone": "Waikiki", 
        "GPS": "Kewalo Basin Harbor", 
        "Adult": 80, "Child": 80, 
        "Link": "https://www.groupon.com/deals/e-sea-diver-31",
        "Desc": "Ride electric underwater scooters; no diving experience needed."
    },
    {
        "Cat": "Act", 
        "Name": "Boat: Glass Bottom Tour (Groupon)", 
        "Zone": "Waikiki", 
        "GPS": "Kewalo Basin Harbor", 
        "Adult": 35, "Child": 25, 
        "Link": "https://www.groupon.com/deals/hawaii-glass-bottom-boats",
        "Desc": "View reefs and marine life through the boat's glass floor."
    },
    {
        "Cat": "Act", 
        "Name": "Tour: Dolphins & You (Groupon)", 
        "Zone": "West", # Usually departs Waianae
        "GPS": "Waianae Small Boat Harbor", 
        "Adult": 130, "Child": 100, 
        "Link": "https://www.groupon.com/deals/gl-and-you-creations-1",
        "Desc": "Boat tour to swim with wild dolphins + snorkel reef."
    },
    {
        "Cat": "Act", 
        "Name": "Tour: Iruka Dolphin Snorkel (Groupon)", 
        "Zone": "West", 
        "GPS": "Waianae Small Boat Harbor", 
        "Adult": 120, "Child": 90, 
        "Link": "https://www.groupon.com/deals/iruka-hawaii-dolphin",
        "Desc": "Morning dolphin watching and snorkeling adventure."
    },

    # --- ORIGINAL ACTIVITIES ---
    {"Cat": "Act", "Name": "Hotel: Hyatt Place (Rest)", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": "https://www.hyatt.com", "Desc": "Rest at hotel."},
    {"Cat": "Act", "Name": "Start: Depart Hotel", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": "", "Desc": "Start driving."},
    {"Cat": "Act", "Name": "Travel: Flight to Oahu", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": "", "Desc": "Flight In."},
    {"Cat": "Act", "Name": "Travel: Flight Home", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Link": "", "Desc": "Flight Out."},
    {"Cat": "Act", "Name": "Relax: Waikiki Beach", "Zone": "Waikiki", "GPS": "Waikiki Beach", "Adult": 0, "Child": 0, "Link": "", "Desc": "Free beach time."},
    {"Cat": "Act", "Name": "Swim: Ala Moana Beach", "Zone": "Waikiki", "GPS": "Ala Moana Beach Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Calm waters for kids."},
    {"Cat": "Act", "Name": "Hike: Diamond Head", "Zone": "Waikiki", "GPS": "Diamond Head State Monument", "Adult": 10, "Child": 0, "Link": "https://gostateparks.hawaii.gov/diamondhead", "Desc": "Famous crater hike."},
    {"Cat": "Act", "Name": "Kualoa: Jurassic Adv", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 150, "Child": 75, "Link": "https://www.kualoa.com", "Desc": "Movie sites tour."},
    {"Cat": "Act", "Name": "Snorkel: Hanauma Bay", "Zone": "HawaiiKai", "GPS": "Hanauma Bay", "Adult": 25, "Child": 0, "Link": "https://pros9.hnl.info/", "Desc": "Famous reef snorkel."},
    {"Cat": "Act", "Name": "Adventure: Waimea Bay", "Zone": "Waimea", "GPS": "Waimea Bay Beach Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Jumping rock & beach."},
    {"Cat": "Act", "Name": "Beach: Lanikai Beach", "Zone": "Kailua", "GPS": "Lanikai Beach", "Adult": 0, "Child": 0, "Link": "", "Desc": "White sand beach."},
    {"Cat": "Act", "Name": "Explore: Dole Plantation", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 7, "Link": "https://doleplantation.com", "Desc": "Pineapple maze & train."},
    {"Cat": "Act", "Name": "Snorkel: Kuilima Cove", "Zone": "Kahuku", "GPS": "Kuilima Cove", "Adult": 0, "Child": 0, "Link": "", "Desc": "Turtle Bay snorkeling."},
    {"Cat": "Act", "Name": "Snorkel: Shark's Cove", "Zone": "Waimea", "GPS": "Shark's Cove", "Adult": 0, "Child": 0, "Link": "", "Desc": "North Shore snorkeling."},
    {"Cat": "Act", "Name": "Sunset: Ko Olina Lagoons", "Zone": "West", "GPS": "Ko Olina Lagoons", "Adult": 0, "Child": 0, "Link": "", "Desc": "Perfect sunset spot."},
    {"Cat": "Act", "Name": "Hike: Lanikai Pillbox", "Zone": "Kailua", "GPS": "Lanikai Pillbox", "Adult": 0, "Child": 0, "Link": "", "Desc": "Scenic ridge hike."},
    {"Cat": "Act", "Name": "Beach: Kailua Beach Park", "Zone": "Kailua", "GPS": "Kailua Beach Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Beach park with amenities."},
    {"Cat": "Act", "Name": "Beach: Ka'a'awa Beach", "Zone": "Kualoa", "GPS": "Kaaawa Beach Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Narrow scenic beach."},
    {"Cat": "Act", "Name": "Beach: Waimanalo Bay", "Zone": "Waimanalo", "GPS": "Waimanalo Bay Beach Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Longest sandy beach."},
    {"Cat": "Act", "Name": "Beach: Makapu'u Tidepools", "Zone": "Waimanalo", "GPS": "Makapuu Tidepools", "Adult": 0, "Child": 0, "Link": "", "Desc": "Tidepools exploration."},
    {"Cat": "Act", "Name": "Kualoa: UTV Raptor", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 165, "Child": 75, "Link": "", "Desc": "Off-road driving tour."},
    {"Cat": "Act", "Name": "Park: Kualoa Regional", "Zone": "Kualoa", "GPS": "Kualoa Regional Park", "Adult": 0, "Child": 0, "Link": "", "Desc": "Chinaman's Hat view."},
    {"Cat": "Act", "Name": "Garden: Ho'omaluhia", "Zone": "Kaneohe", "GPS": "Hoomaluhia Botanical Garden", "Adult": 0, "Child": 0, "Link": "", "Desc": "Botanical gardens."},
    {"Cat": "Act", "Name": "Lookout: Halona Blowhole", "Zone": "HawaiiKai", "GPS": "Halona Blowhole Lookout", "Adult": 0, "Child": 0, "Link": "", "Desc": "Scenic lookout."},
    {"Cat": "Act", "Name": "Statue: King Kamehameha", "Zone": "Waikiki", "GPS": "King Kamehameha Statue", "Adult": 0, "Child": 0, "Link": "", "Desc": "Historic statue downtown."},
    {"Cat": "Act", "Name": "Hike: Waimea Falls", "Zone": "Waimea", "GPS": "Waimea Valley", "Adult": 25, "Child": 14, "Link": "", "Desc": "Waterfall swim & gardens."},
    {"Cat": "Act", "Name": "Culture: Byodo-In Temple", "Zone": "Kaneohe", "GPS": "Byodo-In Temple", "Adult": 5, "Child": 3, "Link": "", "Desc": "Japanese temple replica."},
    {"Cat": "Act", "Name": "Museum: Bishop Museum", "Zone": "Waikiki", "GPS": "Bishop Museum", "Adult": 25, "Child": 15, "Link": "", "Desc": "Hawaiian history museum."},
    {"Cat": "Act", "Name": "Zoo: Honolulu Zoo", "Zone": "Waikiki", "GPS": "Honolulu Zoo", "Adult": 19, "Child": 11, "Link": "", "Desc": "Zoo in Waikiki."},
    {"Cat": "Act", "Name": "Show: Free Hula Show", "Zone": "Waikiki", "GPS": "Kuhio Beach Hula Mound", "Adult": 0, "Child": 0, "Link": "", "Desc": "Free sunset hula."},
    {"Cat": "Act", "Name": "Night: Stargazing", "Zone": "Haleiwa", "GPS": "Waialua", "Adult": 0, "Child": 0, "Link": "", "Desc": "North shore dark skies."},
    {"Cat": "Act", "Name": "(Select Activity)", "Zone": "Waikiki", "GPS": "Waikiki", "Adult": 0, "Child": 0, "Link": "", "Desc": "-"},
    
    # --- FOOD ---
    {"Cat": "Food", "Name": "Breakfast: Hotel Buffet", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Link": "", "Desc": "Included breakfast."},
    {"Cat": "Food", "Name": "Breakfast: Leonard's Bakery", "Zone": "Waikiki", "GPS": "Leonard's Bakery", "Adult": 10, "Child": 10, "Link": "", "Desc": "Famous Malasadas."},
    {"Cat": "Food", "Name": "Breakfast: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 29, "Child": 16, "Link": "https://www.dukeswaikiki.com", "Desc": "Oceanfront buffet."},
    {"Cat": "Food", "Name": "Breakfast: Eggs 'n Things", "Zone": "Waikiki", "GPS": "Eggs 'n Things Saratoga", "Adult": 25, "Child": 15, "Link": "https://eggsnthings.com", "Desc": "Pancakes & eggs."},
    {"Cat": "Food", "Name": "Breakfast: Musubi Cafe Iyasume", "Zone": "Waikiki", "GPS": "Musubi Cafe Iyasume", "Adult": 8, "Child": 8, "Link": "", "Desc": "Quick rice balls."},
    {"Cat": "Food", "Name": "Breakfast: Kono's North Shore", "Zone": "Haleiwa", "GPS": "Kono's North Shore", "Adult": 18, "Child": 18, "Link": "https://www.konosnorthshore.com", "Desc": "Slow-roasted pork."},
    {"Cat": "Food", "Name": "Breakfast: Liliha Bakery", "Zone": "Waikiki", "GPS": "Liliha Bakery", "Adult": 22, "Child": 15, "Link": "https://www.lilihabakery.com", "Desc": "Coco puffs & diner food."},
    {"Cat": "Food", "Name": "Breakfast: Cinnamon's (Ilikai)", "Zone": "Waikiki", "GPS": "Cinnamon's at the Ilikai", "Adult": 25, "Child": 15, "Link": "https://cinnamons808.com", "Desc": "Guava chiffon pancakes."},
    {"Cat": "Food", "Name": "Lunch: McDonald's (Kaneohe)", "Zone": "Kaneohe", "GPS": "McDonald's Kaneohe", "Adult": 12, "Child": 10, "Link": "", "Desc": "Quick stop."},
    {"Cat": "Food", "Name": "Lunch: Giovanni's Shrimp Truck", "Zone": "Kahuku", "GPS": "Giovanni's Shrimp Truck", "Adult": 20, "Child": 15, "Link": "https://giovannisshrimptruck.com", "Desc": "Garlic shrimp scampi."},
    {"Cat": "Food", "Name": "Lunch: Seven Brothers Burgers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Link": "https://www.sevenbrothersburgers.com", "Desc": "Big burgers."},
    {"Cat": "Food", "Name": "Dinner: Hale Koa Luau", "Zone": "Waikiki", "GPS": "Hale Koa Hotel", "Adult": 86, "Child": 45, "Link": "https://www.halekoa.com", "Desc": "Military luau."},
    {"Cat": "Food", "Name": "Dinner: Paradise Cove Luau", "Zone": "West", "GPS": "Paradise Cove Luau", "Adult": 140, "Child": 110, "Link": "https://www.paradisecove.com", "Desc": "Oceanfront luau."},
    {"Cat": "Food", "Name": "Dinner: Chief's Luau", "Zone": "West", "GPS": "Chief's Luau", "Adult": 155, "Child": 135, "Link": "https://www.chiefsluau.com", "Desc": "Fire knife dancing."},
    {"Cat": "Food", "Name": "Dinner: Toa Luau", "Zone": "Waimea", "GPS": "Toa Luau", "Adult": 135, "Child": 105, "Link": "https://www.toaluau.com", "Desc": "Garden setting luau."},
    {"Cat": "Food", "Name": "Dinner: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 50, "Child": 25, "Link": "https://www.dukeswaikiki.com", "Desc": "Dinner on the beach."},
    {"Cat": "Food", "Name": "Dinner: Yard House", "Zone": "Waikiki", "GPS": "Yard House Waikiki", "Adult": 40, "Child": 20, "Link": "", "Desc": "American fusion."},
    {"Cat": "Food", "Name": "Dinner: Marukame Udon", "Zone": "Waikiki", "GPS": "Marukame Udon Waikiki", "Adult": 18, "Child": 12, "Link": "", "Desc": "Fresh udon noodles."},
    {"Cat": "Food", "Name": "Dinner: Rainbow Drive-In", "Zone": "Waikiki", "GPS": "Rainbow Drive-In", "Adult": 18, "Child": 14, "Link": "", "Desc": "Plate lunches."},
    {"Cat": "Food", "Name": "Dinner: Maui Brewing Co.", "Zone": "Waikiki", "GPS": "Maui Brewing Co Waikiki", "Adult": 35, "Child": 18, "Link": "", "Desc": "Local brewpub."},
    {"Cat": "Food", "Name": "Dinner: Paia Fish Market", "Zone": "Waikiki", "GPS": "Paia Fish Market Waikiki", "Adult": 28, "Child": 18, "Link": "", "Desc": "Fresh caught fish."},
    {"Cat": "Food", "Name": "Dinner: Cheesecake Factory", "Zone": "Waikiki", "GPS": "The Cheesecake Factory Honolulu", "Adult": 35, "Child": 18, "Link": "", "Desc": "Large menu."},
    {"Cat": "Food", "Name": "Dinner: Zippy's", "Zone": "Waikiki", "GPS": "Zippy's Kapahulu", "Adult": 20, "Child": 14, "Link": "", "Desc": "Local diner (Chili)."},
    {"Cat": "Food", "Name": "Snack: Matsumoto Shave Ice", "Zone": "Haleiwa", "GPS": "Matsumoto Shave Ice", "Adult": 8, "Child": 8, "Link": "", "Desc": "Famous shave ice."},
    {"Cat": "Food", "Name": "Snack: Dole Whip", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 9, "Link": "", "Desc": "Pineapple soft serve."},
    {"Cat": "Food", "Name": "Dinner: Seven Brothers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Link": "", "Desc": "Burgers & Fries."}
]
df = pd.DataFrame(data_raw)

# --- 3. LOAD DATA ---
if "data_loaded" not in st.session_state:
    st.session_state.budget_db, st.session_state.itin_db = load_data()
    st.session_state.data_loaded = True

# --- 4. SIDEBAR ---
st.sidebar.header("⚙️ Trip Settings")
adults = st.sidebar.number_input("Adults", 1, 10, 2)
kids = st.sidebar.number_input("Kids", 0, 10, 3)
base_cost = st.sidebar.number_input("Fixed Package Cost", value=5344, help="Flight + Hotel + Car")

st.sidebar.markdown("---")
st.sidebar.header("💰 Savings Tracker")

# DB Values
db_pkg = float(st.session_state.budget_db.get("Package", 5000.0))
db_fun = float(st.session_state.budget_db.get("FoodFun", 1500.0))

saved_pkg = st.sidebar.number_input("Saved for Package", value=db_pkg, step=100.0, key="pkg_input")
saved_fun = st.sidebar.number_input("Saved for Food & Fun", value=db_fun, step=50.0, key="fun_input")

st.sidebar.markdown("---")
st.sidebar.header("💾 Controls")

if st.sidebar.button("💾 Save All Changes", type="primary"):
    current_itin_snapshot = []
    for i in range(50):
        if i in st.session_state:
            current_itin_snapshot.append({"ID": i, "Activity": st.session_state[i]})
    save_all(saved_pkg, saved_fun, current_itin_snapshot)
    st.sidebar.success("Saved!")
    st.session_state.budget_db, st.session_state.itin_db = load_data()

if st.sidebar.button("↩️ Discard & Reload"):
    st.cache_data.clear()
    st.session_state.budget_db, st.session_state.itin_db = load_data()
    for k, v in st.session_state.itin_db.items():
        st.session_state[int(k)] = v
    st.rerun()

if st.sidebar.button("⚠️ Factory Reset"):
    st.session_state.itin_db = {}
    st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("🌺 Oahu Trip App")
st.caption("Live GPS • Database Connected • 11 Zones")

days = [
    ("Mon 20", ["Morning (Travel)", "Afternoon (Arr)", "Dinner"]),
    ("Tue 21", ["Morning", "Afternoon", "Dinner"]),
    ("Wed 22", ["Morning", "Lunch", "Afternoon", "Dinner"]),
    ("Thu 23", ["Morning", "Afternoon", "Dinner"]),
    ("Fri 24", ["Morning", "Afternoon (Depart)"])
]

factory_defaults = [
    "Travel: Flight to Oahu", "Hotel: Hyatt Place (Rest)", "Dinner: Hale Koa Luau",
    "Hike: Diamond Head", "Swim: Ala Moana Beach", "Dinner: Yard House",
    "Kualoa: Jurassic Adv", "Lunch: McDonald's (Kaneohe)", "Beach: Lanikai Beach", "Dinner: Seven Brothers",
    "Snorkel: Hanauma Bay", "Adventure: Waimea Bay", "Dinner: Marukame Udon",
    "Relax: Waikiki Beach", "Travel: Flight Home"
]

total_food_fun = 0
prev_zone = "Waikiki"
slot_counter = 0

for day, slots in days:
    st.markdown(f"### 📅 {day}")
    
    for slot_name in slots:
        if slot_counter in st.session_state.itin_db:
            target_val = st.session_state.itin_db[slot_counter]
        elif slot_counter < len(factory_defaults):
            target_val = factory_defaults[slot_counter]
        else:
            target_val = data_raw[0]['Name']
            
        all_options = df['Name'].tolist()
        try:
            default_idx = all_options.index(target_val)
        except ValueError:
            default_idx = 0
            
        c1, c2 = st.columns([3, 1])
        with c1:
            selected = st.selectbox(f"{slot_name}", all_options, index=default_idx, key=slot_counter, label_visibility="collapsed")
        
        row = df[df['Name'] == selected].iloc[0]
        curr_zone = row['Zone']
        gps_target = row['GPS'].replace(" ", "+")
        
        try:
            minutes = time_df.loc[prev_zone, curr_zone]
        except:
            minutes = 0
        
        cost = (row['Adult'] * adults) + (row['Child'] * kids)
        total_food_fun += cost
        live_map_url = f"https://www.google.com/maps/dir/?api=1&origin=?q={gps_target}+Hawaii"
        
        with c2:
            st.link_button("📍 GO", live_map_url, type="primary")

        # Display Note/Desc if available
        if "Desc" in row and row["Desc"] and row["Desc"] != "-":
            st.caption(f"ℹ️ {row['Desc']}")

        s1, s2, s3 = st.columns(3)
        s1.caption(f"📍 {curr_zone}")
        s2.caption(f"Est. Drive: {minutes} min")
        s3.caption(f"Cost: ${cost}")
        
        prev_zone = curr_zone
        slot_counter += 1
    
    st.divider()

# --- 6. TOTALS ---
st.header("💰 Budget Breakdown")

c1, c2 = st.columns(2)
with c1:
    st.subheader("✈️ Package")
    st.metric("Total Cost", f"${base_cost:,.0f}")
    diff_pkg = saved_pkg - base_cost
    if diff_pkg >= 0:
        st.success(f"Fully Funded! (+${diff_pkg:,.0f})")
    else:
        st.error(f"Need: ${abs(diff_pkg):,.0f}")

with c2:
    st.subheader("🍔 Food & Fun")
    st.metric("Total Cost", f"${total_food_fun:,.0f}")
    diff_fun = saved_fun - total_food_fun
    if diff_fun >= 0:
        st.success(f"Fully Funded! (+${diff_fun:,.0f})")
    else:
        st.error(f"Need: ${abs(diff_fun):,.0f}")

grand_total = base_cost + total_food_fun
grand_saved = saved_pkg + saved_fun
grand_diff = grand_saved - grand_total

st.markdown("---")
g1, g2, g3 = st.columns(3)
g1.metric("Grand Total Cost", f"${grand_total:,.0f}")
g2.metric("Total Saved", f"${grand_saved:,.0f}")
g3.metric("Total Remaining", f"${grand_diff:,.0f}", delta_color="normal")
