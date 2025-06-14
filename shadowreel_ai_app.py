import streamlit as st
import os
from shadowreel_ai_core import generate_voiceover, fetch_video_clips, create_shadow_reel, upload_custom_audio

st.set_page_config(layout="centered", page_title="ShadowForge AI", page_icon="🎬")

st.title("🎬 ShadowForge AI")
st.markdown(
    """
    Welcome to **ShadowForge AI**, your cinematic storytelling machine.  
    Drop your script. Pick your vibe. Get your revolution on tape.
    """
)

# === SCRIPT INPUT ===
st.subheader("✍️  Enter Your Script")
script_text = st.text_area("This script will be narrated or paired with your uploaded audio.", height=200)

# === KEYWORD INPUT ===
st.subheader("🔍  Choose Video Theme")
keyword = st.text_input("What visual theme should we search for?", value="surveillance")

# === AUDIO UPLOAD ===
st.subheader("🎤  Upload Optional Voiceover")
uploaded_audio = st.file_uploader("Upload a .mp3 voiceover (or leave blank to auto-generate)", type=["mp3"])

# === GENERATE BUTTON ===
if st.button("🚀 Generate Cinematic Reel"):
    if not script_text.strip():
        st.warning("Please enter a script first.")
    else:
        st.info("⚙️ Generating... This may take up to 1 minute depending on content length.")

        if uploaded_audio:
            with open("voiceover.mp3", "wb") as f:
                f.write(uploaded_audio.read())
            upload_custom_audio("voiceover.mp3")
        else:
            generate_voiceover(script_text)

        fetch_video_clips(keyword)
        create_shadow_reel()

        st.success("✅ Your video is ready!")
        st.video("shadow_reel.mp4")
        st.markdown("[Download Video](shadow_reel.mp4)", unsafe_allow_html=True)
