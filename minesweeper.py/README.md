# Minesweeper Assistant (screen capture)

This small project captures the Minesweeper board and will be used to analyze the board state.

Quick setup
1. Create a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell on Windows
# or on macOS / Linux:
# source .venv/bin/activate
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the capture

```powershell
cd "h:\Visual Studio Code\minesweeper.py"
python screen_capture.py
```

Notes
- `settings.py` holds `COMP_VIZ_TOP_LEFT` and `COMP_VIZ_BOT_RIGHT` (width/height) to crop the board. Update with your coordinates.
- If `opencv-python` fails to install on your machine, either install system tools (Xcode on macOS, Visual Studio Build Tools on Windows) or remove the preview code and use `Pillow` for saving/cropping images.
- To save frames for later analysis: add calls to `cv2.imwrite()` in `screen_capture.py` (or press a key to save a frame).

Backing up / Sharing
- Preferred: push this folder to a GitHub repository (see commands below).
- Quick: create a zip of the folder and upload it to Google Drive / OneDrive / Dropbox.

If you want, I can also create a small helper that auto-saves a sample set of frames for labeling.
