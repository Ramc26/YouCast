
# 📻YouCast - YouTube Audio Downloader

YouCast is a super chill, user-friendly web app built with Streamlit that lets you grab audio from YouTube videos and playlists. It’s clean, powerful, and gives you real-time feedback — all without needing any annoying API keys.  

---

## ✨ How YouCast Came to Life

So here’s the story 😄:  

One day I was traveling and needed some podcasts from YouTube. Yes, I know, not exactly ethical and kinda illegal, but I had no other choice. I tried some online sites… ads everywhere, pop-ups everywhere, download speed slower than a snail, conversion taking ages… ugh!  

Then I sat at my desk, took **1 hour of my “professional time”** for personal mischief, ran `uv init`, and **Bhaaaam!** — in the next 68 minutes I had a working tool exactly how I wanted it. Fast, clean, and frustration-free.  

And that’s how **YouCast** was born. 🎧✨  

---
## 🖼️ App Preview

![YouCast Screenshot](https://raw.githubusercontent.com/ramc26/YouCast/main/assets/app_preview.png)

## ✨ Key Features

- **Multiple Formats:** Download audio in MP3, M4A, WEBM, or WAV.  
- **Quality Selection:** Pick your audio quality from 128, 192, 256, to 320 kbps.  
- **Batch Downloading:** Paste multiple YouTube URLs (one per line) to download them all in one go.  
- **Playlist Support:** Grab audio from an entire YouTube playlist in one click.  
- **Real-Time Progress:** Progress bars for each file and overall batch.  
- **In-App Previews:** Listen to the downloaded audio directly in the app.  
- **Error Handling:** Handles invalid URLs or download hiccups gracefully.  
- **Custom Download Location:** Save files exactly where you want.  
- **No API Keys Needed:** Works out-of-the-box using yt-dlp.  

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+**  
- **FFmpeg:** Required for audio conversion.

**Install FFmpeg:**  
- **Windows:** Download from the official [FFmpeg website](https://ffmpeg.org/) and add the bin folder to PATH.  
- **macOS (Homebrew):** `brew install ffmpeg`  
- **Linux (apt):** `sudo apt-get install ffmpeg`  

### 2. Install Packages Using `uv-astral`
This repo contains a `pyproject.toml` file, so you can use `uv` to install dependencies and sync everything effortlessly:

```
uv sync --active
```
No need for pip install manually — `uv` takes care of it. ✅

---

## 🚀 How to Run the App

1. Save the application code as `app.py`.
2. Open terminal/command prompt.
3. Navigate to the folder where you saved the file.
4. Run:

```bash
streamlit run app.py
```

Your browser will pop up with YouCast ready to go.

---

## 📝 How to Use

1. **Configure Settings:** Use the sidebar to choose audio format, quality, and download mode (single video or playlist).
2. **Set Download Location:** Pick a folder where your files will live.
3. **Enter URLs:** Paste one or more YouTube links.
4. **Start Download:** Hit “Start Download” and watch the progress bars.
5. **Preview & Save:** Once finished, see your downloaded files in a list. Play them in-app or click download to save to your computer.

---

## 🧑‍💻 Developer

* Designed & Developed by: **Ram Bikkina🦉**
* Portfolio: [RamTechSuite](https://ramtechsuite.com)

---

## ⚠️ License / Usage

No license here 😎.
This means: **don’t copy, don’t steal, don’t blame me if you misuse it**. Use it for fun, learn from it, or just geek out like me.

Basically: free to use for personal chaos, not free to copy the code. 🛑

---

Enjoy your music and podcasts the YouCast way! 🎶
---
