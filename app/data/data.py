from typing import Any, Dict, List

DISTRICT_COORDINATES = {                                                                                
        "mandya": {"lat": 12.52, "lon": 76.89, "name": "Mandya"},                                           
        "kolar": {"lat": 13.13, "lon": 78.13, "name": "Kolar"},                                             
        "bangalore": {"lat": 12.97, "lon": 77.59, "name": "Bangalore Urban"},                               
        "mysuru": {"lat": 12.29, "lon": 76.63, "name": "Mysuru"},                                           
        "hubli": {"lat": 15.36, "lon": 75.12, "name": "Hubli-Dharwad"},                                     
        "belagavi": {"lat": 15.84, "lon": 74.49, "name": "Belagavi"},                                       
        "hassan": {"lat": 13.00, "lon": 76.10, "name": "Hassan"},                                           
        "shimoga": {"lat": 13.92, "lon": 75.56, "name": "Shivamogga"},                                      
        "tumakuru": {"lat": 13.33, "lon": 77.10, "name": "Tumakuru"},                                       
        "haveri": {"lat": 14.79, "lon": 75.39, "name": "Haveri"},                                           
        "davanagere": {"lat": 14.46, "lon": 75.92, "name": "Davanagere"},                                   
        "ballari": {"lat": 15.13, "lon": 76.92, "name": "Ballari"},                                         
}


KARNATAKA_DISTRICT_BENCHMARKS: List[Dict[str, Any]] = [
    # Mandya
    {"district": "Mandya", "market": "Mandya APMC", "commodity": "Tomato", "variety": "Hybrid", "min_price": 18.0, "max_price": 26.0, "modal_price": 22.0, "unit": "Kg"},
    {"district": "Mandya", "market": "Pandavapura APMC", "commodity": "Sugarcane", "variety": "CO 86032", "min_price": 31.0, "max_price": 35.0, "modal_price": 33.0, "unit": "Kg"},
    {"district": "Mandya", "market": "Maddur APMC", "commodity": "Tender Coconut", "variety": "Local", "min_price": 25.0, "max_price": 38.0, "modal_price": 32.0, "unit": "Piece"},
    {"district": "Mandya", "market": "Mandya APMC", "commodity": "Ragi", "variety": "Local Red", "min_price": 30.0, "max_price": 35.0, "modal_price": 32.5, "unit": "Kg"},
    {"district": "Mandya", "market": "Mandya APMC", "commodity": "Paddy(Common)", "variety": "Sona Masoori", "min_price": 22.0, "max_price": 28.0, "modal_price": 25.0, "unit": "Kg"},

    # Kolar
    {"district": "Kolar", "market": "Kolar APMC", "commodity": "Tomato", "variety": "Local", "min_price": 16.0, "max_price": 24.0, "modal_price": 20.0, "unit": "Kg"},
    {"district": "Kolar", "market": "Kolar APMC", "commodity": "Capsicum", "variety": "Green", "min_price": 32.0, "max_price": 45.0, "modal_price": 38.0, "unit": "Kg"},
    {"district": "Kolar", "market": "Srinivasapur APMC", "commodity": "Mango", "variety": "Totapuri", "min_price": 22.0, "max_price": 35.0, "modal_price": 28.0, "unit": "Kg"},
    {"district": "Kolar", "market": "Kolar APMC", "commodity": "Beans", "variety": "Ring Beans", "min_price": 40.0, "max_price": 55.0, "modal_price": 48.0, "unit": "Kg"},

    # Bangalore / Bengaluru Urban
    {"district": "Bangalore", "market": "Yeshwanthpur APMC", "commodity": "Onion", "variety": "Bellary", "min_price": 28.0, "max_price": 38.0, "modal_price": 34.0, "unit": "Kg"},
    {"district": "Bangalore", "market": "Yeshwanthpur APMC", "commodity": "Potato", "variety": "Jyoti", "min_price": 22.0, "max_price": 30.0, "modal_price": 26.0, "unit": "Kg"},
    {"district": "Bangalore", "market": "K.R. Market APMC", "commodity": "Green Chilli", "variety": "Guntur", "min_price": 40.0, "max_price": 55.0, "modal_price": 48.0, "unit": "Kg"},
    {"district": "Bangalore", "market": "Yeshwanthpur APMC", "commodity": "Cauliflower", "variety": "Local", "min_price": 25.0, "max_price": 35.0, "modal_price": 30.0, "unit": "Kg"},

    # Mysuru
    {"district": "Mysuru", "market": "Bandipalya APMC", "commodity": "Paddy(Common)", "variety": "Sona Masoori", "min_price": 24.0, "max_price": 30.0, "modal_price": 27.0, "unit": "Kg"},
    {"district": "Mysuru", "market": "Bandipalya APMC", "commodity": "Banana", "variety": "Nanjangud Rasabale", "min_price": 45.0, "max_price": 70.0, "modal_price": 55.0, "unit": "Kg"},
    {"district": "Mysuru", "market": "Mysuru APMC", "commodity": "Ragi", "variety": "Indaf 5", "min_price": 31.0, "max_price": 36.0, "modal_price": 33.0, "unit": "Kg"},
    {"district": "Mysuru", "market": "Bandipalya APMC", "commodity": "Ginger(Green)", "variety": "Local", "min_price": 55.0, "max_price": 75.0, "modal_price": 65.0, "unit": "Kg"},

    # Hubli-Dharwad
    {"district": "Hubli", "market": "Amaragol APMC", "commodity": "Green Chilli", "variety": "Local", "min_price": 42.0, "max_price": 58.0, "modal_price": 50.0, "unit": "Kg"},
    {"district": "Hubli", "market": "Amaragol APMC", "commodity": "Cotton", "variety": "DCH-32", "min_price": 68.0, "max_price": 82.0, "modal_price": 75.0, "unit": "Kg"},
    {"district": "Hubli", "market": "Hubli APMC", "commodity": "Bengal Gram", "variety": "Annigeri", "min_price": 55.0, "max_price": 65.0, "modal_price": 60.0, "unit": "Kg"},
    {"district": "Hubli", "market": "Amaragol APMC", "commodity": "Onion", "variety": "Red", "min_price": 20.0, "max_price": 28.0, "modal_price": 24.0, "unit": "Kg"},

    # Belagavi
    {"district": "Belagavi", "market": "Belagavi APMC", "commodity": "Sugarcane", "variety": "General", "min_price": 30.0, "max_price": 34.0, "modal_price": 32.0, "unit": "Kg"},
    {"district": "Belagavi", "market": "Belagavi APMC", "commodity": "Soyabean", "variety": "Yellow", "min_price": 42.0, "max_price": 49.0, "modal_price": 45.0, "unit": "Kg"},
    {"district": "Belagavi", "market": "Belagavi APMC", "commodity": "Potato", "variety": "Local", "min_price": 18.0, "max_price": 25.0, "modal_price": 22.0, "unit": "Kg"},

    # Hassan
    {"district": "Hassan", "market": "Hassan APMC", "commodity": "Potato", "variety": "Hassan Local", "min_price": 20.0, "max_price": 28.0, "modal_price": 24.0, "unit": "Kg"},
    {"district": "Hassan", "market": "Hassan APMC", "commodity": "Ginger(Green)", "variety": "Green Local", "min_price": 60.0, "max_price": 85.0, "modal_price": 72.0, "unit": "Kg"},
    {"district": "Hassan", "market": "Arasikere APMC", "commodity": "Coconut", "variety": "Grade-A", "min_price": 28.0, "max_price": 35.0, "modal_price": 31.0, "unit": "Piece"},

    # Shimoga / Shivamogga
    {"district": "Shimoga", "market": "Shivamogga APMC", "commodity": "Arecanut", "variety": "Rashi", "min_price": 420.0, "max_price": 490.0, "modal_price": 460.0, "unit": "Kg"},
    {"district": "Shimoga", "market": "Bhadravathi APMC", "commodity": "Paddy(Common)", "variety": "IR 64", "min_price": 21.0, "max_price": 25.0, "modal_price": 23.0, "unit": "Kg"},
    {"district": "Shimoga", "market": "Shivamogga APMC", "commodity": "Maize", "variety": "Yellow", "min_price": 22.0, "max_price": 27.0, "modal_price": 24.5, "unit": "Kg"},

    # Tumakuru
    {"district": "Tumakuru", "market": "Tiptur APMC", "commodity": "Copra (Dry Coconut)", "variety": "Ball", "min_price": 105.0, "max_price": 125.0, "modal_price": 115.0, "unit": "Kg"},
    {"district": "Tumakuru", "market": "Tumakuru APMC", "commodity": "Groundnut", "variety": "Pods with shell", "min_price": 58.0, "max_price": 72.0, "modal_price": 65.0, "unit": "Kg"},
    {"district": "Tumakuru", "market": "Tumakuru APMC", "commodity": "Ragi", "variety": "Local", "min_price": 30.0, "max_price": 34.0, "modal_price": 32.0, "unit": "Kg"},

    # Haveri
    {"district": "Haveri", "market": "Byadagi APMC", "commodity": "Red Chilli", "variety": "Byadagi Kaddi", "min_price": 280.0, "max_price": 420.0, "modal_price": 350.0, "unit": "Kg"},
    {"district": "Haveri", "market": "Ranebennur APMC", "commodity": "Maize", "variety": "Local", "min_price": 22.0, "max_price": 26.0, "modal_price": 24.0, "unit": "Kg"},
    {"district": "Haveri", "market": "Ranebennur APMC", "commodity": "Onion", "variety": "Local", "min_price": 10.0, "max_price": 15.0, "modal_price": 12.0, "unit": "Kg"},

    # Davanagere
    {"district": "Davanagere", "market": "Davanagere APMC", "commodity": "Maize", "variety": "Hybrid", "min_price": 23.0, "max_price": 27.0, "modal_price": 25.0, "unit": "Kg"},
    {"district": "Davanagere", "market": "Davanagere APMC", "commodity": "Paddy(Common)", "variety": "BPT 5204", "min_price": 25.0, "max_price": 32.0, "modal_price": 28.5, "unit": "Kg"},

    # Ballari
    {"district": "Ballari", "market": "Ballari APMC", "commodity": "Red Chilli", "variety": "Guntur/Ballari", "min_price": 140.0, "max_price": 190.0, "modal_price": 165.0, "unit": "Kg"},
    {"district": "Ballari", "market": "Kottur APMC", "commodity": "Cotton", "variety": "Bunny", "min_price": 70.0, "max_price": 85.0, "modal_price": 78.0, "unit": "Kg"},
]