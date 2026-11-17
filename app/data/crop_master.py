from typing import List, Dict, Any                                                                      
                                                                                                            
CROPS_MASTER_DATA: List[Dict[str, Any]] = [                                                             
        # Vegetables                                                                                        
        {"id": "tomato", "name_en": "Tomato", "name_kn": "ಟೊಮೇಟೊ", "name_hi": "टमाटर", "category": "Vegetables",
        "default_unit": "Kg", "icon": "🍅"},                                                                
        {"id": "onion", "name_en": "Onion", "name_kn": "ಈರುಳ್ಳಿ", "name_hi": "प्याज", "category": "Vegetables",   
        "default_unit": "Kg", "icon": "🧅"},                                                                
        {"id": "potato", "name_en": "Potato", "name_kn": "ಆಲೂಗಡ್ಡೆ", "name_hi": "आलू", "category": "Vegetables",
        "default_unit": "Kg", "icon": "🥔"},                                                                
        {"id": "green_chilli", "name_en": "Green Chilli", "name_kn": "ಹಸಿ ಮೆಣಸಿನಕಾಯಿ", "name_hi": "हरी मिर्च",       
        "category": "Vegetables", "default_unit": "Kg", "icon": "🌶️"},                                      
        {"id": "brinjal", "name_en": "Brinjal / Eggplant", "name_kn": "ಬದನೆಕಾಯಿ", "name_hi": "बैंगन", "category":
        "Vegetables", "default_unit": "Kg", "icon": "🍆"},                                                  
        {"id": "carrot", "name_en": "Carrot", "name_kn": "ಕ್ಯಾರೆಟ್", "name_hi": "गाजर", "category": "Vegetables",
        "default_unit": "Kg", "icon": "🥕"},                                                                
        {"id": "cabbage", "name_en": "Cabbage", "name_kn": "ಎಲೆಕೋಸು", "name_hi": "पत्ता गोभी", "category":          
        "Vegetables", "default_unit": "Kg", "icon": "🥬"},                                                  
        {"id": "cauliflower", "name_en": "Cauliflower", "name_kn": "ಹೂಕೋಸು", "name_hi": "फूलगोभी", "category":    
        "Vegetables", "default_unit": "Kg", "icon": "🥦"},                                                  
        {"id": "lady_finger", "name_en": "Lady Finger (Okra)", "name_kn": "ಬೆಂಡೆಕಾಯಿ", "name_hi": "भिंडी",          
        "category": "Vegetables", "default_unit": "Kg", "icon": "🥒"},                                      
        {"id": "beans", "name_en": "Beans", "name_kn": "ಹುರುಳಿಕಾಯಿ", "name_hi": "बीन्स / फलियां", "category":          
        "Vegetables", "default_unit": "Kg", "icon": "🫛"},                                                  
        {"id": "capsicum", "name_en": "Capsicum", "name_kn": "ದಪ್ಪ ಮೆಣಸಿನಕಾಯಿ", "name_hi": "शिमला मिर्च", "category": 
        "Vegetables", "default_unit": "Kg", "icon": "🫑"},                                                  
        {"id": "garlic", "name_en": "Garlic", "name_kn": "ಬೆಳ್ಳುಳ್ಳಿ", "name_hi": "लहसुन", "category":            
        "Vegetables", "default_unit": "Kg", "icon": "🧄"},                                                  
        {"id": "ginger", "name_en": "Ginger", "name_kn": "ಶುಂಠಿ", "name_hi": "अदरक", "category": "Vegetables", 
        "default_unit": "Kg", "icon": "🫚"},                                                                
                                                                                                            
        # Grains & Cereals                                                                                  
        {"id": "paddy", "name_en": "Paddy / Rice", "name_kn": "ಭತ್ತ / ಅಕ್ಕಿ", "name_hi": "धान / चावल",           
        "category": "Grains", "default_unit": "Quintal", "icon": "🌾"},                                     
        {"id": "ragi", "name_en": "Ragi (Finger Millet)", "name_kn": "ರಾಗಿ", "name_hi": "रागी", "category":     
        "Grains", "default_unit": "Quintal", "icon": "🌾"},                                                 
        {"id": "maize", "name_en": "Maize (Corn)", "name_kn": "ಮೆಕ್ಕೆಜೋಳ", "name_hi": "मक्का", "category":         
        "Grains", "default_unit": "Quintal", "icon": "🌽"},                                                 
        {"id": "jowar", "name_en": "Jowar (Sorghum)", "name_kn": "ಜೋಳ", "name_hi": "ज्वार", "category":         
        "Grains", "default_unit": "Quintal", "icon": "🌾"},                                                 
                                                                                                            
        # Pulses                                                                                            
        {"id": "toor_dal", "name_en": "Toor Dal (Red Gram)", "name_kn": "ತೊಗರಿ ಬೇಳೆ", "name_hi": "अरहर / तूर दाल",
        "category": "Pulses", "default_unit": "Quintal", "icon": "🥣"},                                     
        {"id": "bengal_gram", "name_en": "Bengal Gram (Chana)", "name_kn": "ಕಡಲೆ", "name_hi": "चना",          
        "category": "Pulses", "default_unit": "Quintal", "icon": "🌰"},                                     
        {"id": "groundnut", "name_en": "Groundnut (Peanut)", "name_kn": "ಕಡಲೆಕಾಯಿ", "name_hi": "मूंगफली",         
        "category": "Pulses", "default_unit": "Quintal", "icon": "🥜"},                                     
                                                                                                            
        # Fruits                                                                                            
        {"id": "banana", "name_en": "Banana", "name_kn": "ಬಾಳೆಹಣ್ಣು", "name_hi": "केला", "category": "Fruits",    
        "default_unit": "Kg", "icon": "🍌"},                                                                
        {"id": "mango", "name_en": "Mango", "name_kn": "ಮಾವಿನಹಣ್ಣು", "name_hi": "आम", "category": "Fruits",     
        "default_unit": "Kg", "icon": "🥭"},                                                                
        {"id": "tender_coconut", "name_en": "Tender Coconut", "name_kn": "ಎಳನೀರು", "name_hi": "डाभ / नारियल पानी", 
        "category": "Fruits", "default_unit": "Piece", "icon": "🥥"},                                       
        {"id": "coconut", "name_en": "Coconut (Dry/Matured)", "name_kn": "ತೆಂಗಿನಕಾಯಿ", "name_hi": "नारियल",        
        "category": "Fruits", "default_unit": "Piece", "icon": "🥥"},                                       
        {"id": "papaya", "name_en": "Papaya", "name_kn": "ಪರಂಗಿ ಹಣ್ಣು", "name_hi": "पपीता", "category": "Fruits", 
        "default_unit": "Kg", "icon": "🍈"},                                                                
                                                                                                            
        # Commercial & Spices                                                                               
        {"id": "sugarcane", "name_en": "Sugarcane", "name_kn": "ಕಬ್ಬು", "name_hi": "गन्ना", "category":          
        "Commercial", "default_unit": "Ton", "icon": "🎋"},                                                 
        {"id": "cotton", "name_en": "Cotton", "name_kn": "ಹತ್ತಿ", "name_hi": "कपास", "category": "Commercial", 
        "default_unit": "Quintal", "icon": "☁️"},                                                           
        {"id": "arecanut", "name_en": "Arecanut (Supari)", "name_kn": "ಅಡಿಕೆ", "name_hi": "सुपारी", "category":  
        "Commercial", "default_unit": "Quintal", "icon": "🌰"},                                             
        {"id": "red_chilli", "name_en": "Red Chilli (Byadagi)", "name_kn": "ಬ್ಯಾಡಗಿ ಒಣ ಮೆಣಸಿನಕಾಯಿ", "name_hi": "लाल मिर्च", "category": "Spices", "default_unit": "Kg", "icon": "🌶️"},                                     
]

CROP_SYNONYMS: Dict[str, List[str]] = {
    "tomato": [
        "tomato", "ಟೊಮೇಟೊ", "टमाटर", "tometo", "tamatar", "thakkali", "tamata", "tamoto"
    ],
    "onion": [
        "onion", "ಈರುಳ್ಳಿ", "प्याज", "eerulli", "erulli", "irulli", "ullagaddi", "pyaz", "pyaaz", "vengayam"
    ],
    "potato": [
        "potato", "ಆಲೂಗಡ್ಡೆ", "आलू", "alugadde", "aloo", "alu", "batata", "urulaikizhangu", "potatoes"
    ],
    "green_chilli": [
        "green chilli", "ಹಸಿ ಮೆಣಸಿನಕಾಯಿ", "हरी मिर्च", "hasi menasinakayi", "menasinakayi", "hari mirch", "mirchi", "green chili", "chilli", "chili"
    ],
    "brinjal": [
        "brinjal", "eggplant", "aubergine", "ಬದನೆಕಾಯಿ", "बैंगन", "badanekayi", "badane", "baingan", "vankaya"
    ],
    "carrot": [
        "carrot", "ಕ್ಯಾರೆಟ್", "गाजर", "kyaret", "gajar"
    ],
    "cabbage": [
        "cabbage", "ಎಲೆಕೋಸು", "पत्ता गोभी", "elekosu", "patta gobhi", "bandhagobhi"
    ],
    "cauliflower": [
        "cauliflower", "ಹೂಕೋಸು", "फूलगोभी", "hookosu", "phool gobhi", "gobhi"
    ],
    "lady_finger": [
        "lady finger", "okra", "ಬೆಂಡೆಕಾಯಿ", "भिंडी", "bendekayi", "bhendi", "bhindi", "vendakkai"
    ],
    "beans": [
        "beans", "ಹುರುಳಿಕಾಯಿ", "बीन्स", "फलियां", "hurulikayi", "french beans", "ring beans", "phaliyan"
    ],
    "capsicum": [
        "capsicum", "bell pepper", "ದಪ್ಪ ಮೆಣಸಿನಕಾಯಿ", "शिमला मिर्च", "dappa menasinakayi", "shimla mirch"
    ],
    "garlic": [
        "garlic", "ಬೆಳ್ಳುಳ್ಳಿ", "लहसुन", "bellulli", "lahsun", "lehsan", "poondu"
    ],
    "ginger": [
        "ginger", "ಶುಂಠಿ", "अदरक", "shunti", "adrak", "inji", "ginger(green)"
    ],
    "paddy": [
        "paddy", "rice", "ಭತ್ತ", "ಅಕ್ಕಿ", "धान", "चावल", "bhatta", "akki", "dhan", "chawal", "sona masoori"
    ],
    "ragi": [
        "ragi", "finger millet", "ರಾಗಿ", "रागी", "mandua", "nachni", "kezhvaragu"
    ],
    "maize": [
        "maize", "corn", "sweet corn", "ಮೆಕ್ಕೆಜೋಳ", "मक्का", "mekkejola", "makka", "makki", "bhutta"
    ],
    "jowar": [
        "jowar", "sorghum", "ಜೋಳ", "ज्वार", "jola", "cholam"
    ],
    "toor_dal": [
        "toor dal", "red gram", "arhar", "ತೊಗರಿ ಬೇಳೆ", "अरहर", "तूर दाल", "togari", "togaribele", "tur dal"
    ],
    "bengal_gram": [
        "bengal gram", "chana", "chickpea", "ಕಡಲೆ", "चना", "kadale", "kala chana", "channa"
    ],
    "groundnut": [
        "groundnut", "peanut", "ಕಡಲೆಕಾಯಿ", "मूंगफಲಿ", "kadalekayi", "shenga", "moongfali", "mungfali"
    ],
    "banana": [
        "banana", "ಬಾಳೆಹಣ್ಣು", "केला", "balehannu", "bale", "kela", "rasabale", "yelakki"
    ],
    "mango": [
        "mango", "ಮಾವಿನಹಣ್ಣು", "आम", "mavina hannu", "mavu", "aam", "totapuri", "alphonso", "badami"
    ],
    "tender_coconut": [
        "tender coconut", "ಎಳನೀರು", "डाभ", "नारियल पानी", "elaneeru", "yelaneeru", "nariyal pani", "dabh"
    ],
    "coconut": [
        "coconut", "ತೆಂಗಿನಕಾಯಿ", "नारियल", "tenginakayi", "thengai", "nariyal", "copra"
    ],
    "papaya": [
        "papaya", "ಪರಂಗಿ ಹಣ್ಣು", "पपीता", "parangi hannu", "papita"
    ],
    "sugarcane": [
        "sugarcane", "ಕಬ್ಬು", "गन्ना", "kabbu", "ganna", "karumbu"
    ],
    "cotton": [
        "cotton", "ಹತ್ತಿ", "कपास", "hatti", "kapas"
    ],
    "arecanut": [
        "arecanut", "betel nut", "ಅಡಿಕೆ", "सुपारी", "adike", "supari"
    ],
    "red_chilli": [
        "red chilli", "byadagi", "ಬ್ಯಾಡಗಿ ಒಣ ಮೆಣಸಿನಕಾಯಿ", "लाल मिर्च", "ona menasinakayi", "lal mirch", "kaddi"
    ],
}