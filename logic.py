# ==========================
# From import
# ==========================
import os
import getpass
import json

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QProgressBar, QAbstractItemView,
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QInputDialog,
    QListWidgetItem, QMenu, QDialog, QFormLayout, QScrollArea, QTabWidget,
    QSizePolicy, QSplitter, QLineEdit, QDockWidget, QStatusBar
)
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtCore import QSize, Qt, QTimer, QUrl

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
# Config Path Load & save 
# ==========================
DEFAULT_MATERIAL_ROOT = "C:/Materials/"
current_user = getpass.getuser()
CONFIG_PATH = os.path.join("C:/Users", current_user, "Material_asset_config.json").replace("\\", "/")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")

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

