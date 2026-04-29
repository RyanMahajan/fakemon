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

# --- 7. EXECUTION & BUTTONS ---

# Initialize session state for the image so the download button stays visible
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_name" not in st.session_state:
    st.session_state.image_name = ""

# Create two columns for the buttons
btn_col1, btn_col2 = st.columns([1, 1])

with btn_col1:
    generate_pressed = st.button("Generate My Pokémon", use_container_width=True)

with btn_col2:
    # Only show the download button if an image has been generated
    if st.session_state.generated_image is not None:
        st.download_button(
            label="Download PNG",
            data=st.session_state.generated_image,
            file_name=f"{st.session_state.image_name}.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        # Placeholder so the layout stays even
        st.button("Download (Locked)", disabled=True, use_container_width=True)

# THE ACTUAL GENERATION LOGIC
if generate_pressed:
    if not name or not description:
        st.error("Missing Info: Please enter a Name and a Description!")
    else:
        try:
            # 1. Generate Stats
            final_stats = calculate_stats(p_type, description, tier)
            
            # Display results in the main area
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader(f"Name: {name}")
                st.write(f"**Type:** {p_type} | **Tier:** {tier}")
                st.table(pd.DataFrame(final_stats.items(), columns=["Stat", "Value"]))

            with res_col2:
                with st.spinner("Drawing your creature..."):
                    try:
                        safe_art_prompt = get_safe_prompt(name, p_type, description)
                        
                        response = client.images.generate(
                            model="gpt-image-1-mini",
                            prompt=safe_art_prompt,
                            n=1,
                            size="1024x1024",
                            quality="low"
                        )

                        image_data = response.data[0].b64_json
                        
                        if image_data:
                            decoded_image = base64.b64decode(image_data)
                            
                            # SAVE TO SESSION STATE
                            st.session_state.generated_image = decoded_image
                            st.session_state.image_name = name
                            
                            # Show the image
                            st.image(decoded_image, caption=f"A wild {name} appeared!")
                            
                            # Rerun to update the Download Button state
                            st.rerun()
                        else:
                            st.error("The API returned empty data.")

                    except Exception as e:
                        st.error(f"Image Error: {e}")
        
        except Exception as e:
            st.error(f"Calculation Error: {e}")