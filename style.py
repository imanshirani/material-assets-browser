

MAIN_STYLE = """
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
}


QListWidget {
    background-color: #1e1e1e;
    border: 1px solid #3f3f3f;
    border-radius: 4px;
    outline: none;
}
QListWidget::item {
    padding: 5px;
    margin: 2px;
    border-radius: 3px;
}
QListWidget::item:hover {
    background-color: #3d3d3d;
}
QListWidget::item:selected {
    background-color: #505050;
    border: 1px solid #e0e0e0; 
;
    color: white;
}


QPushButton {
    background-color: #3a3a3a;
    border: 1px solid #555;
    border-radius: 3px;
    color: #ddd;
    padding: 4px;
}
QPushButton:hover {
    background-color: #4a4a4a;
    border: 1px solid #e0e0e0; 
;
}
QPushButton:pressed {
    background-color: #222;
}


QLineEdit {
    background-color: #1a1a1a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 5px;
    color: #e0e0e0; 
}
QLineEdit:focus {
    border: 1px solid #e0e0e0; 
;
}
QLineEdit[text=""] {
    color: #888888; 
}

QScrollBar:vertical {
    border: none;
    background: #2b2b2b;
    width: 8px;
}
QScrollBar::handle:vertical {
    background: #555;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #888;
}
"""

DARK_THEME = MAIN_STYLE

BTN_ACTION = """
QPushButton {
    background-color: #005a9e;
    font-weight: bold;
    color: white;
}
QPushButton:hover {
    background-color: #e0e0e0; 
;
}
"""

# (PayPal Blue)
BTN_DONATE = """
    QPushButton {
        background-color: #ffc439;
        color: #003087;
        font-weight: bold;
        border: 1px solid #edb021;
        border-radius: 4px;
        padding: 6px;
    }
    QPushButton:hover {
        background-color: #f2ba36;
    }
    QPushButton:pressed {
        background-color: #e5af32;
    }
"""

# (GitHub Dark)
BTN_GITHUB = """
    QPushButton {
        background-color: #24292e;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        padding: 6px;
    }
    QPushButton:hover {
        background-color: #2f363d;
    }
"""