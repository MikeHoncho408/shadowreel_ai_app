import streamlit as st
import requests
import os
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip

# === API Keys ===
PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
TTS_API_KEY = st.secrets["TTS_API_KEY"]
VOICE_ID = st.secrets["VOICE_ID"]

# === App UI ===
st.set_page_config(page_title="ShadowReel AI", layout="centered")
st.title("ShadowReel AI")
st.markdown("Create powerful, cinematic storytelling reels in one click.")

script_input = st.text_area("\U0001F4DC Paste your script here:", height=250)
theme = st.selectbox("\U0001F3A8 Choose a visual theme:", ["Dystopian", "Surveillance", "Whistleblower", "AI Horror"])
submit = st.button("\u26A1\uFE0F Generate My Shadow Reel")

# === Voiceover Generation ===
def generate_stanza_voiceovers(stanzas):
    os.makedirs("voice", exist_ok=True)
    for i, stanza in enumerate(stanzas):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            'xi-api-key': TTS_API_KEY,
            'Content-Type': 'application/json'
        }
        data = {
            'text': stanza,
            'voice_settings': {
                'stability': 0.5,
                'similarity_boost': 0.75
            }
        }
        response = requests.post(url, headers=headers, json=data)
        with open(f"voice/line_{i}.mp3", 'wb') as f:
            f.write(response.content)

# === Fetch Clips ===
def fetch_video_clips(keywords):
    headers = {'Authorization': PEXELS_API_KEY}
    os.makedirs("clips", exist_ok=True)
    for i, keyword in enumerate(keywords):
        r = requests.get(f"https://api.pexels.com/videos/search?query={keyword}&per_page=1", headers=headers)
        if r.status_code == 200:
            try:
                link = r.json()['videos'][0]['video_files'][0]['link']
                clip_data = requests.get(link)
                with open(f"clips/{keyword}_{i}.mp4", 'wb') as out:
                    out.write(clip_data.content)
            except:
                continue

# === Render Final Video ===
def render_shadowreel(stanzas):
    clips = []
    for i, stanza in enumerate(stanzas):
        try:
            video_path = f"clips/{theme.lower().split()[0]}_{i}.mp4"
            audio_path = f"voice/line_{i}.mp3"
            clip = VideoFileClip(video_path).subclip(0, 5).set_audio(AudioFileClip(audio_path))
            clips.append(clip)
        except Exception as e:
            continue
    if clips:
        final = concatenate_videoclips(clips)
        final.write_videofile("shadowreel_final.mp4", fps=24)

# === Run Sequence ===
if submit and script_input:
    st.info("\U0001F3A4 Generating voiceover clips...")
    stanzas = [s.strip() for s in script_input.strip().split("\n") if s.strip()]
    generate_stanza_voiceovers(stanzas)

    st.info("\U0001F39E\uFE0F Fetching video segments...")
    fetch_video_clips(theme.lower().split())

    st.info("\U0001F504 Rendering video...")
    render_shadowreel(stanzas)

    st.success("\u2705 Done! Your video is ready.")
    with open("shadowreel_final.mp4", "rb") as f:
        st.download_button("\u2B07\uFE0F Download ShadowReel", f, file_name="shadowreel_final.mp4")

    st.success("\u2705 Done! Your video is ready.")
    with open("shadowreel_final.mp4", "rb") as f:
        st.download_button("\u2b07\ufe0f Download ShadowReel", f, file_name="shadowreel_final.mp4")
