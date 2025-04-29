# ------ SPONSOR DASHBOARD ------
def display_sponsor_dashboard():
    """Displays the dashboard for sponsors."""
    st.markdown("<h1 class='sub-title'>📊 Sponsor Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Monitor campaign impact and performance.")

    # Key metrics
    st.markdown("### Key Performance Metrics (Overall)")
    col1, col2, col3 = st.columns(3)
    plants_grown = st.session_state.get('plants_grown',0)
    co2_offset = st.session_state.get('co2_offset',0)
    seed_kits = st.session_state.get('seed_kits',0)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Plants Grown", f"{plants_grown} 🌱", f"+{random.randint(50,150)} wk")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("CO₂ Offset", f"{co2_offset} kg", f"+{random.randint(10, 40)} kg")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Seed Kits Distributed", f"{seed_kits}", f"+{random.randint(30, 80)}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Campaign performance
    st.markdown("### Campaign Performance Analysis")
    # Ensure campaign_names is defined correctly
    campaign_names = ['Grow Your Greens', 'Message to Meal', 'Waste Awareness', 'Urban Farming']
    if not isinstance(campaign_names, list) or len(campaign_names) == 0:
        st.error("Campaign names configuration error.")
        return # Stop rendering if campaign names are invalid

    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    # Ensure the size matches the number of campaigns
    num_campaigns = len(campaign_names)
    try:
        engagement_data = pd.DataFrame(
            np.random.randint(10, 100, size=(30, num_campaigns)), # Use num_campaigns
            index=dates,
            columns=campaign_names
        ) * np.random.uniform(0.7, 1.5, size=num_campaigns) # Apply random multipliers safely

        growth_data = pd.DataFrame(
            np.random.rand(30, num_campaigns) * 5, # Use num_campaigns
            index=dates,
            columns=campaign_names
        ).cumsum()
    except ValueError as e:
        st.error(f"Error generating sample performance data: {e}")
        # Provide default empty dataframes to prevent downstream errors
        engagement_data = pd.DataFrame(index=dates, columns=campaign_names).fillna(0)
        growth_data = pd.DataFrame(index=dates, columns=campaign_names).fillna(0)


    tab_engage, tab_growth, tab_roi = st.tabs(["📈 Engagement", "🌱 Growth", "💰 ROI (Sim)"])
    with tab_engage: st.line_chart(engagement_data); st.caption("Simulated daily engagement (last 30 days)")
    with tab_growth: st.area_chart(growth_data); st.caption("Simulated cumulative growth (last 30 days)")
    with tab_roi:
        st.markdown("#### ROI (Illustrative)")
        # Ensure investment dict covers all campaigns or handle missing ones
        base_investment = {"Grow Your Greens": 15000, "Message to Meal": 12000, "Waste Awareness": 8000, "Urban Farming": 10000}
        investment = {c: base_investment.get(c, 10000) for c in campaign_names} # Default investment if missing

        # Ensure value calculation is robust
        eng_sum = engagement_data.sum()
        growth_last = growth_data.iloc[-1] if not growth_data.empty else pd.Series(0, index=campaign_names)
        value_generated = (eng_sum * 0.5 + growth_last * 10).round(0)

        roi_data = []
        for c in campaign_names:
            inv = investment.get(c, 1) # Use default 1 to avoid division by zero
            val = value_generated.get(c, 0)
            roi = ((val - inv) / inv * 100) if inv else 0
            roi_data.append({"Camp": c, "Invest ($)": inv, "Value ($)": val, "ROI (%)": roi})

        if roi_data:
            roi_df = pd.DataFrame(roi_data).round(1)
            st.dataframe(roi_df.set_index("Camp"), use_container_width=True)
        else:
            st.info("Could not calculate ROI data.")
        st.caption("Note: Illustrative values.")
    st.markdown("---")

    # Campaign management (No changes here)
    st.markdown("### Campaign Management")
    with st.expander("🚀 Launch New Campaign (Example Form)"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", key="sponsor_camp_name")
            campaign_desc = st.text_area("Description", key="sponsor_camp_desc")
            target_audience = st.multiselect("Audience", ["Urban Dwellers", "Families", "Students", "Eco-conscious"], key="sponsor_camp_audience")
        with col2:
            campaign_budget = st.number_input("Budget ($)", 1000, 100000, 10000, 500, key="sponsor_camp_budget")
            start_date = st.date_input("Start Date", key="sponsor_camp_start")
            end_date = st.date_input("End Date", key="sponsor_camp_end")
            uploaded_image = st.file_uploader("Billboard Image", type=['png', 'jpg'], key="sponsor_camp_img")
        if st.button("Submit Campaign Proposal", key="sponsor_camp_submit"):
             if all([campaign_name, campaign_desc, campaign_budget, start_date, end_date]) and start_date <= end_date:
                 st.success("Campaign proposal submitted for review!")
             else: st.warning("Please fill required fields correctly.")
    st.markdown("---")

    # Community analytics (No changes here)
    st.markdown("### Community Analytics")
    col_demo, col_engage = st.columns(2)
    with col_demo:
        st.markdown("#### User Demographics (Sample)")
        demo_data = pd.DataFrame({"Age Group": ["18-24", "25-34", "35-44", "45-54", "55+"], "Percentage": [18, 35, 25, 15, 7]})
        st.bar_chart(demo_data.set_index("Age Group"))
    with col_engage:
        st.markdown("#### Engagement (Sample)")
        # This calculation remains the same, used for display here
        uploads_count = len(st.session_state.get('uploads',[]))
        comments_count = len(st.session_state.get('comments',[]))
        likes_photos = sum(u.get('likes',0) for u in st.session_state.get('uploads',[]))
        likes_comments = sum(c.get('likes',0) for c in st.session_state.get('comments',[]))
        # Estimate claims based on total kits distributed minus starting range
        base_kits = random.randint(700, 800) # Assume a base number of kits before current period
        kit_claims = max(0, st.session_state.get('seed_kits', 0) - base_kits)
        engage_data_display = {"Metric": ["Photos", "Comments", "Likes (Photos)", "Likes (Comments)", "Kit Claims"],
                               "Count (Recent)": [uploads_count, comments_count, likes_photos, likes_comments, kit_claims] }
        engage_df_display = pd.DataFrame(engage_data_display)
        st.bar_chart(engage_df_display.set_index("Metric"))
    st.markdown("---")

    # --- Download Reports ---
    st.markdown("### Download Reports")
    # Make sure report types list is correct
    report_types = ["Campaign Summary", "Engagement Analysis", "Impact Estimate"]
    report_type = st.selectbox("Report Type", report_types, key="report_type_select")
    col_format, col_generate = st.columns([1, 2])
    with col_format: report_format = st.radio("Format", ["CSV", "PDF"], key="report_format_radio")
    with col_generate:
        report_filename = f"{report_type.lower().replace(' ', '_')}_report_{datetime.now():%Y%m%d}.{report_format.lower()}"

        # Generate report data based on type
        try:
            if report_type == "Campaign Summary":
                # FIXED: Calculate SUM for summary, reset index, and rename columns
                if not engagement_data.empty:
                     engagement_summary = engagement_data.sum()
                     report_data_df = engagement_summary.reset_index().rename(columns={'index':'Campaign', 0:'Total Engagement'})
                else:
                     report_data_df = pd.DataFrame({'Campaign': [], 'Total Engagement': []})
                     st.warning("No engagement data available for summary report.")

            elif report_type == "Engagement Analysis":
                # Use the same data calculated for the display chart above
                # Regenerate here to ensure scope is correct
                uploads_count = len(st.session_state.get('uploads',[]))
                comments_count = len(st.session_state.get('comments',[]))
                likes_photos = sum(u.get('likes',0) for u in st.session_state.get('uploads',[]))
                likes_comments = sum(c.get('likes',0) for c in st.session_state.get('comments',[]))
                base_kits = random.randint(700, 800) # Re-use consistent logic if needed
                kit_claims = max(0, st.session_state.get('seed_kits', 0) - base_kits)
                engage_data_report = {"Metric": ["Photos", "Comments", "Likes (Photos)", "Likes (Comments)", "Kit Claims"],
                                      "Count (Recent)": [uploads_count, comments_count, likes_photos, likes_comments, kit_claims] }
                report_data_df = pd.DataFrame(engage_data_report)

            elif report_type == "Impact Estimate":
                # Use session state values
                plants = st.session_state.get('plants_grown',0)
                co2 = st.session_state.get('co2_offset',0)
                kits = st.session_state.get('seed_kits',0)
                report_data_df = pd.DataFrame({'Metric':['Plants','CO2 Offset','Kits Distributed'],'Value':[plants, co2, kits]})

            else: # Should not happen with selectbox, but good practice
                st.error(f"Unknown report type selected: {report_type}")
                report_data_df = pd.DataFrame() # Empty dataframe

            # Proceed only if report_data_df is a valid DataFrame
            if isinstance(report_data_df, pd.DataFrame) and not report_data_df.empty:
                report_data_csv = report_data_df.to_csv(index=False).encode('utf-8')
                report_data_pdf = b"Sample PDF data (generation not implemented)" # Placeholder PDF data
                report_data = report_data_csv if report_format == "CSV" else report_data_pdf
                mime_type = "text/csv" if report_format == "CSV" else "application/pdf"

                if st.button("Generate & Download Report", key="generate_report_btn"):
                    with st.spinner("Generating..."):
                        time.sleep(1.0) # Shorter sleep
                    # Use the button itself to trigger download after generation
                    st.download_button(
                        label=f"Download {report_format}",
                        data=report_data,
                        file_name=report_filename,
                        mime=mime_type,
                        key="download_report_final" # Keep a unique key
                        )
                    # st.success("Report ready for download.") # Optional success message
            elif isinstance(report_data_df, pd.DataFrame) and report_data_df.empty and report_type == "Campaign Summary":
                 # Specific message if summary is empty
                 st.info("No data to generate for Campaign Summary report.")
                 # Disable button or don't show it
                 st.button("Generate & Download Report", key="generate_report_btn_disabled", disabled=True)
            else:
                 # Generic message for other empty DFs or errors
                 st.warning("Could not generate data for the selected report.")
                 st.button("Generate & Download Report", key="generate_report_btn_disabled_other", disabled=True)


        except Exception as e:
             st.error(f"An error occurred during report data generation: {e}")
             # Log the error traceback for debugging
             st.exception(e)
             # Prevent download button from showing if data generation failed
             st.button("Generate & Download Report", key="generate_report_btn_error", disabled=True)

# --- The rest of the code remains the same ---

# (Keep initialize_data, display_sidebar, display_home, display_my_plants,
# display_community, display_admin_panel, and main functions as they were
# in the previous 'no authentication' version)

# ------ MAIN APP LOGIC ------
def main():
    """Main function to run the Streamlit application without authentication."""

    # --- Data Initialization ---
    billboards = initialize_data()

    # --- Sidebar Navigation & Role Simulation ---
    page, simulated_role = display_sidebar()

    # --- Define Generic User Name for Community ---
    current_user_name = "Demo User" # Name used for posts when no login exists

    # --- Page Content Rendering ---
    if page == "Home":
        display_home(billboards)
    elif page == "My Plants":
        display_my_plants()
    elif page == "Community":
        display_community(current_user_name) # Pass generic name
    elif page == "Sponsor Dashboard":
        # Access is controlled by sidebar, but good practice to check role if needed
        if simulated_role in ["sponsor", "admin"]:
            display_sponsor_dashboard()
        else:
            st.error("Access Denied (Simulated Role: User)") # Should not happen if sidebar is correct
            # Optional: Redirect to home or show limited view
    elif page == "Admin Panel":
        if simulated_role == "admin":
            display_admin_panel()
        else:
            st.error("Access Denied (Simulated Role: User/Sponsor)") # Should not happen
            # Optional: Redirect

    # --- Footer ---
    st.markdown("---")
    st.caption("🌿 Growvertising Demo © 2025 | Transforming Ads into Action")

if __name__ == "__main__":
    main()
