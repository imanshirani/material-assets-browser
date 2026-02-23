# --- UI COLORS ---
C_ACCENT    = "#00B2FF"
C_BTN_BLUE  = "#005a9e"
C_BG_WINDOW = "#2B2B2B"
C_BG_PANEL  = "#1E1E1E"
C_BG_HEADER = "#252525"
C_BORDER    = "#383838"
C_TEXT_MAIN = "#E0E0E0"
C_TEXT_DIM  = "#888888"

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
    background-color: #1E1E1E;
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    margin: 10px;
    padding: 0px; 
}}

QListWidget {{
    background-color: {C_BG_PANEL};
    border: none;
    outline: none;
}}


QListWidget::item:selected {{
    background-color: #252525;
    border: 2px solid {C_ACCENT};
}}

QPushButton {{
    background-color: #3a3a3a;
    border: 1px solid #555;
    border-radius: 3px;
    color: #ddd;
    padding: 4px;
}}

QPushButton:hover {{
    background-color: #4a4a4a;
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
    border: 1px solid #333;
    border-radius: 4px;
    color: {C_TEXT_MAIN};
}}
"""

HTML_CARD_STYLE = f"""
<div style='text-align: center; margin-top: 5px;'>
    <div style='color: #E0E0E0; font-size: 11px; font-weight: bold; margin-bottom: 8px;'>{{name}}</div>
    <div style='background-color: {C_BTN_BLUE}; color: white; border-radius: 5px; 
                padding: 6px; font-weight: bold; font-size: 12px; margin: 0 5px;'>
        Assign
    </div>
</div>
"""
HTML_FOLDER_STYLE = f"""
<div style='text-align: center; margin-top: 5px;'>    
    <div style='background-color: #333333; color: {C_TEXT_MAIN}; border: 1px solid #444; 
                border-radius: 5px; padding: 6px; font-weight: bold; font-size: 11px; margin: 0 5px;'>
        {{name}}
    </div>
</div>
"""

BTN_ACTION = f"QPushButton {{ background-color: #005a9e; font-weight: bold; color: white; border: 1px solid {C_ACCENT}; }}"
BTN_DONATE = f"QPushButton {{ background-color: #ffc439; color: #003087; font-weight: bold; border-radius: 4px; }}"
BTN_GITHUB = f"QPushButton {{ background-color: #24292e; color: white; font-weight: bold; border-radius: 4px; }}"