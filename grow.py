import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import random
from PIL import Image
import os
import pandas as pd
import numpy as np
import time

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
    }
</style>
""", unsafe_allow_html=True)

# ------ AUTHENTICATION ------
def setup_authentication():
    # In a production app, this would be stored in a secure database
    credentials_dict = {
        "usernames": {
            "growuser": {"name": "Green User", "password": "pass123"},
            "sponsor1": {"name": "Sponsor One", "password": "sponsorpass"},
            "admin": {"name": "Admin User", "password": "admin123"}
        }
    }
    
    authenticator = stauth.Authenticate(
        credentials_dict, 
        "growvertising_app", 
        "abcdef", 
        cookie_expiry_days=30
    )
    
    name, auth_status, username = authenticator.login("Login", "sidebar")
    
    if auth_status == False:
        st.sidebar.error("Invalid username/password")
        st.warning("Please log in to access the app.")
        st.stop()
    elif auth_status == None:
        st.sidebar.warning("Please enter your credentials")
        st.warning("Please log in to access the app.")
        st.stop()
    
    # Store user role in session state
    if username == "admin":
        st.session_state["user_role"] = "admin"
    elif username == "sponsor1":
        st.session_state["user_role"] = "sponsor"
    else:
        st.session_state["user_role"] = "user"
    
    # Add logout button
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name}!")
    
    return name, username

# ------ DATA INITIALIZATION ------
def initialize_data():
    # Initialize session state variables if they don't exist
    if "comments" not in st.session_state:
        st.session_state["comments"] = []
    
    if "uploads" not in st.session_state:
        st.session_state["uploads"] = []
    
    if "plants_grown" not in st.session_state:
        st.session_state["plants_grown"] = 1230
    
    if "co2_offset" not in st.session_state:
        st.session_state["co2_offset"] = 420
    
    if "seed_kits" not in st.session_state:
        st.session_state["seed_kits"] = 890
    
    if "last_visit" not in st.session_state:
        st.session_state["last_visit"] = datetime.now()
        
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
            "url": "https://i.imgur.com/U4A0lRQ.jpg",
            "description": "Transforming city spaces into productive green gardens.",
            "sponsor": "CityGrow Initiative"
        }
    }
    
    return billboards

# ------ SIDEBAR CONTENT ------
def display_sidebar(name, username):
    st.sidebar.markdown("## 🌿 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "My Plants", "Community", "Sponsor Dashboard", "Admin Panel"],
        index=0
    )
    
    # Only show admin panel to admin users
    if page == "Admin Panel" and st.session_state["user_role"] != "admin":
        st.sidebar.warning("You don't have access to the Admin Panel")
        page = "Home"
    
    # Only show sponsor dashboard to sponsors and admins
    if page == "Sponsor Dashboard" and st.session_state["user_role"] not in ["sponsor", "admin"]:
        st.sidebar.warning("You don't have access to the Sponsor Dashboard")
        page = "Home"
    
    st.sidebar.markdown("---")
    
    # Display user stats
    activity_score = random.randint(10, 100)
    if activity_score > 80:
        badge = "🌟 Super Grower"
    elif activity_score > 50:
        badge = "🌿 Urban Farmer"
    else:
        badge = "🍀 Green Starter"
    
    st.sidebar.markdown(f"### Your Profile")
    st.sidebar.markdown(f"**Badge:** {badge}")
    st.sidebar.progress(activity_score / 100)
    st.sidebar.markdown(f"**Plants Grown:** {random.randint(3, 15)}")
    st.sidebar.markdown(f"**CO₂ Offset:** {random.randint(5, 50)} kg")
    
    # Help section
    with st.sidebar.expander("Need Help?"):
        st.markdown("""
        - **Home**: View billboard campaigns and track progress
        - **My Plants**: Manage your growing plants
        - **Community**: Share photos and interact
        - **Support**: Email help@growvertising.com
        """)
    
    return page

# ------ HOME PAGE ------
def display_home(billboards):
    st.markdown("<h1 class='main-title'>🌿 Growvertising – Billboard to Farmboard</h1>", unsafe_allow_html=True)
    st.markdown("Turn every ad into action – grow plants, offset carbon, and join the green movement.")
    
    # Billboard preview section
    st.markdown("<h2 class='sub-title'>🖼️ Billboard Preview</h2>", unsafe_allow_html=True)
    
    selected_ad = st.selectbox("Select Campaign", list(billboards.keys()))
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(billboards[selected_ad]["url"], caption=selected_ad, use_column_width=True)
    
    with col2:
        st.markdown(f"### Campaign Details")
        st.markdown(f"**Description:** {billboards[selected_ad]['description']}")
        st.markdown(f"**Sponsor:** {billboards[selected_ad]['sponsor']}")
        st.markdown("---")
        
        # Add interaction options
        st.markdown("### Get Involved")
        if st.button("Request Seed Kit"):
            st.session_state["seed_kits"] += 1
            st.success("Seed kit requested! Check your email for details.")
        
        if st.button("Support This Campaign"):
            st.balloons()
            st.success("Thank you for your support!")
    
    # Growth simulation
    st.markdown("<h2 class='sub-title'>🌱 Billboard Growth Status</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        growth = st.slider("Growth Level (%)", 0, 100, 75)
        st.progress(growth / 100)
    
    with col2:
        days_remaining = 30 - int((growth / 100) * 30)
        st.metric("Days Until Harvest", f"{days_remaining} days", f"{-1 if days_remaining < 30 else 0} today")
    
    with col3:
        water_level = st.select_slider(
            "Water Level",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        st.markdown(f"**Status:** {'Needs water!' if water_level == 'Low' else 'Healthy' if water_level == 'Medium' else 'Overwatered!'}")
    
    # Weather and growth conditions
    st.markdown("<h2 class='sub-title'>🌤️ Growing Conditions</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Temperature", "24°C", "+2°C")
    with col2:
        st.metric("Humidity", "65%", "+5%")
    with col3:
        st.metric("Sunlight", "Good", "")
    with col4:
        st.metric("Soil Quality", "Excellent", "")

# ------ MY PLANTS PAGE ------
def display_my_plants():
    st.markdown("<h1 class='sub-title'>🌱 My Plants</h1>", unsafe_allow_html=True)
    
    # Plant tracking
    plant_types = ["Tomato", "Basil", "Lettuce", "Spinach", "Mint"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tab1, tab2 = st.tabs(["Current Plants", "Plant History"])
        
        with tab1:
            # Show current plants with progress
            for i, plant in enumerate(plant_types[:3]):
                with st.container():
                    st.markdown(f"### {plant}")
                    progress = random.randint(20, 95)
                    st.progress(progress / 100)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.markdown(f"**Progress:** {progress}%")
                    with col_b:
                        st.markdown(f"**Days old:** {random.randint(5, 30)}")
                    with col_c:
                        st.markdown(f"**Health:** {'Good' if progress > 60 else 'Needs attention'}")
                    
                    st.markdown("---")
        
        with tab2:
            # Show history
            history_data = {
                "Plant Type": ["Tomato", "Basil", "Lettuce", "Spinach"],
                "Date Planted": ["2025-01-15", "2025-02-03", "2025-02-28", "2025-03-10"],
                "Harvest Date": ["2025-03-20", "2025-03-25", "2025-04-10", "In progress"],
                "Success": ["Yes", "Yes", "Yes", "In progress"]
            }
            
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True)
    
    with col2:
        st.markdown("### Add New Plant")
        new_plant = st.selectbox("Plant Type", plant_types)
        plant_date = st.date_input("Planting Date", datetime.now())
        
        if st.button("Start Growing"):
            st.success(f"Added {new_plant} to your garden!")
            st.balloons()
        
        st.markdown("---")
        st.markdown("### Plant Care Tips")
        st.info("Remember to water your plants regularly and ensure they get enough sunlight.")
        
        st.markdown("### Upcoming Tasks")
        st.markdown("- Water tomato plants (today)")
        st.markdown("- Harvest basil (in 3 days)")
        st.markdown("- Add fertilizer (in 5 days)")

# ------ COMMUNITY PAGE ------
def display_community():
    st.markdown("<h1 class='sub-title'>👨‍👩‍👧‍👦 Community</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Photo Wall", "Comment Wall"])
    
    with tab1:
        st.markdown("### 📸 Share Your Plant Progress")
        
        # Photo upload area
        uploaded_file = st.file_uploader("Share your plant's photo!", type=["jpg", "png", "jpeg"])
        caption = st.text_input("Caption for your photo")
        location = st.text_input("Location (optional)")
        
        if st.button("Upload Photo") and uploaded_file and caption:
            # In a real app, you'd save this to a database
            st.session_state["uploads"].append({
                "image": uploaded_file,
                "caption": caption,
                "location": location,
                "timestamp": datetime.now(),
                "likes": 0
            })
            st.success("Uploaded successfully! 🌿")
        
        # Display uploaded photos
        st.markdown("### Recent Community Photos")
        
        # Placeholder for community photos
        sample_photos = [
            {"caption": "My tomato plants are thriving!", "location": "New York", "likes": 24},
            {"caption": "First harvest of the season!", "location": "Chicago", "likes": 31},
            {"caption": "Urban garden setup complete", "location": "Los Angeles", "likes": 18}
        ]
        
        # Display user uploads first
        if "uploads" in st.session_state and len(st.session_state["uploads"]) > 0:
            for upload in reversed(st.session_state["uploads"]):
                with st.container():
                    st.image(upload["image"], caption=upload["caption"], use_column_width=True)
                    st.markdown(f"📍 {upload['location'] if upload['location'] else 'Unknown location'} | ❤️ {upload['likes']} likes")
                    if st.button(f"Like", key=f"like_{upload['timestamp']}"):
                        upload["likes"] += 1
                    st.markdown("---")
        
        # Display sample photos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://i.imgur.com/GQhuf0U.jpg", caption=sample_photos[0]["caption"])
            st.markdown(f"📍 {sample_photos[0]['location']} | ❤️ {sample_photos[0]['likes']} likes")
        with col2:
            st.image("https://i.imgur.com/U4A0lRQ.jpg", caption=sample_photos[1]["caption"])
            st.markdown(f"📍 {sample_photos[1]['location']} | ❤️ {sample_photos[1]['likes']} likes")
        with col3:
            st.image("https://i.imgur.com/XY5NJJx.jpg", caption=sample_photos[2]["caption"])
            st.markdown(f"📍 {sample_photos[2]['location']} | ❤️ {sample_photos[2]['likes']} likes")
    
    with tab2:
        st.markdown("### 💬 Comment Wall")
        
        # Comment form
        with st.form("comment_form"):
            comment = st.text_area("Leave a message for the community!", max_chars=250)
            if st.form_submit_button("Post Comment") and comment:
                st.session_state["comments"].append({
                    "user": name,
                    "comment": comment,
                    "timestamp": str(datetime.now()),
                    "likes": 0
                })
                st.success("Comment posted! 💬")
        
        # Show latest comments
        st.markdown("### Recent Comments:")
        
        # Add some sample comments if none exist
        if len(st.session_state["comments"]) == 0:
            sample_comments = [
                {"user": "GreenThumb", "comment": "Just harvested my first batch of tomatoes! Can't believe how well they turned out.", "timestamp": "2025-04-25 14:32:00", "likes": 12},
                {"user": "PlantLover", "comment": "Has anyone had issues with yellowing leaves on their basil plants? Looking for advice!", "timestamp": "2025-04-26 09:15:00", "likes": 8},
                {"user": "UrbanFarmer", "comment": "The community garden project is coming along nicely! Check out our progress photos.", "timestamp": "2025-04-27 16:45:00", "likes": 15}
            ]
            for comment in sample_comments:
                st.session_state["comments"].append(comment)
        
        # Display comments
        for i, entry in enumerate(reversed(st.session_state["comments"])):
            with st.container():
                st.markdown(f"**{entry['user']}** says:")
                st.markdown(f"> {entry['comment']}")
                col1, col2 = st.columns([1, 6])
                with col1:
                    if st.button(f"❤️ {entry['likes']}", key=f"like_comment_{i}"):
                        entry["likes"] += 1
                with col2:
                    st.caption(f"Posted on {entry['timestamp']}")
                st.markdown("---")

# ------ SPONSOR DASHBOARD ------
def display_sponsor_dashboard():
    st.markdown("<h1 class='sub-title'>📊 Sponsor Dashboard</h1>", unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("### Key Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Plants Grown", f"{st.session_state['plants_grown']} 🌱", "+230 this week")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("CO₂ Offset", f"{st.session_state['co2_offset']} kg", "+35 kg")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Seed Kits Claimed", f"{st.session_state['seed_kits']}", "+102")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Campaign performance
    st.markdown("### Campaign Performance")
    
    # Generate sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3) * 8 + [40, 30, 20],
        columns=['Grow Your Greens', 'From Message to Meal', 'Food Waste Awareness']
    )
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Engagement", "Growth Rate"])
    
    with tab1:
        st.line_chart(chart_data)
        st.caption("Daily engagement metrics across campaigns (last 20 days)")
    
    with tab2:
        st.bar_chart(chart_data.iloc[-7:])
        st.caption("Weekly growth rate comparison (last 7 days)")
    
    # Campaign management
    st.markdown("### Campaign Management")
    
    with st.expander("Create New Campaign"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name")
            campaign_desc = st.text_area("Campaign Description")
            target_audience = st.multiselect("Target Audience", ["Urban Dwellers", "Families", "Students", "Seniors", "Businesses"])
        
        with col2:
            campaign_budget = st.number_input("Budget ($)", min_value=1000, max_value=50000, value=10000)
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
        
        if st.button("Create Campaign"):
            st.success("Campaign created successfully! Your campaign will be reviewed by our team.")
    
    # Community analytics
    st.markdown("### Community Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### User Demographics")
        demographics_data = {
            "Age Group": [18, 25, 35, 45, 55],
            "Percentage": [15, 32, 28, 18, 7]
        }
        demo_df = pd.DataFrame(demographics_data)
        st.bar_chart(demo_df.set_index("Age Group"))
    
    with col2:
        st.markdown("#### User Engagement")
        engagement_data = {
            "Metric": ["Photo Uploads", "Comments", "Seed Kit Claims", "Support Clicks"],
            "Count": [124, 356, 89, 212]
        }
        engage_df = pd.DataFrame(engagement_data)
        st.bar_chart(engage_df.set_index("Metric"))
    
    # Download reports
    st.markdown("### Reports")
    report_type = st.selectbox("Select Report Type", ["Campaign Performance", "User Engagement", "Environmental Impact", "Financial Summary"])
    col1, col2 = st.columns(2)
    with col1:
        report_format = st.radio("Report Format", ["PDF", "Excel", "CSV"])
    with col2:
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                time.sleep(2)
                st.success(f"{report_type} report generated in {report_format} format!")
                st.download_button(
                    label="Download Report",
                    data=b"Sample report data",
                    file_name=f"{report_type.lower().replace(' ', '_')}_report.{report_format.lower()}",
                    mime="application/octet-stream"
                )

# ------ ADMIN PANEL ------
def display_admin_panel():
    st.markdown("<h1 class='sub-title'>🔧 Admin Panel</h1>", unsafe_allow_html=True)
    
    # User management
    st.markdown("### User Management")
    
    users_data = {
        "Username": ["growuser", "sponsor1", "admin", "greenthumb", "plantlover"],
        "Role": ["User", "Sponsor", "Admin", "User", "User"],
        "Last Login": ["2025-04-28", "2025-04-27", "2025-04-28", "2025-04-25", "2025-04-26"],
        "Status": ["Active", "Active", "Active", "Inactive", "Active"]
    }
    users_df = pd.DataFrame(users_data)
    
    edited_df = st.data_editor(users_df, use_container_width=True)
    
    if st.button("Save User Changes"):
        st.success("User changes saved successfully!")
    
    # Content moderation
    st.markdown("### Content Moderation")
    
    moderation_tabs = st.tabs(["Pending Photos", "Reported Comments"])
    
    with moderation_tabs[0]:
        st.markdown("#### Photos Pending Review")
        
        # Mock pending photos
        pending_photos = [
            {"id": 1, "user": "plantlover", "caption": "My new garden setup", "date": "2025-04-27"},
            {"id": 2, "user": "greenthumb", "caption": "Urban farming initiative", "date": "2025-04-28"}
        ]
        
        for photo in pending_photos:
            with st.container():
                st.markdown(f"**User:** {photo['user']}")
                st.markdown(f"**Caption:** {photo['caption']}")
                st.markdown(f"**Date:** {photo['date']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Approve", key=f"approve_{photo['id']}"):
                        st.success(f"Photo #{photo['id']} approved!")
                with col2:
                    if st.button("Reject", key=f"reject_{photo['id']}"):
                        st.error(f"Photo #{photo['id']} rejected!")
                
                st.markdown("---")
    
    with moderation_tabs[1]:
        st.markdown("#### Reported Comments")
        
        # Mock reported comments
        reported_comments = [
            {"id": 1, "user": "anonymoususer", "comment": "This is spam content", "reported_by": "greenthumb", "date": "2025-04-26"},
        ]
        
        for comment in reported_comments:
            with st.container():
                st.markdown(f"**User:** {comment['user']}")
                st.markdown(f"**Comment:** {comment['comment']}")
                st.markdown(f"**Reported by:** {comment['reported_by']}")
                st.markdown(f"**Date:** {comment['date']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Keep", key=f"keep_{comment['id']}"):
                        st.success(f"Comment #{comment['id']} kept!")
                with col2:
                    if st.button("Delete", key=f"delete_{comment['id']}"):
                        st.warning(f"Comment #{comment['id']} deleted!")
                with col3:
                    if st.button("Ban User", key=f"ban_{comment['id']}"):
                        st.error(f"User banned!")
                
                st.markdown("---")
    
    # System statistics
    st.markdown("### System Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Users", "248", "+12 today")
    with col2:
        st.metric("Server Load", "23%", "-5%")
    with col3:
        st.metric("Storage Used", "4.2 GB", "+0.3 GB")
    
    # System maintenance
    st.markdown("### System Maintenance")
    
    maintenance_options = st.multiselect(
        "Maintenance Tasks",
        ["Clear Cache", "Backup Database", "Update User Statistics", "Check for System Updates"]
    )
    
    if st.button("Run Maintenance") and maintenance_options:
        with st.spinner("Running maintenance tasks..."):
            time.sleep(2)
            st.success(f"Completed {len(maintenance_options)} maintenance tasks!")

# ------ MAIN APP ------
def main():
    global name, username
    
    # Authentication
    name, username = setup_authentication()
    
    # Initialize data
    billboards = initialize_data()
    
    # Display sidebar and get selected page
    page = display_sidebar(name, username)
    
    # Display selected page content
    if page == "Home":
        display_home(billboards)
    elif page == "My Plants":
        display_my_plants()
    elif page == "Community":
        display_community()
    elif page == "Sponsor Dashboard":
        display_sponsor_dashboard()
    elif page == "Admin Panel":
        display_admin_panel()

if __name__ == "__main__":
    main()
