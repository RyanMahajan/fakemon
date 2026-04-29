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
    return pd.read_csv("pokemon_data.csv")

df = load_data()

# --- 3. UI HEADER ---
st.set_page_config(page_title="Fakémon Lab", page_icon="🧬")
st.title("🧬 Fakémon Creator")
st.markdown("Provide details to generate a new Pokémon based on dataset trends.")

# --- 4. USER INPUTS ---
with st.sidebar:
    st.header("Characteristics")
    name = st.text_input("Fakémon Name", placeholder="e.g., Voltkitty")
    p_type = st.selectbox("Primary Type", sorted(df['Type 1'].unique()))
    description = st.text_area("Description", placeholder="e.g., A sleek, metallic feline that moves like lightning.")
    
    tier = st.select_slider(
        "Power Tier",
        options=["Baby", "Basic", "Final Evolution", "Legendary"],
        value="Basic"
    )

# --- 5. LOGIC: STAT CALCULATION ---
def calculate_stats(poke_type, desc, tier_choice):
    # Get averages for the chosen type
    type_averages = df[df['Type 1'] == poke_type].mean(numeric_only=True).to_dict()
    
    # Tier multipliers (scaling the base data)
    multipliers = {"Baby": 0.6, "Basic": 1.0, "Final Evolution": 1.3, "Legendary": 1.6}
    mult = multipliers[tier_choice]
    
    stats = {k: int(v * mult) for k, v in type_averages.items() if k in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']}
    
    # Description-based keyword modifiers
    keywords = {
        "fast": ("Speed", 1.2), "lightning": ("Speed", 1.2),
        "tank": ("Defense", 1.2), "bulky": ("Defense", 1.2), "sturdy": ("Defense", 1.2),
        "strong": ("Attack", 1.2), "vicious": ("Attack", 1.2), "sharp": ("Attack", 1.2),
        "smart": ("Sp. Atk", 1.2), "mystical": ("Sp. Atk", 1.2)
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
            st.subheader("Appearance")
            # Image Generation Prompt
            full_prompt = f"Official Ken Sugimori Pokemon style artwork of {name}, a {p_type} type pokemon. {description}. High quality, white background, digital art, clean lines."
            
            try:
                with st.spinner("AI is sketching your Pokémon..."):
                    response = openai.Image.create(
                        prompt=full_prompt,
                        n=1,
                        size="512x512"
                    )
                    image_url = response['data'][0]['url']
                    st.image(image_url, caption=f"A wild {name} appeared!")
            except Exception as e:
                st.error("Could not generate image. Check your API key or description.")
                st.info("Debugging info: " + str(e))
    else:
        st.error("Please provide both a Name and a Description!")