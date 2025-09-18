# YouCast📻
**Download YouTube audio or 4K video in style—right from your browser.**

_Blast your favorite tracks. Binge your playlists. All offline, all easy, and all super smooth._

***
## 🖼️ App Preview
![YouCast Screenshot](https://raw.githubusercontent.com/ramc26/YouCast/main/assets/app_previewV2.png)

## 🚀 What’s This?
YouCast is a user-friendly web app for downloading YouTube audio (MP3, M4A, WAV—you name it!) and high-quality videos with just a couple of clicks. Full playlist support, shiny UI, live progress bars, and easy peasy downloads straight to your desktop.


## 🌈 Features
- Download audio (MP3, M4A, WAV, WEBM) or video (up to 4K!) from YouTube.
- Single video or whole playlists? Both, of course!
- Choose your format and quality—takes all the guesswork out of saving files.
- Handy progress bars and download history, so you’re never lost.
- Beautiful, modern, and responsive design powered by Streamlit.
- No duplicate files—history stays clean.
- All downloads auto-organize to your chosen folder.
- Works right out of the browser—zero command-line headaches.


## ⚡️ Quickstart: Get Rolling
**You’ll need:**  
- Python 3.8+  
- `uv` package manager  
- `ffmpeg` installed (for audio/video conversion)

### 1. Clone the App
```bash
git clone https://github.com/ramc26/youcast.git
cd youcast
```

### 2. Install the Goods (with uv!)
```bash
uv pip install -r pyproject.toml
```
If you usually use `poetry` or another tool for `pyproject.toml`, run:
```bash
uv venv
uv pip install -r pyproject.toml
```
This pulls in Streamlit, yt-dlp, humanize, and anything else this app needs—all straight from the `pyproject.toml`. No `requirements.txt` drama!

**Make sure** ffmpeg is in your system PATH for audio conversion.

### 3. Run the Magic
```bash
streamlit run app.py
```
(Not using `app.py`? Replace with your file name.)

The app should pop open in your browser.  
Dance break! 💃🕺



## 🎮 How to Use
1. Paste your YouTube links (one per line—video or playlist, mix as much as you want).
2. Pick what you want: Audio or Video, formats, and quality in the sidebar.
3. Decide: Single video or grab the whole playlist.
4. Set the download folder (default: `downloads`).
5. Smash that “Start Download” button and let the app do the heavy lifting!
6. Download your files from the history below. Play them right there—or snag them to your machine.

Need to clear the download list? Hit the trash can!



## 🐞 Troubleshooting
- **Missing ffmpeg?** Make sure it’s installed and in your PATH.
- **Weird error on download?** Chill for a sec and try again—yt-dlp and YouTube like to change things up.
- **Download button not showing?** Chrome loves you—just refresh.



## 🦉 Author & Credits
Made with ☕ + 🎧 by **Ram Bikkina 🦉**  
If you love this, check out [RamTechSuite Portfolio](https://ramc26.github.io/RamTechSuite).

***

**Now go grab those tunes and videos!**  
PS: This is for personal use—respect copyright and all that jazz.

