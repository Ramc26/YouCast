import yt_dlp
import os
import streamlit as st
from pathlib import Path
import humanize
import time

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
st.set_page_config(
    page_title="YouCast - YouTube Audio & Video Downloader", 
    page_icon="📻", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .download-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .file-item {
        # background-color: #f8f9fa;
        # border-radius: 10px;
        padding: 0.5rem;
        # margin-bottom: 1rem;
        # border-left: 4px solid #1f77b4;
    }
    .progress-bar {
        height: 8px;
        border-radius: 4px;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App UI ---
st.markdown('<h1 class="main-header">YouCast</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Download YouTube Audio or 4K Video ⚡</p>', unsafe_allow_html=True)

# --- Sidebar Settings ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    st.markdown("---")
    st.markdown("### 📥 Download Type")
    download_type = st.radio(
        "Download Type",
        ["Audio", "Video"],
        index=0,
        label_visibility="collapsed"
    )

    if download_type == "Audio":
        st.markdown("### 🎶 Audio Format")
        format_choice = st.selectbox(
            "Choose audio format",
            ["mp3", "m4a", "webm", "wav"],
            index=0,
            help="MP3 is recommended for wide compatibility.",
            label_visibility="collapsed"
        )

        st.markdown("### 🎚️ Audio Quality")
        quality = st.selectbox(
            "Audio Quality (kbps)",
            ["128", "192", "256", "320"],
            index=1,
            help="Higher quality results in larger file sizes.",
            label_visibility="collapsed"
        )
    else:
        format_choice = "mp4"
        st.markdown("### 🎚️ Video Quality")
        quality = st.selectbox(
            "Video Quality",
            ["144", "240", "360", "480", "720", "1080", "1440", "2160"],
            index=6,
            help="Higher quality = larger file size. 2160 = 4K",
            label_visibility="collapsed"
        )

    st.markdown("---")
    st.markdown("### 📺 Download Mode")
    download_mode = st.radio(
        "Download Mode",
        ["Single Video", "Whole Playlist"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📂 Download Location")
    folder_path = st.text_input(
        "Enter a folder path:",
        "downloads",
        help="The folder where your files will be saved. It will be created if it doesn't exist.",
        label_visibility="collapsed"
    )
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    st.markdown("---")
    st.markdown("### 🧑‍💻 About")
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
st.markdown("## 🔗 YouTube URLs")
urls_input = st.text_area(
    "Enter YouTube URLs (one per line)",
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/playlist?list=...",
    height=150,
    label_visibility="collapsed"
)

download_btn = st.button("🎬 Start Download", type="primary", use_container_width=True)

if download_btn and urls_input:
    st.session_state.downloaded_items.clear()
    urls = [url.strip() for url in urls_input.split("\n") if url.strip()]

    if not urls:
        st.warning("Please enter at least one YouTube URL.")
    else:
        with st.status("Downloading files...", expanded=True) as status:
            overall_progress_bar = st.progress(0.0, text="Overall Progress")
            
            for i, url in enumerate(urls):
                status.update(label=f"Processing URL {i+1}/{len(urls)}: {url[:50]}...")
                
                progress_bar = st.progress(0, text="Download Progress")
                time_placeholder = st.empty()
                
                processed_files_for_url = []
                start_time = time.time() 

                def progress_hook(d):
                    if d["status"] == "downloading":
                        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                        downloaded = d["downloaded_bytes"]

                        if total:
                            progress = downloaded / total
                            progress_bar.progress(progress, text=f"Downloading: {progress*100:.1f}%")

                            elapsed = time.time() - start_time
                            if downloaded > 0 and elapsed > 0:
                                speed = downloaded / elapsed
                                remaining = (total - downloaded) / speed if speed > 0 else 0
                                time_placeholder.text(
                                    f"⏱️ Elapsed: {elapsed:.1f}s | ⏳ ETA: {remaining:.1f}s | 📊 Speed: {humanize.naturalsize(speed)}/s"
                                )

                    elif d["status"] == "finished":
                        progress_bar.progress(1.0, text="Processing completed")

                def postprocessor_hook(d):
                    if d["status"] == "finished":
                        file_info = {
                            "path": d["info_dict"]["filepath"],
                            "title": d["info_dict"].get(
                                "title", os.path.basename(d["info_dict"]["filepath"])
                            ),
                        }
                        processed_files_for_url.append(file_info)

                # --- yt-dlp Options ---
                if download_type == "Audio":
                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
                        "progress_hooks": [progress_hook],
                        "postprocessor_hooks": [postprocessor_hook],
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": format_choice,
                                "preferredquality": quality,
                            }
                        ],
                        "noplaylist": download_mode == "Single Video",
                        "quiet": True,
                        "noprogress": True,
                    }
                else:  # Video
                    ydl_opts = {
                        "format": f"bestvideo[height<={quality}]+bestaudio/best",
                        "merge_output_format": "mp4",
                        "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
                        "progress_hooks": [progress_hook],
                        "postprocessor_hooks": [postprocessor_hook],
                        "noplaylist": download_mode == "Single Video",
                        "quiet": True,
                        "noprogress": True,
                    }

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                    for file_info in processed_files_for_url:
                        # Check if this file is already in the downloaded items
                        file_already_exists = any(
                            item["path"] == file_info["path"] for item in st.session_state.downloaded_items
                        )
                        
                        if not file_already_exists:
                            st.session_state.downloaded_items.append(
                                {
                                    "title": file_info["title"],
                                    "path": file_info["path"],
                                    "size": get_file_size(file_info["path"]),
                                    "format": format_choice,
                                    "type": download_type,
                                }
                            )
                    
                    st.success(f"✅ Successfully downloaded: {url[:50]}...")
                    
                except yt_dlp.utils.DownloadError as e:
                    st.error(f"❌ Failed to download from {url}.\nReason: {str(e).split(':')[-1].strip()}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred with URL {url}: {e}")
                finally:
                    progress_bar.empty()
                    time_placeholder.empty()
                    overall_progress_bar.progress((i + 1) / len(urls), text=f"Overall Progress: {((i + 1) / len(urls))*100:.1f}%")

            status.update(label="✅ All downloads complete!", state="complete")

# --- Display Downloaded Files ---
if st.session_state.downloaded_items:
    st.markdown("---")
    st.markdown("## 📂 Downloaded Files")
    
    # Debug info (you can remove this after testing)
    st.caption(f"Found {len(st.session_state.downloaded_items)} items in history")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.downloaded_items.clear()
            st.rerun()

    # Use a set to track displayed files and avoid duplicates
    displayed_files = set()
    
    for idx, item in enumerate(st.session_state.downloaded_items):
        # Skip if we've already displayed this file
        if item["path"] in displayed_files:
            continue
            
        displayed_files.add(item["path"])
        
        try:
            with open(item["path"], "rb") as f:
                file_bytes = f.read()

            if item["type"] == "Audio":
                st.audio(file_bytes, format=MIME_TYPES.get(item["format"]))
            else:
                st.video(item["path"])
            st.markdown(f"""
                            <div class="file-item">
                                <h4>{item['title']}</h4>
                                <p>Format: {item['format'].upper()} | Size: {item['size']} | Type: {item['type']}</p>
                            </div>
                        """,
                        unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Download File",
                data=file_bytes,
                file_name=os.path.basename(item["path"]),
                mime=MIME_TYPES.get(item["format"], "video/mp4"),
                key=f"download_btn_{idx}_{item['path']}",  # More unique key
                use_container_width=True
            )
            
        except FileNotFoundError:
            st.error(f"File not found: {item['path']}")
        except Exception as e:
            st.error(f"Could not load file {item['title']}: {e}")
            
        st.markdown("---")