import streamlit as st
import google.generativeai as genai
import os
import requests
from markdown_pdf import MarkdownPdf, Section
from dotenv import load_dotenv

# ==========================================
# 1. SETUP & API
# ==========================================
st.set_page_config(page_title="PocketPath | Travel Jugaad", page_icon="🎒", layout="centered")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# 2. CHAMELEON FETCHER (UNSPLASH API)
# ==========================================
def fetch_adventure_bg():
    fallback_bg = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1920&q=80"
    fallback_color = "#F09819" 
    unsplash_key = os.getenv("UNSPLASH_API_KEY")
    if not unsplash_key: return fallback_bg, fallback_color 
        
    try:
        url = f"https://api.unsplash.com/photos/random?query=landscape,adventure,travel,mountains&orientation=landscape&client_id={unsplash_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['urls']['regular'], data['color']
        return fallback_bg, fallback_color
    except Exception:
        return fallback_bg, fallback_color

def fetch_destination_bg(destination):
    fallback_bg = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1920&q=80"
    fallback_color = "#F09819" 
    unsplash_key = os.getenv("UNSPLASH_API_KEY")
    if not unsplash_key: return fallback_bg, fallback_color 
        
    try:
        # Fetches an image specifically of the destination!
        url = f"https://api.unsplash.com/photos/random?query={destination},landmark,landscape&orientation=landscape&client_id={unsplash_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['urls']['regular'], data['color']
        return fallback_bg, fallback_color
    except Exception:
        return fallback_bg, fallback_color

# Initialize in session state
if 'bg_img' not in st.session_state: 
    st.session_state.bg_img, st.session_state.bg_color = fetch_adventure_bg()

# ==========================================
# 3. LUMINANCE CALCULATOR & SMART COLORS
# ==========================================
hex_col = st.session_state.bg_color

def get_contrast_text(hex_string):
    # Switches text to dark navy if the Unsplash color is too bright!
    try:
        h = str(hex_string).lstrip('#')
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#0f172a" if luminance > 0.6 else "#ffffff"
    except:
        return "#ffffff"

text_col = get_contrast_text(hex_col)

# ==========================================
# 4. BULLETPROOF CSS
# ==========================================
st.markdown(f"""
<style>
    /* Hide Default UI */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Dynamic Background */
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.5), rgba(15, 23, 42, 0.8)), 
                    url('{st.session_state.bg_img}') no-repeat center center fixed !important;
        background-size: cover !important;
        transition: background-image 0.8s ease-in-out !important;
    }}

    /* Main Glass Container (Reduced top padding to fix gap!) */
    .block-container {{
        background: rgba(15, 18, 25, 0.75) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 25px !important;
        padding: 1.5rem 3rem 3rem 3rem !important; 
        margin-top: 2rem !important;
        margin-bottom: 3rem !important;
        max-width: 850px !important;
        box-shadow: 0 30px 60px rgba(0,0,0,0.7) !important;
    }}

    h1, h2, h3, p, label {{ color: #ffffff !important; }}
    [data-testid="stMetricValue"] {{ color: {hex_col} !important; font-weight: 900 !important; }}

    /* Buttons (Targets BOTH Submit and Download buttons) */

    /* Forces the text INSIDE the button to switch colors! */
    .stButton > button p, .stDownloadButton > button p, 
    .stButton > button span, .stDownloadButton > button span,
    .stButton > button div, .stDownloadButton > button div {{
        color: {text_col} !important; 
    }}

    .stButton > button, .stDownloadButton > button {{
        background: {hex_col} !important;
        color: {text_col} !important; /* Auto dark/light text */
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        padding: 12px !important;
        transition: 0.3s all ease-in-out !important;
        width: 100% !important;
        margin-top: 15px !important;
        box-shadow: 0 8px 20px {hex_col}50 !important; 
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 25px {hex_col}80 !important;
    }}

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }}

    /* Travel Style Cards */
    div[role="radiogroup"] {{
        display: flex; flex-direction: row !important; gap: 50px; width: 177%;
    }}
    div[role="radiogroup"] label {{
        flex: 1; 
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 15px 10px !important;
        cursor: pointer;
        transition: all 0.3s ease-in-out !important;
        display: flex; justify-content: center; align-items: center; margin: 0 !important;
    }}
    div[role="radiogroup"] label > div:first-child {{ display: none !important; }}
    div[role="radiogroup"] label p {{
        display: flex; flex-direction: column; align-items: center; text-align: center;
        font-size: 1.05rem !important; font-weight: 600 !important; color: #cbd5e1 !important; 
        margin: 0 !important; white-space: pre-wrap !important; line-height: 1.4 !important;
    }}
    div[role="radiogroup"] label:hover {{
        border-color: {hex_col} !important; background: {hex_col}15 !important; transform: translateY(-2px);
    }}
    div[role="radiogroup"] label:has(input:checked) {{
        border-color: {hex_col} !important; background: {hex_col}30 !important;
        box-shadow: 0 0 15px {hex_col}40 !important; transform: translateY(-2px);
    }}
    div[role="radiogroup"] label:has(input:checked) p {{ color: #ffffff !important; text-shadow: 0 0 8px rgba(255, 255, 255, 0.3) !important; }}

    /* Loader */
    .loading-overlay {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;border-radius: 30px;
        background-color: rgba(0, 0, 0, 0.85); backdrop-filter: blur(10px);
        display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 99999;
    }}
    .loader-ring {{
        width: 80px; height: 80px; border-radius: 50%;
        border: 8px solid {hex_col}30 !important; border-top: 8px solid {hex_col} !important;
        animation: spin 1s linear infinite; margin-bottom: 20px;
    }}
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================
if 'itinerary' not in st.session_state: st.session_state.itinerary = None
if 'dest' not in st.session_state: st.session_state.dest = ""
if 'actual_budget' not in st.session_state: st.session_state.actual_budget = 0
if 'g_size' not in st.session_state: st.session_state.g_size = 1

def create_pdf(text, destination):
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(f"# Trip Plan to {destination}\n\n{text}"))
    pdf.save("PocketPath_Itinerary.pdf")
    with open("PocketPath_Itinerary.pdf", "rb") as f:
        return f.read()

# ==========================================
# PAGE 1: THE INPUT FORM
# ==========================================
if st.session_state.itinerary is None:
    
    # Header margins fixed
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 0px; margin-bottom: 0px;'>🎒 PocketPath</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {hex_col} !important; font-weight: 700; font-size: 1.2rem;'>Smart 'Jugaad' Travel Planning</p>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("### 📍 Plan Your Route")
    col1, col2, col3 = st.columns([1.2, 1.2, 1])
    with col1: origin = st.text_input("From (City)", "Mumbai")
    with col2: dest = st.text_input("To (Destination)", placeholder="e.g. Goa")
    with col3: travel_mode = st.selectbox("Traveler Type", ["Solo Traveler", "Group Travel"])
    
    g_size = st.number_input("How many people?", min_value=2, value=4) if travel_mode == "Group Travel" else 1
    st.write("---")
    
    st.markdown("### ⏳ Details & Budget")
    col4, col5 = st.columns(2)
    with col4:
        has_dates = st.checkbox("I have specific dates in mind")
        if has_dates:
            dates = st.date_input("Select Window", [])
            if len(dates) == 2:
                days = (dates[1] - dates[0]).days + 1
                date_info = f"from {dates[0]} to {dates[1]} ({days} days)"
            else:
                days, date_info = 3, "Specific dates not fully selected."
        else:
            days = st.slider("Duration (Days)", 1, 14, 4)
            date_info = f"for a {days}-day trip"
            
    with col5:
        custom_budget = st.number_input("Custom Budget (₹) - Leave 0 for AI Package", min_value=0, value=0, step=1000)
    st.write("---")

    # Smart Cards logic
    if custom_budget == 0:
        st.markdown("<h4 style='color: white; margin-bottom: 10px;'>✈️ Travel Style</h4>", unsafe_allow_html=True)
        travel_style = st.radio("Travel Style", ["🎒\nTight\n(Backpacker)", "📸\nMid\n(Explorer)", "🏨\nLux\n(Comfort)"], horizontal=True, label_visibility="collapsed")
    else:
        travel_style = "Dynamic" 
        st.markdown(f"<h4 style='color: {hex_col}; margin-bottom: 10px;'>✨ AI Auto-Pilot Activated</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #cbd5e1;'>Since you set a strict budget of <b>₹{custom_budget}</b>, the AI will automatically optimize your stay and travel style!</p>", unsafe_allow_html=True)

    st.write("") 

    placeholder = st.empty()
    if st.button("🚀 GENERATE ITINERARY", use_container_width=True):
        if not dest:
            st.error("Bhai, destination toh daal do!")
        else:
            with placeholder.container():
                st.markdown(f"""
                <div class="loading-overlay">
                    <div class="loader-ring"></div>
                    <h2 style='color: white;'>Crafting Jugaad plan for {dest}...</h2>
                    <p style='color: {hex_col}; font-weight: bold;'>Fetching night trains & student deals!</p>
                </div>
                """, unsafe_allow_html=True)

            if custom_budget > 0:
                actual_budget = custom_budget
                tier_to_send = "Dynamic (AI MUST decide the best travel style strictly based on this exact budget)"
            else:
                base_rates = {"🎒\nTight\n(Backpacker)": 3000, "📸\nMid\n(Explorer)": 6000, "🏨\nLux\n(Comfort)": 12000}
                actual_budget = base_rates[travel_style] * (days/3) * g_size
                tier_to_send = travel_style

            prompt = f"""
            Act as a 'Jugaad' Travel Expert for Indian students with a Desi accent.
            Route: {origin} to {dest} | Mode: {travel_mode} | Group: {g_size} | Budget: ₹{actual_budget}
            Travel Window: {date_info} | Tier: {tier_to_send}

            STRICT OPERATIONAL RULES:
            1. THE HOLIDAY HACK: If specific dates are provided ({date_info}), check if they overlap with weekends or holidays to minimize leave. If no dates are fixed, suggest the best upcoming long weekend in 2026.
            2. THE NIGHT JOURNEY: You MUST prioritize overnight trains. Explain: "Bhai, ek raat ka hotel ka paisa bach gaya!".
            3. PERFECT DAY-WISE ITINERARY: Create a detailed schedule for exactly {days} days. For each day, provide:
               - 🌅 Morning: Sightseeing or Activity
               - 🥘 Afternoon: Budget-friendly lunch spot
               - 🌆 Evening: Chill spot or nightlife
            4. BUDGET TABLE: Provide a Markdown table showing Category, Cost, and 'Jugaad Tip'.

            ACCENT & TONE:
            Speak like a travel-savvy 'Bhai'. Use Hinglish naturally (Yaar, Mast, Scene kya hai, Full power).

            REQUIRED SECTIONS:
            - 🚀 **The Scene Kya Hai?** (Overview + Holiday Hack)
            - 🚂 **Level 1 Jugaad: Transport** (Train names/numbers)
            - 📅 **The Perfect {days}-Day Itinerary** (Morning/Afternoon/Evening breakdown)
            - 🏨 **Sasta & Mast Stay** (Hostel recommendations)
            - 💡 **Pro Student Tips** (Student ID discounts)
            - 📊 **Budget Bifurcation Table**
            """
            
            try:
                response = model.generate_content(prompt)
                st.session_state.itinerary = response.text
                st.session_state.dest = dest
                st.session_state.actual_budget = actual_budget
                st.session_state.g_size = g_size
                
                # MAGIC: Fetch destination background!
                st.session_state.bg_img, st.session_state.bg_color = fetch_destination_bg(dest)
                
                placeholder.empty()
                st.rerun()
            except Exception as e:
                placeholder.empty()
                st.error(f"AI Error: {e}")

# ==========================================
# PAGE 2: THE RESULT PAGE
# ==========================================
else:
    st.markdown(f"<h2 style='color: {hex_col}; text-align: center; margin-top: 0;'>🗺️ Epic Plan for {st.session_state.dest}</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.metric("Paisa Vasool Share (Per Person)", f"₹{round(st.session_state.actual_budget / st.session_state.g_size)}")
    st.write("")
    
    col_dl, col_restart = st.columns(2)
    with col_dl:
        pdf_data = create_pdf(st.session_state.itinerary, st.session_state.dest)
        st.download_button("📥 DOWNLOAD ITINERARY (PDF)", data=pdf_data, file_name=f"{st.session_state.dest}_Adventure.pdf", use_container_width=True)
    
    with col_restart:
        if st.button("🔄 PLAN ANOTHER TRIP", use_container_width=True):
            st.session_state.itinerary = None
            # Fetch a generic adventure background when restarting!
            st.session_state.bg_img, st.session_state.bg_color = fetch_adventure_bg() 
            st.rerun()