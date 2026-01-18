import streamlit as st
import pandas as pd
from collections import Counter
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

def wipe_itinerary_db():
    empty_data = pd.DataFrame(columns=["ID", "Activity"])
    conn.update(worksheet="Itinerary", data=empty_data)
    st.cache_data.clear()

# --- 2. SETUP DATA ---
zones = ['Waikiki', 'Airport', 'West', 'Haleiwa', 'Waimea', 'Kahuku', 'Kualoa', 'Kaneohe', 'Kailua', 'Waimanalo', 'HawaiiKai']

# Time Matrix
time_data = [
    [15, 20, 45, 50, 60, 70, 50, 30, 35, 40, 25], 
    [20, 0,  25, 40, 50, 60, 40, 25, 30, 40, 35], 
    [45, 25, 0,  40, 50, 65, 50, 45, 50, 60, 55], 
    [50, 40, 40, 0,  15, 30, 45, 55, 60, 75, 80], 
    [60, 50, 50, 15, 0,  15, 35, 60, 70, 80, 90], 
    [70, 60, 65, 30, 15, 0,  20, 45, 55, 65, 80], 
    [50, 40, 50, 45, 35, 20, 0,  25, 35, 45, 60], 
    [30, 25, 45, 55, 60, 45, 25, 0,  20, 30, 40], 
    [35, 30, 50, 60, 70, 55, 35, 20, 0,  15, 30], 
    [40, 40, 60, 75, 80, 65, 45, 30, 15, 0,  15], 
    [25, 35, 55, 80, 90, 80, 60, 40, 30, 15, 0]   
]
time_df = pd.DataFrame(time_data, index=zones, columns=zones)

# Distance Matrix (Miles)
dist_data = [
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
]
dist_df = pd.DataFrame(dist_data, index=zones, columns=zones)

# --- MASTER DATABASE (Fixed: GPS Added Back) ---
data_raw = [
    # --- TRAVEL ---
    {"Cat": "Act", "Name": "[Airport] Travel: Flight to Oahu (ELP->HNL)", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.google.com/travel/flights", "Desc": "11 hrs from El Paso.", "Time": "Any", "Dur": "11h", "Hours": "24/7"},
    {"Cat": "Act", "Name": "[Airport] Travel: Flight Home (HNL->ELP)", "Zone": "Airport", "GPS": "Daniel K Inouye International Airport", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.google.com/travel/flights", "Desc": "10 hrs to El Paso.", "Time": "Any", "Dur": "10h", "Hours": "24/7"},
    {"Cat": "Act", "Name": "[Airport] Travel: Rental Car Pickup", "Zone": "Airport", "GPS": "Enterprise Rent-A-Car", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.enterprise.com", "Desc": "Pick up vehicle.", "Time": "Any", "Dur": "1h", "Hours": "24/7"},
    
    # --- ATTRACTIONS ---
    {"Cat": "Act", "Name": "[Waimanalo] Attraction: Sea Life Park", "Zone": "Waimanalo", "GPS": "Sea Life Park Hawaii", "Adult": 60, "Child": 50, "Discount": 0.58, "Parking": 9, "Link": "https://www.sealifeparkhawaii.com/", "Desc": "Marine park.", "Time": "Day", "Dur": "3-4h", "Hours": "10am-4pm"},
    {"Cat": "Act", "Name": "[Waikiki] Attraction: Waikiki Aquarium", "Zone": "Waikiki", "GPS": "Waikiki Aquarium", "Adult": 12, "Child": 5, "Discount": 0.33, "Parking": 5, "Link": "https://www.waikikiaquarium.org/", "Desc": "Reef exhibits.", "Time": "Day", "Dur": "1-2h", "Hours": "9am-4:30pm"},

    # --- KUALOA ---
    {"Cat": "Act", "Name": "[Kualoa] Best of Kualoa (Full Day)", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 199, "Child": 149, "Discount": 0.15, "Parking": 0, "Link": "https://www.kualoa.com/packages/", "Desc": "Full Day Pkg.", "Time": "AM", "Dur": "6h", "Hours": "Starts 8:30am"},
    {"Cat": "Act", "Name": "[Kualoa] ✅ Included in Full Day Pkg", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Activity continues...", "Time": "Any", "Dur": "-", "Hours": "-"},
    {"Cat": "Act", "Name": "[Kualoa] Jurassic Adv (Tour)", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 150, "Child": 75, "Discount": 0.15, "Parking": 0, "Link": "https://www.kualoa.com/tours/", "Desc": "Premium Tour.", "Time": "Day", "Dur": "2.5h", "Hours": "8am-5pm"},
    {"Cat": "Act", "Name": "[Kualoa] UTV Raptor (Tour)", "Zone": "Kualoa", "GPS": "Kualoa Ranch", "Adult": 165, "Child": 75, "Discount": 0.15, "Parking": 0, "Link": "https://www.kualoa.com/tours/", "Desc": "Off-road.", "Time": "Day", "Dur": "2h", "Hours": "8am-5pm"},

    # --- GROUPON ---
    {"Cat": "Act", "Name": "[Waikiki] Snorkel: Turtle Canyon (Groupon)", "Zone": "Waikiki", "GPS": "Kewalo Basin Harbor", "Adult": 50, "Child": 40, "Discount": 0, "Parking": 2, "Link": "https://www.groupon.com/deals/gl-waikiki-turtle-snorkeling-2", "Desc": "Turtle snorkel.", "Time": "Day", "Dur": "2-3h", "Hours": "8am-3pm"},
    {"Cat": "Act", "Name": "[Waikiki] Adventure: E-Sea Scooters (Groupon)", "Zone": "Waikiki", "GPS": "Kewalo Basin Harbor", "Adult": 80, "Child": 80, "Discount": 0, "Parking": 2, "Link": "https://www.groupon.com/deals/e-sea-diver-31", "Desc": "Scooters.", "Time": "Day", "Dur": "2h", "Hours": "9am-2pm"},
    {"Cat": "Act", "Name": "[Waikiki] Boat: Glass Bottom Tour (Groupon)", "Zone": "Waikiki", "GPS": "Kewalo Basin Harbor", "Adult": 35, "Child": 25, "Discount": 0, "Parking": 2, "Link": "https://www.groupon.com/deals/hawaii-glass-bottom-boats", "Desc": "Glass bottom.", "Time": "Day", "Dur": "1h", "Hours": "9am-4pm"},
    {"Cat": "Act", "Name": "[West] Tour: Dolphins & You (Groupon)", "Zone": "West", "GPS": "Waianae Small Boat Harbor", "Adult": 130, "Child": 100, "Discount": 0, "Parking": 0, "Link": "https://www.groupon.com/deals/gl-and-you-creations-1", "Desc": "Swim w/ dolphins.", "Time": "AM", "Dur": "4-5h", "Hours": "Early (7am/10am)"},
    {"Cat": "Act", "Name": "[West] Tour: Iruka Dolphin Snorkel (Groupon)", "Zone": "West", "GPS": "Waianae Small Boat Harbor", "Adult": 120, "Child": 90, "Discount": 0, "Parking": 0, "Link": "https://www.groupon.com/deals/iruka-hawaii-dolphin", "Desc": "Dolphin watch.", "Time": "AM", "Dur": "3h", "Hours": "Early"},

    # --- ACTIVITIES ---
    {"Cat": "Act", "Name": "[Waikiki] Hotel: Hyatt Place (Return/Rest)", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.hyatt.com", "Desc": "Rest.", "Time": "Any", "Dur": "-", "Hours": "24/7"},
    {"Cat": "Act", "Name": "[Waikiki] Start: Depart Hotel (Hyatt Place)", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Start.", "Time": "Any", "Dur": "-", "Hours": "-"},
    {"Cat": "Act", "Name": "[Waikiki] Relax: Waikiki Beach", "Zone": "Waikiki", "GPS": "Waikiki Beach", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Beach.", "Time": "Day", "Dur": "Flex", "Hours": "Any"},
    {"Cat": "Act", "Name": "[Waikiki] Swim: Ala Moana Beach", "Zone": "Waikiki", "GPS": "Ala Moana Beach Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Beach.", "Time": "Day", "Dur": "Flex", "Hours": "Any"},
    {"Cat": "Act", "Name": "[Waikiki] Hike: Diamond Head", "Zone": "Waikiki", "GPS": "Diamond Head State Monument", "Adult": 10, "Child": 0, "Discount": 1.0, "Parking": 10, "Link": "https://gostateparks.hawaii.gov/diamondhead", "Desc": "Crater Hike.", "Time": "AM", "Dur": "1.5-2h", "Hours": "6am-4pm (Last entry 4p)"},
    {"Cat": "Act", "Name": "[HawaiiKai] Snorkel: Hanauma Bay", "Zone": "HawaiiKai", "GPS": "Hanauma Bay", "Adult": 25, "Child": 0, "Discount": 1.0, "Parking": 3, "Link": "https://pros9.hnl.info/", "Desc": "Reef Snorkel.", "Time": "AM", "Dur": "3-4h", "Hours": "6:45am-4pm (Closed Mon/Tue)"},
    {"Cat": "Act", "Name": "[Waimea] Adventure: Waimea Bay", "Zone": "Waimea", "GPS": "Waimea Bay Beach Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Jumping rock.", "Time": "Day", "Dur": "2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Kailua] Beach: Lanikai Beach", "Zone": "Kailua", "GPS": "Lanikai Beach", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "White sand.", "Time": "Day", "Dur": "2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Haleiwa] Explore: Dole Plantation", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 7, "Discount": 0.15, "Parking": 0, "Link": "https://doleplantation.com", "Desc": "Maze/Train.", "Time": "Day", "Dur": "1.5h", "Hours": "9:30am-5:30pm"},
    {"Cat": "Act", "Name": "[Kahuku] Snorkel: Kuilima Cove", "Zone": "Kahuku", "GPS": "Kuilima Cove", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://turtlebayresort.com", "Desc": "Turtle Bay.", "Time": "Day", "Dur": "1-2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Waimea] Snorkel: Shark's Cove", "Zone": "Waimea", "GPS": "Shark's Cove", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Snorkel.", "Time": "Day", "Dur": "1-2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[West] Sunset: Ko Olina Lagoons", "Zone": "West", "GPS": "Ko Olina Lagoons", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://koolina.com/", "Desc": "Sunset.", "Time": "PM", "Dur": "1h", "Hours": "Sunset"},
    {"Cat": "Act", "Name": "[Kailua] Hike: Lanikai Pillbox", "Zone": "Kailua", "GPS": "Lanikai Pillbox", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.alltrails.com/trail/hawaii/oahu/lanikai-pillbox-trail", "Desc": "Ridge Hike.", "Time": "Day", "Dur": "1-1.5h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Kailua] Beach: Kailua Beach Park", "Zone": "Kailua", "GPS": "Kailua Beach Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Beach.", "Time": "Day", "Dur": "2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Kualoa] Beach: Ka'a'awa Beach", "Zone": "Kualoa", "GPS": "Kaaawa Beach Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Beach.", "Time": "Day", "Dur": "1h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Waimanalo] Beach: Waimanalo Bay", "Zone": "Waimanalo", "GPS": "Waimanalo Bay Beach Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Beach.", "Time": "Day", "Dur": "2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Waimanalo] Beach: Makapu'u Tidepools", "Zone": "Waimanalo", "GPS": "Makapuu Tidepools", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Tidepools.", "Time": "Day", "Dur": "2h", "Hours": "Daylight"},
    {"Cat": "Act", "Name": "[Kualoa] Park: Kualoa Regional", "Zone": "Kualoa", "GPS": "Kualoa Regional Park", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "View.", "Time": "Day", "Dur": "30m", "Hours": "7am-8pm"},
    {"Cat": "Act", "Name": "[Kaneohe] Garden: Ho'omaluhia", "Zone": "Kaneohe", "GPS": "Hoomaluhia Botanical Garden", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.honolulu.gov/parks/hbg/hmbg.html", "Desc": "Botanic Garden.", "Time": "Day", "Dur": "1h", "Hours": "9am-4pm"},
    {"Cat": "Act", "Name": "[HawaiiKai] Lookout: Halona Blowhole", "Zone": "HawaiiKai", "GPS": "Halona Blowhole Lookout", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Lookout.", "Time": "Any", "Dur": "15m", "Hours": "Any"},
    {"Cat": "Act", "Name": "[Waikiki] Statue: King Kamehameha", "Zone": "Waikiki", "GPS": "King Kamehameha Statue", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Statue.", "Time": "Any", "Dur": "15m", "Hours": "Any"},
    {"Cat": "Act", "Name": "[Waimea] Hike: Waimea Falls", "Zone": "Waimea", "GPS": "Waimea Valley", "Adult": 25, "Child": 14, "Discount": 0.50, "Parking": 0, "Link": "https://www.waimeavalley.net/", "Desc": "Waterfall.", "Time": "Day", "Dur": "1.5h", "Hours": "9am-4pm"},
    {"Cat": "Act", "Name": "[Kaneohe] Culture: Byodo-In Temple", "Zone": "Kaneohe", "GPS": "Byodo-In Temple", "Adult": 5, "Child": 3, "Discount": 0, "Parking": 0, "Link": "https://byodo-in.com/", "Desc": "Temple.", "Time": "Day", "Dur": "1h", "Hours": "8:30am-4:30pm"},
    {"Cat": "Act", "Name": "[Waikiki] Museum: Bishop Museum", "Zone": "Waikiki", "GPS": "Bishop Museum", "Adult": 25, "Child": 15, "Discount": 0.20, "Parking": 5, "Link": "https://www.bishopmuseum.org/", "Desc": "History.", "Time": "Day", "Dur": "2-3h", "Hours": "9am-5pm"},
    {"Cat": "Act", "Name": "[Waikiki] Zoo: Honolulu Zoo", "Zone": "Waikiki", "GPS": "Honolulu Zoo", "Adult": 19, "Child": 11, "Discount": 0, "Parking": 6, "Link": "https://www.honoluluzoo.org/", "Desc": "Zoo.", "Time": "Day", "Dur": "2-3h", "Hours": "10am-3pm"},
    {"Cat": "Act", "Name": "[Waikiki] Show: Free Hula Show", "Zone": "Waikiki", "GPS": "Kuhio Beach Hula Mound", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.kuhiobeachhulas.com/", "Desc": "Hula.", "Time": "PM", "Dur": "1h", "Hours": "Tue/Thu/Sat 6pm"},
    {"Cat": "Act", "Name": "[Waikiki] Night: Fireworks", "Zone": "Waikiki", "GPS": "Hilton Hawaiian Village", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "https://www.hiltonhawaiianvillage.com/resort-experiences/entertainment-and-events", "Desc": "Fireworks.", "Time": "PM", "Dur": "15m", "Hours": "Fri 7:45pm"},
    {"Cat": "Act", "Name": "[Haleiwa] Night: Stargazing", "Zone": "Haleiwa", "GPS": "Waialua", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Stars.", "Time": "PM", "Dur": "Flex", "Hours": "Night"},
    {"Cat": "Act", "Name": "(Select Activity)", "Zone": "Waikiki", "GPS": "Waikiki", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "-", "Time": "Any", "Dur": "-", "Hours": "-"},
    
    # --- FOOD ---
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Hotel Buffet", "Zone": "Waikiki", "GPS": "Hyatt Place Waikiki Beach", "Adult": 0, "Child": 0, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Buffet.", "Time": "AM", "Dur": "45m", "Hours": "6am-10am"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Leonard's Bakery", "Zone": "Waikiki", "GPS": "Leonard's Bakery", "Adult": 10, "Child": 10, "Discount": 0, "Parking": 0, "Link": "https://www.leonardshawaii.com/", "Desc": "Bakery.", "Time": "AM", "Dur": "30m", "Hours": "5:30am-9pm"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 29, "Child": 16, "Discount": 0, "Parking": 6, "Link": "https://www.dukeswaikiki.com", "Desc": "Buffet.", "Time": "AM", "Dur": "1h", "Hours": "7am-11am"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Eggs 'n Things", "Zone": "Waikiki", "GPS": "Eggs 'n Things Saratoga", "Adult": 25, "Child": 15, "Discount": 0.10, "Parking": 0, "Link": "https://eggsnthings.com", "Desc": "Pancakes.", "Time": "AM", "Dur": "1h", "Hours": "6am-2pm"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Musubi Cafe Iyasume", "Zone": "Waikiki", "GPS": "Musubi Cafe Iyasume", "Adult": 8, "Child": 8, "Discount": 0, "Parking": 0, "Link": "https://iyasumehawaii.com/", "Desc": "Musubis.", "Time": "Any", "Dur": "15m", "Hours": "7am-8pm"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Liliha Bakery", "Zone": "Waikiki", "GPS": "Liliha Bakery", "Adult": 22, "Child": 15, "Discount": 0, "Parking": 0, "Link": "https://www.lilihabakery.com", "Desc": "Diner.", "Time": "Any", "Dur": "1h", "Hours": "7am-10pm"},
    {"Cat": "Food", "Name": "[Waikiki] Breakfast: Cinnamon's", "Zone": "Waikiki", "GPS": "Cinnamon's at the Ilikai", "Adult": 25, "Child": 15, "Discount": 0, "Parking": 1, "Link": "https://cinnamons808.com", "Desc": "Pancakes.", "Time": "AM", "Dur": "1h", "Hours": "7am-2pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Hale Koa Luau", "Zone": "Waikiki", "GPS": "Hale Koa Hotel", "Adult": 86, "Child": 45, "Discount": 0, "Parking": 15, "Link": "https://www.halekoa.com", "Desc": "Luau.", "Time": "PM", "Dur": "3h", "Hours": "5pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Duke's Waikiki", "Zone": "Waikiki", "GPS": "Duke's Waikiki", "Adult": 50, "Child": 25, "Discount": 0, "Parking": 6, "Link": "https://www.dukeswaikiki.com", "Desc": "Dinner.", "Time": "PM", "Dur": "1.5h", "Hours": "4:45pm-9pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Yard House", "Zone": "Waikiki", "GPS": "Yard House Waikiki", "Adult": 40, "Child": 20, "Discount": 0.10, "Parking": 0, "Link": "https://www.yardhouse.com/locations/hi/honolulu/waikiki-beach-walk/8316", "Desc": "Fusion.", "Time": "PM", "Dur": "1.5h", "Hours": "11am-1am"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Marukame Udon", "Zone": "Waikiki", "GPS": "Marukame Udon Waikiki", "Adult": 18, "Child": 12, "Discount": 0, "Parking": 0, "Link": "https://www.marugameudon.com/", "Desc": "Udon.", "Time": "PM", "Dur": "1h", "Hours": "10am-10pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Rainbow Drive-In", "Zone": "Waikiki", "GPS": "Rainbow Drive-In", "Adult": 18, "Child": 14, "Discount": 0, "Parking": 0, "Link": "https://rainbowdrivein.com/", "Desc": "Plate Lunch.", "Time": "Any", "Dur": "45m", "Hours": "7am-9pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Maui Brewing Co.", "Zone": "Waikiki", "GPS": "Maui Brewing Co Waikiki", "Adult": 35, "Child": 18, "Discount": 0, "Parking": 6, "Link": "https://mauibrewingco.com/waikiki/", "Desc": "Brewpub.", "Time": "PM", "Dur": "1.5h", "Hours": "11am-10pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Paia Fish Market", "Zone": "Waikiki", "GPS": "Paia Fish Market Waikiki", "Adult": 28, "Child": 18, "Discount": 0, "Parking": 0, "Link": "https://paiafishmarket.com/", "Desc": "Fish.", "Time": "PM", "Dur": "1h", "Hours": "10am-9:30pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Cheesecake Factory", "Zone": "Waikiki", "GPS": "The Cheesecake Factory Honolulu", "Adult": 35, "Child": 18, "Discount": 0, "Parking": 0, "Link": "https://www.thecheesecakefactory.com/locations/honolulu-hi", "Desc": "Dinner.", "Time": "PM", "Dur": "1.5h", "Hours": "11am-11pm"},
    {"Cat": "Food", "Name": "[Waikiki] Dinner: Zippy's", "Zone": "Waikiki", "GPS": "Zippy's Kapahulu", "Adult": 20, "Child": 14, "Discount": 0, "Parking": 0, "Link": "https://www.zippys.com/", "Desc": "Diner.", "Time": "Any", "Dur": "1h", "Hours": "24/7"},
    
    {"Cat": "Food", "Name": "[Haleiwa] Breakfast: Kono's", "Zone": "Haleiwa", "GPS": "Kono's North Shore", "Adult": 18, "Child": 18, "Discount": 0.10, "Parking": 0, "Link": "https://www.konosnorthshore.com", "Desc": "Pork.", "Time": "AM", "Dur": "45m", "Hours": "7am-2pm"},
    {"Cat": "Food", "Name": "[Haleiwa] Snack: Matsumoto Shave Ice", "Zone": "Haleiwa", "GPS": "Matsumoto Shave Ice", "Adult": 8, "Child": 8, "Discount": 0, "Parking": 0, "Link": "https://matsumotoshaveice.com/", "Desc": "Ice.", "Time": "Day", "Dur": "30m", "Hours": "10am-6pm"},
    {"Cat": "Food", "Name": "[Haleiwa] Snack: Dole Whip", "Zone": "Haleiwa", "GPS": "Dole Plantation", "Adult": 9, "Child": 9, "Discount": 0, "Parking": 0, "Link": "https://doleplantation.com", "Desc": "Dole Whip.", "Time": "Day", "Dur": "30m", "Hours": "9:30am-5:30pm"},
    
    {"Cat": "Food", "Name": "[Kahuku] Lunch: Giovanni's Shrimp", "Zone": "Kahuku", "GPS": "Giovanni's Shrimp Truck", "Adult": 20, "Child": 15, "Discount": 0, "Parking": 2, "Link": "https://giovannisshrimptruck.com", "Desc": "Shrimp.", "Time": "Day", "Dur": "45m", "Hours": "10:30am-6:30pm"},
    {"Cat": "Food", "Name": "[Kahuku] Dinner: Seven Brothers", "Zone": "Kahuku", "GPS": "Seven Brothers Burgers Kahuku", "Adult": 20, "Child": 14, "Discount": 0, "Parking": 0, "Link": "https://www.sevenbrothersburgers.com/", "Desc": "Burgers.", "Time": "PM", "Dur": "1h", "Hours": "11am-9pm"},
    
    {"Cat": "Food", "Name": "[Kaneohe] Lunch: McDonald's", "Zone": "Kaneohe", "GPS": "McDonald's Kaneohe", "Adult": 12, "Child": 10, "Discount": 0, "Parking": 0, "Link": "", "Desc": "Fast Food.", "Time": "Any", "Dur": "30m", "Hours": "24/7"},
    
    {"Cat": "Food", "Name": "[West] Dinner: Paradise Cove Luau", "Zone": "West", "GPS": "Paradise Cove Luau", "Adult": 140, "Child": 110, "Discount": 0.15, "Parking": 0, "Link": "https://www.paradisecove.com", "Desc": "Luau.", "Time": "PM", "Dur": "3-4h", "Hours": "5pm"},
    {"Cat": "Food", "Name": "[West] Dinner: Chief's Luau", "Zone": "West", "GPS": "Chief's Luau", "Adult": 155, "Child": 135, "Discount": 0.15, "Parking": 0, "Link": "https://www.chiefsluau.com", "Desc": "Luau.", "Time": "PM", "Dur": "3-4h", "Hours": "5pm"},
    
    {"Cat": "Food", "Name": "[Waimea] Dinner: Toa Luau", "Zone": "Waimea", "GPS": "Toa Luau", "Adult": 135, "Child": 105, "Discount": 0.15, "Parking": 0, "Link": "https://www.toaluau.com", "Desc": "Luau.", "Time": "PM", "Dur": "3h", "Hours": "5pm"}
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
st.sidebar.header("⛽ Gas Settings")
gas_price = st.sidebar.number_input("Gas Price ($/gal)", value=4.85, step=0.10)
car_mpg = st.sidebar.number_input("Car MPG", value=30, step=5)

st.sidebar.markdown("---")
st.sidebar.header("💰 Savings Tracker")

db_pkg = float(st.session_state.budget_db.get("Package", 5000.0))
db_fun = float(st.session_state.budget_db.get("FoodFun", 1500.0))

saved_pkg = st.sidebar.number_input("Saved for Package", value=db_pkg, step=100.0, key="pkg_input")
saved_fun = st.sidebar.number_input("Saved for Food & Fun", value=db_fun, step=50.0, key="fun_input")

st.sidebar.markdown("---")
st.sidebar.header("💾 Controls")

if st.sidebar.button("💾 Save All Changes", type="primary"):
    current_itin_snapshot = []
    # Save up to 50 slots
    for i in range(50):
        if i in st.session_state:
            current_itin_snapshot.append({"ID": i, "Activity": st.session_state[i]})
    save_all(saved_pkg, saved_fun, current_itin_snapshot)
    st.sidebar.success("Saved!")
    st.session_state.budget_db, st.session_state.itin_db = load_data()

# --- SWAP DAYS TOOL ---
with st.sidebar.expander("🔄 Swap Days"):
    swap_days_list = [
        "Mon 20 (Arrival)", 
        "Tue 21 (Windward Side)", 
        "Wed 22 (North Shore)", 
        "Thu 23 (West/Dolphins)", 
        "Fri 24 (Departure)"
    ]
    day_a = st.selectbox("Swap Day A", swap_days_list, key="swap_a")
    day_b = st.selectbox("With Day B", swap_days_list, key="swap_b")
    
    if st.button("Swap Itinerary"):
        day_ranges = {
            "Mon 20 (Arrival)": range(0, 5),
            "Tue 21 (Windward Side)": range(5, 13),
            "Wed 22 (North Shore)": range(13, 21),
            "Thu 23 (West/Dolphins)": range(21, 29),
            "Fri 24 (Departure)": range(29, 34)
        }
        
        range_a = day_ranges[day_a]
        range_b = day_ranges[day_b]
        
        if len(range_a) != len(range_b):
            st.error("Cannot swap days with different slot counts.")
        else:
            current_itin = {}
            for i in range(34):
                if i in st.session_state:
                    current_itin[i] = st.session_state[i]
                elif i in st.session_state.itin_db:
                    current_itin[i] = st.session_state.itin_db[i]
                elif i < len(factory_defaults):
                    current_itin[i] = factory_defaults[i]
                else:
                    current_itin[i] = data_raw[0]['Name']
            
            for idx_a, idx_b in zip(range_a, range_b):
                val_a = current_itin[idx_a]
                val_b = current_itin[idx_b]
                st.session_state.itin_db[idx_a] = val_b
                st.session_state.itin_db[idx_b] = val_a
                st.session_state[idx_a] = val_b
                st.session_state[idx_b] = val_a
            
            st.success(f"Swapped {day_a} with {day_b}! Save to permanent.")
            st.rerun()

# --- NUCLEAR OPTION (Wipe Cloud) ---
if st.sidebar.button("⚠️ Factory Reset (Wipe Cloud)"):
    st.session_state.itin_db = {}
    wipe_itinerary_db()
    st.success("Cloud data wiped! Loading Smart Defaults...")
    st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("🌺 Oahu Ultimate Planner")
st.caption("Live GPS • Smart Geographically Grouped • Veteran Savings 🪖")

days = [
    ("Mon 20 (Arrival)", ["Morning (Travel)", "Transport (Car Rental)", "Afternoon (Check-In)", "Dinner (Easy)", "End"]),
    ("Tue 21 (Windward Side)", ["Start", "Breakfast", "Morning (Temple)", "Lunch (Kaneohe)", "Afternoon (Kualoa)", "Dinner", "Night (Stargazing)", "End"]),
    ("Wed 22 (North Shore)", ["Start", "Breakfast (North)", "Morning (Waimea)", "Lunch (Shrimp)", "Afternoon (Dole)", "Dinner (North)", "Night", "End"]),
    ("Thu 23 (West/Dolphins)", ["Start", "Breakfast (Early)", "Morning (Dolphins)", "Lunch", "Afternoon (Relax)", "Dinner (Luau)", "Night", "End"]),
    ("Fri 24 (Departure)", ["Start", "Breakfast (Waikiki)", "Morning (Beach)", "Lunch (Local)", "Afternoon (Travel)"])
]

# --- SMART GEOGRAPHIC DEFAULTS (Matched to 34 Slots) ---
factory_defaults = [
    # MON
    "[Airport] Travel: Flight to Oahu (ELP->HNL)", "[Airport] Travel: Rental Car Pickup", "[Waikiki] Hotel: Hyatt Place (Return/Rest)", "[Waikiki] Dinner: Duke's Waikiki", "[Waikiki] Hotel: Hyatt Place (Return/Rest)",
    # TUE
    "[Waikiki] Start: Depart Hotel (Hyatt Place)", "[Waikiki] Breakfast: Hotel Buffet (Included)", "[Kaneohe] Culture: Byodo-In Temple", "[Kaneohe] Lunch: McDonald's", "[Kualoa] Jurassic Adv (Tour)", "[Kailua] Beach: Lanikai Beach", "[Waikiki] Dinner: Maui Brewing Co.", "[Waikiki] Hotel: Hyatt Place (Return/Rest)",
    # WED
    "[Waikiki] Start: Depart Hotel (Hyatt Place)", "[Haleiwa] Breakfast: Kono's", "[Waimea] Adventure: Waimea Bay", "[Kahuku] Lunch: Giovanni's Shrimp", "[Haleiwa] Explore: Dole Plantation", "[Waimea] Snorkel: Shark's Cove", "[Kahuku] Dinner: Seven Brothers", "[Waikiki] Hotel: Hyatt Place (Return/Rest)",
    # THU
    "[Waikiki] Start: Depart Hotel (Hyatt Place)", "[Waikiki] Breakfast: Leonard's Bakery", "[West] Tour: Dolphins & You (Groupon)", "[Kaneohe] Lunch: McDonald's", "[Waikiki] Swim: Ala Moana Beach", "[West] Dinner: Paradise Cove Luau", "[Haleiwa] Night: Stargazing", "[Waikiki] Hotel: Hyatt Place (Return/Rest)",
    # FRI
    "[Waikiki] Start: Depart Hotel (Hyatt Place)", "[Waikiki] Breakfast: Duke's Waikiki", "[Waikiki] Relax: Waikiki Beach", "[Waikiki] Dinner: Rainbow Drive-In", "[Airport] Travel: Flight Home (HNL->ELP)"
]

# --- HELPER TO CHECK DUPLICATES & TIME ---
def get_current_selections_for_dupe_check():
    current_sel = []
    temp_counter = 0
    for day_name, day_slots in days:
        for _ in day_slots:
            if temp_counter in st.session_state:
                val = st.session_state[temp_counter]
            elif temp_counter in st.session_state.itin_db:
                val = st.session_state.itin_db[temp_counter]
            elif temp_counter < len(factory_defaults):
                val = factory_defaults[temp_counter]
            else:
                val = data_raw[0]['Name']
            
            if not any(x in val for x in ["Hotel:", "Travel:", "Start:", "End:", "Included"]):
                current_sel.append(val)
            temp_counter += 1
    return current_sel

# LOGIC TO CHECK TIME CONFLICTS
def check_time_warning(activity_name, slot_name):
    try:
        act_row = df[df['Name'] == activity_name].iloc[0]
        best_time = act_row.get('Time', 'Any')
        hours = act_row.get('Hours', '-')
    except:
        return None

    is_morning = any(x in slot_name for x in ["Morning", "Breakfast", "Start"])
    is_afternoon = any(x in slot_name for x in ["Afternoon", "Lunch"])
    is_night = any(x in slot_name for x in ["Night", "Dinner"])
    
    warning = None
    if "Stargazing" in activity_name and not is_night:
        warning = f"⚠️ Better at Night (Stars visible)"
    elif best_time == "AM" and (is_afternoon or is_night):
        warning = f"⚠️ Best in Morning ({hours})"
    elif best_time == "PM" and (is_morning or is_afternoon):
        warning = f"⚠️ Evening Activity ({hours})"
    elif best_time == "Day" and is_night:
        warning = f"⚠️ Closed at Night ({hours})"
        
    return warning

all_active_acts = get_current_selections_for_dupe_check()
dupe_counts = Counter(all_active_acts)

total_food_fun = 0
total_miles = 0
prev_zone = "Waikiki"
slot_counter = 0

for day_name, slots in days:
    st.markdown(f"### 📅 {day_name}")
    
    for slot_name in slots:
        if slot_counter in st.session_state.itin_db:
            target_val = st.session_state.itin_db[slot_counter]
        elif slot_counter < len(factory_defaults):
            target_val = factory_defaults[slot_counter]
        else:
            target_val = data_raw[0]['Name']
            
        all_options = sorted(df['Name'].tolist())
        try:
            default_idx = all_options.index(target_val)
        except ValueError:
            default_idx = 0
            
        # 3 COLUMNS: SELECT, MAP, WEB
        c1, c2, c3 = st.columns([2.8, 0.6, 0.6])
        with c1:
            selected = st.selectbox(f"{slot_name}", all_options, index=default_idx, key=slot_counter, label_visibility="collapsed")
        
        row = df[df['Name'] == selected].iloc[0]
        curr_zone = row['Zone']
        gps_target = row['GPS'].replace(" ", "+")
        
        try:
            minutes = time_df.loc[prev_zone, curr_zone]
            miles = dist_df.loc[prev_zone, curr_zone]
        except:
            minutes = 0
            miles = 0
        
        discount = row.get('Discount', 0)
        parking = row.get('Parking', 0)
        
        base_price = (row['Adult'] * adults) + (row['Child'] * kids)
        discounted_price = base_price * (1 - discount)
        cost = discounted_price + parking
        
        total_food_fun += cost
        total_miles += miles
        live_map_url = f"https://www.google.com/maps/dir/?api=1&origin=?q={gps_target}+Hawaii"
        
        # MAP
        with c2:
            st.link_button("📍 Map", live_map_url, use_container_width=True)
            
        # WEB
        with c3:
            web_link = row.get('Link', '')
            if web_link:
                st.link_button("🌍 Web", web_link, use_container_width=True)

        # WARNINGS: DUPLICATES & TIME
        warnings = []
        if not any(x in selected for x in ["Hotel:", "Travel:", "Start:", "End:", "Included"]) and dupe_counts[selected] > 1:
            warnings.append(f"⚠️ Duplicate! Selected {dupe_counts[selected]} times.")
            
        time_warn = check_time_warning(selected, slot_name)
        if time_warn:
            warnings.append(time_warn)
            
        if warnings:
            for w in warnings:
                st.error(w)

        # INFO LINE
        desc_text = row.get('Desc', '-')
        duration = row.get('Dur', '-')
        hours = row.get('Hours', '-')
        
        if desc_text != "-":
            st.caption(f"ℹ️ {desc_text} • ⏳ {duration} • 🕒 {hours}")

        s1, s2, s3 = st.columns(3)
        s1.caption(f"📍 {curr_zone}")
        s2.caption(f"Est. Drive: {minutes} min")
        
        if discount > 0:
            s3.caption(f"Cost: ${cost:,.0f} (🪖 Saved {int(discount*100)}%)")
        elif parking > 0:
             s3.caption(f"Cost: ${cost:,.0f} (Inc. ${parking} Park)")
        else:
            s3.caption(f"Cost: ${cost:,.0f}")
        
        prev_zone = curr_zone
        slot_counter += 1
    
    st.divider()

# --- 6. TOTALS ---
st.header("💰 Budget Breakdown")

est_gas_cost = (total_miles / car_mpg) * gas_price

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
    st.caption(f"Gas Estimate: ${est_gas_cost:,.2f} ({total_miles} mi)")
    
    grand_food_fun = total_food_fun + est_gas_cost
    diff_fun = saved_fun - grand_food_fun
    
    if diff_fun >= 0:
        st.success(f"Fully Funded! (+${diff_fun:,.0f})")
    else:
        st.error(f"Need: ${abs(diff_fun):,.0f}")

grand_total = base_cost + grand_food_fun
grand_saved = saved_pkg + saved_fun
grand_diff = grand_saved - grand_total

st.markdown("---")
g1, g2, g3 = st.columns(3)
g1.metric("Grand Total Cost", f"${grand_total:,.0f}")
g2.metric("Total Saved", f"${grand_saved:,.0f}")
g3.metric("Total Remaining", f"${grand_diff:,.0f}", delta_color="normal")
