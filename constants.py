import os

# --- PRODUCT INFO ---
PRODUCT_NAME = "Material Assets Browser"
WINDOW_TITLE = "Material Assets Browser"
DOCK_OBJECT_NAME = "MaterialAssetsBrowserDock"
VERSION = "0.0.19 Beta"
AUTHOR = "Iman Shirani"
DEVELOPER_TAG = "Developed by IMAN SHIRANI"


# --- LOGGER COLORS ---
LOGGER_INFO = "#00FF00" 
LOGGER_WARN = "#FFA500"
LOGGER_ERROR = "#FF0000"

# --- LINKS & SOCIAL ---
GITHUB_URL = "https://github.com/imanshirani/material-assets-browser"
DONATION_LINK = "https://www.paypal.com/donate/?hosted_button_id=LAMNRY6DDWDC4"

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#icons
ICON_DIR = os.path.join(BASE_DIR, "icons")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DEFAULT_MATERIAL_ROOT = "C:/Materials/"
# --- UI CONSTANTS ---
HEADER_HEIGHT = 80
BUTTON_MIN_WIDTH = 120