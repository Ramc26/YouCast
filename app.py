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
    "mp4": "video/mp4",
}

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="YouCast - YouTube Audio & Video Downloader",
    page_icon="📻",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
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
    .file-item {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App UI ---
st.markdown('<h1 class="main-header">YouCast</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Download YouTube Audio or 4K Video ⚡</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    download_type = st.radio("Download Type", ["Audio", "Video"], index=0)

    if download_type == "Audio":
        format_choice = st.selectbox("Audio Format", ["mp3", "m4a", "webm", "wav"], index=0)
        quality = st.selectbox("Audio Quality (kbps)", ["128", "192", "256", "320"], index=1)
    else:
        format_choice = "mp4"
        quality = st.selectbox("Video Quality", ["144", "240", "360", "480", "720", "1080", "1440", "2160"], index=6)

    download_mode = st.radio("Download Mode", ["Single Video", "Whole Playlist"], index=0)
    folder_path = st.text_input("Download Folder", "downloads")
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

# --- Progress Hooks ---
def progress_hook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        downloaded = d["downloaded_bytes"]
        if total > 0:
            progress = downloaded / total
            st.session_state.current_progress.progress(progress, text=f"Downloading: {progress*100:.1f}%")
    elif d["status"] == "finished":
        st.session_state.current_progress.progress(1.0, text="Processing completed")

def postprocessor_hook(d):
    if d["status"] == "finished":
        file_info = {
            "path": d["info_dict"]["filepath"],
            "title": d["info_dict"].get("title", os.path.basename(d["info_dict"]["filepath"])),
        }
        st.session_state.processed_files.append(file_info)

# --- Robust Fallback Downloader ---
def download_with_fallback(url, download_type, folder_path, format_choice="mp3", quality="192"):
    """
    Attempts to download media using several format fallbacks and includes
    options to bypass common HTTP 403 errors on hosted services.
    """
    safe_formats = []

    if download_type == "Audio":
        safe_formats = [
            ("bestaudio/best", format_choice),
            ("best", format_choice),
        ]
    else:  # Video
        safe_formats = [
            ("bv*+ba/b", "mp4"),
            ("bestvideo+bestaudio/best", "mp4"),
            ("best", "mp4"),
        ]

    last_error = None
    for fmt, container in safe_formats:
        ydl_opts = {
            "format": fmt,
            "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "postprocessor_hooks": [postprocessor_hook],
            "noplaylist": download_mode == "Single Video",
            "quiet": True,
            "noprogress": True,
            # --- Changes to bypass blocking ---
            # Use a common browser user-agent to avoid being identified as a bot.
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
            # Force requests to use IPv4, which can sometimes resolve connection issues.
            "force_ipv4": True,
            # For debugging, you can uncomment the next line to get detailed logs
            # 'verbose': True,
        }

        if download_type == "Audio":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": container,
                "preferredquality": quality,
            }]
        else:
            ydl_opts["merge_output_format"] = container

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True  # Success
        except Exception as e:
            last_error = e
            st.warning(f"Download attempt failed with format '{fmt}'. Trying next fallback... Error: {e}")
            continue

    # If all fallbacks fail, raise the last encountered error
    raise RuntimeError(f"All fallback attempts failed for {url}. Last error: {last_error}")

# --- Main UI ---
st.markdown("## 🔗 YouTube URLs")
urls_input = st.text_area("Enter one or more YouTube URLs (one per line)", placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/playlist?list=...", height=150)

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
                st.session_state.current_progress = st.progress(0, text="Initializing...")
                st.session_state.processed_files = []

                try:
                    download_with_fallback(url, download_type, folder_path, format_choice, quality)

                    for file_info in st.session_state.processed_files:
                        if not any(item["path"] == file_info["path"] for item in st.session_state.downloaded_items):
                            st.session_state.downloaded_items.append({
                                "title": file_info["title"],
                                "path": file_info["path"],
                                "size": get_file_size(file_info["path"]),
                                "format": format_choice,
                                "type": download_type,
                            })

                    st.success(f"✅ Successfully processed: {url[:50]}...")
                except Exception as e:
                    st.error(f"❌ Failed to download {url}. Reason: {e}")
                finally:
                    overall_progress_bar.progress((i + 1) / len(urls), text=f"Overall Progress: {((i+1)/len(urls))*100:.1f}%")

            status.update(label="✅ All downloads complete!", state="complete", expanded=False)

# --- Display Files ---
if st.session_state.downloaded_items:
    st.markdown("---")
    st.markdown("## 📂 Downloaded Files")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.downloaded_items.clear()
            st.rerun()

    displayed_files = set()
    for idx, item in enumerate(st.session_state.downloaded_items):
        if item["path"] in displayed_files:
            continue
        displayed_files.add(item["path"])

        try:
            with open(item["path"], "rb") as f:
                file_bytes = f.read()

            st.markdown(f"""
                <div class="file-item">
                    <h4>{item['title']}</h4>
                    <p>Format: {item['format'].upper()} | Size: {item['size']} | Type: {item['type']}</p>
                </div>
            """, unsafe_allow_html=True)

            if item["type"] == "Audio":
                st.audio(file_bytes, format=MIME_TYPES.get(item["format"]))
            else:
                st.video(file_bytes, format=MIME_TYPES.get(item["format"]))

            st.download_button(
                label="⬇️ Download File",
                data=file_bytes,
                file_name=os.path.basename(item["path"]),
                mime=MIME_TYPES.get(item["format"], "application/octet-stream"),
                key=f"download_btn_{idx}_{item['path']}",
                use_container_width=True
            )
            st.markdown("---")
        except FileNotFoundError:
            st.error(f"Could not find file: {item['title']}. It may have been moved or deleted.")
        except Exception as e:
            st.error(f"Could not load {item['title']}: {e}")