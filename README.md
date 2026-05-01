# Fakemon Website

> This is a streamlit repository. Live Website at https://fakemon.streamlit.app

<img width="1510" height="763" alt="Screenshot 2026-04-30 at 6 00 05 PM" src="https://github.com/user-attachments/assets/f6551440-0119-42a4-b49e-e17acf6fad29" />

# How to Create Your Own Fakemon Website!

### Fork this Github Repository (**IMPORTANT! Make Repo Public**)

> There are two options to fork the repo. 

1. Fork from Github
> <img width="146" height="58" alt="Screenshot 2026-04-30 at 6 07 57 PM" src="https://github.com/user-attachments/assets/3158540f-6143-4696-a1ba-a04eb0c817d5" />
2. Fork from Website
> - In the upper right hand corner you will find the fork option. <img width="134" height="58" alt="Screenshot 2026-04-30 at 6 03 02 PM" src="https://github.com/user-attachments/assets/88b498a4-6fef-4f13-81a4-0ad85079151c" />


### How to Set Up Streamlit

1. Create a Streamlit Account at https://https://share.streamlit.io/
2. Create a New Project and Link Repository from the top right hand corner of the Dashboard
> <img width="130" height="77" alt="Screenshot 2026-04-30 at 7 28 14 PM" src="https://github.com/user-attachments/assets/16decd31-f623-40ae-b737-73119b461368" />
3. Choose to Deploy a public app from Github
> <img width="331" height="243" alt="Screenshot 2026-04-30 at 7 29 55 PM" src="https://github.com/user-attachments/assets/a94a911f-7f77-43e0-b447-f9ab6263b9b1" />
4. Enter the url of your forked Repository.
> <img width="784" height="104" alt="Screenshot 2026-04-30 at 7 32 18 PM" src="https://github.com/user-attachments/assets/601ed6fc-24a8-4a0a-ac4e-0b7d0a40db45" />
5. Click Advanced Options and be ready to add API Keys later (For Database and OpenAI)
> <img width="733" height="386" alt="Screenshot 2026-04-30 at 7 33 26 PM" src="https://github.com/user-attachments/assets/2127912e-3a02-40fe-bb7a-96c647768794" />
6. Hit Deploy
> <img width="95" height="58" alt="Screenshot 2026-04-30 at 7 30 37 PM" src="https://github.com/user-attachments/assets/d2ba9a30-b408-4501-92c5-f35ac78b9fcd" />

### Managing Your OpenAI API Key

1. Create/Login to your OpenAI Account at https://auth.openai.com/log-in
2. Follow Website Instructions to Create an API key and load Credits (**Make sure to save API key code**)
> <img width="271" height="254" alt="Screenshot 2026-04-30 at 7 38 56 PM" src="https://github.com/user-attachments/assets/e250d221-a1c9-48f7-b96a-aa19a3294a05" />
3. Manage API keys by clicking on Dashboard
> <img width="199" height="105" alt="Screenshot 2026-04-30 at 7 40 21 PM" src="https://github.com/user-attachments/assets/f4eaf15c-4ae5-44bc-af78-aa1e6cf80d1f" />
4. Edit API key to have image generation permissions.
> <img width="188" height="81" alt="Screenshot 2026-04-30 at 7 42 36 PM" src="https://github.com/user-attachments/assets/9f16fa3e-a148-4699-a0ba-18d8a31834c4" />
5. Change to Request Image Permissions
> <img width="440" height="540" alt="Screenshot 2026-04-30 at 7 44 36 PM" src="https://github.com/user-attachments/assets/9e972eb8-35bb-4eac-8f47-fea4a486dcef" />

### How to Create Supabase DB

1. Create/Login to your Supabase Account at https://supabase.com/dashboard/sign-up
2. Create new Organization
> <img width="156" height="50" alt="Screenshot 2026-04-30 at 7 48 49 PM" src="https://github.com/user-attachments/assets/1a85d8f6-77b3-4cfd-b5f7-e3ed90d20b91" />
3. Create new Project
> <img width="188" height="50" alt="Screenshot 2026-04-30 at 7 49 39 PM" src="https://github.com/user-attachments/assets/2d215b2f-1a59-4a1e-8d30-7c0cb74eecfa" />
4. Move to Table Editor found on left ribbon on Dashboard
> <img width="196" height="126" alt="Screenshot 2026-04-30 at 7 51 46 PM" src="https://github.com/user-attachments/assets/24ccbdb5-fd67-4c56-ada8-420250948084" />
5. Create new Table and add Pokemon Datatypes (**Make sure to use same parameters**)
> <img width="241" height="136" alt="Screenshot 2026-04-30 at 7 53 06 PM" src="https://github.com/user-attachments/assets/e7777c83-db7c-429a-a362-44d30f388ad3" />
> <img width="633" height="544" alt="Screenshot 2026-04-30 at 7 54 03 PM" src="https://github.com/user-attachments/assets/80a80c5b-aaf0-4116-ad09-b3f5476322e8" />
6. Add Database Policies for `SELECT` and `INSERT` using RLS Policies
> <img width="203" height="140" alt="Screenshot 2026-04-30 at 7 55 52 PM" src="https://github.com/user-attachments/assets/d5202f7b-9a19-47a5-a810-5ee1fda14930" />
7. Create General Permission Policies for `SELECT` and `INSERT` using Supabase Default Templates
> <img width="994" height="336" alt="Screenshot 2026-04-30 at 7 57 40 PM" src="https://github.com/user-attachments/assets/df2f3930-0d92-4cad-aa78-631477b628dd" />
> <img width="1155" height="390" alt="Screenshot 2026-04-30 at 7 58 07 PM" src="https://github.com/user-attachments/assets/e3ad485a-9337-4752-a07d-1cb576938658" />
8. Go to Project Settings to find API keys
> <img width="199" height="564" alt="Screenshot 2026-04-30 at 8 01 55 PM" src="https://github.com/user-attachments/assets/920e88c1-b42d-41bf-9506-f721f682733a" />
9. Navigate to API key Settings
> <img width="247" height="236" alt="Screenshot 2026-04-30 at 8 02 40 PM" src="https://github.com/user-attachments/assets/80384326-74ea-40af-adb0-e3a037039ddf" />
10. Save `anon public key`
11. Save Database URL from General Settings
> <img width="288" height="367" alt="Screenshot 2026-04-30 at 8 04 02 PM" src="https://github.com/user-attachments/assets/62b2ed78-fd41-4171-bc7c-bcd2fbc602f1" />

### Pulling it all Togeather

1. Return to your Streamlit app and add the keys from OpenAI and the Database. These include `OPENAI_API_KEY`, `SUPABASE_URL`, and `SUPABASE_KEY`
> <img width="733" height="386" alt="Screenshot 2026-04-30 at 7 33 26 PM" src="https://github.com/user-attachments/assets/d547b58f-e9af-4047-a1f5-2b4d8cff9c7e" />
2. The App should now Run!

# Going over `app.py` file

1. The streamlit library covers css and html elements so we can just call different elements from the st library.
2. Lets go over individual methods.
> 1. `save_pokemon_to_db(pokemon_entry)`
>   - this sends an `INSERT` request to the supabase db to add the pokemon_entry data to the database
> 2. `load_pokemon_from_db()`
>   - this requests the pokemon data from the supabase db using `SELECT`
> 3. `calculate_stats(poke_type, desc, tier_choice)`
>   - this calculate the stats of the new pokemon based off of the type, description, and tier of the pokemon
>   - admittedly this function is very simple and linear. there is definettly room to improve the functionality of how stats are generated.
> 4. `get_safe_prompt(name, p_type, desc)`
>   - this method creates and prompt engineers the text that will be sent to the OpenAI image generation model.
