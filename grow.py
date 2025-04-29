import streamlit as st
# Removed streamlit_authenticator import
from datetime import datetime
import random
# Removed PIL import as it's not explicitly used
import pandas as pd
import numpy as np
import time
import io

# ------ PAGE CONFIGURATION ------
st.set_page_config(
    page_title="Growvertising - Billboard to Farmboard (Demo)", # Updated title
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

# ------ AUTHENTICATION (REMOVED) ------
# The setup_authentication function has been removed.
# We will use session state to simulate the user role.

# ------ DATA INITIALIZATION ------
def initialize_data():
    """Initializes session state variables and static data."""
    # Initialize session state variables if they don't exist
    if "comments" not in st.session_state:
        st.session_state["comments"] = []

    if "uploads" not in st.session_state:
        st.session_state["uploads"] = []

    if "plants_grown" not in st.session_state:
        st.session_state["plants_grown"] = random.randint(1000, 1500)

    if "co2_offset" not in st.session_state:
        st.session_state["co2_offset"] = random.randint(300, 500)

    if "seed_kits" not in st.session_state:
        st.session_state["seed_kits"] = random.randint(700, 1000)

    if "last_visit" not in st.session_state:
        st.session_state["last_visit"] = datetime.now()

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

    # Billboard data remains the same
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
def display_sidebar():
    """Displays the navigation sidebar and allows role simulation."""
    st.sidebar.markdown("## 🌿 Navigation")

    # --- Role Simulation (Replaces Login) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Simulate User Role (Demo)")
    # Define roles and get current selection from session state, default to 'user'
    roles = ["user", "sponsor", "admin"]
    default_role_index = roles.index(st.session_state.get("simulated_role", "user"))
    
    simulated_role = st.sidebar.selectbox(
        "Select Role",
        roles,
        index=default_role_index,
        key="simulated_role_selector",
        format_func=lambda x: x.capitalize() # Display roles nicely capitalized
    )
    # Store the selected simulated role in session state
    st.session_state["simulated_role"] = simulated_role
    st.sidebar.markdown("---")
    # --- End Role Simulation ---


    # Determine available pages based on the *simulated* role
    available_pages = ["Home", "My Plants", "Community"]
    if simulated_role in ["sponsor", "admin"]:
        available_pages.append("Sponsor Dashboard")
    if simulated_role == "admin":
        available_pages.append("Admin Panel")

    # Set default page index (e.g., always start at Home)
    default_index = 0

    page = st.sidebar.radio(
        "Go to",
        available_pages,
        index=default_index,
        key="navigation_radio"
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

    st.sidebar.markdown(f"### Profile ({simulated_role.capitalize()})") # Show simulated role instead of username
    st.sidebar.markdown(f"**Badge:** {badge}")
    st.sidebar.progress(activity_score / 100)
    plants_grown_user = len(st.session_state.get("user_plants", []))
    st.sidebar.markdown(f"**Plants Currently Growing:** {plants_grown_user}")
    st.sidebar.markdown(f"**Est. CO₂ Offset:** {plants_grown_user * random.randint(2, 5)} kg")

    # Help section remains the same
    with st.sidebar.expander("Need Help?"):
        st.markdown("""
        - **Home**: View billboard campaigns and track progress.
        - **My Plants**: Manage your growing plants.
        - **Community**: Share photos and interact with others.
        - **Sponsor Dashboard**: (Sponsors/Admin Roles) View campaign metrics.
        - **Admin Panel**: (Admin Role) Manage users and content.
        - **Support**: Email help@growvertising.com
        """)

    return page, simulated_role # Return role for use in main logic

# ------ HOME PAGE ------
# Unchanged from the previous version
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
        growth_percentage = random.randint(60, 90)
        st.progress(growth_percentage / 100)
        st.markdown(f"**Growth Level:** {growth_percentage}%")

    with col_days:
        days_remaining = max(0, 30 - int((growth_percentage / 100) * 30))
        delta_days = -1 if days_remaining < 30 else 0
        st.metric("Est. Days Until Harvest", f"{days_remaining} days", f"{delta_days} vs yesterday")

    with col_water:
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
# Unchanged from the previous version
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
                            days_old = (datetime.now() - plant_data['planted_date']).days
                            st.markdown(f"**Days old:** {days_old}")
                        with col_c:
                            health = 'Good' if plant_data['progress'] > 60 else 'Needs Attention' if plant_data['progress'] > 30 else 'Struggling'
                            st.markdown(f"**Health:** {health}")

                        # Add action buttons
                        col_actions1, col_actions2 = st.columns(2)
                        with col_actions1:
                            if st.button("Update Progress", key=f"update_{i}"):
                                st.session_state["user_plants"][i]["progress"] = min(100, plant_data['progress'] + random.randint(5,15))
                                st.rerun()
                        with col_actions2:
                            if st.button("Mark as Harvested/Finished", key=f"finish_{i}"):
                                harvested_plant = st.session_state["user_plants"].pop(i)
                                st.session_state["user_plant_history"].append({
                                    "Plant Type": harvested_plant['name'],
                                    "Date Planted": harvested_plant['planted_date'].strftime('%Y-%m-%d'),
                                    "Harvest Date": datetime.now().strftime('%Y-%m-%d'),
                                    "Success": "Yes"
                                })
                                st.success(f"{harvested_plant['name']} moved to history.")
                                st.rerun()

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
                st.session_state["user_plants"].append({
                    "name": new_plant_type,
                    "progress": random.randint(5, 15),
                    "planted_date": datetime.combine(plant_date, datetime.min.time()),
                    "notes": notes
                })
                st.success(f"Added {new_plant_type} to your garden!")
                st.balloons()

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
# Modified to accept a generic user name
def display_community(current_user_name="Community User"): # Default user name
    """Displays the community interaction page."""
    st.markdown("<h1 class='sub-title'>👨‍👩‍👧‍👦 Community Hub</h1>", unsafe_allow_html=True)
    st.markdown("Share your progress, ask questions, and connect with fellow growers!")

    tab_photos, tab_comments = st.tabs(["📸 Photo Wall", "💬 Discussion Forum"])

    with tab_photos:
        st.markdown("### Share Your Plant Photos")

        uploaded_file = st.file_uploader(
            "Upload a photo of your plants!",
            type=["jpg", "png", "jpeg"],
            key="photo_uploader"
        )
        caption = st.text_input("Caption for your photo", key="photo_caption")
        location = st.text_input("Location (optional, e.g., 'City, State')", key="photo_location")

        if st.button("Upload Photo", key="upload_photo_btn") and uploaded_file is not None:
            if caption:
                image_bytes = uploaded_file.getvalue()
                st.session_state["uploads"].append({
                    "image_bytes": image_bytes,
                    "caption": caption,
                    "location": location if location else "Unknown Location",
                    "user": current_user_name, # Use the generic name
                    "timestamp": datetime.now(),
                    "likes": 0
                })
                st.success("Photo uploaded successfully! 🌿")
                st.rerun()
            else:
                st.warning("Please add a caption for your photo.")
        elif st.button("Upload Photo", key="upload_photo_btn_clicked_no_file") and uploaded_file is None:
             st.warning("Please select a photo file first.")

        st.markdown("---")
        st.markdown("### Recent Community Photos")

        if not st.session_state.get("uploads"):
            st.info("No photos shared yet. Be the first!")
        else:
            num_photos = len(st.session_state["uploads"])
            cols = st.columns(3)

            for i, upload in enumerate(reversed(st.session_state["uploads"])):
                col_index = i % 3
                with cols[col_index]:
                    with st.container():
                        try:
                            st.image(upload["image_bytes"], caption=f"{upload['caption']} ({upload['user']})", use_column_width='always')
                        except Exception as e:
                             st.error(f"Could not display image: {e}")

                        like_key = f"like_photo_{upload['timestamp'].isoformat()}"
                        likes = upload.get("likes", 0)

                        if st.button(f"❤️ {likes} Like", key=like_key):
                            for original_upload in st.session_state["uploads"]:
                                if original_upload["timestamp"] == upload["timestamp"]:
                                     original_upload["likes"] = original_upload.get("likes", 0) + 1
                                     break
                            st.rerun()

                        st.caption(f"📍 {upload['location']} | ⏰ {upload['timestamp'].strftime('%Y-%m-%d %H:%M')}")

    with tab_comments:
        st.markdown("### 💬 Community Discussion")

        with st.form("comment_form", clear_on_submit=True):
            comment_text = st.text_area("Leave a message, tip, or question for the community!", max_chars=300, height=100, key="comment_text_area")
            submitted = st.form_submit_button("Post Comment")

            if submitted and comment_text:
                st.session_state["comments"].append({
                    "user": current_user_name, # Use the generic name
                    "comment": comment_text,
                    "timestamp": datetime.now(),
                    "likes": 0
                })
                st.success("Comment posted! 💬")
            elif submitted and not comment_text:
                st.warning("Please enter a comment before posting.")

        st.markdown("---")
        st.markdown("### Recent Comments:")

        # Initialize sample comments if none exist
        if not st.session_state.get("comments") and not st.session_state.get("comments_initialized"):
            sample_comments = [
                {"user": "GreenThumb", "comment": "Just harvested my first batch of tomatoes! Can't believe how well they turned out.", "timestamp": datetime(2025, 4, 25, 14, 32), "likes": 12},
                {"user": "PlantLover", "comment": "Has anyone had issues with yellowing leaves on their basil plants? Looking for advice!", "timestamp": datetime(2025, 4, 26, 9, 15), "likes": 8},
                {"user": "UrbanFarmer", "comment": "The community garden project is coming along nicely! Check out our progress photos.", "timestamp": datetime(2025, 4, 27, 16, 45), "likes": 15}
            ]
            st.session_state["comments"] = sample_comments
            st.session_state["comments_initialized"] = True

        if not st.session_state.get("comments"):
             st.info("No comments yet. Start the conversation!")
        else:
             for i, entry in enumerate(reversed(st.session_state["comments"])):
                 with st.container():
                     st.markdown(f"**{entry['user']}** ({entry['timestamp'].strftime('%Y-%m-%d %H:%M')})")
                     st.markdown(f"> {entry['comment']}")

                     like_key = f"like_comment_{entry['timestamp'].isoformat()}"
                     likes = entry.get("likes", 0)

                     if st.button(f"❤️ {likes}", key=like_key, help="Like this comment"):
                          for original_comment in st.session_state["comments"]:
                              if original_comment["timestamp"] == entry["timestamp"]:
                                   original_comment["likes"] = original_comment.get("likes", 0) + 1
                                   break
                          st.rerun()

                     st.markdown("---")

# ------ SPONSOR DASHBOARD ------
# Unchanged from the previous version
import streamlit as st
from datetime import datetime
import random
import pandas as pd
import numpy as np
import time
import io # Keep io for download button

# Note: Assuming other necessary parts of the script (like initialize_data) exist elsewhere.
# Also assuming session state variables ('plants_grown', 'co2_offset', 'seed_kits', 'uploads', 'comments')
# are initialized before this function is called.

# ------ PAGE CONFIGURATION (Example - might be in main script) ------
# st.set_page_config(layout="wide")

# ------ CSS STYLING (Example - might be in main script) ------
# st.markdown("""<style> ... </style>""", unsafe_allow_html=True)

# ------ SPONSOR DASHBOARD ------
def display_sponsor_dashboard():
    """Displays the dashboard for sponsors."""
    st.markdown("<h1 class='sub-title'>📊 Sponsor Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Monitor the impact and performance of sponsored campaigns.")

    # Key metrics - Use session state values
    st.markdown("### Key Performance Metrics (Overall)")

    col1, col2, col3 = st.columns(3)
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

    campaign_names = ['Grow Your Greens', 'From Message to Meal', 'Food Waste Awareness', 'Urban Farming']
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

    # This is the DataFrame for campaign trends
    engagement_data = pd.DataFrame(
        np.random.randint(10, 100, size=(30, len(campaign_names))),
        index=dates,
        columns=campaign_names
    ) * [1.5, 1.2, 0.8, 1.0]

    growth_data = pd.DataFrame(
        np.random.rand(30, len(campaign_names)) * 5,
        index=dates,
        columns=campaign_names
    ).cumsum()


    tab_engage, tab_growth, tab_roi = st.tabs(["📈 Engagement Trends", "🌱 Growth Rate", "💰 ROI Metrics (Example)"])

    with tab_engage:
        st.line_chart(engagement_data) # Uses the DataFrame defined above
        st.caption("Simulated daily engagement (e.g., interactions, kit requests) across campaigns (last 30 days)")

    with tab_growth:
        st.area_chart(growth_data)
        st.caption("Simulated cumulative growth contribution per campaign (last 30 days)")

    with tab_roi:
        st.markdown("#### Return on Investment (Illustrative)")
        investment = {"Grow Your Greens": 15000, "From Message to Meal": 12000, "Food Waste Awareness": 8000, "Urban Farming": 10000}
        # Uses the engagement_data DataFrame and growth_data DataFrame correctly
        value_generated = (engagement_data.sum() * 0.5 + growth_data.iloc[-1] * 10).round(0)

        roi_data = []
        for campaign in campaign_names:
             cost = investment.get(campaign, 1)
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
        age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
        percentages = [18, 35, 25, 15, 7]
        demo_data = pd.DataFrame({"Age Group": age_groups, "Percentage": percentages})
        st.bar_chart(demo_data.set_index("Age Group"))
        st.caption("Distribution of active users by age group.")

    with col_engage:
        st.markdown("#### Top Engaging Content (Sample)")
        # --- FIX: Use a different variable name for this dictionary ---
        community_engagement_dict = {
            "Content Type": ["Photo Uploads", "Comments", "Likes (Photos)", "Likes (Comments)", "Seed Kit Claims"],
            "Count (Last 30d)": [
                len(st.session_state.get('uploads', [])),
                len(st.session_state.get('comments', [])),
                sum(u.get('likes', 0) for u in st.session_state.get('uploads', [])),
                sum(c.get('likes', 0) for c in st.session_state.get('comments', [])),
                # Calculate based on current kits minus some baseline if needed for 'last 30d' simulation
                max(0, st.session_state.get('seed_kits', 0) - (st.session_state.get('seed_kits', 0) // 1.1 if st.session_state.get('seed_kits', 0) > 100 else random.randint(50,100)))
            ]
        }
        # --- FIX: Create engage_df from the new dictionary name ---
        engage_df = pd.DataFrame(community_engagement_dict)
        st.bar_chart(engage_df.set_index("Content Type"))
        st.caption("User interactions with community features (approx. last 30 days).")

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
        report_format = st.radio("Report Format", ["CSV", "PDF"], key="report_format_radio")
    with col_generate:
        report_filename = f"{report_type.lower().replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d')}.{report_format.lower()}"

        # Simplified report data generation
        if report_type == "Campaign Performance Summary":
            # Now correctly uses the engagement_data DataFrame
            report_data_df = engagement_data.reset_index().rename(columns={'index': 'Date'})
            report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
            report_data_pdf = b"Sample PDF data for Campaign Performance" # Placeholder PDF
        elif report_type == "User Engagement Analysis":
             # Correctly uses engage_df (derived from community_engagement_dict)
             report_data_df = engage_df
             report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
             report_data_pdf = b"Sample PDF data for User Engagement" # Placeholder PDF
        elif report_type == "Financial Overview":
             # Use roi_df defined in the ROI tab
             report_data_df = roi_df
             report_data_csv = report_data_df.to_csv(index=True).encode('utf-8') # Index=True as campaign is index
             report_data_pdf = b"Sample PDF data for Financial Overview" # Placeholder PDF
        else: # Environmental Impact Estimate or other
            # Create a simple placeholder DataFrame for environmental impact
            env_impact_data = {
                "Metric": ["Total Plants Grown", "Estimated CO₂ Offset (kg)", "Water Saved (Est. Liters)"],
                "Value": [plants_grown, co2_offset, plants_grown * random.randint(5, 15)]
            }
            report_data_df = pd.DataFrame(env_impact_data)
            report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
            report_data_pdf = b"Sample PDF data for Environmental Impact" # Placeholder PDF

        report_data = report_data_csv if report_format == "CSV" else report_data_pdf
        mime_type = "text/csv" if report_format == "CSV" else "application/pdf"

        # Check if button already exists in session state from previous run within the spinner
        # This prevents error on rerun after download
        if f"download_report_final_{report_filename}" not in st.session_state:
             st.session_state[f"download_report_final_{report_filename}"] = False

        if st.button("Generate & Download Report", key=f"generate_report_btn_{report_filename}"):
            with st.spinner("Generating report..."):
                time.sleep(1.0) # Shortened sleep
                # Use a unique key for the download button based on filename to avoid reuse issues
                st.download_button(
                    label=f"Click to Download {report_format}",
                    data=report_data,
                    file_name=report_filename,
                    mime=mime_type,
                    key=f"download_report_final_{report_filename}" # Unique key
                )
            # Can't show success *after* download button logic in this structure easily
            # st.success(f"{report_type} report ready for download.") # This might appear too early or late

# --- Example Usage (if running this file directly) ---
# if __name__ == "__main__":
#     # Minimal initialization for testing this function
#     if "comments" not in st.session_state: st.session_state["comments"] = []
#     if "uploads" not in st.session_state: st.session_state["uploads"] = []
#     if "plants_grown" not in st.session_state: st.session_state["plants_grown"] = random.randint(1000, 1500)
#     if "co2_offset" not in st.session_state: st.session_state["co2_offset"] = random.randint(300, 500)
#     if "seed_kits" not in st.session_state: st.session_state["seed_kits"] = random.randint(700, 1000)
#
#     display_sponsor_dashboard()
# ------ ADMIN PANEL ------
# Unchanged from the previous version
def display_admin_panel():
    """Displays the administrative panel for managing the app."""
    st.markdown("<h1 class='sub-title'>🔧 Admin Panel</h1>", unsafe_allow_html=True)
    st.info("This panel shows administrative functions (simulation).") # Changed warning to info

    admin_tabs = st.tabs(["👤 User Management", "💬 Content Moderation", "📈 System Statistics", "⚙️ Settings & Maintenance"])

    with admin_tabs[0]:
        st.markdown("### User Management (Simulated)")

        # Sample user data (no real login data)
        users_data = {
            "Username": ["growuser_demo", "sponsor_demo", "admin_demo", "greenthumb_demo", "plantlover_demo"],
            "Name": ["Green User", "Sponsor One", "Admin User", "Gaia Green", "Peter Plant"],
            "Simulated Role": ["user", "sponsor", "admin", "user", "user"],
            "Email": ["g@e.com", "s@e.com", "a@e.com", "gg@e.com", "pp@e.com"],
            "Last Action": pd.to_datetime(["2025-04-28", "2025-04-27", "2025-04-28", "2025-04-25", "2025-04-26"]),
            "Status": ["Active", "Active", "Active", "Active", "Active"]
        }
        users_df = pd.DataFrame(users_data)

        st.info("Displaying sample user data. Editing is disabled in this demo.")
        st.dataframe(users_df, use_container_width=True, hide_index=True) # Display as static table

        # Disabled editing controls
        st.text_input("Search User (disabled)", disabled=True)
        if st.button("Save User Changes (disabled)", key="save_users_disabled", disabled=True):
             pass

    with admin_tabs[1]:
        st.markdown("### Content Moderation (Simulated)")

        mod_tabs = st.tabs(["Pending Photos", "Reported Comments"])

        with mod_tabs[0]:
            st.markdown("#### Photos Pending Review")
            # Mock pending photos
            pending_photos = [
                  {"id": f"photo_{random.randint(1000,9999)}", "user": "plantlover_demo", "caption": "My new garden setup", "timestamp": datetime.now() - pd.Timedelta(hours=2), "image_bytes": None, "status": "pending"},
                  {"id": f"photo_{random.randint(1000,9999)}", "user": "greenthumb_demo", "caption": "Urban farming progress", "timestamp": datetime.now() - pd.Timedelta(hours=1), "image_bytes": None, "status": "pending"}
            ]
            if not pending_photos:
                 st.info("No photos currently pending review.")
            else:
                 for i, photo in enumerate(pending_photos):
                     with st.container():
                         st.markdown(f"**User:** {photo['user']} | **Posted:** {photo['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                         st.markdown(f"**Caption:** {photo['caption']}")
                         st.markdown("*(Image preview N/A)*")

                         col1, col2 = st.columns(2)
                         with col1:
                             if st.button("Approve (Sim)", key=f"approve_photo_{photo['id']}"):
                                 st.success(f"Photo approved! (Simulation)")
                         with col2:
                             if st.button("Reject (Sim)", key=f"reject_photo_{photo['id']}"):
                                 st.error(f"Photo rejected! (Simulation)")
                         st.markdown("---")

        with mod_tabs[1]:
            st.markdown("#### Reported Comments")
            # Mock reported comments
            reported_comments = [
                  {"id": f"comment_{random.randint(1000,9999)}", "user": "SpamBot_demo", "comment": "Buy cheap widgets now! www.spam.com", "timestamp": datetime.now() - pd.Timedelta(days=1), "reported_by": "greenthumb_demo", "status": "reported"},
                  {"id": f"comment_{random.randint(1000,9999)}", "user": "RudeUser_demo", "comment": "Your plants look terrible!", "timestamp": datetime.now() - pd.Timedelta(hours=5), "reported_by": "plantlover_demo", "status": "reported"}
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

                         col1, col2 = st.columns(2)
                         with col1:
                             if st.button("Dismiss Report (Sim)", key=f"keep_comment_{comment['id']}"):
                                 st.success(f"Report dismissed. (Simulation)")
                         with col2:
                             if st.button("Delete Comment (Sim)", key=f"delete_comment_{comment['id']}"):
                                 st.warning(f"Comment deleted! (Simulation)")
                         st.markdown("---")

    with admin_tabs[2]:
        st.markdown("### System Statistics (Simulated)")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Users (Sample)", "248", f"{random.randint(-5, 15)} today")
        with col2:
            st.metric("Server Load (Simulated)", f"{random.randint(15, 45)}%", f"{random.randint(-5, 5)}%")
        with col3:
            num_uploads = len(st.session_state.get('uploads', []))
            storage_gb = round(num_uploads * 0.002, 2)
            st.metric("Estimated Media Storage", f"{storage_gb} GB", f"+{round(random.random()*0.1, 2)} GB")

        st.markdown("#### Activity Overview (Last 7 Days - Sample Data)")
        activity_dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
        activity_data = pd.DataFrame({
             'Page Views': np.random.randint(500, 2000, size=7),
             'Posts (Photos+Comments)': np.random.randint(10, 50, size=7),
             'Kit Requests': np.random.randint(5, 25, size=7)
             }, index=activity_dates)
        st.line_chart(activity_data)

    with admin_tabs[3]:
        st.markdown("### Settings & Maintenance (Simulated)")

        st.markdown("#### System Settings (Example)")
        st.toggle("Enable New User Registration", value=True, key="setting_reg_disabled", disabled=True)
        st.number_input("Max Upload Size (MB)", min_value=1, max_value=20, value=5, key="setting_upload_disabled", disabled=True)
        st.selectbox("Default User Role on Signup", ["user", "pending_approval"], key="setting_role_disabled", disabled=True)

        if st.button("Save Settings (Disabled)", key="save_settings_disabled", disabled=True):
             pass

        st.markdown("---")
        st.markdown("#### Maintenance Tasks")

        task_options = {
            "Clear Application Cache": "Clears Streamlit's internal caches.",
            "Backup Database": "Triggers a backup of the application database (simulation).",
            "Recalculate User Statistics": "Updates derived stats like badges or activity scores.",
        }

        selected_tasks = st.multiselect(
            "Select Maintenance Tasks to Run",
            list(task_options.keys()),
            help="Select one or more tasks to execute.",
            key="maint_tasks"
        )

        if st.button("Run Selected Maintenance Tasks (Sim)", key="run_maint") and selected_tasks:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i, task in enumerate(selected_tasks):
                 status_text.info(f"Simulating: {task} ({task_options[task]})")
                 time.sleep(random.uniform(0.5, 1.0)) # Simulate work
                 progress_bar.progress((i + 1) / len(selected_tasks))
            status_text.success(f"Completed {len(selected_tasks)} maintenance tasks! (Simulation)")
            st.balloons()
        elif st.button("Run Selected Maintenance Tasks (Sim)", key="run_maint_no_select") and not selected_tasks:
             st.warning("Please select at least one maintenance task to run.")


# ------ MAIN APP LOGIC ------
def main():
    """Main function to run the Streamlit application without authentication."""

    # --- Data Initialization ---
    # Initialize data using session state
    billboards = initialize_data()

    # --- Sidebar Navigation & Role Simulation ---
    # Display sidebar and get selected page and simulated role
    page, simulated_role = display_sidebar()

    # Define a generic user name for display purposes
    current_user_name = "Community User" # Can be changed if desired

    # --- Page Content Rendering ---
    # Display content based on selected page and simulated role
    if page == "Home":
        display_home(billboards)
    elif page == "My Plants":
        display_my_plants()
    elif page == "Community":
        display_community(current_user_name) # Pass the generic name
    elif page == "Sponsor Dashboard":
        # Access controlled by sidebar logic based on simulated_role
        display_sponsor_dashboard()
    elif page == "Admin Panel":
        # Access controlled by sidebar logic based on simulated_role
        display_admin_panel()

    # --- Footer --- (Optional)
    st.markdown("---")
    st.caption("🌿 Growvertising © 2025 | Transforming Ads into Action| developed sangita biswas")


if __name__ == "__main__":
    main()
