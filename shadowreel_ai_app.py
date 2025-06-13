import streamlit as st
import requests
import os
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip

PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
TTS_API_KEY = st.secrets["TTS_API_KEY"]
VOICE_ID = st.secrets["VOICE_ID"]

st.set_page_config(page_title="ShadowReel AI", layout="centered")
st.title("🎬 ShadowReel AI")
st.markdown("Create powerful, cinematic storytelling reels in one click.")

script_input = st.text_area("📜 Paste your script here:", height=250)
theme = st.selectbox("🎨 Choose a visual theme:", ["Dystopian", "Surveillance", "Whistleblower", "AI Horror"])
submit = st.button("⚡ Generate My Shadow Reel")

def generate_voiceover(script):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        'xi-api-key': TTS_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'text': script,
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    }
    response = requests.post(url, headers=headers, json=data)
    with open("voiceover.mp3", 'wb') as f:
        f.write(response.content)

def fetch_video_clips(keywords):
    headers = {'Authorization': PEXELS_API_KEY}
    os.makedirs("clips", exist_ok=True)
    for keyword in keywords:
        r = requests.get(f"https://api.pexels.com/videos/search?query={keyword}&per_page=1", headers=headers)
        if r.status_code == 200:
            try:
                link = r.json()['videos'][0]['video_files'][0]['link']
                clip_data = requests.get(link)
                with open(f"clips/{keyword}.mp4", 'wb') as out:
                    out.write(clip_data.content)
            except:
                continue

def render_video():
    clips = []
    for f in os.listdir("clips"):
        if f.endswith(".mp4"):
            clip = VideoFileClip(f"clips/{f}").subclip(0, 5)
            clips.append(clip)
    if not clips:
        st.error("No clips were found. Try another theme or keyword.")
        return
    final_clip = concatenate_videoclips(clips)
    audio = AudioFileClip("voiceover.mp3")
    final_video = final_clip.set_audio(audio)
    final_video.write_videofile("shadowreel_final.mp4", fps=24)

if submit and script_input:
    st.info("🎤 Generating voiceover...")
    generate_voiceover(script_input)
    st.info("🎥 Fetching cinematic footage clips...")
    fetch_video_clips(theme.lower().split())
    st.info("🧩 Assembling your video...")
    render_video()
    st.success("✅ Done! Download your reel below.")
    with open("shadowreel_final.mp4", "rb") as f:
        st.download_button("⬇️ Download Shadow Reel", f, file_name="shadowreel_final.mp4")
