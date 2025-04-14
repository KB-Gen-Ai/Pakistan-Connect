import streamlit as st
from database import init_db, save_user, search_users, get_user_by_keys, get_all_users
from pdf_generator import generate_pdf
from qr_generator import generate_qr_code
import tempfile

st.set_page_config(page_title="Pakistan Connect", layout="centered")

st.title("🇵🇰 Pakistan Connect")
st.markdown("Helping Pakistanis globally connect, collaborate, and grow 🌍")

init_db()

# --- Profile Creation / Editing ---
st.header("👤 Create or Update Your Profile")

with st.form("profile_form"):
    name = st.text_input("Full Name", max_chars=50)
    email = st.text_input("Email")
    phone = st.text_input("Phone (without +)")
    city = st.text_input("City")
    country = st.text_input("Country")
    job_title = st.text_input("Job Title")
    industry = st.text_input("Industry")
    experience = st.slider("Years of Experience", 0, 50, 5)
    expertise = st.text_area("Your Areas of Expertise (comma-separated)")
    help_areas = st.text_area("How Can You Help Other Members?")
    linkedin = st.text_input("LinkedIn Profile (optional)")

    submitted = st.form_submit_button("Submit / Update Profile")
    if submitted:
        if not name or not email or not phone:
            st.warning("Please fill in required fields: Name, Email, Phone.")
        else:
            save_user(name, email, phone, city, country, job_title, industry,
                      experience, expertise, help_areas, linkedin)
            st.success("✅ Your profile has been saved/updated.")

# --- View Own Profile with PDF & QR ---
st.markdown("---")
st.header("📄 View Your Profile")

email_key = st.text_input("Enter your email to view your profile")
phone_key = st.text_input("Enter your phone")

if st.button("View My Profile"):
    record = get_user_by_keys(email_key, phone_key)
    if record:
        st.markdown(f"### 👤 {record[1]}")
        st.markdown(f"- 📧 Email: {record[2]}")
        st.markdown(f"- 📞 Phone: {record[3]}")
        st.markdown(f"- 📍 City: {record[4]}, {record[5]}")
        st.markdown(f"- 💼 Title: {record[6]}, Industry: {record[7]}")
        st.markdown(f"- 📊 Experience: {record[8]} years")
        st.markdown(f"- 📚 Expertise: {record[9]}")
        st.markdown(f"- 🤝 Can Help: {record[10]}")
        if record[11]:
            st.markdown(f"- 🔗 LinkedIn: [{record[11]}]({record[11]})")

        # QR Code
        qr_img = generate_qr_code(record[2], record[3])
        st.image(qr_img, caption="Scan to Save Contact")

        # PDF Download
        pdf_bytes = generate_pdf(record)
        st.download_button("📄 Download Profile as PDF", pdf_bytes,
                           file_name=f"{record[1]}_profile.pdf",
                           mime="application/pdf")
    else:
        st.error("Profile not found. Please check email/phone.")

# --- Member Directory Search ---
st.markdown("---")
st.header("🔍 Pakistan Connect Directory")

search_query = st.text_input("Search by name, city, title, expertise, or help area")

if search_query:
    results = search_users(search_query)
    if results:
        for r in results:
            st.markdown(f"### 👤 {r[1]}")
            st.markdown(f"- 📍 **City:** {r[4]}, {r[5]}")
            st.markdown(f"- 💼 **Title:** {r[6]}, **Industry:** {r[7]}")
            st.markdown(f"- 📚 **Expertise:** {r[9]}")
            st.markdown(f"- 🤝 **Can Help With:** {r[10]}")
            profile_url = f"?email={r[2]}&phone={r[3]}"
            st.markdown(f"[🔗 View Profile]({profile_url})")
            st.markdown("---")
    else:
        st.info("No matches found.")

# --- Admin CSV Export ---
st.markdown("---")
st.subheader("🔒 Admin Panel")

admin_password = st.text_input("Enter admin password", type="password")

if admin_password == st.secrets["ADMIN_PASSWORD"]:
    st.success("✅ Access granted")

    if st.button("📥 Download All Data as CSV"):
        import pandas as pd

        users = get_all_users()
        df = pd.DataFrame(users, columns=[
            "ID", "Name", "Email", "Phone", "City", "Country",
            "Job Title", "Industry", "Experience", "Expertise",
            "Help Areas", "LinkedIn"
        ])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, file_name="pakistan_connect_members.csv", mime="text/csv")
else:
    if admin_password:
        st.error("❌ Incorrect password")
