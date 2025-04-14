import streamlit as st
from database import init_db, add_user, get_user, update_user

# Initialize DB
init_db()

st.set_page_config(page_title="Pakistan Connect", layout="centered")

st.title("🇵🇰 Pakistan Connect — Member Profile Form")
st.markdown("Please fill your details to join the national collaboration hub.")

# Step 1: Identification
st.subheader("🔑 Identification")
email = st.text_input("Email", key="email")
phone = st.text_input("Phone", key="phone")

if email and phone:
    existing_user = get_user(email, phone)
else:
    existing_user = None

# Step 2: Profile Info
st.subheader("👤 Personal & Professional Info")

name = st.text_input("Full Name", value=existing_user[1] if existing_user else "")
city = st.text_input("City", value=existing_user[4] if existing_user else "")
country = st.text_input("Country", value=existing_user[5] if existing_user else "Pakistan")
job_title = st.text_input("Job Title", value=existing_user[6] if existing_user else "")
industry = st.text_input("Industry", value=existing_user[7] if existing_user else "")
experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, value=existing_user[8] if existing_user else 0)

expertise = st.text_area("Areas of Expertise (comma separated)", value=existing_user[9] if existing_user else "")
help_areas = st.text_area("How can you help others? (comma separated)", value=existing_user[10] if existing_user else "")
linkedin = st.text_input("LinkedIn or Profile URL (optional)", value=existing_user[11] if existing_user else "")

# Step 3: Submit
if st.button("💾 Submit"):
    if not name or not email or not phone:
        st.warning("Name, email, and phone are required.")
    else:
        if existing_user:
            update_user(
                (name, city, country, job_title, industry, experience_years, expertise, help_areas, linkedin),
                email, phone
            )
            st.success("✅ Profile updated successfully!")
        else:
            success, msg = add_user((name, email, phone, city, country, job_title, industry, experience_years, expertise, help_areas, linkedin))
            if success:
                st.success("✅ Profile submitted successfully!")
            else:
                st.warning(f"⚠️ {msg}")

