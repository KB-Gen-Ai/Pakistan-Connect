import streamlit as st
import pandas as pd
import uuid
from database import save_profile, get_profile_by_id
from pdf_generator import generate_pdf
from qr_generator import generate_qr_code

# ✅ MUST be first Streamlit command!
st.set_page_config(page_title="Pakistan Connect", layout="centered")

# Background with dim overlay
flag_url = "https://raw.githubusercontent.com/YOUR_USERNAME/pakistan-connect/main/pakistan-flag.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{flag_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div {{
        background-color: #ffffffdd;
        color: black;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- Check if user opened a shared profile link ---
query_params = st.query_params
if "profile_id" in query_params:
    profile_id = query_params["profile_id"][0]
    profile_data = get_profile_by_id(profile_id)

    if profile_data:
        st.title("📄 Public Profile View")
        st.markdown("This is a read-only profile shared by a member.")

        st.write(f"**Name:** {profile_data['full_name']}")
        st.write(f"**Email:** {profile_data['email']}")
        st.write(f"**Phone:** {profile_data['phone']}")
        st.write(f"**Profession:** {profile_data['profession']}")
        st.write(f"**Expertise:** {profile_data['expertise']}")
        st.write(f"**How I Can Help:** {profile_data['how_to_help']}")

        if st.button("📄 Download Profile as PDF"):
            pdf_bytes = generate_pdf(profile_data)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{profile_data['full_name']}_profile.pdf",
                mime="application/pdf"
            )

        st.stop()
    else:
        st.error("❌ Profile not found.")
        st.stop()

# --- Main Profile Submission Form ---
st.title("🇵🇰 Pakistan Connect Member Registration")

with st.form("profile_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    profession = st.text_input("Profession / Job Title")
    expertise = st.text_area("Areas of Expertise")
    how_to_help = st.text_area("How Can You Help Other Members?")

    submitted = st.form_submit_button("Submit Profile")

if submitted:
    profile_id = str(uuid.uuid4())

    profile_data = {
        "id": profile_id,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "profession": profession,
        "expertise": expertise,
        "how_to_help": how_to_help,
    }

    save_profile(profile_data)

    # Generate profile link + QR
    profile_url = f"https://pakistan-connect.streamlit.app/?profile_id={profile_id}"
    qr_image = generate_qr_code(profile_url)

    st.success("🎉 Your profile has been saved!")

    st.markdown(f"🔗 **Share your profile:** [Click here]({profile_url})")
    st.image(qr_image, caption="Scan to View Your Profile", use_column_width=False)

    st.download_button(
        label="📄 Download Profile as PDF",
        data=generate_pdf(profile_data),
        file_name=f"{full_name}_profile.pdf",
        mime="application/pdf"
    )
