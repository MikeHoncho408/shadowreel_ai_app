import streamlit as st
from shadowreel_ai_core import generate_voiceover, fetch_video_clips, create_shadow_reel

st.set_page_config(layout="wide", page_title="ShadowForge AI")
st.title("🎬 ShadowForge AI — Cinematic Video Generator")

st.markdown("Create cinematic video reels from a single script input, matched with B-roll, music, and captions.")

# === SCRIPT INPUT ===
script_text = st.text_area("✍️ Enter your video script below:", height=200)

# === VIDEO KEYWORD ===
keyword = st.text_input("🔍 B-Roll Search Keyword:", value="surveillance")

# === BUTTONS ===
if st.button("🚀 Generate Video"):
    if script_text.strip() == "":
        st.warning("Please enter a script before generating.")
    else:
        generate_voiceover(script_text)
        fetch_video_clips(keyword)
        create_shadow_reel()
        st.success("✅ Video generated successfully!")

        st.video("shadow_reel.mp4")
