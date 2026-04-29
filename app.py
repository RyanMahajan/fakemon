import streamlit as st
import pandas as pd
import openai

# --- 1. CONFIGURATION & SECRETS ---
# Ensure you have set up 'OPENAI_API_KEY' in your Streamlit Secrets or environment variables
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("API Key not found. Image generation will be bypassed.")

# --- 2. LOAD DATASET ---
@st.cache_data
def load_data():
    # Replace with your actual filename. 
    # Assumes columns: 'Type 1', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'
    return pd.read_csv("PKDATA.csv")

df = load_data()

# --- 3. UI HEADER ---
st.set_page_config(page_title="Fakémon Lab", page_icon="🧬")
st.title("🧬 Fakémon Creator")
st.markdown("Provide details to generate a new Pokémon based on dataset trends.")

# --- 4. USER INPUTS ---
with st.sidebar:
    st.header("Characteristics")
    name = st.text_input("Fakémon Name", placeholder="e.g., Voltkitty")
    p_type = st.selectbox("Primary Type", sorted(df['type_1'].unique()))
    description = st.text_area("Description", placeholder="e.g., A sleek, metallic feline that moves like lightning.")
    
    tier = st.select_slider(
        "Power Tier",
        options=["Baby", "Basic", "Final Evolution", "Legendary"],
        value="Basic"
    )

# --- 5. LOGIC: STAT CALCULATION ---
def calculate_stats(poke_type, desc, tier_choice):
    # Get averages for the chosen type
    type_averages = df[df['type_1'] == poke_type].mean(numeric_only=True).to_dict()
    
    # Tier multipliers (scaling the base data)
    multipliers = {"Baby": 0.6, "Basic": 1.0, "Final Evolution": 1.3, "Legendary": 1.6}
    mult = multipliers[tier_choice]
    
    stats = {k: int(v * mult) for k, v in type_averages.items() if k in ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']}
    
    # Description-based keyword modifiers
    keywords = {
        "fast": ("speed", 1.2), "lightning": ("speed", 1.2),
        "tank": ("defense", 1.2), "bulky": ("defense", 1.2), "sturdy": ("defense", 1.2),
        "strong": ("attack", 1.2), "vicious": ("attack", 1.2), "sharp": ("attack", 1.2),
        "smart": ("sp_attack", 1.2), "mystical": ("sp_attack", 1.2)
    }
    
    for word, (stat, boost) in keywords.items():
        if word in desc.lower():
            stats[stat] = int(stats[stat] * boost)
            
    return stats

# --- 6. EXECUTION & GENERATION ---
if st.button("Generate My Pokémon"):
    if name and description:
        # Calculate stats
        final_stats = calculate_stats(p_type, description, tier)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Name: {name}")
            st.write(f"**Type:** {p_type}")
            st.write(f"**Tier:** {tier}")
            st.table(pd.DataFrame(final_stats.items(), columns=["Stat", "Value"]))

        with col2:
                # UPDATED: Using the gpt-image-1-mini model
                with st.spinner("Generating budget-friendly art..."):
                    try:
                        response = client.images.generate(
                            model="gpt-image-1-mini",  # The specific 'mini' model ID
                            prompt=f"Official Ken Sugimori Pokemon style, {name}, {p_type} type, {description}, white background",
                            n=1,
                            size="1024x1024",
                            quality="low"  # 'low' corresponds to the $0.005 price tier
                        )
                        st.image(response.data[0].url)
                    except Exception as e:
                        st.error(f"Error: {e}")
    else:
        st.error("Please provide both a Name and a Description!")