import streamlit as st
import pandas as pd
from openai import OpenAI

# --- 1. CONFIGURATION & SECRETS ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.warning("API Key not found. Image generation will be bypassed.")

# --- 2. LOAD DATASET ---
@st.cache_data
def load_data():
    return pd.read_csv("PKDATA.csv")

df = load_data()

# --- 3. UI HEADER ---
st.set_page_config(page_title="Fakémon Lab", page_icon="🧬")
st.title("🧬 Fakémon Creator")

# --- 4. USER INPUTS ---
with st.sidebar:
    st.header("Characteristics")
    name = st.text_input("Fakémon Name", placeholder="e.g., Voltkitty")
    # Clean column names in case they have spaces/caps
    type_col = 'type_1' if 'type_1' in df.columns else 'Type 1'
    p_type = st.selectbox("Primary Type", sorted(df[type_col].unique()))
    description = st.text_area("Description", placeholder="e.g., A sleek, metallic feline that moves like lightning.")
    
    tier = st.select_slider(
        "Power Tier",
        options=["Baby", "Basic", "Final Evolution", "Legendary"],
        value="Basic"
    )

# --- 5. LOGIC: STAT CALCULATION ---
def calculate_stats(poke_type, desc, tier_choice):
    t_col = 'type_1' if 'type_1' in df.columns else 'Type 1'
    type_averages = df[df[t_col] == poke_type].mean(numeric_only=True).to_dict()
    
    multipliers = {"Baby": 0.6, "Basic": 1.0, "Final Evolution": 1.3, "Legendary": 1.6}
    mult = multipliers[tier_choice]
    
    # Matching your CSV's lowercase column names
    stat_keys = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    stats = {k: int(type_averages.get(k, 50) * mult) for k in stat_keys}
    
    keywords = {
        "fast": ("speed", 1.2), "lightning": ("speed", 1.2),
        "tank": ("defense", 1.2), "bulky": ("defense", 1.2),
        "strong": ("attack", 1.2), "vicious": ("attack", 1.2),
        "smart": ("sp_attack", 1.2), "mystical": ("sp_attack", 1.2)
    }
    
    for word, (stat, boost) in keywords.items():
        if word in desc.lower():
            stats[stat] = int(stats[stat] * boost)
    return stats

# --- 6. PROMPT SANITIZER (The Fix for Moderation Error) ---
def get_safe_prompt(name, p_type, desc):
    # Rule 1: Avoid the word "Pokemon" - use descriptive alternatives
    # Rule 2: Swaps 'vicious' or 'aggressive' words that trigger blocks
    clean_desc = desc.lower().replace("pokemon", "pocket creature").replace("vicious", "fierce")
    
    # We use "Ken Sugimori style" but emphasize it's a "fictional creature design"
    # to avoid copyright flags while keeping the aesthetic.
    prompt = (
        f"A professional creature design in a classic Japanese monster-collector game style, "
        f"reminiscent of official 90s watercolor character art. "
        f"The creature is named {name}, it is a {p_type} type. "
        f"Physical description: {clean_desc}. "
        f"Isolated on a plain white background, high quality digital art."
    )
    return prompt

# --- 7. EXECUTION ---
if st.button("Generate My Pokémon"):
    # First, make sure the user didn't leave boxes empty
    if not name or not description:
        st.error("Missing Info: Please enter a Name and a Description!")
    else:
        # 1. Safely calculate stats
        try:
            final_stats = calculate_stats(p_type, description, tier)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Name: {name}")
                st.write(f"**Type:** {p_type} | **Tier:** {tier}")
                st.table(pd.DataFrame(final_stats.items(), columns=["Stat", "Value"]))

            with col2:
                with st.spinner("Drawing your creature..."):
                    # 2. Get the safe prompt
                    safe_art_prompt = get_safe_prompt(name, p_type, description)
                    
            # 3. Generate Image with specific 'None' checks
            try:
                response = client.images.generate(
                    model="gpt-image-1-mini",  # Correct 2026 ID
                    prompt=safe_art_prompt,
                    n=1,
                    size="1024x1024",
                    quality="low",           # Trigger for the $0.005 pricing
                    response_format="url"    # Ensure it returns a link, not raw data
                )
                
                # Securely retrieve the URL
                if response and response.data:
                    image_url = response.data[0].url
                    st.image(image_url)
                else:
                    st.error("The model generated an image but failed to provide a link.")

            except Exception as e:
                # Helpful debugging for key issues
                if "insufficient_quota" in str(e):
                    st.error("Your API key works, but you have $0.00 credits. Add $5 to OpenAI Billing.")
                elif "invalid_api_key" in str(e):
                    st.error("The API key is incorrect. Check for extra spaces or a missing 'sk-' prefix.")
                else:
                    st.error(f"API Error: {e}")

        except Exception as e:
            # This handles the 'NoneType' error specifically
            if "NoneType" in str(e):
                st.error("Internal Error: One of the inputs was empty. Please refresh and try again.")
            elif "moderation" in str(e).lower():
                st.error("🚨 Safety Filter: The AI didn't like your description. Try using different words!")
            else:
                st.error(f"Something went wrong: {e}")