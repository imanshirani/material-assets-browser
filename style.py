# ==========================
# --- UI COLOR VARIABLES ---
# ==========================
C_ACCENT       = "#00B2FF"
C_BTN_BLUE     = "#005a9e"
C_BG_WINDOW    = "#2B2B2B"
C_BG_PANEL     = "#1E1E1E"
C_BG_HEADER    = "#252525"
C_BORDER       = "#383838"
C_BORDER_DARK  = "#333333"
C_TEXT_MAIN    = "#E0E0E0"
C_TEXT_DIM     = "#888888"
C_WHITE        = "#FFFFFF"

# --- Button Colors ---
C_BTN_BG       = "#3a3a3a"
C_BTN_HOVER    = "#4a4a4a"
C_BTN_BORDER   = "#555555"
C_BTN_TEXT     = "#dddddd"

# --- Folder Item Colors ---
C_FOLDER_BG    = "#333333"
C_FOLDER_BORDER= "#444444"

# --- Brand Colors ---
C_DONATE_BG    = "#ffc439"
C_DONATE_TEXT  = "#003087"
C_GITHUB_BG    = "#24292e"

# ==========================
# --- MAIN STYLESHEET ---
# ==========================
MAIN_STYLE = f"""
QWidget {{
    background-color: {C_BG_WINDOW};
    color: {C_TEXT_MAIN};
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
}}

QListWidget {{
    background-color: {C_BG_PANEL};
    border: 1px solid {C_BORDER};
    border-radius: 4px;
    outline: none;
    padding: 5px;
}}

QListWidget::item {{
    background-color: {C_BG_PANEL};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    margin: 4px;
    padding: 2px; 
}}

QListWidget::item:selected {{
    background-color: {C_BG_HEADER};
    border: 2px solid {C_ACCENT};
}}

QPushButton {{
    background-color: {C_BTN_BG};
    border: 1px solid {C_BTN_BORDER};
    border-radius: 3px;
    color: {C_BTN_TEXT};
    padding: 4px;
}}

QPushButton:hover {{
    background-color: {C_BTN_HOVER};
    border: 1px solid {C_ACCENT}; 
}}

/* --- GroupBox & Header Section --- */
QGroupBox {{
    font-weight: bold;
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: {C_BG_HEADER};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 0 5px;
    color: {C_TEXT_DIM};
}}

#SystemInfoLabel {{
    color: {C_ACCENT}; 
    font-size: 15px;
    font-weight: bold;
}}

#VersionLabel {{
    color: {C_TEXT_DIM};
    font-size: 11px;
}}

QPushButton#HeaderSettingsBtn {{
    background-color: {C_BG_PANEL};
    border: 1px solid {C_BORDER_DARK};
    border-radius: 4px;
    color: {C_TEXT_MAIN};
}}
"""

# ==========================
# --- HTML TEMPLATES ---
# ==========================
HTML_CARD_STYLE = f"""
<div style='text-align: center; margin-top: 5px;'>
    <div style='color: {C_TEXT_MAIN}; font-size: 11px; font-weight: bold; margin-bottom: 8px;'>{{name}}</div>
    <div style='background-color: {C_BTN_BLUE}; color: {C_WHITE}; border-radius: 5px; 
                padding: 6px; font-weight: bold; font-size: 12px; margin: 0 5px;'>
        Assign
    </div>
</div>
"""

HTML_FOLDER_STYLE = f"""
<div style='text-align: center; margin-top: 5px;'>    
    <div style='background-color: {C_FOLDER_BG}; color: {C_TEXT_MAIN}; border: 1px solid {C_FOLDER_BORDER}; 
                border-radius: 5px; padding: 6px; font-weight: bold; font-size: 11px; margin: 0 5px;'>
        {{name}}
    </div>
</div>
"""

# ==========================
# --- INDIVIDUAL BUTTONS ---
# ==========================
BTN_ACTION = f"QPushButton {{ background-color: {C_BTN_BLUE}; font-weight: bold; color: {C_WHITE}; border: 1px solid {C_ACCENT}; }}"
BTN_DONATE = f"QPushButton {{ background-color: {C_DONATE_BG}; color: {C_DONATE_TEXT}; font-weight: bold; border-radius: 4px; }}"
BTN_GITHUB = f"QPushButton {{ background-color: {C_GITHUB_BG}; color: {C_WHITE}; font-weight: bold; border-radius: 4px; }}"