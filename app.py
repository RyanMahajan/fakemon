import streamlit as st
import pandas as pd
import base64
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

# --- 6. PROMPT SANITIZER ---
def get_safe_prompt(name, p_type, desc):
    clean_desc = desc.lower().replace("pokemon", "pocket monster").replace("vicious", "fierce")
    
    # Modern Vector Formula:
    prompt = (
        f"Modern 2D vector character sprite of {name}, a {p_type} type creature. "
        f"Style: Official high-resolution monster-collector game art, Gen 9 aesthetic. "
        f"Visuals: Thick clean black outlines, bold saturated flat colors, crisp cel-shading, "
        f"professional digital illustration, no sketchy lines, no paper texture. "
        f"Physical Details: {clean_desc}. "
        f"Background: PURE TRANSPARENT BACKGROUND, ALPHA CHANNEL, NO BACKGROUND SCENERY."
    )
    return prompt

# --- 7. EXECUTION ---
if st.button("Generate My Pokémon"):
    if not name or not description:
        st.error("Missing Info: Please enter a Name and a Description!")
    else:
        try:
            # 1. Generate Stats
            final_stats = calculate_stats(p_type, description, tier)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Name: {name}")
                st.write(f"**Type:** {p_type} | **Tier:** {tier}")
                st.table(pd.DataFrame(final_stats.items(), columns=["Stat", "Value"]))

            with col2:
                with st.spinner("Generating modern vector asset..."):
                    try:
                        safe_art_prompt = get_safe_prompt(name, p_type, description)
                        
                        response = client.images.generate(
                            model="gpt-image-1-mini",
                            prompt=safe_art_prompt,
                            n=1,
                            size="1024x1024",
                            quality="low",  # 'standard' is better than 'low' for clean vector lines
                            # In 2026, we don't need 'response_format' for b64, but we specify the type
                        )

                        image_data = response.data[0].b64_json
                        
                        if image_data:
                            decoded_image = base64.b64decode(image_data)
                            
                            # Streamlit displays transparency perfectly!
                            st.image(decoded_image, caption=f"Modern {name} Generated!")
                            
                            # Add a download button for the PNG
                            st.download_button(
                                label="Download Transparent PNG",
                                data=decoded_image,
                                file_name=f"{name}_transparent.png",
                                mime="image/png"
                            )

                    except Exception as e:
                        if "moderation" in str(e).lower():
                            st.error("🚨 Safety Filter: Try changing your description words!")
                        else:
                            st.error(f"Image Generation Error: {e}")
        
        except Exception as e:
            st.error(f"Stat Calculation Error: {e}")