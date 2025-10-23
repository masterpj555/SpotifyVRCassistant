#!/usr/bin/env python3
"""
spotify_to_youtube_gui.py — Dark UI

Paste a Spotify *track* URL → uses Spotify Web API (your Client ID/Secret)
to get Title + Artist(s), then searches YouTube and gives a share URL.

Features
- Settings → Spotify API Credentials… (saved locally)
- Settings → Auto Clipboard Mode (watches clipboard for Spotify track URLs; auto-fetch + auto-copy)
- Auto-fetch on paste/typing (debounced) and on Enter
- About menu with creator info and clickable links (dialog centered; aligned rows)
- Compact dark UI + dark title bars on Windows (DWM)

Requirements:
    pip install requests
"""

import json
import os
import sys
import base64
import re
import threading
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
import webbrowser
import subprocess
from typing import Optional

# Embedded app icon (PNG, base64)
ICON_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFyGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDggNzkuMTY0MDM2LCAyMDE5LzA4LzEzLTAxOjA2OjU3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI1LTEwLTIzVDE0OjA2OjUzKzAyOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDI1LTEwLTIzVDE0OjA2OjUzKzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNS0xMC0yM1QxNDowNjo1MyswMjowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5MmNmYzg4My03NDM0LTk4NDMtOWMxYi0wOGVmNDA1ZTFkNGQiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDozNDViNzUzNy05YTY5LWMxNDYtOGUxMC05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"


import requests

APP_NAME = "SpotifyToYouTube"
CONFIG_NAME = "settings.json"


# --------------------------- Config paths & storage ---------------------------
def _platform_config_dir() -> str:
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser(r"~\\AppData\\Roaming")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.config")
    return os.path.join(base, APP_NAME)


def _config_file_path() -> str:
    return os.path.join(_platform_config_dir(), CONFIG_NAME)


def load_settings() -> dict:
    path = _config_file_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return {
            "client_id": data.get("client_id", ""),
            "client_secret": data.get("client_secret", ""),
            "auto_clipboard": bool(data.get("auto_clipboard", False)),
        }
    except Exception:
        return {}


def save_settings(client_id: str, client_secret: str, auto_clipboard: bool=False) -> None:
    cfg_dir = _platform_config_dir()
    os.makedirs(cfg_dir, exist_ok=True)
    path = _config_file_path()
    data = {
        "client_id": client_id or "",
        "client_secret": client_secret or "",
        "auto_clipboard": bool(auto_clipboard),
    }
    # Try to restrict permissions where possible (best-effort)
    try:
        if not sys.platform.startswith("win"):
            # 0o600 -> rw-------
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            fd = os.open(path, flags, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return
    except Exception:
        pass
    # Fallback simple write
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def open_config_folder():
    path = _platform_config_dir()
    os.makedirs(path, exist_ok=True)
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        messagebox.showinfo("Config folder", f"Config folder is here:\n{path}")


# --------------------------- Spotify + YouTube logic --------------------------
def get_spotify_token(client_id: str, client_secret: str) -> str:
    if not (client_id and client_secret):
        raise RuntimeError("Spotify API credentials are missing. Use Settings → Spotify API Credentials…")
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}
    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data, timeout=15)
    r.raise_for_status()
    return r.json()["access_token"]


def extract_track_id(spotify_url: str) -> Optional[str]:
    m = re.search(r"/track/([A-Za-z0-9]+)", spotify_url)
    return m.group(1) if m else None


def fetch_title_artist_from_spotify(spotify_url: str, client_id: str, client_secret: str) -> tuple[str, str]:
    track_id = extract_track_id(spotify_url)
    if not track_id:
        raise ValueError("Please paste a valid Spotify *track* URL.")
    token = get_spotify_token(client_id, client_secret)
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
    title = (data.get("name") or "").strip()
    artists = [a.get("name") for a in data.get("artists", []) if isinstance(a, dict) and a.get("name")]
    artist = " & ".join(artists)
    if not title:
        raise RuntimeError("Spotify API did not return a track title.")
    return title, artist


def _extract_json_block(html: str, marker: str):
    import json as _json
    start = html.find(marker)
    if start == -1:
        return None
    i = html.find("{", start)
    if i == -1:
        return None
    depth, end = 0, None
    for j in range(i, len(html)):
        if html[j] == "{":
            depth += 1
        elif html[j] == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    if end is None:
        return None
    s = html[i:end]
    try:
        return _json.loads(s)
    except Exception:
        s = s.replace("&quot;", '"').replace("&amp;", "&")
        try:
            return _json.loads(s)
        except Exception:
            return None


def _walk_dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk_dicts(v)
    elif isinstance(obj, list):
        for it in obj:
            yield from _walk_dicts(it)


def search_youtube_first_video_id(query: str):
    base = "https://www.youtube.com/results"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
               "Accept-Language":"en-US,en;q=0.9"}
    resp = requests.get(base, params={"search_query": query}, headers=headers, timeout=20)
    resp.raise_for_status()
    html = resp.text
    for marker in ['var ytInitialData = ', 'window["ytInitialData"] = ', 'window.ytInitialData = ', 'ytInitialData = ']:
        data = _extract_json_block(html, marker)
        if data:
            break
    else:
        data = None
    if not data:
        return None
    for d in _walk_dicts(data):
        if "videoRenderer" in d:
            vid = d["videoRenderer"].get("videoId")
            if vid:
                return vid
    return None


def build_query(title: str, artist: str) -> str:
    return f"{title} {artist}".strip() if (title and artist) else (title or artist)


def is_probably_spotify_track_url(s: str) -> bool:
    return bool(re.search(r"^https?://open\.spotify\.com/track/[A-Za-z0-9]+", s))


# --------------------------- Dark theme + title bar ---------------------------
def apply_dark_theme(root: tk.Tk) -> ttk.Style:
    BG = "#1e1f22"
    FG = "#e6e6e6"
    SUB = "#b9b9b9"
    ACCENT = "#52a8ff"
    FIELD = "#2b2d31"
    BTN = "#3b3d42"
    BTN_ACTIVE = "#4a4d53"
    BTN_DISABLED = "#2a2c31"

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=BG)

    style.configure(".", background=BG, foreground=FG, fieldbackground=FIELD)
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG)
    style.configure("Sub.TLabel", foreground=SUB)
    style.configure("Link.TLabel", foreground=ACCENT)

    style.configure("Dark.TEntry", fieldbackground=FIELD, foreground=FG, insertcolor=FG)
    style.map("Dark.TEntry", fieldbackground=[("disabled", FIELD)], foreground=[("disabled", SUB)])

    style.configure("Dark.TButton", background=BTN, foreground=FG, padding=(14, 10))
    style.map("Dark.TButton", background=[("active", BTN_ACTIVE), ("disabled", BTN_DISABLED)])

    return style


def enable_dark_titlebar(win: tk.Tk | tk.Toplevel):
    """Best-effort dark title bar on Windows 10/11 using DWM."""
    if not sys.platform.startswith("win"):
        return
    try:
        import ctypes
        from ctypes import wintypes
        hwnd = wintypes.HWND(win.winfo_id())
        # Two possible indices used across Windows builds
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
        value = ctypes.c_int(1)
        dwm = ctypes.windll.dwmapi
        # Try both attributes
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                  ctypes.byref(value), ctypes.sizeof(value))
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                                  ctypes.byref(value), ctypes.sizeof(value))
    except Exception:
        pass


# ------------------------------------ UI -------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify → YouTube Linker (Spotify API)")
        # Compact window sized to content
        self.resizable(False, False)
        self._debounce_id = None
        self._last_fetched_url = ""
        self._clipboard_job = None
        self._last_clip_text = None
        self._last_auto_url = None
        # Dark theme
        self.style = apply_dark_theme(self)
        try:
            self._icon_img = tk.PhotoImage(data=ICON_PNG_B64)
            self.iconphoto(True, self._icon_img)
        except Exception:
            pass
        # Credentials and settings
        st = load_settings()
        self.client_id = st.get("client_id", "")
        self.client_secret = st.get("client_secret", "")
        self.auto_clipboard_default = bool(st.get("auto_clipboard", False))
        # Build UI
        self._build()
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        enable_dark_titlebar(self)
        if self.auto_clipboard_default:
            self.after(0, self._start_clipboard_watch)

    def _build(self):
        menubar = tk.Menu(self, tearoff=0, bg=self.cget("bg"), fg="#e6e6e6", activebackground="#4a4d53", activeforeground="#e6e6e6")
        self.config(menu=menubar)
        # Settings menu
        m_settings = tk.Menu(menubar, tearoff=0, bg=self.cget("bg"), fg="#e6e6e6", activebackground="#4a4d53", activeforeground="#e6e6e6")
        m_settings.add_command(label="Spotify API Credentials…", command=self.edit_credentials)
        m_settings.add_command(label="Open Config Folder", command=open_config_folder)
        self.auto_clipboard_var = tk.BooleanVar(value=self.auto_clipboard_default)
        m_settings.add_checkbutton(label="Auto Clipboard Mode", onvalue=True, offvalue=False,
                                   variable=self.auto_clipboard_var, command=self.on_toggle_auto_clipboard)
        m_settings.add_separator()
        m_settings.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="Settings", menu=m_settings)
        # About menu
        m_about = tk.Menu(menubar, tearoff=0, bg=self.cget("bg"), fg="#e6e6e6", activebackground="#4a4d53", activeforeground="#e6e6e6")
        m_about.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="About", menu=m_about)

        pad = 10
        # Top: URL input (shorter width)
        top = ttk.Frame(self, padding=(pad, pad, pad, 0)); top.pack(anchor="w")
        ttk.Label(top, text="Spotify track URL:").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.url_var, width=56, style="Dark.TEntry")
        ent.grid(row=1, column=0, sticky="w", pady=(4,0))
        ent.bind("<Return>", lambda e: self.fetch_now())
        ent.bind("<<Paste>>", lambda e: self.schedule_fetch())
        self.url_var.trace_add("write", lambda *args: self.schedule_fetch())

        # Buttons row (bigger buttons)
        btns = ttk.Frame(self, padding=(pad, 8)); btns.pack(anchor="w")
        self.btn_open = ttk.Button(btns, text="Open", style="Dark.TButton", command=self.on_open, state="disabled", width=12)
        self.btn_open.pack(side="left")
        self.btn_copy = ttk.Button(btns, text="Copy", style="Dark.TButton", command=self.on_copy, state="disabled", width=12)
        self.btn_copy.pack(side="left", padx=(8,0))

        # Status
        status = ttk.Frame(self, padding=(pad, 4, pad, pad)); status.pack(anchor="w")
        self.lbl_track = ttk.Label(status, text="Track: —"); self.lbl_track.grid(row=0, column=0, sticky="w")
        self.lbl_query = ttk.Label(status, text="YouTube query: —"); self.lbl_query.grid(row=1, column=0, sticky="w", pady=(2,0))
        self.result_var = tk.StringVar(value="YouTube link: —")
        self.lbl_result = ttk.Label(status, textvariable=self.result_var, style="Link.TLabel", cursor="hand2")
        self.lbl_result.grid(row=2, column=0, sticky="w", pady=(2,0))
        self.lbl_result.bind("<Button-1>", lambda e: self.on_open())
        self.progress = ttk.Label(status, text="", style="Sub.TLabel")
        self.progress.grid(row=3, column=0, sticky="w", pady=(4,0))

    # ---- Helpers ----
    def _center_window(self, win: tk.Toplevel):
        self.update_idletasks()
        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        w, h = win.winfo_reqwidth(), win.winfo_reqheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        win.geometry(f"+{x}+{y}")

    def _link_label(self, parent, text, url):
        # Label that underlines on hover without changing size
        lbl = ttk.Label(parent, text=text, style="Link.TLabel", cursor="hand2")
        try:
            base_font = tkfont.nametofont(lbl.cget("font"))
            norm = base_font.copy()
            under = base_font.copy()
            under.configure(underline=1)
            lbl.configure(font=norm)
            lbl.bind("<Enter>", lambda _e: lbl.configure(font=under))
            lbl.bind("<Leave>", lambda _e: lbl.configure(font=norm))
        except Exception:
            pass
        lbl.bind("<Button-1>", lambda e: webbrowser.open(url))
        return lbl

    # ---- Settings ----
    def edit_credentials(self):
        dlg = tk.Toplevel(self)
        dlg.title("Spotify API Credentials")
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.configure(bg=self.cget("bg"))
        enable_dark_titlebar(dlg)
        dlg.grab_set()

        pad = 10
        frm = ttk.Frame(dlg, padding=pad); frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Client ID:").grid(row=0, column=0, sticky="w", padx=(0,8), pady=(0,6))
        id_var = tk.StringVar(value=self.client_id)
        ttk.Entry(frm, textvariable=id_var, width=56, style="Dark.TEntry").grid(row=0, column=1, sticky="ew", pady=(0,6))

        ttk.Label(frm, text="Client Secret:").grid(row=1, column=0, sticky="w", padx=(0,8))
        sec_var = tk.StringVar(value=self.client_secret)
        ttk.Entry(frm, textvariable=sec_var, width=56, show="•", style="Dark.TEntry").grid(row=1, column=1, sticky="ew")

        frm.columnconfigure(1, weight=1)

        info = ttk.Label(frm, text="Saved locally in your user config folder.", style="Sub.TLabel")
        info.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8,0))

        btns = ttk.Frame(frm); btns.grid(row=3, column=0, columnspan=2, sticky="e", pady=(10,0))
        def on_save():
            self.client_id = id_var.get().strip()
            self.client_secret = sec_var.get().strip()
            save_settings(self.client_id, self.client_secret, auto_clipboard=self.auto_clipboard_var.get())
            self.progress.config(text="Credentials saved.")
            dlg.destroy()
            if is_probably_spotify_track_url((self.url_var.get() or "").strip()):
                self.fetch_now()
        ttk.Button(btns, text="Save", style="Dark.TButton", command=on_save).pack(side="right")
        ttk.Button(btns, text="Cancel", style="Dark.TButton", command=dlg.destroy).pack(side="right", padx=(0,8))

        self._center_window(dlg)
        dlg.wait_window()

    def show_about(self):
        dlg = tk.Toplevel(self)
        dlg.title("About")
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.configure(bg=self.cget("bg"))
        enable_dark_titlebar(dlg)

        pad = 12
        frm = ttk.Frame(dlg, padding=pad); frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Created by Pieterjan Ruysch", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        # Aligned rows (two columns)
        ttk.Label(frm, text="Twitter:").grid(row=1, column=0, sticky="w", pady=(8,0), padx=(0,8))
        self._link_label(frm, "https://x.com/masterpj55", "https://x.com/masterpj55").grid(row=1, column=1, sticky="w", pady=(8,0))

        ttk.Label(frm, text="Bluesky:").grid(row=2, column=0, sticky="w", padx=(0,8))
        self._link_label(frm, "https://bsky.app/profile/laserstroopwaffle.bsky.social",
                         "https://bsky.app/profile/laserstroopwaffle.bsky.social").grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="VRChat:").grid(row=3, column=0, sticky="w", padx=(0,8), pady=(0,6))
        self._link_label(frm, "Laser",
                         "https://vrchat.com/home/user/usr_eedfede4-efb3-43b4-9f43-93f83a9549d7").grid(row=3, column=1, sticky="w", pady=(0,6))

        ttk.Button(frm, text="Close", style="Dark.TButton", command=dlg.destroy).grid(row=4, column=0, columnspan=2, sticky="e", pady=(8,0))

        self._center_window(dlg)

    def on_toggle_auto_clipboard(self):
        save_settings(self.client_id, self.client_secret, auto_clipboard=self.auto_clipboard_var.get())
        if self.auto_clipboard_var.get():
            self._start_clipboard_watch()
        else:
            self._stop_clipboard_watch()

    def _start_clipboard_watch(self):
        if self._clipboard_job is None:
            self._last_clip_text = None
            self._last_auto_url = None
            self._clipboard_job = self.after(800, self._poll_clipboard)

    def _stop_clipboard_watch(self):
        job = self._clipboard_job
        if job is not None:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._clipboard_job = None

    def _poll_clipboard(self):
        try:
            text = self.clipboard_get()
        except Exception:
            text = ""
        if text != self._last_clip_text:
            self._last_clip_text = text
            m = re.search(r"https?://open\.spotify\.com/track/[A-Za-z0-9]+", text)
            if m:
                url = m.group(0)
                if url != self._last_auto_url:
                    self._last_auto_url = url
                    self.url_var.set(url)
                    self._detected_via_clipboard = True
                    self.fetch_now()
        if self.auto_clipboard_var.get():
            self._clipboard_job = self.after(800, self._poll_clipboard)
        else:
            self._stop_clipboard_watch()

    # ---- Fetch flow ----
    def set_busy(self, busy: bool):
        self.btn_open.config(state="disabled" if busy else ("normal" if getattr(self, "_last", None) else "disabled"))
        self.btn_copy.config(state="disabled" if busy else ("normal" if getattr(self, "_last", None) else "disabled"))
        self.progress.config(text="Working…" if busy else "")

    def schedule_fetch(self):
        if self._debounce_id:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(600, self.fetch_now)

    def fetch_now(self):
        url = (self.url_var.get() or "").strip()
        if not is_probably_spotify_track_url(url):
            return
        if url == self._last_fetched_url:
            return
        self._last_fetched_url = url
        self.set_busy(True)
        self.btn_open.config(state="disabled")
        self.btn_copy.config(state="disabled")
        self.result_var.set("YouTube link: —")
        self.lbl_track.config(text="Track: —")
        self.lbl_query.config(text="YouTube query: —")
        threading.Thread(target=self._work, args=(url,), daemon=True).start()

    def _work(self, url: str):
        try:
            if not (self.client_id and self.client_secret):
                raise RuntimeError("Spotify API credentials are missing. Use Settings → Spotify API Credentials…")
            title, artist = fetch_title_artist_from_spotify(url, self.client_id, self.client_secret)
            query_for_yt = build_query(title, artist)
            vid = search_youtube_first_video_id(query_for_yt)
            if not vid:
                raise RuntimeError("No YouTube results found for that track.")
            share_url = f"https://youtu.be/{vid}"
            self.after(0, self._ok, title, artist, query_for_yt, share_url)
        except Exception as e:
            self.after(0, self._err, str(e))

    def _ok(self, title: str, artist: str, yt_query: str, share_url: str):
        self.lbl_track.config(text=f"Track: {title} — {artist}" if (title and artist) else f"Track: {title or artist or '—'}")
        self.lbl_query.config(text=f"YouTube query: {yt_query}")
        self.result_var.set(f"YouTube link: {share_url}")
        self._last = share_url
        self.btn_open.config(state="normal")
        self.btn_copy.config(state="normal")
        if getattr(self, "_detected_via_clipboard", False) and self.auto_clipboard_var.get():
            try:
                self.clipboard_clear()
                self.clipboard_append(share_url)
                self.progress.config(text="Auto: YouTube link copied to clipboard.")
            except Exception:
                pass
            self._detected_via_clipboard = False
        self.set_busy(False)

    def _err(self, msg: str):
        self.set_busy(False)
        messagebox.showerror("Error", msg + "\n\nTip: enter your Client ID/Secret via Settings → Spotify API Credentials…")

    def on_open(self):
        url = getattr(self, "_last", None)
        if url:
            webbrowser.open(url)

    def on_copy(self):
        url = getattr(self, "_last", None)
        if url:
            self.clipboard_clear()
            self.clipboard_append(url)
            self.progress.config(text="Copied to clipboard.")

def main():
    App().mainloop()

if __name__ == "__main__":
    main()
