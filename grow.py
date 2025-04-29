import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import random
# Removed PIL import as it's not explicitly used after photo upload refactor
# from PIL import Image
# Removed os import as it's not used
# import os
import pandas as pd
import numpy as np
import time
import io  # Needed for handling uploaded file bytes for display

# ------ PAGE CONFIGURATION ------
st.set_page_config(
    page_title="Growvertising - Billboard to Farmboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------ CSS STYLING ------
st.markdown("""
<style>
    .main-title {
        font-size: 42px !important;
        color: #2E7D32;
        text-align: center;
    }
    .sub-title {
        font-size: 28px !important;
        color: #388E3C;
    }
    .sidebar-text {
        font-size: 16px;
    }
    .highlight {
        background-color: #E8F5E9;
        padding: 10px;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #F1F8E9;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px; /* Add some spacing */
    }
    /* Ensure buttons within columns are aligned well */
    .stButton>button {
        width: 100%;
        margin-bottom: 5px;
    }
    /* Style containers for better visual separation */
    .stContainer {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ------ AUTHENTICATION ------
def setup_authentication():
    """Sets up user authentication using streamlit-authenticator."""
    # In a production app, this would be stored securely (e.g., env variables, secrets manager)
    # For simplicity, using a dictionary here.
    # IMPORTANT: Passwords should be hashed in a real application!
    # Use the hashing utility provided by streamlit-authenticator to generate hashes.
    # Example:
    # import streamlit_authenticator as stauth
    # hashed_passwords = stauth.Hasher(['pass123', 'sponsorpass', 'admin123']).generate()
    # print(hashed_passwords) # Use these hashes below
    
    hashed_passwords = {
        'pass123': '$2b$12$Eix1jN0Lw1T9f5uW9lQ.Aua1J3Z/W5B.E5f8k/2R3r7Z.zXwXy9hW', # Hashed 'pass123'
        'sponsorpass': '$2b$12$hP7.Q9rM2r.o5uJ1eX3zIuO/kL.p9T/yG4N7nE.f8U.l6W/t2v.yK', # Hashed 'sponsorpass'
        'admin123': '$2b$12$S.N0wU1xL9o3m.P5q/R7r.uH/jK.zW8B.g9T/l2X.e5f8k/v1N.hG' # Hashed 'admin123' - Replace with actual hash
    }
    
    credentials_dict = {
        "usernames": {
            "growuser": {"name": "Green User", "password": hashed_passwords['pass123'], "email": "growuser@example.com"},
            "sponsor1": {"name": "Sponsor One", "password": hashed_passwords['sponsorpass'], "email": "sponsor1@example.com"},
            "admin": {"name": "Admin User", "password": hashed_passwords['admin123'], "email": "admin@example.com"}
        }
    }
    
    authenticator = stauth.Authenticate(
        credentials_dict['usernames'], # Pass the usernames dict directly
        "growvertising_app_cookie",    # Cookie name, unique for the app
        "abcdefg_random_key_12345",    # Secret key, should be complex and stored securely
        cookie_expiry_days=30,
        # preauthorized=None # Optional: preauthorized emails
    )
    
    # FIX: Correct parameter order - 'Login' is the label, 'sidebar' is the location
    name, auth_status, username = authenticator.login('Login', 'sidebar')
    
    # Handle authentication status
    if auth_status is False:
        st.sidebar.error("Invalid username/password")
        st.warning("Please log in to access the app.")
        st.stop()
    elif auth_status is None:
        st.sidebar.warning("Please enter your credentials")
        st.warning("Please log in to access the app.")
        st.stop()
    elif auth_status is True:
        # Store user role in session state upon successful login
        if username == "admin":
            st.session_state["user_role"] = "admin"
        elif username == "sponsor1":
            st.session_state["user_role"] = "sponsor"
        else:
            st.session_state["user_role"] = "user"
        
        # Display welcome message and logout button
        st.sidebar.success(f"Welcome, {name}!")
        authenticator.logout("Logout", "sidebar")
        
        return name, username
    
    # Should not reach here if logic above is correct, but added for safety
    st.stop()


# ------ DATA INITIALIZATION ------
def initialize_data():
    """Initializes session state variables and static data."""
    # Initialize session state variables if they don't exist
    if "comments" not in st.session_state:
        st.session_state["comments"] = []
    
    if "uploads" not in st.session_state:
        # Store simplified upload data (bytes, caption, etc.) instead of UploadedFile object
        st.session_state["uploads"] = []
    
    if "plants_grown" not in st.session_state:
        st.session_state["plants_grown"] = random.randint(1000, 1500) # More dynamic start
    
    if "co2_offset" not in st.session_state:
        st.session_state["co2_offset"] = random.randint(300, 500)
    
    if "seed_kits" not in st.session_state:
        st.session_state["seed_kits"] = random.randint(700, 1000)
    
    if "last_visit" not in st.session_state:
        st.session_state["last_visit"] = datetime.now()
    
    # Initialize user plants if not present
    if "user_plants" not in st.session_state:
        st.session_state["user_plants"] = [
            {"name": "Tomato", "progress": random.randint(20, 95), "days_old": random.randint(5, 30), "planted_date": datetime(2025, 1, 15)},
            {"name": "Basil", "progress": random.randint(20, 95), "days_old": random.randint(5, 30), "planted_date": datetime(2025, 2, 3)}
        ]
        
    if "user_plant_history" not in st.session_state:
         st.session_state["user_plant_history"] = [
                {"Plant Type": "Lettuce", "Date Planted": "2025-02-28", "Harvest Date": "2025-04-10", "Success": "Yes"},
                {"Plant Type": "Spinach", "Date Planted": "2025-03-10", "Harvest Date": "Failed", "Success": "No"}
            ]
        
    # Billboard data
    billboards = {
        "Grow Your Greens": {
            "url": "https://i.imgur.com/U4A0lRQ.jpg",
            "description": "A campaign promoting home vegetable gardening for urban dwellers.",
            "sponsor": "OrganicFoods Co."
        },
        "From Message to Meal": {
            "url": "https://i.imgur.com/GQhuf0U.jpg",
            "description": "An initiative turning advertising space into food production.",
            "sponsor": "EcoEats"
        },
        "Food Waste Awareness": {
            "url": "https://i.imgur.com/XY5NJJx.jpg",
            "description": "Highlighting the importance of reducing food waste in our communities.",
            "sponsor": "WasteNot Foundation"
        },
        "Urban Farming Revolution": {
            "url": "https://i.imgur.com/U4A0lRQ.jpg", # Using same image for example
            "description": "Transforming city spaces into productive green gardens.",
            "sponsor": "CityGrow Initiative"
        }
    }
    
    return billboards

# ------ SIDEBAR CONTENT ------
def display_sidebar(name, username):
    """Displays the navigation sidebar and user profile info."""
    st.sidebar.markdown("## 🌿 Navigation")
    
    available_pages = ["Home", "My Plants", "Community"]
    if st.session_state.get("user_role") in ["sponsor", "admin"]:
        available_pages.append("Sponsor Dashboard")
    if st.session_state.get("user_role") == "admin":
        available_pages.append("Admin Panel")

    # Determine default index based on role if needed, otherwise 0
    default_index = 0 
    
    page = st.sidebar.radio(
        "Go to",
        available_pages,
        index=default_index,
        key="navigation_radio" # Add a key for stability
    )
    
    st.sidebar.markdown("---")
    
    # Display dynamic user stats (simplified for demo)
    activity_score = random.randint(10, 100) # Example score
    if activity_score > 80:
        badge = "🌟 Super Grower"
    elif activity_score > 50:
        badge = "🌿 Urban Farmer"
    else:
        badge = "🍀 Green Starter"
    
    st.sidebar.markdown(f"### Your Profile ({username})") # Show username
    st.sidebar.markdown(f"**Badge:** {badge}")
    st.sidebar.progress(activity_score / 100)
    # Link plants grown to session state if possible, otherwise random example
    plants_grown_user = len(st.session_state.get("user_plants", []))
    st.sidebar.markdown(f"**Plants Currently Growing:** {plants_grown_user}")
    st.sidebar.markdown(f"**Est. CO₂ Offset:** {plants_grown_user * random.randint(2, 5)} kg") # Example calculation
    
    # Help section
    with st.sidebar.expander("Need Help?"):
        st.markdown("""
        - **Home**: View billboard campaigns and track progress.
        - **My Plants**: Manage your growing plants.
        - **Community**: Share photos and interact with others.
        - **Sponsor Dashboard**: (Sponsors/Admin) View campaign metrics.
        - **Admin Panel**: (Admin) Manage users and content.
        - **Support**: Email help@growvertising.com
        """)
    
    return page

# ------ HOME PAGE ------
def display_home(billboards):
    """Displays the main home page with billboard previews and stats."""
    st.markdown("<h1 class='main-title'>🌿 Growvertising – Billboard to Farmboard</h1>", unsafe_allow_html=True)
    st.markdown("Turn every ad into action – grow plants, offset carbon, and join the green movement.")
    
    # --- Overall Impact Metrics ---
    st.markdown("<h2 class='sub-title'>🌍 Overall Impact</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Plants Grown", f"{st.session_state['plants_grown']} 🌱")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Community CO₂ Offset", f"{st.session_state['co2_offset']} kg")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Seed Kits Distributed", f"{st.session_state['seed_kits']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---") # Separator

    # --- Billboard Preview Section ---
    st.markdown("<h2 class='sub-title'>🖼️ Featured Campaigns</h2>", unsafe_allow_html=True)
    
    selected_ad = st.selectbox("Select Campaign", list(billboards.keys()), key="campaign_select")
    
    col_img, col_details = st.columns([2, 1])
    with col_img:
        st.image(billboards[selected_ad]["url"], caption=selected_ad, use_column_width='always')
    
    with col_details:
        st.markdown(f"### Campaign Details")
        st.markdown(f"**Description:** {billboards[selected_ad]['description']}")
        st.markdown(f"**Sponsor:** {billboards[selected_ad]['sponsor']}")
        st.markdown("---")
        
        # Add interaction options
        st.markdown("### Get Involved")
        if st.button("Request Seed Kit", key=f"seed_kit_{selected_ad}"):
            st.session_state["seed_kits"] += 1
            st.success("Seed kit request submitted! Check your email for details.")
            st.balloons() # Add visual feedback
        
        if st.button("Support This Campaign", key=f"support_{selected_ad}"):
            # In a real app, this might track support or link to a donation page
            st.balloons()
            st.success("Thank you for your support!")
    
    st.markdown("---") # Separator

    # --- Growth Simulation --- (Simplified for demo)
    st.markdown("<h2 class='sub-title'>🌱 Simulated Billboard Growth</h2>", unsafe_allow_html=True)
    st.info("This section shows a simulated representation of plant growth on a physical billboard.")
    
    col_growth, col_days, col_water = st.columns(3)
    with col_growth:
        # Use a fixed or slowly changing value for demo, slider is less intuitive here
        growth_percentage = random.randint(60, 90) # Example dynamic value
        st.progress(growth_percentage / 100)
        st.markdown(f"**Growth Level:** {growth_percentage}%")
    
    with col_days:
        days_remaining = max(0, 30 - int((growth_percentage / 100) * 30)) # Assuming 30 day cycle
        delta_days = -1 if days_remaining < 30 else 0 # Simple indicator of progress
        st.metric("Est. Days Until Harvest", f"{days_remaining} days", f"{delta_days} vs yesterday")
    
    with col_water:
         # Simplified status display
        water_status = random.choice(["Optimal", "Needs Water", "Slightly Dry"])
        st.metric("Water Level Status", water_status)
        if water_status == "Needs Water":
            st.warning("💧 Water levels are low!")
        elif water_status == "Optimal":
            st.success("💧 Water levels are good.")

    # --- Growing Conditions --- (Example static data)
    st.markdown("<h2 class='sub-title'>🌤️ Current Conditions (Example Location)</h2>", unsafe_allow_html=True)
    
    col_cond1, col_cond2, col_cond3, col_cond4 = st.columns(4)
    with col_cond1:
        st.metric("Temperature", "24°C", "+1.5°C")
    with col_cond2:
        st.metric("Humidity", "65%", "-3%")
    with col_cond3:
        st.metric("Sunlight", "Good", "UV Index: 6")
    with col_cond4:
        st.metric("Soil Moisture", "Okay", "-2%")

# ------ MY PLANTS PAGE ------
def display_my_plants():
    """Displays the user's plant management page."""
    st.markdown("<h1 class='sub-title'>🌱 My Plants</h1>", unsafe_allow_html=True)
    st.markdown("Track and manage the plants you are growing.")
    
    plant_types = ["Tomato", "Basil", "Lettuce", "Spinach", "Mint", "Pepper", "Chives"]
    
    col_manage, col_add = st.columns([2, 1])
    
    with col_manage:
        tab_current, tab_history = st.tabs(["Current Plants", "Plant History"])
        
        with tab_current:
            st.markdown("### Plants Currently Growing")
            if not st.session_state.get("user_plants"):
                st.info("You haven't added any plants yet. Use the form on the right to start growing!")
            else:
                # Iterate through user's plants stored in session state
                for i, plant_data in enumerate(st.session_state["user_plants"]):
                    with st.container(): # Use container for better separation
                        st.markdown(f"#### {plant_data['name']}")
                        st.progress(plant_data['progress'] / 100)
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.markdown(f"**Progress:** {plant_data['progress']}%")
                        with col_b:
                            # Calculate days old based on stored planted date
                            days_old = (datetime.now() - plant_data['planted_date']).days
                            st.markdown(f"**Days old:** {days_old}")
                        with col_c:
                            health = 'Good' if plant_data['progress'] > 60 else 'Needs Attention' if plant_data['progress'] > 30 else 'Struggling'
                            st.markdown(f"**Health:** {health}")

                        # Add action buttons
                        col_actions1, col_actions2 = st.columns(2)
                        with col_actions1:
                            if st.button("Update Progress", key=f"update_{i}"):
                                # Placeholder for update logic (e.g., modal popup)
                                st.session_state["user_plants"][i]["progress"] = min(100, plant_data['progress'] + random.randint(5,15))
                                st.rerun() # Rerun to show updated progress
                        with col_actions2:
                            if st.button("Mark as Harvested/Finished", key=f"finish_{i}"):
                                harvested_plant = st.session_state["user_plants"].pop(i)
                                # Add to history
                                st.session_state["user_plant_history"].append({
                                    "Plant Type": harvested_plant['name'],
                                    "Date Planted": harvested_plant['planted_date'].strftime('%Y-%m-%d'),
                                    "Harvest Date": datetime.now().strftime('%Y-%m-%d'),
                                    "Success": "Yes" # Assume success for now
                                })
                                st.success(f"{harvested_plant['name']} moved to history.")
                                st.rerun() # Rerun to update the list

                        st.markdown("---") # Separator between plants
        
        with tab_history:
            st.markdown("### Past Plants")
            if not st.session_state.get("user_plant_history"):
                 st.info("No plant history yet.")
            else:
                history_df = pd.DataFrame(st.session_state["user_plant_history"])
                st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with col_add:
        st.markdown("### Add New Plant")
        with st.form("add_plant_form", clear_on_submit=True):
            new_plant_type = st.selectbox("Plant Type", plant_types, key="new_plant_type")
            plant_date = st.date_input("Planting Date", datetime.now().date(), key="new_plant_date")
            notes = st.text_area("Notes (optional)", key="new_plant_notes")
            
            submitted = st.form_submit_button("Start Growing")
            if submitted:
                # Add the new plant to session state
                st.session_state["user_plants"].append({
                    "name": new_plant_type,
                    "progress": random.randint(5, 15), # Start with low progress
                    "planted_date": datetime.combine(plant_date, datetime.min.time()), # Combine date with time
                    "notes": notes
                })
                st.success(f"Added {new_plant_type} to your garden!")
                st.balloons()
                # No need to rerun here, adding to list is enough unless you need immediate display update handled differently
        
        st.markdown("---")
        st.markdown("### Plant Care Tips")
        tip = random.choice([
            "Tomatoes love sunlight! Ensure they get at least 6-8 hours daily.",
            "Basil prefers consistently moist soil. Water when the top inch feels dry.",
            "Lettuce can bolt (go to seed) in hot weather. Provide some afternoon shade.",
            "Rotate your crops each season to prevent soil depletion and pests.",
            "Check for common pests like aphids regularly. Neem oil can be an organic solution."
        ])
        st.info(f"💡 Tip: {tip}")
        
        st.markdown("### Upcoming Tasks (Example)")
        st.markdown("- Water tomato plants (check soil first)")
        st.markdown("- Harvest outer lettuce leaves soon")
        st.markdown("- Consider adding organic fertilizer to basil")

# ------ COMMUNITY PAGE ------
def display_community(current_user_name):
    """Displays the community interaction page."""
    st.markdown("<h1 class='sub-title'>👨‍👩‍👧‍👦 Community Hub</h1>", unsafe_allow_html=True)
    st.markdown("Share your progress, ask questions, and connect with fellow growers!")
    
    tab_photos, tab_comments = st.tabs(["📸 Photo Wall", "💬 Discussion Forum"])
    
    with tab_photos:
        st.markdown("### Share Your Plant Photos")
        
        # Photo upload area
        uploaded_file = st.file_uploader(
            "Upload a photo of your plants!",
            type=["jpg", "png", "jpeg"],
            key="photo_uploader"
        )
        caption = st.text_input("Caption for your photo", key="photo_caption")
        location = st.text_input("Location (optional, e.g., 'City, State')", key="photo_location")
        
        if st.button("Upload Photo", key="upload_photo_btn") and uploaded_file is not None:
            if caption:
                # Read the file content as bytes
                image_bytes = uploaded_file.getvalue()
                
                # Store necessary info in session state (NOT the UploadedFile object)
                st.session_state["uploads"].append({
                    "image_bytes": image_bytes, # Store bytes
                    "caption": caption,
                    "location": location if location else "Unknown Location",
                    "user": current_user_name,
                    "timestamp": datetime.now(),
                    "likes": 0
                })
                st.success("Photo uploaded successfully! 🌿")
                st.rerun() # Rerun to display the new photo immediately
            else:
                st.warning("Please add a caption for your photo.")
        elif st.button("Upload Photo", key="upload_photo_btn_clicked_no_file") and uploaded_file is None:
             st.warning("Please select a photo file first.")


        st.markdown("---")
        st.markdown("### Recent Community Photos")
        
        # Display uploaded photos from session state
        if not st.session_state.get("uploads"):
            st.info("No photos shared yet. Be the first!")
        else:
            # Display user uploads in reverse chronological order
            num_photos = len(st.session_state["uploads"])
            cols = st.columns(3) # Display in 3 columns
            
            for i, upload in enumerate(reversed(st.session_state["uploads"])):
                col_index = i % 3
                with cols[col_index]:
                    with st.container():
                        try:
                             # Display image from bytes
                            st.image(upload["image_bytes"], caption=f"{upload['caption']} ({upload['user']})", use_column_width='always')
                        except Exception as e:
                             st.error(f"Could not display image: {e}") # Handle potential errors loading image data

                        like_key = f"like_photo_{upload['timestamp'].isoformat()}" # Unique key using timestamp
                        likes = upload.get("likes", 0) # Default to 0 likes if key missing
                        
                        if st.button(f"❤️ {likes} Like", key=like_key):
                            # Find the original upload and increment its likes
                            for original_upload in st.session_state["uploads"]:
                                if original_upload["timestamp"] == upload["timestamp"]:
                                     original_upload["likes"] = original_upload.get("likes", 0) + 1
                                     break
                            st.rerun() # Rerun to update the like count display

                        st.caption(f"📍 {upload['location']} | ⏰ {upload['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                        # Add a small visual separator within the column if needed
                        # st.markdown("---")
    
    with tab_comments:
        st.markdown("### 💬 Community Discussion")
        
        # Comment form
        with st.form("comment_form", clear_on_submit=True):
            comment_text = st.text_area("Leave a message, tip, or question for the community!", max_chars=300, height=100, key="comment_text_area")
            submitted = st.form_submit_button("Post Comment")
            
            if submitted and comment_text:
                st.session_state["comments"].append({
                    "user": current_user_name, # Use logged-in user's name
                    "comment": comment_text,
                    "timestamp": datetime.now(), # Store datetime object
                    "likes": 0
                })
                st.success("Comment posted! 💬")
                # Rerun optional, depending on desired UX
            elif submitted and not comment_text:
                st.warning("Please enter a comment before posting.")
        
        st.markdown("---")
        st.markdown("### Recent Comments:")
        
        # Add sample comments if none exist (only on first load ideally)
        if not st.session_state.get("comments"):
             # Add sample comments only if the list is empty
             if not st.session_state.get("comments_initialized"):
                 sample_comments = [
                    {"user": "GreenThumb", "comment": "Just harvested my first batch of tomatoes! Can't believe how well they turned out.", "timestamp": datetime(2025, 4, 25, 14, 32), "likes": 12},
                    {"user": "PlantLover", "comment": "Has anyone had issues with yellowing leaves on their basil plants? Looking for advice!", "timestamp": datetime(2025, 4, 26, 9, 15), "likes": 8},
                    {"user": "UrbanFarmer", "comment": "The community garden project is coming along nicely! Check out our progress photos.", "timestamp": datetime(2025, 4, 27, 16, 45), "likes": 15}
                 ]
                 st.session_state["comments"] = sample_comments
                 st.session_state["comments_initialized"] = True # Flag to prevent re-adding samples

        # Display comments
        if not st.session_state.get("comments"):
             st.info("No comments yet. Start the conversation!")
        else:
             # Display comments in reverse chronological order
             for i, entry in enumerate(reversed(st.session_state["comments"])):
                 with st.container():
                     st.markdown(f"**{entry['user']}** ({entry['timestamp'].strftime('%Y-%m-%d %H:%M')})")
                     st.markdown(f"> {entry['comment']}")
                     
                     like_key = f"like_comment_{entry['timestamp'].isoformat()}" # Unique key using timestamp
                     likes = entry.get("likes", 0)
                     
                     # Use a small button for likes to take less space
                     if st.button(f"❤️ {likes}", key=like_key, help="Like this comment"):
                          # Find the original comment and increment its likes
                          for original_comment in st.session_state["comments"]:
                              if original_comment["timestamp"] == entry["timestamp"]:
                                   original_comment["likes"] = original_comment.get("likes", 0) + 1
                                   break
                          st.rerun() # Update display
                     
                     st.markdown("---") # Separator

# ------ SPONSOR DASHBOARD ------
def display_sponsor_dashboard():
    """Displays the dashboard for sponsors."""
    st.markdown("<h1 class='sub-title'>📊 Sponsor Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Monitor the impact and performance of sponsored campaigns.")
    
    # Key metrics - Use session state values
    st.markdown("### Key Performance Metrics (Overall)")
    
    col1, col2, col3 = st.columns(3)
    # Use try-except or .get for safety if session state might not be initialized
    plants_grown = st.session_state.get('plants_grown', 0)
    co2_offset = st.session_state.get('co2_offset', 0)
    seed_kits = st.session_state.get('seed_kits', 0)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Plants Grown (All Campaigns)", f"{plants_grown} 🌱", f"+{random.randint(50,150)} this week")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Estimated CO₂ Offset", f"{co2_offset} kg", f"+{random.randint(10, 40)} kg")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Seed Kits Distributed", f"{seed_kits}", f"+{random.randint(30, 80)}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Campaign performance - Use more realistic data generation
    st.markdown("### Campaign Performance Analysis")
    
    # Generate sample data for charts
    campaign_names = ['Grow Your Greens', 'From Message to Meal', 'Food Waste Awareness', 'Urban Farming']
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # Simulate engagement (e.g., clicks, kit requests per campaign)
    engagement_data = pd.DataFrame(
        np.random.randint(10, 100, size=(30, len(campaign_names))),
        index=dates,
        columns=campaign_names
    ) * [1.5, 1.2, 0.8, 1.0] # Weight campaigns differently
    
    # Simulate growth rate (e.g., % completion or plants added daily)
    growth_data = pd.DataFrame(
        np.random.rand(30, len(campaign_names)) * 5, # Simulate small daily growth %
        index=dates,
        columns=campaign_names
    ).cumsum() # Cumulative growth
    
    
    tab_engage, tab_growth, tab_roi = st.tabs(["📈 Engagement Trends", "🌱 Growth Rate", "💰 ROI Metrics (Example)"])
    
    with tab_engage:
        st.line_chart(engagement_data)
        st.caption("Simulated daily engagement (e.g., interactions, kit requests) across campaigns (last 30 days)")
    
    with tab_growth:
        st.area_chart(growth_data)
        st.caption("Simulated cumulative growth contribution per campaign (last 30 days)")
        
    with tab_roi:
        st.markdown("#### Return on Investment (Illustrative)")
        # Example ROI calculation - replace with real data
        investment = {"Grow Your Greens": 15000, "From Message to Meal": 12000, "Food Waste Awareness": 8000, "Urban Farming": 10000}
        # Calculate a simple 'value' metric (e.g., based on plants + CO2 offset)
        value_generated = (engagement_data.sum() * 0.5 + growth_data.iloc[-1] * 10).round(0) # Example formula
        
        roi_data = []
        for campaign in campaign_names:
             cost = investment.get(campaign, 1) # Avoid division by zero
             value = value_generated.get(campaign, 0)
             roi_percent = ((value - cost) / cost) * 100 if cost > 0 else 0
             roi_data.append({"Campaign": campaign, "Investment ($)": cost, "Estimated Value ($)": value, "ROI (%)": roi_percent})
        
        roi_df = pd.DataFrame(roi_data)
        st.dataframe(roi_df.set_index("Campaign"), use_container_width=True)
        st.caption("Note: Value and ROI calculations are illustrative examples.")

    st.markdown("---")

    # Campaign management (Simplified for demo)
    st.markdown("### Campaign Management")
    
    with st.expander("🚀 Launch New Campaign (Example Form)"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", key="sponsor_camp_name")
            campaign_desc = st.text_area("Campaign Description", key="sponsor_camp_desc")
            target_audience = st.multiselect(
                "Target Audience",
                ["Urban Dwellers", "Families", "Students", "Seniors", "Businesses", "Eco-conscious"],
                key="sponsor_camp_audience"
                )
        
        with col2:
            campaign_budget = st.number_input("Budget ($)", min_value=1000, max_value=100000, value=10000, step=500, key="sponsor_camp_budget")
            start_date = st.date_input("Start Date", key="sponsor_camp_start")
            end_date = st.date_input("End Date", key="sponsor_camp_end")
            uploaded_image = st.file_uploader("Upload Billboard Image", type=['png', 'jpg', 'jpeg'], key="sponsor_camp_img")

        if st.button("Submit Campaign Proposal", key="sponsor_camp_submit"):
             if campaign_name and campaign_desc and campaign_budget and start_date and end_date and start_date <= end_date:
                 st.success("Campaign proposal submitted for review by the Growvertising team!")
                 # In a real app, this data would be saved to a database.
             elif not campaign_name or not campaign_desc:
                 st.warning("Please fill in Campaign Name and Description.")
             elif start_date > end_date:
                  st.error("End Date cannot be before Start Date.")
             else:
                  st.warning("Please fill in all required fields.")

    st.markdown("---")
    
    # Community analytics (More detailed examples)
    st.markdown("### Community Analytics")
    
    col_demo, col_engage = st.columns(2)
    with col_demo:
        st.markdown("#### User Demographics (Sample)")
        # More realistic demographic data
        age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
        percentages = [18, 35, 25, 15, 7]
        demo_data = pd.DataFrame({"Age Group": age_groups, "Percentage": percentages})
        st.bar_chart(demo_data.set_index("Age Group"))
        st.caption("Distribution of active users by age group.")
    
    with col_engage:
        st.markdown("#### Top Engaging Content (Sample)")
        # Example data on content performance
        engagement_data = {
            "Content Type": ["Photo Uploads", "Comments", "Likes (Photos)", "Likes (Comments)", "Seed Kit Claims"],
            "Count (Last 30d)": [len(st.session_state.get('uploads',[])), len(st.session_state.get('comments',[])), sum(u.get('likes',0) for u in st.session_state.get('uploads',[])), sum(c.get('likes',0) for c in st.session_state.get('comments',[])), st.session_state.get('seed_kits', 0) - random.randint(50,100)] # Example counts
        }
        engage_df = pd.DataFrame(engagement_data)
        st.bar_chart(engage_df.set_index("Content Type"))
        st.caption("User interactions with community features.")
    
    st.markdown("---")

    # Download reports
    st.markdown("### Download Reports")
    report_type = st.selectbox(
        "Select Report Type",
        ["Campaign Performance Summary", "User Engagement Analysis", "Environmental Impact Estimate", "Financial Overview"],
        key="report_type_select"
        )
    col_format, col_generate = st.columns([1, 2])
    with col_format:
        report_format = st.radio("Report Format", ["CSV", "PDF"], key="report_format_radio") # Offer CSV and PDF
    with col_generate:
        report_filename = f"{report_type.lower().replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d')}.{report_format.lower()}"
        
        # Generate sample data based on report type
        if report_type == "Campaign Performance Summary":
            # Use engagement data for CSV
            report_data_df = engagement_data.reset_index().rename(columns={'index': 'Date'})
            report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
            report_data_pdf = b"Sample PDF data for Campaign Performance" # Placeholder for PDF generation
        elif report_type == "User Engagement Analysis":
             report_data_df = engage_df
             report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
             report_data_pdf = b"Sample PDF data for User Engagement" # Placeholder
        else: # Default/Other reports
            report_data_df = pd.DataFrame({'Info': ["Data not available for this sample report"]})
            report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
            report_data_pdf = b"Sample PDF data for selected report" # Placeholder
            
        report_data = report_data_csv if report_format == "CSV" else report_data_pdf
        mime_type = "text/csv" if report_format == "CSV" else "application/pdf"

        if st.button("Generate & Download Report", key="generate_report_btn"):
            with st.spinner("Generating report..."):
                time.sleep(1.5) # Simulate generation time
                st.download_button(
                    label=f"Click to Download {report_format}",
                    data=report_data,
                    file_name=report_filename,
                    mime=mime_type,
                    key="download_report_final"
                )
            st.success(f"{report_type} report ready for download.")


# ------ ADMIN PANEL ------
def display_admin_panel():
    """Displays the administrative panel for managing the app."""
    st.markdown("<h1 class='sub-title'>🔧 Admin Panel</h1>", unsafe_allow_html=True)
    st.warning("⚠️ Administrative actions can impact the entire application. Proceed with caution.")
    
    admin_tabs = st.tabs(["👤 User Management", "💬 Content Moderation", "📈 System Statistics", "⚙️ Settings & Maintenance"])

    with admin_tabs[0]:
        st.markdown("### User Management")
        
        # Fetch user data (example - replace with actual user fetching)
        # In a real app, you'd load this from your database or user store
        users_data = {
            "Username": ["growuser", "sponsor1", "admin", "greenthumb", "plantlover", "newuser"],
            "Name": ["Green User", "Sponsor One", "Admin User", "Gaia Green", "Peter Plant", "Nina New"],
            "Role": ["user", "sponsor", "admin", "user", "user", "user"],
            "Email": ["g@e.com", "s@e.com", "a@e.com", "gg@e.com", "pp@e.com", "nn@e.com"],
            "Last Login": pd.to_datetime(["2025-04-28", "2025-04-27", "2025-04-28", "2025-04-25", "2025-04-26", None]),
            "Status": ["Active", "Active", "Active", "Active", "Active", "Pending"]
        }
        users_df = pd.DataFrame(users_data)
        
        st.info("Select rows to perform actions like Edit Role or Change Status.")
        edited_df = st.data_editor(
            users_df,
            use_container_width=True,
            num_rows="dynamic", # Allow adding/deleting rows (careful in production)
            hide_index=True,
            # Configure column types for better editing
            column_config={
                 "Role": st.column_config.SelectboxColumn("Role", options=["user", "sponsor", "admin"], required=True),
                 "Status": st.column_config.SelectboxColumn("Status", options=["Active", "Inactive", "Pending", "Banned"], required=True),
                 "Last Login": st.column_config.DatetimeColumn("Last Login", format="YYYY-MM-DD HH:mm"),
                 "Email": st.column_config.TextColumn("Email", validate="^.+@.+.[a-zA-Z]+$"), # Basic email validation
            },
            key="user_data_editor"
        )
        
        if st.button("Save User Changes", key="save_users"):
             # In a real app, validate changes and save back to the database
             st.session_state['edited_users_df'] = edited_df # Store edited df for potential use
             st.success("User changes staged (in a real app, this would save to DB).")
             st.dataframe(edited_df, use_container_width=True, hide_index=True) # Show the edited df

        st.markdown("---")
        st.markdown("#### Bulk Actions (Example)")
        selected_action = st.selectbox("Select Action", ["None", "Set Status to Inactive", "Set Status to Active", "Delete Selected Users (Caution!)"], key="bulk_action")
        if selected_action != "None" and st.button(f"Apply Action: {selected_action}", key="apply_bulk"):
             st.warning(f"Bulk action '{selected_action}' would be applied here (simulation).")
             # Add logic here to apply action to selected rows in the data editor if needed

    with admin_tabs[1]:
        st.markdown("### Content Moderation")
        
        mod_tabs = st.tabs(["Pending Photos", "Reported Comments", "Flagged Users"])
        
        with mod_tabs[0]:
            st.markdown("#### Photos Pending Review")
            # Mock pending photos (in real app, query DB for status='pending')
            # Use uploads from session state for demo, filter by a hypothetical 'status'
            pending_photos = [up for up in st.session_state.get("uploads", []) if up.get("status") == "pending"]
            
            if not pending_photos:
                 # Add mock data if empty for demo purposes
                 pending_photos = [
                      {"id": f"photo_{random.randint(1000,9999)}", "user": "plantlover", "caption": "My new garden setup", "timestamp": datetime.now() - pd.Timedelta(hours=2), "image_bytes": None, "status": "pending"}, # Add placeholder image bytes if needed
                      {"id": f"photo_{random.randint(1000,9999)}", "user": "greenthumb", "caption": "Urban farming initiative progress", "timestamp": datetime.now() - pd.Timedelta(hours=1), "image_bytes": None, "status": "pending"}
                 ]

            if not pending_photos:
                 st.info("No photos currently pending review.")
            else:
                 for i, photo in enumerate(pending_photos):
                     with st.container():
                         st.markdown(f"**User:** {photo['user']} | **Posted:** {photo['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                         st.markdown(f"**Caption:** {photo['caption']}")
                         if photo.get('image_bytes'):
                              st.image(photo['image_bytes'], width=200) # Show thumbnail
                         else:
                              st.markdown("*(Image preview not available in this demo)*")

                         col1, col2, col3 = st.columns(3)
                         with col1:
                             if st.button("Approve", key=f"approve_photo_{photo['id']}"):
                                 # Logic to update photo status to 'approved' in DB
                                 st.success(f"Photo approved!")
                                 # Remove from pending list (or update status in real app)
                                 photo['status'] = 'approved' # Simulate status change
                                 st.rerun()
                         with col2:
                             if st.button("Reject", key=f"reject_photo_{photo['id']}"):
                                 # Logic to update photo status to 'rejected' or delete
                                 st.error(f"Photo rejected!")
                                 photo['status'] = 'rejected' # Simulate status change
                                 st.rerun()
                         with col3:
                             # Optional: Flag user action
                             if st.button("Flag User", key=f"flag_user_photo_{photo['id']}"):
                                  st.warning(f"User '{photo['user']}' flagged for review.")
                                  # Add logic to flag the user in the user management system
                         st.markdown("---")

        with mod_tabs[1]:
            st.markdown("#### Reported Comments")
            # Mock reported comments (query DB for status='reported')
            reported_comments = [c for c in st.session_state.get("comments", []) if c.get("status") == "reported"]

            if not reported_comments:
                 # Add mock data if empty for demo purposes
                 reported_comments = [
                      {"id": f"comment_{random.randint(1000,9999)}", "user": "SpamBot", "comment": "Buy cheap widgets now! www.spam.com", "timestamp": datetime.now() - pd.Timedelta(days=1), "reported_by": "greenthumb", "status": "reported"},
                      {"id": f"comment_{random.randint(1000,9999)}", "user": "RudeUser", "comment": "Your plants look terrible!", "timestamp": datetime.now() - pd.Timedelta(hours=5), "reported_by": "plantlover", "status": "reported"}
                 ]

            if not reported_comments:
                 st.info("No comments currently reported.")
            else:
                 for i, comment in enumerate(reported_comments):
                     with st.container():
                         st.markdown(f"**User:** {comment['user']} | **Reported by:** {comment.get('reported_by', 'Unknown')}")
                         st.markdown(f"**Comment:**")
                         st.markdown(f"> {comment['comment']}")
                         st.caption(f"Posted: {comment['timestamp'].strftime('%Y-%m-%d %H:%M')}")

                         col1, col2, col3 = st.columns(3)
                         with col1:
                             if st.button("Dismiss Report", key=f"keep_comment_{comment['id']}"):
                                 st.success(f"Report dismissed. Comment kept.")
                                 comment['status'] = 'approved' # Simulate
                                 st.rerun()
                         with col2:
                             if st.button("Delete Comment", key=f"delete_comment_{comment['id']}"):
                                 st.warning(f"Comment deleted!")
                                 comment['status'] = 'deleted' # Simulate
                                 # In real app, remove/flag comment in DB
                                 st.rerun()
                         with col3:
                             if st.button("Ban User", key=f"ban_user_comment_{comment['id']}"):
                                 st.error(f"User '{comment['user']}' banned!")
                                 # Logic to update user status to 'Banned'
                                 comment['status'] = 'deleted' # Also delete comment
                                 st.rerun()
                         st.markdown("---")

        with mod_tabs[2]:
             st.markdown("#### Flagged Users")
             st.info("Display users flagged for review based on reports or suspicious activity.")
             # Add logic to display flagged users from user data based on a 'flagged' status or report count

    with admin_tabs[2]:
        st.markdown("### System Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # Example: Get active users from edited_df if available
            active_users = len(st.session_state.get('edited_users_df', users_df)[st.session_state.get('edited_users_df', users_df)['Status'] == 'Active'])
            st.metric("Active Users", active_users, f"{random.randint(-5, 15)} today")
        with col2:
            # Mock server load
            st.metric("Server Load (Simulated)", f"{random.randint(15, 45)}%", f"{random.randint(-5, 5)}%")
        with col3:
            # Mock storage - calculate based on uploads maybe
            num_uploads = len(st.session_state.get('uploads', []))
            storage_gb = round(num_uploads * 0.002, 2) # Assuming avg 2MB per photo
            st.metric("Estimated Media Storage", f"{storage_gb} GB", f"+{round(random.random()*0.1, 2)} GB")

        st.markdown("#### Activity Overview (Last 7 Days)")
        # Generate simple activity chart
        activity_dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
        activity_data = pd.DataFrame({
             'Logins': np.random.randint(50, 200, size=7),
             'Posts (Photos+Comments)': np.random.randint(10, 50, size=7),
             'New Registrations': np.random.randint(1, 10, size=7)
             }, index=activity_dates)
        st.line_chart(activity_data)

    with admin_tabs[3]:
        st.markdown("### Settings & Maintenance")
        
        st.markdown("#### System Settings (Example)")
        setting1 = st.toggle("Enable New User Registration", value=True, key="setting_reg")
        setting2 = st.number_input("Max Upload Size (MB)", min_value=1, max_value=20, value=5, key="setting_upload")
        setting3 = st.selectbox("Default User Role on Signup", ["user", "pending_approval"], key="setting_role")

        if st.button("Save Settings", key="save_settings"):
             st.success("System settings updated (simulation).")

        st.markdown("---")
        st.markdown("#### Maintenance Tasks")
        
        task_options = {
            "Clear Application Cache": "Clears Streamlit's internal caches.",
            "Backup Database": "Triggers a backup of the application database (simulation).",
            "Recalculate User Statistics": "Updates derived stats like badges or activity scores.",
            "Check for System Updates": "Checks for new versions of dependencies (simulation)."
        }
        
        selected_tasks = st.multiselect(
            "Select Maintenance Tasks to Run",
            list(task_options.keys()),
            help="Select one or more tasks to execute.",
            key="maint_tasks"
        )
        
        if st.button("Run Selected Maintenance Tasks", key="run_maint") and selected_tasks:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i, task in enumerate(selected_tasks):
                 status_text.info(f"Running: {task} ({task_options[task]})")
                 time.sleep(random.uniform(0.5, 1.5)) # Simulate work
                 progress_bar.progress((i + 1) / len(selected_tasks))
            
            status_text.success(f"Completed {len(selected_tasks)} maintenance tasks!")
            st.balloons()
        elif st.button("Run Selected Maintenance Tasks", key="run_maint_no_select") and not selected_tasks:
             st.warning("Please select at least one maintenance task to run.")

# ------ MAIN APP LOGIC ------
def main():
    """Main function to run the Streamlit application."""
    global name, username # Make them accessible if needed elsewhere, though prefer passing as args

    # --- Authentication ---
    # Authentication must happen first
    try:
         name, username = setup_authentication()
    except Exception as e:
         # Catch potential errors during auth setup (e.g., config issues)
         st.error("An error occurred during the login process. Please contact support.")
         st.exception(e) # Log the full error for debugging
         st.stop()

    # --- Data Initialization ---
    # Initialize data only *after* successful login, using session state
    billboards = initialize_data()

    # --- Sidebar Navigation ---
    page = display_sidebar(name, username)

    # --- Page Content Rendering ---
    if page == "Home":
        display_home(billboards)
    elif page == "My Plants":
        display_my_plants()
    elif page == "Community":
        display_community(name) # Pass current user's name for posting
    elif page == "Sponsor Dashboard":
        # Double-check access although sidebar logic should prevent unauthorized access
        if st.session_state.get("user_role") in ["sponsor", "admin"]:
            display_sponsor_dashboard()
        else:
            st.error("Access Denied.")
            st.switch_page("grow.py") # Redirect to home potentially
    elif page == "Admin Panel":
        # Double-check access
        if st.session_state.get("user_role") == "admin":
            display_admin_panel()
        else:
             st.error("Access Denied.")
             st.switch_page("grow.py") # Redirect to home potentially

    # --- Footer --- (Optional)
    st.markdown("---")
    st.caption("🌿 Growvertising © 2025 | Transforming Ads into Action")


if __name__ == "__main__":
    main()
