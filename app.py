import yt_dlp
import os
import streamlit as st
from pathlib import Path
import humanize

# --- Helper Functions ---

def get_file_size(file_path):
    """Returns the file size in a human-readable format."""
    return humanize.naturalsize(os.path.getsize(file_path))

MIME_TYPES = {
    "mp3": "audio/mpeg",
    "m4a": "audio/mp4",
    "wav": "audio/wav",
    "webm": "audio/webm",
}

# --- Streamlit Page Config ---
st.set_page_config(page_title="YouCast", page_icon="📻", layout="centered")

# --- Main App UI ---
st.title("You📻Cast")
st.caption("Download YouTube audio with style ⚡")

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")

    format_choice = st.selectbox(
        "🎶 Choose audio format",
        ["mp3", "m4a", "webm", "wav"],
        index=0,
        help="MP3 is recommended for wide compatibility."
    )

    quality = st.selectbox(
        "🎚️ Audio Quality (kbps)",
        ["128", "192", "256", "320"],
        index=1,
        help="Higher quality results in larger file sizes."
    )

    download_mode = st.radio(
        "📺 Download Mode",
        ["Single Video", "Whole Playlist"],
        index=0,
        horizontal=True
    )

    st.markdown("---")
    st.markdown("📂 **Download Location**")
    folder_path = st.text_input("Enter a folder path:", "downloads", help="The folder where your audio files will be saved. It will be created if it doesn't exist.")
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    # --- NEW: Developer Credits Section ---
    st.markdown("---")
    st.header("🧑‍💻 About the Developer")
    st.markdown(
        """
        <div style="text-align: center;">
            <h2 style="margin-bottom: 0; font-size: 3rem;">🦉</h2>
            <p>Designed & Developed by<br><strong>Ram Bikkina</strong></p>
            <a href="https://ramc26.github.io/RamTechSuite" target="_blank">RamTechSuite Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- State Initialization ---
if "downloaded_items" not in st.session_state:
    st.session_state.downloaded_items = []

# --- Main Download UI ---
urls_input = st.text_area(
    "🔗 **Enter YouTube URLs** (one per line)",
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/playlist?list=...",
    height=150
)
download_btn = st.button("🎧 Start Download", type="primary")

if download_btn and urls_input:
    # Clear previous run's results
    st.session_state.downloaded_items.clear()
    
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    if not urls:
        st.warning("Please enter at least one YouTube URL.")
    else:
        # Placeholders for overall progress
        overall_progress_text = st.empty()
        overall_progress_bar = st.progress(0.0)

        for i, url in enumerate(urls):
            overall_progress_text.info(f"🔄 Processing URL {i+1}/{len(urls)}: {url}")
            
            # Placeholders for individual file progress
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            # This list will be populated by the postprocessor hook
            processed_files_for_url = []

            def progress_hook(d):
                if d["status"] == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                    if total:
                        progress = d["downloaded_bytes"] / total
                        progress_bar.progress(progress)
                        # Display title if available
                        title = d.get('info_dict', {}).get('title', '...')
                        status_placeholder.text(f"📥 Downloading: {title[:50]}... ({progress*100:.1f}%)")
                elif d["status"] == "finished":
                    status_placeholder.text("⚙️ Download finished. Converting audio...")

            def postprocessor_hook(d):
                # This hook runs after a file is converted
                if d['status'] == 'finished' and d['postprocessor'] == 'FFmpegExtractAudio':
                    file_info = {
                        'path': d['info_dict']['filepath'],
                        'title': d['info_dict'].get('title', os.path.basename(d['info_dict']['filepath']))
                    }
                    processed_files_for_url.append(file_info)

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
                "progress_hooks": [progress_hook],
                "postprocessor_hooks": [postprocessor_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format_choice,
                    "preferredquality": quality,
                }],
                "noplaylist": download_mode == "Single Video",
                "quiet": True,
                "noprogress": True, # Disable yt-dlp's console progress
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Append successfully processed files to the session state
                for file_info in processed_files_for_url:
                    st.session_state.downloaded_items.append({
                        "title": file_info["title"],
                        "path": file_info["path"],
                        "size": get_file_size(file_info["path"]),
                        "format": format_choice,
                    })

            except yt_dlp.utils.DownloadError as e:
                st.error(f"❌ Failed to download from {url}.\nReason: {str(e).split(':')[-1].strip()}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred with URL {url}: {e}")
            finally:
                # Clean up placeholders for the next URL
                status_placeholder.empty()
                progress_bar.empty()
                overall_progress_bar.progress((i + 1) / len(urls))

        overall_progress_text.success("✅ All downloads complete!")

# --- Display Downloaded Files ---
if st.session_state.downloaded_items:
    st.markdown("---")
    st.subheader("📂 Downloaded Files")
    
    if st.button("🗑️ Clear History"):
        st.session_state.downloaded_items.clear()
        st.rerun()

    for item in st.session_state.downloaded_items:
        with st.expander(f"✅ **{item['title']}**"):
            st.markdown(f"**File Size:** `{item['size']}`")
            
            try:
                with open(item['path'], 'rb') as audio_file:
                    audio_bytes = audio_file.read()

                # --- Audio Player ---
                st.audio(audio_bytes, format=MIME_TYPES.get(item['format']))

                # --- Download Button ---
                st.download_button(
                    label="⬇️ Download File",
                    data=audio_bytes,
                    file_name=os.path.basename(item['path']),
                    mime=MIME_TYPES.get(item['format'])
                )
            except FileNotFoundError:
                st.error(f"File not found: {item['path']}. It may have been moved or deleted.")
            except Exception as e:
                st.error(f"Could not load audio player for {item['title']}: {e}")