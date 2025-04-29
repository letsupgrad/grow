# --- IMPORTS ---
import streamlit as st
from datetime import datetime
import random
import pandas as pd
import numpy as np
import time
import io

# ------ PAGE CONFIGURATION ------
st.set_page_config(
    page_title="Growvertising - Billboard to Farmboard (Demo)",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------ CSS STYLING ------
st.markdown("""
<style>
    .main-title { font-size: 42px !important; color: #2E7D32; text-align: center; }
    .sub-title { font-size: 28px !important; color: #388E3C; }
    .sidebar-text { font-size: 16px; }
    .highlight { background-color: #E8F5E9; padding: 10px; border-radius: 5px; }
    .metric-card { background-color: #F1F8E9; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .stButton>button { width: 100%; margin-bottom: 5px; }
    .stContainer { border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ------ DATA INITIALIZATION FUNCTION ------
# MUST BE DEFINED BEFORE main()
def initialize_data():
    """Initializes session state variables and static data."""
    if "comments" not in st.session_state: st.session_state["comments"] = []
    if "uploads" not in st.session_state: st.session_state["uploads"] = []
    if "plants_grown" not in st.session_state: st.session_state["plants_grown"] = random.randint(1000, 1500)
    if "co2_offset" not in st.session_state: st.session_state["co2_offset"] = random.randint(300, 500)
    if "seed_kits" not in st.session_state: st.session_state["seed_kits"] = random.randint(700, 1000)
    if "last_visit" not in st.session_state: st.session_state["last_visit"] = datetime.now()
    if "user_plants" not in st.session_state:
        st.session_state["user_plants"] = [
            {"name": "Tomato", "progress": random.randint(20, 95), "days_old": random.randint(5, 30), "planted_date": datetime(2025, 1, 15)},
            {"name": "Basil", "progress": random.randint(20, 95), "days_old": random.randint(5, 30), "planted_date": datetime(2025, 2, 3)} ]
    if "user_plant_history" not in st.session_state:
         st.session_state["user_plant_history"] = [
                {"Plant Type": "Lettuce", "Date Planted": "2025-02-28", "Harvest Date": "2025-04-10", "Success": "Yes"},
                {"Plant Type": "Spinach", "Date Planted": "2025-03-10", "Harvest Date": "Failed", "Success": "No"} ]
    if "simulated_role" not in st.session_state: st.session_state["simulated_role"] = "user"
    if not st.session_state.get("comments_initialized"): # Add initialization check for sample comments
        st.session_state["comments_initialized"] = False

    billboards = {
        "Grow Your Greens": {"url": "https://i.imgur.com/U4A0lRQ.jpg", "description": "Promoting home vegetable gardening.", "sponsor": "OrganicFoods Co."},
        "From Message to Meal": {"url": "https://i.imgur.com/GQhuf0U.jpg", "description": "Turning ad space into food production.", "sponsor": "EcoEats"},
        "Food Waste Awareness": {"url": "https://i.imgur.com/XY5NJJx.jpg", "description": "Highlighting reducing food waste.", "sponsor": "WasteNot Foundation"},
        "Urban Farming Revolution": {"url": "https://i.imgur.com/U4A0lRQ.jpg", "description": "Transforming city spaces.", "sponsor": "CityGrow Initiative"} }
    return billboards

# ------ SIDEBAR CONTENT FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_sidebar():
    """Displays the navigation sidebar and allows role simulation."""
    st.sidebar.markdown("## 🌿 Navigation")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Simulate User Role")
    roles = ["user", "sponsor", "admin"]
    default_role_index = roles.index(st.session_state.get("simulated_role", "user"))
    simulated_role = st.sidebar.selectbox(
        "Select Role", roles, index=default_role_index, key="simulated_role_selector",
        format_func=lambda x: x.capitalize() )
    st.session_state["simulated_role"] = simulated_role
    st.sidebar.markdown("---")

    available_pages = ["Home", "My Plants", "Community"]
    if simulated_role in ["sponsor", "admin"]: available_pages.append("Sponsor Dashboard")
    if simulated_role == "admin": available_pages.append("Admin Panel")
    default_index = 0
    page = st.sidebar.radio("Go to", available_pages, index=default_index, key="navigation_radio")
    st.sidebar.markdown("---")

    activity_score = random.randint(10, 100)
    if activity_score > 80: badge = "🌟 Super Grower"
    elif activity_score > 50: badge = "🌿 Urban Farmer"
    else: badge = "🍀 Green Starter"
    st.sidebar.markdown(f"### Profile ({simulated_role.capitalize()})")
    st.sidebar.markdown(f"**Badge:** {badge}")
    st.sidebar.progress(activity_score / 100)
    plants_grown_user = len(st.session_state.get("user_plants", []))
    st.sidebar.markdown(f"**Plants Growing:** {plants_grown_user}")
    st.sidebar.markdown(f"**Est. CO₂ Offset:** {plants_grown_user * random.randint(2, 5)} kg")

    with st.sidebar.expander("Need Help?"):
        st.markdown("""
        - **Home**: View campaigns & progress.
        - **My Plants**: Manage your plants.
        - **Community**: Share & interact.
        - **Sponsor Dashboard**: View metrics.
        - **Admin Panel**: Manage users/content.
        - **Support**: help@growvertising.com
        """)
    return page, simulated_role

# ------ HOME PAGE FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_home(billboards):
    st.markdown("<h1 class='main-title'>🌿 Growvertising – Billboard to Farmboard</h1>", unsafe_allow_html=True)
    st.markdown("Turn every ad into action – grow plants, offset carbon, and join the green movement.")
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
    st.markdown("---")
    st.markdown("<h2 class='sub-title'>🖼️ Featured Campaigns</h2>", unsafe_allow_html=True)
    selected_ad = st.selectbox("Select Campaign", list(billboards.keys()), key="campaign_select")
    col_img, col_details = st.columns([2, 1])
    with col_img: st.image(billboards[selected_ad]["url"], caption=selected_ad, use_column_width='always')
    with col_details:
        st.markdown(f"### {selected_ad}")
        st.markdown(f"**Description:** {billboards[selected_ad]['description']}")
        st.markdown(f"**Sponsor:** {billboards[selected_ad]['sponsor']}")
        st.markdown("---")
        st.markdown("### Get Involved")
        if st.button("Request Seed Kit", key=f"seed_kit_{selected_ad}"):
            st.session_state["seed_kits"] += 1; st.success("Seed kit requested!"); st.balloons()
        if st.button("Support Campaign", key=f"support_{selected_ad}"):
            st.balloons(); st.success("Thank you!")
    st.markdown("---")
    st.markdown("<h2 class='sub-title'>🌱 Simulated Billboard Growth</h2>", unsafe_allow_html=True)
    st.info("Simulated representation of plant growth.")
    col_growth, col_days, col_water = st.columns(3)
    with col_growth:
        growth = random.randint(60, 90); st.progress(growth / 100); st.markdown(f"**Growth:** {growth}%")
    with col_days:
        days = max(0, 30-int((growth/100)*30)); delta = -1 if days<30 else 0; st.metric("Days Left", f"{days}", f"{delta}")
    with col_water:
        status = random.choice(["Optimal", "Needs Water"]); st.metric("Water Level", status)
        if status == "Needs Water": st.warning("💧 Low!") else: st.success("💧 Good.")
    st.markdown("---")
    st.markdown("<h2 class='sub-title'>🌤️ Current Conditions (Example)</h2>", unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4); c1.metric("Temp", "24°C"); c2.metric("Humidity", "65%"); c3.metric("Sunlight", "Good"); c4.metric("Soil", "Okay")

# ------ MY PLANTS PAGE FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_my_plants():
    st.markdown("<h1 class='sub-title'>🌱 My Plants</h1>", unsafe_allow_html=True)
    st.markdown("Track and manage your growing plants.")
    plant_types = ["Tomato", "Basil", "Lettuce", "Spinach", "Mint", "Pepper", "Chives"]
    col_manage, col_add = st.columns([2, 1])
    with col_manage:
        tab_current, tab_history = st.tabs(["Current Plants", "Plant History"])
        with tab_current:
            st.markdown("### Currently Growing")
            if not st.session_state.get("user_plants"): st.info("Add plants using the form.")
            else:
                for i, plant in enumerate(st.session_state["user_plants"]):
                    with st.container():
                        st.markdown(f"#### {plant['name']}")
                        st.progress(plant['progress'] / 100)
                        ca, cb, cc = st.columns(3)
                        ca.markdown(f"**Progress:** {plant['progress']}%")
                        days = (datetime.now() - plant['planted_date']).days; cb.markdown(f"**Days:** {days}")
                        health = 'Good' if plant['progress']>60 else 'Needs Attention' if plant['progress']>30 else 'Struggling'
                        cc.markdown(f"**Health:** {health}")
                        c_act1, c_act2 = st.columns(2)
                        if c_act1.button("Update", key=f"upd_{i}"):
                            st.session_state["user_plants"][i]["progress"] = min(100, plant['progress'] + random.randint(5,15)); st.rerun()
                        if c_act2.button("Finish", key=f"fin_{i}"):
                            h_plant = st.session_state["user_plants"].pop(i)
                            st.session_state["user_plant_history"].append({
                                "Plant Type": h_plant['name'], "Date Planted": h_plant['planted_date'].strftime('%Y-%m-%d'),
                                "Harvest Date": datetime.now().strftime('%Y-%m-%d'), "Success": "Yes" })
                            st.success(f"{h_plant['name']} history updated."); st.rerun()
                        st.markdown("---")
        with tab_history:
            st.markdown("### Plant History")
            if not st.session_state.get("user_plant_history"): st.info("No history.")
            else: st.dataframe(pd.DataFrame(st.session_state["user_plant_history"]), use_container_width=True, hide_index=True)
    with col_add:
        st.markdown("### Add New Plant")
        with st.form("add_plant_form", clear_on_submit=True):
            type = st.selectbox("Type", plant_types, key="np_type")
            date = st.date_input("Planted", datetime.now().date(), key="np_date")
            notes = st.text_area("Notes", key="np_notes")
            if st.form_submit_button("Start Growing"):
                st.session_state["user_plants"].append({
                    "name": type, "progress": random.randint(5, 15),
                    "planted_date": datetime.combine(date, datetime.min.time()), "notes": notes })
                st.success(f"Added {type}!"); st.balloons()
        st.markdown("---")
        st.markdown("### Care Tips")
        tip = random.choice(["Tomatoes love sun.", "Basil likes moist soil.", "Lettuce dislikes heat.", "Rotate crops.", "Check for pests."])
        st.info(f"💡 Tip: {tip}")
        st.markdown("### Tasks (Example)")
        st.markdown("- Water tomatoes\n- Harvest lettuce\n- Fertilize basil")

# ------ COMMUNITY PAGE FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_community(current_user_name="Demo User"):
    st.markdown("<h1 class='sub-title'>👨‍👩‍👧‍👦 Community Hub</h1>", unsafe_allow_html=True)
    st.markdown("Share progress, ask questions, connect!")
    tab_photos, tab_comments = st.tabs(["📸 Photo Wall", "💬 Discussion"])
    with tab_photos:
        st.markdown("### Share Photos")
        uploaded_file = st.file_uploader("Upload photo!", type=["jpg", "png", "jpeg"], key="photo_uploader")
        caption = st.text_input("Caption", key="photo_caption")
        location = st.text_input("Location (optional)", key="photo_location")
        if st.button("Upload", key="upload_photo_btn") and uploaded_file:
            if caption:
                img_bytes = uploaded_file.getvalue()
                st.session_state["uploads"].append({
                    "image_bytes": img_bytes, "caption": caption, "location": location or "Unknown",
                    "user": current_user_name, "timestamp": datetime.now(), "likes": 0 })
                st.success("Uploaded! 🌿"); st.rerun()
            else: st.warning("Add caption.")
        elif st.button("Upload", key="upload_photo_btn_no") and not uploaded_file: st.warning("Select photo.")
        st.markdown("---")
        st.markdown("### Recent Photos")
        if not st.session_state.get("uploads"): st.info("No photos yet.")
        else:
            cols = st.columns(3)
            for i, upload in enumerate(reversed(st.session_state["uploads"])):
                with cols[i % 3], st.container():
                    try: st.image(upload["image_bytes"], caption=f"{upload['caption']} ({upload['user']})", use_column_width='always')
                    except Exception as e: st.error(f"Bad image: {e}")
                    key = f"like_photo_{upload['timestamp'].isoformat()}"; likes = upload.get("likes", 0)
                    if st.button(f"❤️ {likes}", key=key):
                        for u in st.session_state["uploads"]:
                            if u["timestamp"] == upload["timestamp"]: u["likes"] = u.get("likes", 0) + 1; break
                        st.rerun()
                    st.caption(f"📍 {upload['location']} | ⏰ {upload['timestamp']:%Y-%m-%d %H:%M}")
    with tab_comments:
        st.markdown("### 💬 Discussion")
        with st.form("comment_form", clear_on_submit=True):
            txt = st.text_area("Leave message!", max_chars=300, height=100, key="cmt_txt")
            if st.form_submit_button("Post") and txt:
                st.session_state["comments"].append({
                    "user": current_user_name, "comment": txt, "timestamp": datetime.now(), "likes": 0 })
                st.success("Posted! 💬")
            elif st.form_submit_button("Post") and not txt: st.warning("Enter comment.")
        st.markdown("---")
        st.markdown("### Recent Comments:")
        # Initialize sample comments only once
        if not st.session_state.get("comments_initialized"):
            if not st.session_state.get("comments"): # Check if comments list is actually empty
                st.session_state["comments"] = [
                    {"user": "GreenThumb", "comment": "Harvested!", "timestamp": datetime(2025, 4, 25, 14, 32), "likes": 12},
                    {"user": "PlantLover", "comment": "Yellowing basil?", "timestamp": datetime(2025, 4, 26, 9, 15), "likes": 8},
                    {"user": "UrbanFarmer", "comment": "Garden progress!", "timestamp": datetime(2025, 4, 27, 16, 45), "likes": 15} ]
            st.session_state["comments_initialized"] = True # Mark as initialized

        if not st.session_state.get("comments"): st.info("No comments yet.")
        else:
             for i, entry in enumerate(reversed(st.session_state["comments"])):
                 with st.container():
                     st.markdown(f"**{entry['user']}** ({entry['timestamp']:%Y-%m-%d %H:%M})")
                     st.markdown(f"> {entry['comment']}")
                     key = f"like_cmt_{entry['timestamp'].isoformat()}"; likes = entry.get("likes", 0)
                     if st.button(f"❤️ {likes}", key=key, help="Like"):
                          for c in st.session_state["comments"]:
                              if c["timestamp"] == entry["timestamp"]: c["likes"] = c.get("likes", 0) + 1; break
                          st.rerun()
                     st.markdown("---")

# ------ SPONSOR DASHBOARD FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_sponsor_dashboard():
    st.markdown("<h1 class='sub-title'>📊 Sponsor Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Monitor campaign impact and performance.")
    st.markdown("### Key Performance Metrics (Overall)")
    col1, col2, col3 = st.columns(3)
    plants, co2, kits = st.session_state.get('plants_grown',0), st.session_state.get('co2_offset',0), st.session_state.get('seed_kits',0)
    with col1: st.markdown("<div class='metric-card'>",True); st.metric("Plants Grown", f"{plants} 🌱", f"+{random.randint(50,150)} wk"); st.markdown("</div>",True)
    with col2: st.markdown("<div class='metric-card'>",True); st.metric("CO₂ Offset", f"{co2} kg", f"+{random.randint(10, 40)} kg"); st.markdown("</div>",True)
    with col3: st.markdown("<div class='metric-card'>",True); st.metric("Kits Distributed", f"{kits}", f"+{random.randint(30, 80)}"); st.markdown("</div>",True)
    st.markdown("---")

    st.markdown("### Campaign Performance Analysis")
    camp_names = ['Grow Greens', 'Msg->Meal', 'Waste Aware', 'Urban Farm']
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    n_camps = len(camp_names)
    try:
        eng_data = pd.DataFrame(np.random.randint(10, 100, (30, n_camps)), index=dates, columns=camp_names) * np.random.uniform(0.7, 1.5, n_camps)
        grw_data = pd.DataFrame(np.random.rand(30, n_camps)*5, index=dates, columns=camp_names).cumsum()
    except Exception as e:
        st.error(f"Data gen error: {e}"); eng_data = pd.DataFrame(); grw_data = pd.DataFrame()

    tab_eng, tab_grw, tab_roi = st.tabs(["📈 Engagement", "🌱 Growth", "💰 ROI (Sim)"])
    with tab_eng: st.line_chart(eng_data); st.caption("Sim. daily engagement (30d)")
    with tab_grw: st.area_chart(grw_data); st.caption("Sim. cumulative growth (30d)")
    with tab_roi:
        st.markdown("#### ROI (Illustrative)")
        inv_base = {"Grow Greens": 15k, "Msg->Meal": 12k, "Waste Aware": 8k, "Urban Farm": 10k} # Simplified amounts
        inv = {c: inv_base.get(c, 10000) for c in camp_names}
        eng_sum = eng_data.sum() if not eng_data.empty else pd.Series(0, index=camp_names)
        grw_last = grw_data.iloc[-1] if not grw_data.empty else pd.Series(0, index=camp_names)
        val_gen = (eng_sum*0.5 + grw_last*10).round(0)
        roi_data = []
        for c in camp_names:
            cost=inv.get(c,1); val=val_gen.get(c,0); roi=((val-cost)/cost*100) if cost else 0
            roi_data.append({"Campaign": c, "Invest ($)": cost, "Value ($)": val, "ROI (%)": roi})
        if roi_data: st.dataframe(pd.DataFrame(roi_data).round(1).set_index("Campaign"), use_container_width=True)
        else: st.info("ROI data N/A.")
        st.caption("Note: Illustrative values.")
    st.markdown("---")

    st.markdown("### Campaign Management")
    with st.expander("🚀 Launch New Campaign (Example)"):
        c1, c2 = st.columns(2)
        with c1: name=st.text_input("Name", key="sp_c_n"); desc=st.text_area("Desc", key="sp_c_d"); aud=st.multiselect("Audience", ["Urban", "Families", "Students"], key="sp_c_a")
        with c2: bud=st.number_input("Budget ($)", 1k, 100k, 10k, 500, key="sp_c_b"); sd=st.date_input("Start", key="sp_c_s"); ed=st.date_input("End", key="sp_c_e"); img=st.file_uploader("Image", ['png','jpg'], key="sp_c_i")
        if st.button("Submit Proposal", key="sp_c_sub"):
            if all([name, desc, bud, sd, ed]) and sd <= ed: st.success("Submitted!")
            else: st.warning("Fill required fields.")
    st.markdown("---")

    st.markdown("### Community Analytics")
    col_dem, col_eng = st.columns(2)
    with col_dem:
        st.markdown("#### Demographics (Sample)")
        dem_df = pd.DataFrame({"Age": ["18-24","25-34","35-44","45+"], "%": [18,35,25,22]})
        st.bar_chart(dem_df.set_index("Age"))
    with col_eng:
        st.markdown("#### Engagement (Sample)")
        up_c = len(st.session_state.get('uploads',[])); cmt_c = len(st.session_state.get('comments',[]))
        lk_p = sum(u.get('likes',0) for u in st.session_state.get('uploads',[])); lk_c = sum(c.get('likes',0) for c in st.session_state.get('comments',[]))
        kit_c = max(0, st.session_state.get('seed_kits', 0) - random.randint(700,800))
        eng_df_disp = pd.DataFrame({"Metric": ["Photos", "Comments", "Likes (Ph)", "Likes (Cmt)", "Kit Claims"], "Count": [up_c, cmt_c, lk_p, lk_c, kit_c]})
        st.bar_chart(eng_df_disp.set_index("Metric"))
    st.markdown("---")

    st.markdown("### Download Reports")
    rep_types = ["Campaign Summary", "Engagement Analysis", "Impact Estimate"]
    rep_type = st.selectbox("Report Type", rep_types, key="rep_type_sel")
    cf, cg = st.columns([1, 2])
    with cf: rep_fmt = st.radio("Format", ["CSV", "PDF"], key="rep_fmt_rad")
    with cg:
        rep_fname = f"{rep_type.lower().replace(' ','_')}_report_{datetime.now():%Y%m%d}.{rep_fmt.lower()}"
        rep_df = pd.DataFrame() # Init empty
        try:
            if rep_type == "Campaign Summary":
                if not eng_data.empty: rep_df=eng_data.sum().reset_index().rename(columns={'index':'Campaign',0:'Engagement'})
                else: st.warning("No data for Campaign Summary.")
            elif rep_type == "Engagement Analysis":
                 rep_df = eng_df_disp.rename(columns={'Count':'Value'}) # Use display data
            elif rep_type == "Impact Estimate":
                 rep_df = pd.DataFrame({'Metric':['Plants','CO2 (kg)','Kits'],'Value':[plants,co2,kits]})
            else: st.error("Unknown report.")

            if not rep_df.empty:
                csv = rep_df.to_csv(index=False).encode('utf-8')
                pdf = b"Sample PDF" # Placeholder
                data = csv if rep_fmt == "CSV" else pdf
                mime = "text/csv" if rep_fmt == "CSV" else "application/pdf"
                if st.button("Generate & Download", key="gen_rep_btn"):
                    with st.spinner("Generating..."): time.sleep(1.0)
                    st.download_button(f"Download {rep_fmt}", data, rep_fname, mime, key="dl_rep_final")
            else:
                 st.button("Generate & Download", key="gen_rep_btn_dis", disabled=True)
        except Exception as e:
            st.error(f"Report gen error: {e}"); st.exception(e)
            st.button("Generate & Download", key="gen_rep_btn_err", disabled=True)

# ------ ADMIN PANEL FUNCTION ------
# MUST BE DEFINED BEFORE main()
def display_admin_panel():
    st.markdown("<h1 class='sub-title'>🔧 Admin Panel</h1>", unsafe_allow_html=True)
    st.info("Displaying administrative functions (simulation only).")
    tabs = st.tabs(["👤 Users (Sim)", "💬 Content (Sim)", "📈 Stats (Sim)", "⚙️ Settings (Sim)"])
    with tabs[0]:
        st.markdown("### User Management (Simulated)")
        users_df=pd.DataFrame({"Username": ["user_a","user_b","sponsor_x"], "Role": ["user","user","sponsor"], "Status": ["Active","Active","Active"]})
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        st.button("Save (Disabled)", disabled=True)
    with tabs[1]:
        st.markdown("### Content Moderation (Simulated)")
        t_ph, t_cm = st.tabs(["Pending Photos", "Reported Comments"])
        with t_ph:
            st.markdown("#### Photos Pending"); st.info("No photos pending (Sim).")
            # Mock display logic if needed
        with t_cm:
            st.markdown("#### Reported Comments"); st.info("No comments reported (Sim).")
            # Mock display logic if needed
    with tabs[2]:
        st.markdown("### System Statistics (Simulated)")
        c1,c2,c3=st.columns(3); c1.metric("Users","248"); c2.metric("Load","23%"); c3.metric("Storage","4.2GB")
        st.markdown("#### Activity (Sample)"); st.line_chart(np.random.rand(7, 2), use_container_width=True)
    with tabs[3]:
        st.markdown("### Settings & Maintenance (Simulated)")
        st.toggle("Enable Reg.", True, disabled=True); st.number_input("Max Upload", 1, 20, 5, disabled=True)
        st.markdown("---"); st.markdown("#### Maintenance")
        tasks = st.multiselect("Select Tasks", ["Clear Cache", "Backup DB"])
        if st.button("Run Tasks (Sim)") and tasks:
            prg = st.progress(0); txt=st.empty()
            for i,t in enumerate(tasks): txt.info(f"Running: {t}"); time.sleep(0.8); prg.progress((i+1)/len(tasks))
            txt.success("Done! (Sim)"); st.balloons()
        elif st.button("Run Tasks (Sim)") and not tasks: st.warning("Select tasks.")

# ------ MAIN FUNCTION ------
# MUST BE DEFINED AFTER ALL OTHER FUNCTIONS
def main():
    """Main function to run the Streamlit application."""
    # --- Initialization ---
    # This MUST be called after initialize_data is defined
    billboards = initialize_data()

    # --- Sidebar & Page Selection ---
    # This MUST be called after display_sidebar is defined
    page, simulated_role = display_sidebar()

    # --- User Name for Community ---
    current_user_name = "Demo User"

    # --- Page Rendering ---
    # This requires all display_ functions to be defined first
    if page == "Home":
        display_home(billboards)
    elif page == "My Plants":
        display_my_plants()
    elif page == "Community":
        display_community(current_user_name)
    elif page == "Sponsor Dashboard":
        if simulated_role in ["sponsor", "admin"]:
            display_sponsor_dashboard()
        else:
            st.error("Access Denied")
    elif page == "Admin Panel":
        if simulated_role == "admin":
            display_admin_panel()
        else:
            st.error("Access Denied")

    # --- Footer ---
    st.markdown("---")
    st.caption("🌿 Growvertising Demo © 2025")

# ------ SCRIPT EXECUTION GUARD ------
# This should be the LAST part of the script
if __name__ == "__main__":
    main() # Call main() only when script is run directly
