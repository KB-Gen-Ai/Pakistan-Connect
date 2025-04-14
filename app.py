import streamlit as st
from database import init_db, add_user, get_user, update_user
from profile_generator import generate_pdf, generate_qr_code

# Initialize DB
init_db()
from urllib.parse import unquote

query_params = st.experimental_get_query_params()
if "email" in query_params and "phone" in query_params:
    # PUBLIC VIEW MODE
    email_param = unquote(query_params["email"][0])
    phone_param = unquote(query_params["phone"][0])
    profile = get_user(email_param, phone_param)

    if profile:
        st.title("👤 Public Member Profile")
        st.markdown(f"**Name:** {profile[1]}")
        st.markdown(f"**City:** {profile[4]}, **Country:** {profile[5]}")
        st.markdown(f"**Job Title:** {profile[6]}, **Industry:** {profile[7]}")
        st.markdown(f"**Experience:** {profile[8]} years")
        st.markdown(f"**Expertise:** {profile[9]}")
        st.markdown(f"**Can Help With:** {profile[10]}")
        st.markdown(f"**LinkedIn:** {profile[11]}" if profile[11] else "")

        qr_path = generate_qr_code(profile[2], profile[3], profile[11])
        st.image(qr_path, caption="Scan to Contact")

        pdf_path = generate_pdf(profile)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Profile PDF", f, file_name="profile.pdf")

        st.stop()
    else:
        st.warning("❌ Profile not found.")
        st.stop()

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

        # Generate PDF + QR Code
        profile_data = (name, email, phone, city, country, job_title, industry, experience_years, expertise, help_areas, linkedin)
        pdf_path = generate_pdf(profile_data)
        qr_path = generate_qr_code(email, phone, linkedin)

        st.subheader("📎 Download Your Profile")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Profile PDF", f, file_name="profile.pdf")

        with open(qr_path, "rb") as f:
            st.download_button("🔗 Download QR Code", f, file_name="contact_qr.png")
