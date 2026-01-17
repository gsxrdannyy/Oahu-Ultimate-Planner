import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Oahu Ultimate Planner", page_icon="🌺", layout="centered")

# --- STEP 1: DATA SETUP ---
zones = ['Waikiki', 'Airport', 'West', 'Haleiwa', 'Waimea', 'Kahuku', 'Kualoa', 'Kaneohe', 'Kailua', 'Waimanalo', 'HawaiiKai']

# Travel Matrices (From v28)
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

dist_matrix = pd.DataFrame([
    [2,  9,  25, 30, 35, 40, 22, 12, 15, 18, 10],
    [9,  0,  18, 25, 30, 38, 20, 12, 18, 22, 18],
    [25, 18, 0,  25, 30, 40, 35, 28, 32, 38, 35],
    [30, 25, 25, 0,  5,  12, 22, 30, 35, 42, 50],
    [35, 30, 30, 5,  0,  8,  18, 35, 40, 48, 55],
    [40, 38, 40, 12, 8,  0,  12, 25, 30, 38, 50],
    [22, 20, 35, 22, 18, 12, 0,  10, 18, 25, 35],
    [12, 12, 28, 30, 35, 25, 10, 0,  8,  15, 20],
    [15, 18, 32, 35, 40, 30, 18, 8,  0,  6,  15],
    [18, 22, 38, 42, 48, 38, 25, 15, 6,  0,  8],
    [10, 18, 35, 50, 55, 50, 35, 20, 15, 8,  0]
], index=zones, columns=zones)

# Master Database (Food + Activities)
data_source = [
    # FOOD
    {"Cat": "Food", "Name": "Breakfast: Hotel Buffet", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "Free"},
    {"Cat": "Food", "Name": "Breakfast: Duke's Waikiki", "Zone": "Waikiki", "Link": "https://www.dukeswaikiki.com", "Adult": 29, "Child": 16, "Note": "Oceanfront"},
    {"Cat": "Food", "Name": "Breakfast: Leonard's Bakery", "Zone": "Waikiki", "Link": "https://www.leonardshawaii.com", "Adult": 10, "Child": 10, "Note": "Malasadas"},
    {"Cat": "Food", "Name": "Breakfast: Eggs 'n Things", "Zone": "Waikiki", "Link": "https://eggsnthings.com", "Adult": 25, "Child": 15, "Note": "Pancakes"},
    {"Cat": "Food", "Name": "Breakfast: Musubi Cafe Iyasume", "Zone": "Waikiki", "Link": "https://iyasumehawaii.com", "Adult": 8, "Child": 8, "Note": "Musubis"},
    {"Cat": "Food", "Name": "Breakfast: Kono's North Shore", "Zone": "Haleiwa", "Link": "https://www.konosnorthshore.com", "Adult": 18, "Child": 18, "Note": "Burritos"},
    {"Cat": "Food", "Name": "Breakfast: Liliha Bakery", "Zone": "Waikiki", "Link": "https://www.lilihabakery.com", "Adult": 22, "Child": 15, "Note": "Coco Puffs"},
    {"Cat": "Food", "Name": "Breakfast: Cinnamon's (Ilikai)", "Zone": "Waikiki", "Link": "https://cinnamons808.com", "Adult": 25, "Child": 15, "Note": "Guava Pancakes"},
    {"Cat": "Food", "Name": "Lunch: McDonald's (Kaneohe)", "Zone": "Kaneohe", "Link": "", "Adult": 12, "Child": 10, "Note": "Quick stop"},
    {"Cat": "Food", "Name": "Lunch: Giovanni's Shrimp Truck", "Zone": "Kahuku", "Link": "https://giovannisshrimptruck.com", "Adult": 20, "Child": 15, "Note": "Garlic Shrimp"},
    {"Cat": "Food", "Name": "Lunch: Seven Brothers Burgers", "Zone": "Kahuku", "Link": "https://www.sevenbrothersburgers.com", "Adult": 20, "Child": 14, "Note": "Burgers"},
    {"Cat": "Food", "Name": "Dinner: Hale Koa Luau (Mil)", "Zone": "Waikiki", "Link": "https://www.halekoa.com", "Adult": 86, "Child": 45, "Note": "Military Only"},
    {"Cat": "Food", "Name": "Dinner: Paradise Cove Luau", "Zone": "West", "Link": "https://www.paradisecove.com", "Adult": 140, "Child": 110, "Note": "Ko Olina"},
    {"Cat": "Food", "Name": "Dinner: Chief's Luau", "Zone": "West", "Link": "https://www.chiefsluau.com", "Adult": 155, "Child": 135, "Note": "Fire Knife"},
    {"Cat": "Food", "Name": "Dinner: Toa Luau", "Zone": "Waimea", "Link": "https://www.toaluau.com", "Adult": 135, "Child": 105, "Note": "Waimea Valley"},
    {"Cat": "Food", "Name": "Dinner: Duke's Waikiki", "Zone": "Waikiki", "Link": "https://www.dukeswaikiki.com", "Adult": 50, "Child": 25, "Note": "Prime Rib"},
    {"Cat": "Food", "Name": "Dinner: Yard House", "Zone": "Waikiki", "Link": "https://www.yardhouse.com", "Adult": 40, "Child": 20, "Note": "Variety"},
    {"Cat": "Food", "Name": "Dinner: Marukame Udon", "Zone": "Waikiki", "Link": "https://www.marugameudon.com", "Adult": 18, "Child": 12, "Note": "Udon"},
    {"Cat": "Food", "Name": "Dinner: Rainbow Drive-In", "Zone": "Waikiki", "Link": "https://rainbowdrivein.com", "Adult": 18, "Child": 14, "Note": "Plate Lunch"},
    {"Cat": "Food", "Name": "Dinner: Maui Brewing Co.", "Zone": "Waikiki", "Link": "https://mauibrewingco.com", "Adult": 35, "Child": 18, "Note": "Brewery"},
    {"Cat": "Food", "Name": "Dinner: Paia Fish Market", "Zone": "Waikiki", "Link": "https://paiafishmarket.com", "Adult": 28, "Child": 18, "Note": "Fresh Fish"},
    {"Cat": "Food", "Name": "Dinner: Cheesecake Factory", "Zone": "Waikiki", "Link": "https://www.thecheesecakefactory.com", "Adult": 35, "Child": 18, "Note": "Standard"},
    {"Cat": "Food", "Name": "Dinner: Zippy's", "Zone": "Waikiki", "Link": "https://www.zippys.com", "Adult": 20, "Child": 14, "Note": "Chili"},
    {"Cat": "Food", "Name": "Snack: Matsumoto Shave Ice", "Zone": "Haleiwa", "Link": "https://matsumotoshaveice.com", "Adult": 8, "Child": 8, "Note": "Shave Ice"},
    {"Cat": "Food", "Name": "Snack: Dole Whip", "Zone": "Haleiwa", "Link": "https://doleplantation.com", "Adult": 9, "Child": 9, "Note": "Pineapple"},

    # ACTIVITIES
    {"Cat": "Act", "Name": "Hotel: Hyatt Place (Rest)", "Zone": "Waikiki", "Link": "https://www.hyatt.com", "Adult": 0, "Child": 0, "Note": "Rest"},
    {"Cat": "Act", "Name": "Travel: Flight to Oahu", "Zone": "Airport", "Link": "", "Adult": 0, "Child": 0, "Note": "Arrival"},
    {"Cat": "Act", "Name": "Travel: Flight Home", "Zone": "Airport", "Link": "", "Adult": 0, "Child": 0, "Note": "Departure"},
    {"Cat": "Act", "Name": "Travel: Rental Car Pickup", "Zone": "Airport", "Link": "", "Adult": 0, "Child": 0, "Note": "Enterprise"},
    {"Cat": "Act", "Name": "Start: Depart Hotel", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "Start"},
    {"Cat": "Act", "Name": "Relax: Waikiki Beach", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "Beach"},
    {"Cat": "Act", "Name": "Swim: Ala Moana Beach", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "Calm Water"},
    {"Cat": "Act", "Name": "Snorkel: Kuilima Cove", "Zone": "Kahuku", "Link": "", "Adult": 0, "Child": 0, "Note": "Turtle Bay"},
    {"Cat": "Act", "Name": "Adventure: Waimea Bay", "Zone": "Waimea", "Link": "", "Adult": 0, "Child": 0, "Note": "Jumping Rock"},
    {"Cat": "Act", "Name": "Snorkel: Shark's Cove", "Zone": "Waimea", "Link": "", "Adult": 0, "Child": 0, "Note": "Snorkel"},
    {"Cat": "Act", "Name": "Sunset: Ko Olina Lagoons", "Zone": "West", "Link": "", "Adult": 0, "Child": 0, "Note": "Sunset"},
    {"Cat": "Act", "Name": "Hike: Lanikai Pillbox", "Zone": "Kailua", "Link": "", "Adult": 0, "Child": 0, "Note": "Hike"},
    {"Cat": "Act", "Name": "Beach: Lanikai Beach", "Zone": "Kailua", "Link": "", "Adult": 0, "Child": 0, "Note": "Soft Sand"},
    {"Cat": "Act", "Name": "Beach: Kailua Beach Park", "Zone": "Kailua", "Link": "", "Adult": 0, "Child": 0, "Note": "Beach"},
    {"Cat": "Act", "Name": "Beach: Ka'a'awa Beach", "Zone": "Kualoa", "Link": "", "Adult": 0, "Child": 0, "Note": "Scenic"},
    {"Cat": "Act", "Name": "Beach: Waimanalo Bay", "Zone": "Waimanalo", "Link": "", "Adult": 0, "Child": 0, "Note": "Bodyboarding"},
    {"Cat": "Act", "Name": "Beach: Makapu'u Tidepools", "Zone": "Waimanalo", "Link": "", "Adult": 0, "Child": 0, "Note": "Tidepools"},
    {"Cat": "Act", "Name": "Kualoa: Jurassic Adv", "Zone": "Kualoa", "Link": "https://www.kualoa.com", "Adult": 150, "Child": 75, "Note": "Valley Tour"},
    {"Cat": "Act", "Name": "Kualoa: UTV Raptor", "Zone": "Kualoa", "Link": "https://www.kualoa.com", "Adult": 165, "Child": 75, "Note": "UTV Drive"},
    {"Cat": "Act", "Name": "Park: Kualoa Regional", "Zone": "Kualoa", "Link": "", "Adult": 0, "Child": 0, "Note": "Chinaman's Hat"},
    {"Cat": "Act", "Name": "Snorkel: Hanauma Bay", "Zone": "HawaiiKai", "Link": "https://pros9.hnl.info/", "Adult": 25, "Child": 0, "Note": "Reservations!"},
    {"Cat": "Act", "Name": "Hike: Diamond Head", "Zone": "Waikiki", "Link": "https://gostateparks.hawaii.gov", "Adult": 10, "Child": 0, "Note": "Hike"},
    {"Cat": "Act", "Name": "Explore: Dole Plantation", "Zone": "Haleiwa", "Link": "https://doleplantation.com", "Adult": 9, "Child": 7, "Note": "Maze"},
    {"Cat": "Act", "Name": "Garden: Ho'omaluhia", "Zone": "Kaneohe", "Link": "", "Adult": 0, "Child": 0, "Note": "Botanical"},
    {"Cat": "Act", "Name": "Lookout: Halona Blowhole", "Zone": "HawaiiKai", "Link": "", "Adult": 0, "Child": 0, "Note": "Scenic"},
    {"Cat": "Act", "Name": "Statue: King Kamehameha", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "History"},
    {"Cat": "Act", "Name": "Hike: Waimea Falls", "Zone": "Waimea", "Link": "https://www.waimeavalley.net", "Adult": 25, "Child": 14, "Note": "Waterfall"},
    {"Cat": "Act", "Name": "Culture: Byodo-In Temple", "Zone": "Kaneohe", "Link": "https://byodo-in.com", "Adult": 5, "Child": 3, "Note": "Temple"},
    {"Cat": "Act", "Name": "Museum: Bishop Museum", "Zone": "Waikiki", "Link": "https://www.bishopmuseum.org", "Adult": 25, "Child": 15, "Note": "Museum"},
    {"Cat": "Act", "Name": "Zoo: Honolulu Zoo", "Zone": "Waikiki", "Link": "https://www.honoluluzoo.org", "Adult": 19, "Child": 11, "Note": "Zoo"},
    {"Cat": "Act", "Name": "Show: Free Hula Show", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "Free"},
    {"Cat": "Act", "Name": "Night: Stargazing", "Zone": "Haleiwa", "Link": "", "Adult": 0, "Child": 0, "Note": "Dark Skies"},
    {"Cat": "Act", "Name": "(Select Activity)", "Zone": "Waikiki", "Link": "", "Adult": 0, "Child": 0, "Note": "-"}
]
df = pd.DataFrame(data_source)

# --- SIDEBAR: SETTINGS ---
st.sidebar.header("⚙️ Trip Settings")
adults = st.sidebar.number_input("Adults", min_value=1, value=2)
kids = st.sidebar.number_input("Kids", min_value=0, value=3)
resort_fees = st.sidebar.number_input("Hotel Fees (Total)", value=430)
package_cost = st.sidebar.number_input("Package Cost (Air+Hotel)", value=4914)

st.sidebar.markdown("---")
st.sidebar.info(f"**Travel Party:** {adults + kids} people")

# --- MAIN APP ---
st.title("🌺 Oahu Ultimate Planner")
st.markdown(f"**Mon 20th - Fri 24th** | *{adults} Adults, {kids} Kids*")

# Define Schedule Structure (5 Days)
# Day 1: Mon 20
# Day 2: Tue 21
# Day 3: Wed 22
# Day 4: Thu 23
# Day 5: Fri 24

# Helper function to generate default schedule
def get_default_schedule():
    return [
        # MONDAY
        {"Day": "Mon 20", "Time": "Morning", "Label": "Travel", "Def": "Travel: Flight to Oahu"},
        {"Day": "Mon 20", "Time": "Afternoon", "Label": "Arrival", "Def": "Hotel: Hyatt Place (Rest)"},
        {"Day": "Mon 20", "Time": "Late PM", "Label": "Activity", "Def": "Relax: Waikiki Beach"},
        {"Day": "Mon 20", "Time": "Dinner", "Label": "Dinner", "Def": "Dinner: Hale Koa Luau (Mil)"},
        {"Day": "Mon 20", "Time": "Night", "Label": "Rest", "Def": "Hotel: Hyatt Place (Rest)"},
        
        # TUESDAY
        {"Day": "Tue 21", "Time": "Start", "Label": "Start", "Def": "Start: Depart Hotel"},
        {"Day": "Tue 21", "Time": "Breakfast", "Label": "Food", "Def": "Breakfast: Hotel Buffet"},
        {"Day": "Tue 21", "Time": "Morning", "Label": "Act", "Def": "Hike: Diamond Head"},
        {"Day": "Tue 21", "Time": "Afternoon", "Label": "Act", "Def": "Swim: Ala Moana Beach"},
        {"Day": "Tue 21", "Time": "Dinner", "Label": "Food", "Def": "Dinner: Yard House"},
        {"Day": "Tue 21", "Time": "Night", "Label": "Rest", "Def": "Hotel: Hyatt Place (Rest)"},

        # WEDNESDAY
        {"Day": "Wed 22", "Time": "Start", "Label": "Start", "Def": "Start: Depart Hotel"},
        {"Day": "Wed 22", "Time": "Breakfast", "Label": "Food", "Def": "Breakfast: Leonard's Bakery"},
        {"Day": "Wed 22", "Time": "Morning", "Label": "Act", "Def": "Kualoa: Jurassic Adv"},
        {"Day": "Wed 22", "Time": "Lunch", "Label": "Food", "Def": "Lunch: McDonald's (Kaneohe)"},
        {"Day": "Wed 22", "Time": "Afternoon", "Label": "Act", "Def": "Beach: Lanikai Beach"},
        {"Day": "Wed 22", "Time": "Dinner", "Label": "Food", "Def": "Dinner: Seven Brothers Burgers"},
        {"Day": "Wed 22", "Time": "Night", "Label": "Rest", "Def": "Hotel: Hyatt Place (Rest)"},

        # THURSDAY
        {"Day": "Thu 23", "Time": "Start", "Label": "Start", "Def": "Start: Depart Hotel"},
        {"Day": "Thu 23", "Time": "Breakfast", "Label": "Food", "Def": "Breakfast: Hotel Buffet"},
        {"Day": "Thu 23", "Time": "Morning", "Label": "Act", "Def": "Snorkel: Hanauma Bay"},
        {"Day": "Thu 23", "Time": "Afternoon", "Label": "Act", "Def": "Adventure: Waimea Bay"},
        {"Day": "Thu 23", "Time": "Dinner", "Label": "Food", "Def": "Dinner: Marukame Udon"},
        {"Day": "Thu 23", "Time": "Night", "Label": "Rest", "Def": "Hotel: Hyatt Place (Rest)"},

        # FRIDAY
        {"Day": "Fri 24", "Time": "Start", "Label": "Start", "Def": "Start: Depart Hotel"},
        {"Day": "Fri 24", "Time": "Breakfast", "Label": "Food", "Def": "Breakfast: Duke's Waikiki"},
        {"Day": "Fri 24", "Time": "Morning", "Label": "Act", "Def": "Relax: Waikiki Beach"},
        {"Day": "Fri 24", "Time": "Afternoon", "Label": "Travel", "Def": "Travel: Depart for Airport"},
        {"Day": "Fri 24", "Time": "Evening", "Label": "Travel", "Def": "Travel: Flight Home"}
    ]

schedule = get_default_schedule()
total_cost = package_cost + resort_fees
prev_zone = "Waikiki"

# --- DISPLAY LOOP ---
current_day_header = ""

for i, slot in enumerate(schedule):
    # Header logic
    if slot['Day'] != current_day_header:
        st.markdown(f"## 📅 {slot['Day']}")
        current_day_header = slot['Day']
        prev_zone = "Waikiki" # Reset start of day logic usually implies hotel start, or continue from prev night
        # Actually, for accurate drive times, we usually track Zone continuously. 
        # But for 'Start of Day', we assume starting from Hotel (Waikiki).
    
    st.markdown(f"**{slot['Time']}**")
    
    # 1. Selection
    # Filter based on broad type if needed, or show all
    # Just show all sorted by Name for ease
    all_options = df['Name'].tolist()
    
    # Defaults
    def_index = 0
    if slot['Def'] in all_options:
        def_index = all_options.index(slot['Def'])
        
    selected_name = st.selectbox(f"Select Activity ({slot['Time']})", all_options, index=def_index, key=i, label_visibility="collapsed")
    
    # 2. Get Data
    row = df[df['Name'] == selected_name].iloc[0]
    curr_zone = row['Zone']
    
    # 3. Travel Logic
    # If "Start: Depart Hotel", force prev_zone to Waikiki (Hotel)
    if "Start:" in selected_name:
        prev_zone = "Waikiki"
    
    drive_time = time_matrix.loc[prev_zone, curr_zone]
    drive_dist = dist_matrix.loc[prev_zone, curr_zone]
    
    # 4. Cost Logic
    slot_cost = (row['Adult'] * adults) + (row['Child'] * kids)
    total_cost += slot_cost
    
    # 5. UI Columns
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    
    with c1:
        st.write(f"📍 **{curr_zone}**")
        if row['Note'] != "-":
            st.caption(f"📝 {row['Note']}")
            
    with c2:
        if drive_time > 0:
            st.warning(f"🚗 {drive_time} min ({drive_dist} mi)")
        else:
            st.success("🚶 Nearby / No Travel")
            
    with c3:
        if slot_cost > 0:
            st.write(f"💵 **${slot_cost}**")
        else:
            st.write("Free / Prepaid")
            
    with c4:
        if row['Link']:
            st.link_button("🌐 Link", row['Link'])
            
    st.divider()
    prev_zone = curr_zone # Update for next leg

# --- FOOTER TOTALS ---
st.header("💰 Final Summary")
c_a, c_b, c_c = st.columns(3)
c_a.metric("Grand Total", f"${total_cost:,.2f}")
c_b.metric("Hotel/Air/Fees", f"${package_cost + resort_fees:,.2f}")
c_c.metric("Food/Activities", f"${total_cost - (package_cost + resort_fees):,.2f}")