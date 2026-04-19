# ==========================
# From import
# ==========================
import os
import getpass
import json
import uuid
import tempfile
import subprocess
import inspect  
import platform
from collections import deque, Counter
from settings_dialog import SettingsDialog

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QProgressBar, QAbstractItemView,
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QInputDialog,
    QListWidgetItem, QMenu, QDialog, QFormLayout, QScrollArea, QTabWidget,
    QSizePolicy, QSplitter, QLineEdit, QDockWidget, QStatusBar, QLabel, QVBoxLayout
)
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtCore import QSize, Qt, QTimer, QUrl

import style

# ==========================
# Runing Inside 3Dsmax
# ==========================
def running_inside_3dsmax():
    try:
        from pymxs import runtime as rt
        return True
    except ImportError:
        return False

# ==========================
# Find 3ds Max CMD
# ==========================
def find_3dsmaxcmd():
    # Version Of 3ds max
    preferred_versions = ["2025", "2026", "2027"]

    for version in preferred_versions:
        exe_path = fr"C:\Program Files\Autodesk\3ds Max {version}\3dsmaxcmd.exe"
        if os.path.exists(exe_path):
            print(f"[FOUND] 3dsmaxcmd: {exe_path}")
            return exe_path

    print("[NOT FOUND] No suitable 3dsmaxcmd version found.")
    return None
# ==========================
# Find Ocaten 
# ==========================
def find_octane_max():
    import os

    base_path = r"C:\Program Files\Autodesk"
    versions = ["2025", "2026", "2027"]  # ADD More Version

    for version in versions:
        max_dir = f"3ds Max {version}"
        max_path = os.path.join(base_path, max_dir)
        plugin_path = os.path.join(max_path, "plugins", "Octane3dsmax.dlr")
        exe_path = os.path.join(max_path, "3dsmaxcmd.exe")
        exe_path = exe_path.replace("\\", "/")

        print(f"[DEBUG] Checking Max {version} ? {exe_path}")
        
        if os.path.isfile(plugin_path) and os.path.isfile(exe_path):
            print(f"[FOUND] Octane-enabled Max: {exe_path}")
            return exe_path

    print("[NOT FOUND] No Octane-enabled Max found.")
    return None
    
# ==========================
# Config Path Load & save 
# ==========================
CONFIG_PATH = os.path.join(os.path.expanduser("~"), "Material_asset_config.json")
DEFAULT_MATERIAL_ROOT = "C:/Materials/"
current_user = getpass.getuser()
CONFIG_PATH = os.path.join("C:/Users", current_user, "Material_asset_config.json").replace("\\", "/")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            pass
    
    
    
    fallback_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    return {"material_root": fallback_path}

def save_config(config):
    try:
        
        config_dir = os.path.dirname(CONFIG_PATH)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"[SUCCESS] Config saved automatically to: {CONFIG_PATH}")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save config: {e}")
        return False

# ==========================
# Material Database Load & Save 
# ==========================
def load_material_db(root_path):
    import json
    import os
    db_path = os.path.join(root_path, "material_db.json").replace("\\", "/")
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Could not load material DB: {e}")
    return [] 

def save_material_db(root_path, db_data):
    import json
    import os
    db_path = os.path.join(root_path, "material_db.json").replace("\\", "/")
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Material DB saved to: {db_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save material DB: {e}")
        return False
    
# ==========================
# ThumbnailProgressDialog 
# ==========================
class ThumbnailProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Rendering Thumbnails")
        self.setModal(True)
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()

        label = QLabel("Rendering thumbnails...\nPlease wait.")
        label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate (infinite loop style)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("QProgressBar { height: 10px; } QProgressBar::chunk { background-color: #4CAF50; }")

        layout.addWidget(label)
        layout.addWidget(self.progress)
        self.setLayout(layout)
# ==========================
# Setting Dialog
# ==========================
class SettingsDialog(QDialog):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.setStyleSheet(style.MAIN_STYLE)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.config = config

        # ======== QTabWidget ========
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tabs.addTab(self.create_general_tab(), "General")
        self.tabs.addTab(self.create_about_tab(), "About")

    def create_general_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.change_material_btn = QPushButton("Change Material Root Folder")
        self.change_material_btn.clicked.connect(self.change_material_path)
        layout.addRow(self.change_material_btn)

        return widget

    

    def change_material_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Material Root Folder")
        if dir_path:
            self.config["material_root"] = dir_path
            save_config(self.config)
            QMessageBox.information(self, "Saved", "Material path updated. Please restart the application.")
            self.accept()

