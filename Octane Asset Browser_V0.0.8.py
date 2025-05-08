# ==========================
# IMAN SHIRANI
# 2025 V0.0.8 UI\UX
# ==========================


# ==========================
# From import
# ==========================
import os
import json
import uuid
import tempfile
import subprocess
import inspect  
import platform
from collections import deque, Counter

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QProgressBar, QAbstractItemView,
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QInputDialog,
    QListWidgetItem, QMenu, QDialog, QFormLayout, QScrollArea, QTabWidget,
    QSizePolicy, QSplitter, QLineEdit, QDockWidget, QStatusBar, QLabel, QVBoxLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, QTimer

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
    preferred_versions = ["2025", "2026"]

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
CONFIG_PATH = os.path.join(os.path.expanduser("~"), "octane_asset_config.json")
DEFAULT_MATERIAL_ROOT = "C:/OctaneMaterials/"


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {"material_root": DEFAULT_MATERIAL_ROOT}


def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

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
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.config = config

        # ??????? ?? QTabWidget ???? ??? ??
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

    def create_about_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        layout.addRow("App Name:", QLabel("Octane Asset Browser"))
        layout.addRow("Version:", QLabel("v0.0.8"))
        layout.addRow("Developer:", QLabel("IMAN SHIRANI"))
        layout.addRow("Config Path:", QLabel(self.config.get("config_path", "Not Set")))
        link = QLabel('<a href="https://github.com/yourrepo">GitHub Repo</a>')
        link.setOpenExternalLinks(True)
        layout.addRow("GitHub:", link)
        link = QLabel('<a href="https://www.paypal.com/donate/?hosted_button_id=LAMNRY6DDWDC4">Donate Link</a>')
        link.setOpenExternalLinks(True)
        layout.addRow("Donate:", link)

        return widget

    def change_material_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Material Root Folder")
        if dir_path:
            self.config["material_root"] = dir_path
            save_config(self.config)
            QMessageBox.information(self, "Saved", "Material path updated. Please restart the application.")
            self.accept()



# ==========================
# Main Asset Browser
# ==========================
class AssetBrowserWidget(QWidget):
    def __init__(self):              
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        import os
        import inspect
        from collections import deque
        self.thumbnail_queue = deque()
        self.thumbnail_processing = False
        self.render_queue = deque()
        self.is_rendering = False

        self.config = load_config()
        self.active_render_engine = self.detect_active_render_engine()        
        self.root_path = self.config.get("material_root", DEFAULT_MATERIAL_ROOT)
        self.current_path = self.root_path
        
        #thumbnail queue
        self.thumbnail_queue = deque()
        self.thumbnail_running = False
        self.thumbnail_processing = False
        
        #move Folder
        self._move_in_progress = False
        self.context_menu = None
        self.clicked_item_data = None
        
        #Material cache
        self.material_class_cache = {}
        
        #PBR PATH
        #self.pbr_output_path = os.path.join(self.root_path, "PBR Material", "pbr_library.mat")
        #os.makedirs(os.path.dirname(self.pbr_output_path), exist_ok=True)
        
        # Path to local icon folder (robust for inside Max)
        current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.icon_path = os.path.join(current_dir, "etc", "icon")
        self.icon_path = self.icon_path.replace("\\", "/")
        print("[DEBUG] Icon path:", self.icon_path)
        print("[DEBUG] Folder exists:", os.path.exists(self.icon_path))

        # --- Toolbar buttons ---
        #Back To home Icon 
        self.btn_up = QPushButton()
        up_icon = QIcon(os.path.join(self.icon_path, "up.ico"))
        if up_icon.isNull():
            print("[DEBUG] up.png icon is NULL   fallback to text")
            self.btn_up.setText("Back To Folder")
        else:
            self.btn_up.setIcon(up_icon)
        self.btn_up.setToolTip("Go Up")
        self.btn_up.setIconSize(QSize(18, 18))
        self.btn_up.setFixedSize(32, 32)
        self.btn_up.clicked.connect(self.navigate_up)

        #New Folder Icon
        self.btn_new_folder = QPushButton()
        folder_icon = QIcon(os.path.join(self.icon_path, "folder.ico"))
        if folder_icon.isNull():
            print("[DEBUG] folder.png icon is NULL   fallback to text")
            self.btn_new_folder.setText("New Folder")
        else:
            self.btn_new_folder.setIcon(folder_icon)
        self.btn_new_folder.setToolTip("New Folder")
        self.btn_new_folder.setIconSize(QSize(18, 18))
        self.btn_new_folder.setFixedSize(32, 32)
        self.btn_new_folder.clicked.connect(self.create_folder)

        #Refresh Icon
        self.btn_refresh = QPushButton()
        refresh_icon = QIcon(os.path.join(self.icon_path, "refresh.ico"))
        if refresh_icon.isNull():
            print("[DEBUG] refresh.png icon is NULL   fallback to text")
            self.btn_refresh.setText("Refresh")
        else:
            self.btn_refresh.setIcon(refresh_icon)
        self.btn_refresh.setToolTip("Refresh")
        self.btn_refresh.setIconSize(QSize(18, 18))
        self.btn_refresh.setFixedSize(32, 32)
        self.btn_refresh.clicked.connect(lambda: self.load_folder(self.current_path))
        
        #Settin Icon
        self.btn_settings = QPushButton()
        settings_icon = QIcon(os.path.join(self.icon_path, "settins.ico"))
        if settings_icon.isNull():
            print("[DEBUG] settings.png icon is NULL   fallback to text")
            self.btn_settings.setText("Setting")
        else:
            self.btn_settings.setIcon(settings_icon)
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.setIconSize(QSize(18, 18))
        self.btn_settings.setFixedSize(32, 32)
        self.btn_settings.clicked.connect(self.open_settings)
        
        # Assign to objects Icon
        self.btn_assign = QPushButton()
        assign_icon = QIcon(os.path.join(self.icon_path, "assign.ico"))
        if assign_icon.isNull():
            print("[DEBUG] assign.ico icon is NULL   fallback to text")
            self.btn_assign.setText("Assign To Object")  # If no icon, use text
        else:
            self.btn_assign.setIcon(assign_icon)
        self.btn_assign.setToolTip("Assign selected material to selected objects")
        self.btn_assign.setIconSize(QSize(18, 18))
        self.btn_assign.setFixedSize(32, 32)
        self.btn_assign.clicked.connect(self.assign_selected_material)
        
        

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(6)
        toolbar_layout.addWidget(self.btn_up)
        toolbar_layout.addWidget(self.btn_new_folder)
        toolbar_layout.addWidget(self.btn_refresh)
        toolbar_layout.addWidget(self.btn_settings)
        toolbar_layout.addWidget(self.btn_assign)
        toolbar_layout.addStretch()

        # --- Path bar ---
        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)        
        clean_path = self.current_path.replace("\\", "/")
        self.path_display.setText(clean_path)
        print("[DEBUG] current_path before display:", self.current_path)
        

        # --- Search bar ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_items)

        # --- Main asset list ---
        self.asset_list = QListWidget()
        self.asset_list.setViewMode(QListWidget.IconMode)
        self.asset_list.setIconSize(QSize(128, 128))
        self.asset_list.setGridSize(QSize(140, 160))
        self.asset_list.setResizeMode(QListWidget.Adjust)
        self.asset_list.setWrapping(True)
        self.asset_list.setWordWrap(False)
        self.asset_list.setSpacing(8)
        self.asset_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.asset_list.customContextMenuRequested.connect(self.show_context_menu)
        self.asset_list.itemDoubleClicked.connect(self.handle_double_click)
        self.asset_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.asset_list.setDragEnabled(False)
        self.asset_list.setAcceptDrops(False)
        #self.asset_list.setDragDropMode(QListWidget.NoDragDrop)    
         
        
        
        
        self.asset_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: none;
            }
            QListWidget::item {
                margin: 2px;
                padding: 2px;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #505050;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #3c3c3c;
            }
        """)

        def format_item_label(text):
            return f'<div style="color:#ddd; font-size:11px; font-family:Segoe UI, sans-serif; text-align:center; padding-top:4px;">{text}</div>'
        self.format_item_label = format_item_label

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.asset_list)

        self.status_label = QLabel("Ready")
        self.show_status_message(f"Active Render Engine: {self.active_render_engine.upper()}", "green")
        self.status_label.setStyleSheet("color: gray; font-style: italic; padding: 4px;")
        
        # --- Render Engines Lib Class ---
        self.allowed_classes = {
            "octane": [
                "Clipping_material","Composite_material","Diffuse_layer","Diffuse_material","Glossy_material",
                "Hair_material","Layer_group","Layered_material","Material_Selector","Material_layer_switch",
                "Material_switch","Metallic_layer","Metallic_material","Mix_material","Portal_material",
                "Shadow_catcher_material","Sheen_layer","Specular_layer","Specular_material","Std_Surface_Mtl",
                "Toon_material","Universal_material" 
            ],
            "arnold": [
                "ai_standard_surface", "ai_car_paint", "ai_standard_hair",
                "ai_standard_volume", "ai_skin", "ai_shadow_mat",
                "ai_wireframe", "ai_flat", "ai_layer_shader", "ai_mix_shader",
                "standard_surface", "aistandard", "aistandardsurface"
            ],
            "vray": [
                "vraymtl", "vraylightmtl"
            ],
            "corona": [
                "coronamtl", "coronalightmtl", "coronaphysicalmtl"
            ],
            "other": [
                "physicalmaterial", "standard", "raytrace", "architectural",
            ]}
            
        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.path_display)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(scroll)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)
        self.load_folder(self.current_path)

# ==========================
# Detect Render Engine
# ========================== 
    def detect_active_render_engine(self):
        try:
            from pymxs import runtime as rt
            engine = str(rt.renderers.current).lower()
            print(f"[DEBUG] Active Render Engine: {engine}")

            # ?????? ?? Octane
            if "octane" in engine:
                return "octane"
            elif "arnold" in engine:
                return "arnold"
            elif "vray" in engine:
                return "vray"
            elif "corona" in engine:
                return "corona"
            else:
                return "other"

        except Exception as e:
            print(f"[ERROR] Failed to detect render engine: {e}")
            return "other"


# ==========================
# Material class allowed
# ========================== 
    def is_material_class_allowed(self, mat, engine=None):
        try:
            from pymxs import runtime as rt
            engine = engine or self.active_render_engine
            mat_class_obj = rt.classOf(mat)
            mat_class = str(mat_class_obj.name).lower() if hasattr(mat_class_obj, "name") else str(mat_class_obj).lower()
            allowed = [cls.lower() for cls in self.allowed_classes.get(engine, [])]

            if engine == "arnold":
                return any(cls in mat_class for cls in allowed)
            else:
                return mat_class in allowed

        except Exception as e:
            print(f"[FILTER ERROR] Failed to check material class: {e}")
            return False

# ==========================
# show status message
# ========================== 
    def show_status_message(self, message: str, color: str = "black"):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-style: italic; padding: 4px;")
     
# ==========================
# update status message
# ========================== 
    def update_status_message(self, message, color="gray", duration=3000):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-style: italic;")

        # Back to Ready After s
        QTimer.singleShot(duration, lambda: self.status_label.setText("Ready"))
            
        
# ==========================
# Assign with Butten 
# ==========================
    def assign_selected_material(self):
        selected_item = self.asset_list.currentItem()
        if not selected_item:
            self.show_status_message("No item selected.", "red")
            return

        path = selected_item.data(Qt.UserRole)
        if not path or "::" not in path:
            self.show_status_message("Selected item is not a material.", "red")
            return

        try:
            mat_path, mat_name = path.split("::")
            mat_path = mat_path.replace("\\", "/")
            self.assign_material_to_selection(mat_path, mat_name)
            self.show_status_message(f"Assigned '{mat_name}' to selected object(s).", "green")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to assign material:\n{e}")  
# ==========================
# Assign with select  Object
# ==========================
    def assign_material_to_selection(self, mat_path, mat_name):
        try:
            print(f"[DEBUG] Assigning material: {mat_name} from {mat_path}")
            from pymxs import runtime as rt

            lib = rt.loadTempMaterialLibrary(mat_path)
            if not lib:
                print(f"[ERROR] Cannot load material library: {mat_path}")
                return

            print(f"[DEBUG] Material library loaded. Count: {lib.count}")
            target_mat = None
            for i in range(lib.count):
                print(f"[DEBUG] Checking material: {lib[i].name}")
                if lib[i].name == mat_name:
                    target_mat = lib[i]
                    break

            if not target_mat:
                print(f"[ERROR] Material '{mat_name}' not found in library.")
                return

            selected_nodes = rt.selection
            if not selected_nodes:
                print("[INFO] No objects selected.")
                return

            print(f"[DEBUG] Assigning to {len(selected_nodes)} objects.")
            for node in selected_nodes:
                node.material = target_mat
                print(f"[INFO] Assigned to: {node.name}")

            print(f"[INFO] Successfully assigned material '{mat_name}' to selected objects.")

        except Exception as e:
            print(f"[ERROR] assign_material_to_selection failed: {e}")  


# ==========================
# Move selected materials to folder (multi-material safe)
# ==========================
    def move_selected_materials_to_folder(self):
        import os
        import shutil
        from PySide6.QtWidgets import QFileDialog, QMessageBox

        items = self.asset_list.selectedItems()
        if not items:
            return

        destination = QFileDialog.getExistingDirectory(self, "Select Destination Folder", self.root_path)
        if not destination or not destination.startswith(self.root_path):
            QMessageBox.warning(self, "Invalid Destination", "You can only move items inside the material root folder.")
            return

        for item in items:
            data = item.data(Qt.UserRole)
            if not data or "::" not in data:
                continue

            mat_path, mat_name = data.split("::")

            # Real File [mat_name].mat
            actual_file = os.path.join(os.path.dirname(mat_path), f"{mat_name}.mat")

            if not os.path.exists(actual_file):
                print(f"[WARNING] File not found: {actual_file}")
                continue

            try:
                destination_file = os.path.join(destination, f"{mat_name}.mat")
                shutil.move(actual_file, destination_file)
                print(f"[MOVE] {mat_name} ? {destination}")

                # --- Move thumbnail if exists ---
                mat_dir = os.path.dirname(mat_path)
                found_thumb = False
                for file in os.listdir(mat_dir):
                    if file.lower().endswith(".jpg") and file.startswith(mat_name):
                        thumb_src = os.path.join(mat_dir, file)
                        thumb_dest = os.path.join(destination, file)
                        shutil.move(thumb_src, thumb_dest)
                        print(f"[THUMB] Moved thumbnail: {thumb_src} ? {thumb_dest}")
                        found_thumb = True
                        break
                if not found_thumb:
                    print(f"[THUMB] No thumbnail found for material: {mat_name}")

            except Exception as e:
                print(f"[ERROR] Failed to move {mat_name}: {e}")

        self.load_folder(self.current_path)
    
# ==========================
# Move .mat Material File
# ==========================
    def move_material_to_folder(self, path):
        if self._move_in_progress:
            print("[DEBUG] Move already in progress. Skipping duplicate.")
            return
        self._move_in_progress = True

        try:
            mat_path, mat_name = path.split("::")
            mat_dir = os.path.dirname(mat_path)

            destination = QFileDialog.getExistingDirectory(self, "Select Destination Folder", self.root_path)
            if not destination or not destination.startswith(self.root_path):
                QMessageBox.warning(self, "Invalid Destination", "You can only move items inside the material root folder.")
                return

            new_mat_path = os.path.join(destination, f"{mat_name}.mat").replace("\\", "/")
            mat_path_escaped = repr(mat_path).replace("'", '"')
            new_mat_path_escaped = repr(new_mat_path).replace("'", '"')

            print(f"[DEBUG] Moving material: {mat_name}")
            print(f"[DEBUG] From: {mat_path}")
            print(f"[DEBUG] To: {new_mat_path}")

            ms_code = f'''
                try (
                    print "*** MOVE DEBUG START ***"
                    local src = loadTempMaterialLibrary @{mat_path_escaped}
                    print ("[MS] Source loaded: " + src.count as string)

                    local dst_path = @{new_mat_path_escaped}
                    local dst = if doesFileExist dst_path then loadTempMaterialLibrary dst_path else MaterialLibrary()
                    print ("[MS] Destination lib loaded: " + dst.count as string)

                    local found = undefined
                    for i = src.count to 1 by -1 do (
                        print ("[MS] Checking: " + src[i].name)
                        if src[i].name == "{mat_name}" then (
                            found = src[i]
                            deleteItem src i
                            print ("[MS] Found and deleted from source.")
                            exit
                        )
                    )

                    if found != undefined then (
                        append dst found
                        print ("[MS] Appended to destination.")
                        saveTempMaterialLibrary dst dst_path
                        print ("[MS] Saved destination.")
                        saveTempMaterialLibrary src @{mat_path_escaped}
                        print ("[MS] Saved source.")

                        if src.count == 0 then (
                            print ("[MS] Source is now empty.")
                            "EMPTY"
                        ) else (
                            "OK"
                        )
                    ) else (
                        print ("[MS] Material not found!")
                        "NOT_FOUND"
                    )
                ) catch (
                    print "*** MOVE DEBUG ERROR ***"
                    print (getCurrentException())
                    "ERROR"
                )
            '''

            from pymxs import runtime as rt
            result = rt.execute(ms_code)
            print(f"[DEBUG] MaxScript result: {result}")
            if result == "EMPTY":
                if os.path.exists(mat_path):
                    os.remove(mat_path)
                    print(f"[CLEANUP] Deleted empty .mat file: {mat_path}")
            elif result != "OK":
                raise Exception(f"MaxScript failed: {result}")
                
            
            # ? RIGHT HERE
            if self.context_menu:
                self.context_menu.close()
                self.context_menu = None

            # Move thumbnail if it exists
            try:
                found_thumb = False
                for file in os.listdir(mat_dir):
                    if file.lower().endswith(".jpg") and file.startswith(mat_name):
                        thumb_src = os.path.join(mat_dir, file)
                        thumb_dest = os.path.join(destination, file)
                        shutil.move(thumb_src, thumb_dest)
                        print(f"[THUMB] Moved thumbnail: {thumb_src} -> {thumb_dest}")
                        found_thumb = True
                        break
                if not found_thumb:
                    print(f"[THUMB] No thumbnail found for material: {mat_name}")
            except Exception as e:
                print(f"[THUMB ERROR] Could not move thumbnail for {mat_name}: {e}")
            

            # Refresh and clean UI
            self.load_folder(self.current_path)
            self.asset_list.clearFocus()             # ? prevent right-click triggering again
            QApplication.processEvents()             # ? flush pending UI events
            self.show_status_message(f"Moved material '{mat_name}'", "green")

        except Exception as e:
            print(f"[ERROR] Failed to move material: {e}")
            QMessageBox.critical(self, "Error", f"Failed to move material:\n{e}")
        finally:
            self._move_in_progress = False

# ==========================
# Static method arnold materials
# ==========================
    @staticmethod
    def is_arnold_material(mat):
        try:
            from pymxs import runtime as rt
            cat = rt.getPluginCategory(rt.classOf(mat))
            return "arnold" in cat.lower()
        except:
            return False
    
# ==========================
# generate thumbnail
# ==========================     
    def generate_thumbnail(self, mat_path, mat_name, callback=None):
        print(f"[GENERATE] Starting thumbnail for: {mat_name}")
        try:
            import inspect, re, os
            from pymxs import runtime as rt

            current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
            scene_dir = os.path.join(current_dir, "etc", "3dfile")

            # Load material
            # ==========================  
            self.log_status(f"[DEBUG] Loading material from: {mat_path} / name: {mat_name}")
            lib = rt.loadTempMaterialLibrary(mat_path)
            mat = None
            for i in range(lib.count):
                if lib[i].name == mat_name:
                    mat = lib[i]
                    break

            if not mat:
                self.log_status(f"[ERROR] Material '{mat_name}' not found in {mat_path}")
                return

            # Determine if Octane
            # ==========================  
            class_name = str(rt.classOf(mat)).lower()
            mat_path_clean = mat_path.replace("\\", "/")
            octane_classes = [cls.lower() for cls in self.allowed_classes.get("octane", [])]
            is_octane = any(cls in class_name for cls in octane_classes)        

            # Thumbnail path
            # ==========================
            mat_clean = re.sub(r'[^\w\-_\.]', '_', mat_name)
            thumb_name = f"{mat_name}.jpg"
            thumb_path = os.path.join(os.path.dirname(mat_path), thumb_name).replace("\\", "/")
            self.log_status(f"[DEBUG] Thumbnail output path: {thumb_path}")
            self.log_status(f"[DEBUG] Thumbnail output path: {thumb_path}")

            if not running_inside_3dsmax():
                self.log_status("[ERROR] This must run inside 3ds Max.")
                return

            # === Octane: Use Render Scene ===
            if is_octane:
                scene_file = os.path.join(scene_dir, "Octane.max").replace("\\", "/")
                self.log_status(f"[DEBUG] Scene file selected: {scene_file}")

                if not os.path.isfile(scene_file):
                    self.log_status(f"[ERROR] Scene file does not exist: {scene_file}")
                    return

                self.log_status("[INFO] Rendering inside 3ds Max (Octane)...")
                rt.loadMaxFile(scene_file, quiet=True)

                sphere = rt.getNodeByName("Sphere001")
                cylinder = rt.getNodeByName("Cylinder001")

                if sphere and cylinder:
                    sphere.material = mat
                    cylinder.material = mat
                    self.log_status("[DEBUG] Materials assigned. Starting render...")

                    rt.render(width=128, height=128, vfb=False, outputfile=thumb_path)

                    if os.path.exists(thumb_path):
                        self.log_status(f"[SUCCESS] Thumbnail rendered at: {thumb_path}")
                    else:
                        self.log_status("[ERROR] Render did not produce output.")

                    self.log_status("[DEBUG] Calling resetMaxFile...")
                    rt.resetMaxFile(rt.name("noPrompt"))
                    self.log_status("[DEBUG] resetMaxFile done.")
                    self.log_status("[DEBUG] Scene reset after render.")
                else:
                    self.log_status("[ERROR] Scene objects not found: Sphere001 or Cylinder001")
                    return

            # === Non-Octane: Procedural scene render ===
            else:
                try:
                    thumb_width, thumb_height = 128, 128
                    rt.renderWidth = thumb_width
                    rt.renderHeight = thumb_height

                    # Create sphere
                    # ==========================  
                    sphere = rt.sphere(radius=25, segments=32, pos=rt.Point3(0, 0, 0))
                    sphere.material = mat
                    uvwmod = rt.UVWMap()
                    uvwmod.mapping = rt.Name("spherical")
                    rt.addModifier(sphere, uvwmod)

                    # Background
                    # ==========================  
                    bg = rt.plane(length=300, width=300)
                    bg.rotation = rt.eulerangles(-50, 0, 0)
                    bg.position = rt.Point3(0, 35, 0)

                    # Background material
                    # ==========================  
                    uv_texture_path = os.path.join(scene_dir, "UVChecke2.png").replace("\\", "/")
                    if os.path.exists(uv_texture_path):
                        tex = rt.Bitmaptexture()
                        tex.filename = uv_texture_path

                        if self.active_render_engine == "arnold":
                            bg_mat = rt.PhysicalMaterial()
                            bg_mat.base_color_map = tex
                        else:
                            bg_mat = rt.standardMaterial()
                            bg_mat.diffuseMap = tex
                        bg.material = bg_mat

                        uvw_bg = rt.UVWMap()
                        uvw_bg.mapping = rt.Name("planar")
                        rt.addModifier(bg, uvw_bg)

                    # Lighting
                    # ==========================  
                    if self.active_render_engine == "arnold":
                        light = rt.Arnold_Light()
                        light.type = 3
                        light.width = 200
                        light.height = 200
                        light.position = rt.Point3(0, -100, 0)
                        light.rotation = rt.eulerangles(90, 0, 0)
                        light.intensity = 300
                        light.castShadows = True
                    else:
                        light = rt.omniLight()
                        light.position = rt.Point3(50, -80, 100)

                    # Camera
                    # ==========================  
                    cam = rt.freeCamera()
                    cam.position = rt.Point3(0, -70, 40)
                    cam.target = sphere
                    rt.viewport.setCamera(cam)
                    cam.depthOfField = False

                    # Render
                    # ==========================  
                    rt.render(camera=cam, width=thumb_width, height=thumb_height, vfb=False, outputfile=thumb_path)

                    if os.path.exists(thumb_path):
                        self.log_status(f"[SUCCESS] Thumbnail saved: {thumb_path}")
                    else:
                        self.log_status(f"[ERROR] Thumbnail NOT saved: {thumb_path}")

                    # Cleanup
                    # ==========================  
                    rt.delete(sphere)
                    rt.delete(bg)
                    rt.delete(light)
                    rt.delete(cam)

                except Exception as e:
                    self.log_status(f"[EXCEPTION] Thumbnail render failed: {e}")

        except Exception as e:
            self.log_status(f"[ERROR] Thumbnail generation failed: {e}")

        finally:
            if getattr(self, 'thumbnail_dialog', None):
                try:
                    self.thumbnail_dialog.close()
                except Exception as e:
                    self.log_status(f"[WARNING] Could not close thumbnail dialog: {e}")
                self.thumbnail_dialog = None  # ??? ?????

            self.show_status_message("Ready", "orange")
            self.process_next_thumbnail()

# ==========================  
# split material library 
# ========================== 
    def split_material_library(self, mat_path):
        import os
        from pymxs import runtime as rt

        if not os.path.exists(mat_path):
            self.log_status(f"[WARNING] File not found: {mat_path}")
            return

        try:
            lib = rt.loadTempMaterialLibrary(mat_path)
            mat_dir = os.path.dirname(mat_path)

            if lib.count == 0:
                self.log_status(f"[INFO] Empty library removed: {mat_path}")
                os.remove(mat_path)
                return

            if lib.count == 1:
                self.log_status(f"[INFO] Library has 1 material, skipping split: {mat_path}")
                return

            self.log_status(f"[SPLIT] Splitting {lib.count} materials from: {mat_path}")

            split_count = 0
            for i in range(lib.count):
                mat = lib[i]
                mat_name = mat.name
                mat_file = f"{mat_name}.mat"
                mat_path_out = os.path.join(mat_dir, mat_file).replace("\\", "/")

                if not os.path.exists(mat_path_out):
                    single_lib = rt.MaterialLibrary()
                    rt.append(single_lib, mat)
                    rt.saveTempMaterialLibrary(single_lib, mat_path_out)
                    self.log_status(f"[SPLIT] ? Saved: {mat_path_out}")
                    split_count += 1
                else:
                    self.log_status(f"[SKIP] Already exists: {mat_path_out}")

            os.remove(mat_path)
            self.log_status(f"[CLEANUP] Original multi-material file removed: {mat_path}")
            self.log_status(f"[DONE] Total split: {split_count} materials")

        except Exception as e:
            self.log_status(f"[ERROR] Failed to split {mat_path} - {e}")

        
# ==========================  
# LoG STATUS 
# ==========================  
    def log_status(self, message, level="INFO"):
        tag = {
            "INFO": "[INFO]",
            "DEBUG": "[DEBUG]",
            "ERROR": "[ERROR]",
            "QUEUE": "[QUEUE]",
            "THUMB": "[THUMB]"
        }.get(level.upper(), "[LOG]")
        print(f"{tag} {message}")    

# ==========================  
# enqueue_thumbnail 
# ==========================   
    def enqueue_thumbnail(self, mat_path, mat_name):
        print(f"[QUEUE] Enqueuing thumbnail: {mat_name}")
        self.thumbnail_queue.append((mat_path, mat_name))

        # ??? ??? thumbnail_dialog ???? ?????? ????? ??
        if not getattr(self, 'thumbnail_dialog', None):
            self.thumbnail_dialog = ThumbnailProgressDialog(self)
            self.thumbnail_dialog.show()
            print("[QUEUE] Thumbnail dialog shown")

        # if was free
        if not self.thumbnail_running:
            self.thumbnail_running = True
            self.process_next_thumbnail()
            
# ==========================  
#process next thumbnail 
# =========================            
    def process_next_thumbnail(self):
        if not self.thumbnail_queue:
            self.thumbnail_running = False

            if getattr(self, 'thumbnail_dialog', None):
                try:
                    self.thumbnail_dialog.close()
                except Exception as e:
                    self.log_status(f"[WARNING] Could not close thumbnail dialog: {e}")
                self.thumbnail_dialog = None

            self.log_status("[QUEUE] Done. No more items.")
            self.show_status_message("Thumbnails generated successfully.", "green")
            self.status_label.setText("Ready")
            
            # ?? Refresh UI to show new thumbnails
            self.load_folder(self.current_path)
            return

        self.thumbnail_processing = True

        mat_path, mat_name = self.thumbnail_queue.popleft()
        self.log_status(f"[QUEUE] Processing: {mat_name}")
        self.status_label.setText(f"Rendering thumbnail for: {mat_name}...")

        # Defer thumbnail rendering slightly to let UI update
        QTimer.singleShot(100, lambda: self.generate_thumbnail(mat_path, mat_name))
        
    
     

    def write_maxscript(self, scene_file, mat_path, mat_name, thumb_path, script_path):
        try:
            # ?? LOG SECEN
            self.log_status(f"[DEBUG] Raw scene_file: {scene_file}", level="DEBUG")

            # ?? CHECK MAX FILE
            if not scene_file.lower().endswith(".max"):
                raise ValueError(f"? scene_file is invalid: {scene_file}")

            with open(script_path, "w", encoding="utf-8") as f:
                # ? LODE MAX FILE
                f.write(f'loadMaxFile @"{scene_file}" quiet:true\n')
                f.write('sleep 0.2\n')

                # ?? FIND Material
                f.write(f'matlib = loadTempMaterialLibrary @"{mat_path}"\n')
                f.write(f'format "Searching for: {mat_name}\\n"\n')
                f.write('theMat = undefined\n')
                f.write('for i = 1 to matlib.count do (\n')
                f.write(f'    if matlib[i].name == "{mat_name}" then (\n')
                f.write('        theMat = matlib[i]\n')
                f.write('        exit\n')
                f.write('    )\n')
                f.write(')\n')

                # ? FIND Materil LOG
                f.write('format "Loaded material: %\\n" (if theMat != undefined then theMat.name else "NOT FOUND")\n')

                # ?? ADD MATERIAL AND RENDER
                f.write('if (isValidNode $Sphere001 and isValidNode $Cylinder001 and theMat != undefined) then (\n')
                f.write('    $Sphere001.material = theMat\n')
                f.write('    $Cylinder001.material = theMat\n')
                f.write(f'    render width:128 height:128 vfb:false outputfile:@"{thumb_path}"\n')
                f.write(') else (\n')
                f.write('    format "ERROR: Material or scene objects not found.\\n"\n')
                f.write(')\n')

                # ? EXIT 3DMAX
                f.write('quitMax #noPrompt\n')

            self.log_status(f"? MXS written to: {script_path}", level="DEBUG")
            return True

        except Exception as e:
            self.log_status(f"? Failed to write .ms file: {e}", level="ERROR")
            return False

# ==========================
# Show Material From .mat
# ==========================
    def show_material_list_from_mat(self, mat_path):
        try:
            from pymxs import runtime as rt
            lib = rt.loadTempMaterialLibrary(mat_path)
            if lib is None:
                QMessageBox.critical(self, "Error", "Cannot load material library.")
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Materials in: " + os.path.basename(mat_path))
            layout = QVBoxLayout()
            list_widget = QListWidget()

            for i in range(lib.count):
                mat = lib[i]
                list_widget.addItem(mat.name)

            layout.addWidget(list_widget)
            dialog.setLayout(layout)
            dialog.setMinimumSize(400, 300)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read .mat file:{e}")  
    
    
   
# ==========================
# Load Folder Contents
# ==========================    
    def load_folder(self, path):
        print("[DEBUG] load_folder called with path:", path)
        import os
        import re
        from pymxs import runtime as rt
        from PySide6.QtGui import QPixmap

        
        self.asset_list.clear()
        if not os.path.isdir(path):
            return

        self.current_path = path
        self.path_display.setText(self.current_path.replace("\\", "/"))
        
        # Split any multi-material .mat files
        # ==========================
        for file in os.listdir(path):
            if file.lower().endswith(".mat"):
                full_path = os.path.join(path, file).replace("\\", "/")
                self.split_material_library(full_path)

        # --- Load and display materials + cache class ---
        # ==========================
        

        # ==========================
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)

            if os.path.isdir(item_path):
                icon_file = os.path.join(item_path, "icon.png")
                thumb_file = os.path.join(item_path, f"{item}.jpg")

                if os.path.exists(icon_file):
                    icon = QIcon(QPixmap(icon_file))
                elif os.path.exists(thumb_file):
                    icon = QIcon(QPixmap(thumb_file))
                else:
                    default_pixmap = QPixmap(128, 128)
                    default_pixmap.fill(Qt.black)  # ?? ??? ???????
                    icon = QIcon(default_pixmap)

                # PBR folder detection
                # ==========================
                display_name = item
                if self.is_pbr_folder(item_path):
                    display_name += " [PBR]"

                entry = QListWidgetItem(icon, display_name)
                entry.setData(Qt.UserRole, item_path)
                self.asset_list.addItem(entry)

            # ==========================
            # Material Library (.mat) File
            # ==========================
            elif item.lower().endswith(".mat"):
                mat_path = os.path.join(path, item).replace("\\", "/")
                try:
                    lib = rt.loadTempMaterialLibrary(mat_path)

                    for i in range(lib.count):
                        mat = lib[i]
                        mat_name = mat.name

                        try:
                            mat_class = rt.classOf(mat).name.lower()
                        except:
                            classof = rt.classOf(mat)
                            mat_class = str(classof.name).lower() if hasattr(classof, "name") else str(classof).lower()

                        print(f"[DEBUG] Mat name: {mat_name}, class: {mat_class}")

                        if not mat_class:
                            print(f"[SKIP] {mat_name} has no valid class.")
                            continue

                        if not self.is_material_class_allowed(mat):
                            print(f"[SKIP] '{mat.name}' skipped (class not allowed)")
                            continue

                        print(f"[?] Accepted material: {mat_name}")

                        # Generate potential thumbnail names (default + fallback)
                        # ==========================
                        mat_clean = re.sub(r'[^\w\-_\.]', '_', mat.name)
                        thumb_path = os.path.join(os.path.dirname(mat_path), f"{mat_name}.jpg").replace("\\", "/")


                        # Check if it already exists (optional fallback logic)
                        if not os.path.exists(thumb_path):
                            print(f"[AUTO-GEN] Enqueue thumbnail: {thumb_path}")
                            self.enqueue_thumbnail(mat_path, mat.name)

                        

                        # Queue thumbnail generation if not found
                        # ==========================
                        if not thumb_path:
                            print(f"[TODO] Enqueue thumbnail for: {mat_name}")
                            self.enqueue_thumbnail(mat_path, mat_name)

                        icon = QIcon(QPixmap(thumb_path)) if thumb_path and os.path.exists(thumb_path) else QIcon.fromTheme("document")

                        entry = QListWidgetItem(icon, mat_name)
                        entry.setData(Qt.UserRole, f"{mat_path}::{mat_name}")
                        self.asset_list.addItem(entry)

                except Exception as e:
                    print(f"[ERROR] Cannot load .mat file: {e}")

                    



    
# ==========================
# double_click
# ==========================
    def handle_double_click(self, item):
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
            self.load_folder(path)
        elif isinstance(path, str) and ".mat::" in path:
            print(f"[DEBUG] Double clicked material: {path}")

# ==========================
# UP 
# ==========================
    def navigate_up(self):
        parent_path = os.path.dirname(self.current_path)
        if os.path.abspath(parent_path).startswith(os.path.abspath(self.root_path)):
            self.load_folder(parent_path)
# ==========================
# create folder
# ==========================
    def create_folder(self):
        new_name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and new_name:
            new_path = os.path.join(self.current_path, new_name)
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Folder Exists", f"A folder named '{new_name}' already exists.")
                return
            try:
                os.makedirs(new_path, exist_ok=True)

                import shutil
                import inspect
                current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
                icon_template = os.path.join(current_dir, "icon.png")
                if os.path.exists(icon_template):
                    shutil.copy(icon_template, os.path.join(new_path, "icon.png"))

                self.load_folder(self.current_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")

# ==========================
# debug_log_all_mat_files
# ==========================
    def debug_log_all_mat_files(self, folder_path):
        from pymxs import runtime as rt
        import os

        print(f"\n=== [DEBUG] Scanning .mat files in: {folder_path} ===")
        for file in os.listdir(folder_path):
            if file.lower().endswith(".mat"):
                full_path = os.path.join(folder_path, file).replace("\\", "/")
                try:
                    lib = rt.loadTempMaterialLibrary(full_path)
                    if lib and lib.count > 0:
                        print(f"[?] {file} - Loaded ({lib.count} materials):")
                        for i in range(lib.count):
                            print(f"    +- {lib[i].name} ({rt.classOf(lib[i])})")
                    else:
                        print(f"[?] {file} - EMPTY or failed to load.")
                except Exception as e:
                    print(f"[ERROR] {file} - Exception: {e}")
        print("=== [END] ===\n")

# ==========================
# PBR Material
# ==========================  
    def is_pbr_folder(self, folder_path):
        if not os.path.isdir(folder_path):
            return False

        files = [f.lower() for f in os.listdir(folder_path)]
        required_keywords = ["albedo", "basecolor", "diffuse", "roughness", "normal", "metal", "ao"]

        for name in files:
            for keyword in required_keywords:
                if keyword in name:
                    return True
        return False    
        
# ==========================
# Right Click Menu
# ==========================    
    def show_context_menu(self, position):
        self.log_status("Right-click triggered", level="DEBUG")
        
        import os
        import uuid
        import tempfile
        import subprocess
        import inspect
        import re
        from PySide6.QtWidgets import QMessageBox
        
        self.asset_list.selectedItems()
        item = self.asset_list.itemAt(position)
        print("[DEBUG] itemAt:", item)
        if item:
            # multi-select Move If Selected
            if item not in self.asset_list.selectedItems():
                self.asset_list.clearSelection()
                item.setSelected(True)
        else:
            return
            
        selected = self.asset_list.selectedItems()
        self.log_status(f"Selected items: {[i.text() for i in selected]}", level="DEBUG")
        
        self.log_status(f"Item: {item.text() if item else 'None'}", level="DEBUG")
        if item is None:
            return
            
        data = item.data(Qt.UserRole)
        if not data:
            return

        
        # Start Right Click Menu
        # ========================== 
        
        
        path = item.data(Qt.UserRole)
        self.log_status(f"Path: {path}", level="DEBUG")

        menu = QMenu()
        is_folder = os.path.isdir(path)
        is_mat = "::" in path and path.lower().endswith(".mat::" + path.split("::")[-1].lower())
        is_orbx = "::" in path and path.lower().endswith(".orbx::orbx")
        
        

        # ORBX File
        if is_orbx:
            import_orbx_action = menu.addAction("Import ORBX to Material Library")
        
        
        
        #Folder File
        if is_folder:
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")
            set_icon_action = menu.addAction("Set Icon")
            if self.is_pbr_folder(path):
                make_pbr_action = menu.addAction("Make PBR Material (Octane)")
               
        
        #Mat File 
        elif is_mat:
            move_action = menu.addAction("Move to Another Folder...")
            mat_path, mat_name = path.split("::")
            print(f"[DEBUG] MAT path: {mat_path}, name: {mat_name}")

            generate_thumb_action = None  # ? fix for unbound variable

            try:
                from pymxs import runtime as rt
                lib = rt.loadTempMaterialLibrary(mat_path)
                print(f"[DEBUG] Library loaded. Count: {lib.count}")

                mat = None
                for i in range(lib.count):
                    m = lib[i]
                    print(f"[DEBUG] Checking material: {m.name}")
                    if m.name == mat_name:
                        mat = m
                        break

                if not mat:
                    print(f"[ERROR] Material not found in library: {mat_name}")
                    return

                classof = rt.classOf(mat)
                mat_class = str(classof.name).lower() if hasattr(classof, "name") else str(classof).lower()
                print(f"[DEBUG] Material class: {mat_class}")

                engine_key = self.active_render_engine
                allowed = self.allowed_classes.get(engine_key, [])
                print(f"[DEBUG] Active engine: {engine_key}, Allowed classes: {allowed}")

                try:
                    classof = rt.classOf(mat)
                    mat_class = str(classof.name) if hasattr(classof, "name") else str(classof)
                    mat_class_clean = mat_class.strip()

                    if engine_key == "octane" and mat_class_clean in self.allowed_classes["octane"]:
                        generate_thumb_action = menu.addAction("Generate Thumbnail")
                except Exception as e:
                    print(f"[ERROR] Failed to detect class: {e}")

                assign_action = menu.addAction("Assign to Selected Object(s)")
                rename_mat_action = menu.addAction("Rename Material")
                delete_mat_action = menu.addAction("Delete Material")

                
                
                if action == assign_action:
                    self.assign_material_to_selection(mat_path, mat_name)

                elif action == rename_mat_action:
                    self.rename_material(mat_path, mat_name)

                elif action == delete_mat_action:
                    self.delete_material(mat_path, mat_name)

                elif generate_thumb_action and action == generate_thumb_action:
                    from PySide6.QtWidgets import QMessageBox
                    confirm = QMessageBox.question(
                        self,
                        "Confirm Thumbnail Generation",
                        f"Do you want to generate thumbnail for: {mat_name}?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if confirm == QMessageBox.Yes:
                        self.enqueue_thumbnail(mat_path, mat_name)

            except Exception as e:
                print(f"[ERROR] show_context_menu failed: {e}")
          
               
        # Run Action
        action = menu.exec(self.asset_list.mapToGlobal(position))
        
        # Check PBR FOLDER
        if is_folder and self.is_pbr_folder(path) and action == make_pbr_action:
            try:
                from pymxs import runtime as rt
                import os

                folder_name = os.path.basename(path)
                lib_path = os.path.join(path, f"{folder_name}.mat").replace("\\", "/")
                files = {f.lower(): f for f in os.listdir(path)}

                def find_map(keywords):
                    for name in files:
                        lower_name = name.lower()
                        if any(lower_name.endswith(k + ext) for k in keywords for ext in [".jpg", ".png", ".jpeg", ".tif", ".exr"]):
                            return os.path.join(path, files[name])
                    return None

                # ?? Find all supported maps
                map_albedo   = find_map(["albedo", "basecolor", "diffuse"])
                map_rough    = find_map(["roughness"])
                map_norm     = find_map(["normal", "nor"])
                map_metal    = find_map(["metal", "metallic"])
                map_opacity  = find_map(["opacity", "transparency"])
                map_displace = find_map(["displace", "displacement", "height"])
                map_ao       = find_map(["ao", "ambientocclusion"])
                map_emission = find_map(["emission", "emit", "glow"])
                map_gloss    = find_map(["gloss", "glossiness", "specular"])

                if not map_albedo:
                    QMessageBox.warning(self, "Missing Map", "No Albedo/BaseColor found in folder.")
                    return

                def norm_path(p): return p.replace("\\", "/") if p else ""

                # Normalize all paths
                map_albedo   = norm_path(map_albedo)
                map_rough    = norm_path(map_rough)
                map_norm     = norm_path(map_norm)
                map_metal    = norm_path(map_metal)
                map_opacity  = norm_path(map_opacity)
                map_displace = norm_path(map_displace)
                map_ao       = norm_path(map_ao)
                map_emission = norm_path(map_emission)
                map_gloss    = norm_path(map_gloss)
                lib_dir = os.path.join(self.root_path, "PBR")  
                os.makedirs(lib_dir, exist_ok=True)
                lib_path = os.path.join(lib_dir, f"{folder_name}.mat").replace("\\", "/")


                
                def tex_block(tex_path, slot_name):
                    """
                    tex_path: (string)
                    slot_name:  ("baseColor_tex")
                    """
                    if not tex_path:
                        return ""
                    # 
                    if slot_name == "displacement_tex":
                        return f'''
                        if doesFileExist "{tex_path}" do (
                            
                            dispNode = Texture_displacement()
                            
                            dispTex = RGB_image name:"{folder_name}_displacement.png"
                            dispTex.filename = "{tex_path}"
                            dispTex.filename_bitmaptex = bitmaptexture filename:dispTex.filename
                            
                            dispNode.texture_tex = dispTex
                            
                            mtl.displacement = dispNode
                        )'''
                    # 
                    var_name   = slot_name.replace("_tex", "Tex")                  # "baseColor_tex" -> "baseColorTex"
                    input_prop = slot_name.replace("_tex", "") + "_input_type"     # "baseColor_input_type"
                    return f'''
                    if doesFileExist "{tex_path}" do (
                        {var_name} = RGB_image()
                        {var_name}.filename = "{tex_path}"
                        {var_name}.filename_bitmaptex = bitmaptexture filename:{var_name}.filename
                        mtl.{input_prop} = 2
                        mtl.{slot_name} = {var_name}
                    )'''
                    
    

                # Assign all map slots if found
                tex_blocks = [
                    tex_block(map_albedo,   "baseColor_tex"),
                    tex_block(map_rough,    "roughness_tex"),
                    tex_block(map_metal,    "metallic_tex"),
                    tex_block(map_norm,     "normal_tex"),
                    tex_block(map_opacity,  "opacity_tex"),
                    tex_block(map_displace, "displacement_tex"),  # ??? ???? ???????????
                    # tex_block(map_ao,       "ambient_occlusion_tex"),
                    tex_block(map_emission, "emission_tex"),
                    tex_block(map_gloss,    "specularLevel_tex")
                ]

                tex_code = "\n".join(tex_blocks)
                lib_path = os.path.join(path, f"{folder_name}.mat").replace("\\", "/")
                
                ms_code = f'''
                try (
                    local mtl = Std_Surface_Mtl name:"{folder_name}"

                    -- here we inject the actual MXS lines,
                    -- not the Python list object!
                    {tex_code}

                    -- Next Slot Material Editor
                    local slot_index = 1
                    for i = 1 to meditMaterials.count do (
                        if meditMaterials[i] == undefined do (
                            slot_index = i
                            exit
                        )
                    )
                    meditMaterials[slot_index] = mtl

                    -- Save to new dedicated .mat file
                    local lib = MaterialLibrary()
                    append lib mtl
                    saveTempMaterialLibrary lib "{lib_path}"
                    "OK"
                ) catch (
                    format "Failed to create Std_Surface_Mtl.\\n"
                    "ERROR"
                )
                '''

                print("[DEBUG] MaxScript for Octane Std_Surface_Mtl:\n", ms_code)
                result = rt.execute(ms_code)


                if result != "OK":
                    raise Exception("MaxScript failed to create Octane Std_Surface_Mtl.")

                self.show_status_message(f"Created Octane Std_Surface_Mtl: '{folder_name}'", "green")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create Octane Std_Surface_Mtl:\n{e}")
        
        
        
        #IF FOLDER
        if is_folder:
            if action == rename_action:
                new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=item.text())
                if ok and new_name and new_name != item.text():
                    new_path = os.path.join(os.path.dirname(path), new_name)
                    try:
                        os.rename(path, new_path)
                        self.load_folder(self.current_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Rename failed: {e}")
            elif action == delete_action:
                confirm = QMessageBox.question(
                    self, "Delete",
                    f"Are you sure you want to delete '{item.text()}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    import shutil
                    try:
                        shutil.rmtree(path)
                        self.load_folder(self.current_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Delete failed: {e}")
            elif action == set_icon_action:
                file_path, _ = QFileDialog.getOpenFileName(self, "Choose Icon", "", "Images (*.png *.jpg *.jpeg *.bmp)")
                if file_path:
                    try:
                        import shutil
                        dest_path = os.path.join(path, "icon.png")
                        shutil.copyfile(file_path, dest_path)
                        self.load_folder(self.current_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to set icon: {e}")

        #Assgin Materil to objects On Rigth Click
        elif is_mat and action == assign_action:
            try:
                mat_path, mat_name = path.split("::")
                mat_path = mat_path.replace("\\", "/")
                self.assign_material_to_selection(mat_path, mat_name)
                self.show_status_message(f"Assigned '{mat_name}' to selected object(s).", "green")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to assign material:\n{e}")
        
        #Generation Thumbnil On Rigth Click
        elif is_mat and action and action.text() == "Generate Thumbnail":
            try:
                mat_path, mat_name = path.split("::")
                mat_path = mat_path.replace("\\", "/")

                confirm = QMessageBox.question(
                    self,
                    "Confirm Thumbnail Generation",
                    f"Do you want to generate thumbnail for: {mat_name}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm != QMessageBox.Yes:
                    return

                self.status_label.setText(f"? Generating thumbnail for: {mat_name}... Please wait.")
                self.enqueue_thumbnail(mat_path, mat_name)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to enqueue thumbnail:\n{e}")
                
        
        #Rename Material
        elif is_mat and action == rename_mat_action:
            try:
                mat_path, old_name = path.split("::")

                new_name, ok = QInputDialog.getText(
                    self,
                    "Rename Material",
                    f"Enter new name for material '{old_name}':",
                    text=old_name
                )
                if not ok or not new_name or new_name == old_name:
                    return

                from pymxs import runtime as rt

                # MaxScript ???? rename ???? ??????
                ms_code = f'''
                try (
                    local lib = loadTempMaterialLibrary @"{mat_path}"
                    for i = 1 to lib.count do (
                        if lib[i].name == "{old_name}" then (
                            lib[i].name = "{new_name}"
                            exit
                        )
                    )
                    saveTempMaterialLibrary lib @"{mat_path}"
                    true
                ) catch (
                    false
                )
                '''

                result = rt.execute(ms_code)
                if not result:
                    raise Exception("Failed to rename material via MaxScript")

                # rename thumbnail (??? ???? ????)
                thumb_dir = os.path.dirname(mat_path)
                thumb_found = None
                for fname in os.listdir(thumb_dir):
                    if fname.lower().endswith(old_name.lower() + ".jpg"):
                        thumb_found = os.path.join(thumb_dir, fname)
                        new_thumb = os.path.join(thumb_dir, fname.replace(old_name, new_name))
                        os.rename(thumb_found, new_thumb)
                        print(f"[DEBUG] Renamed thumbnail: {thumb_found} ? {new_thumb}")
                        break

                self.load_folder(self.current_path)
                self.show_status_message(f"Renamed '{old_name}' ? '{new_name}'", "green")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to rename material:\n{e}")
        
        #Delete Material On Rigth Click
        elif is_mat and action == delete_mat_action:
            try:
                mat_path, mat_name = path.split("::")
                from pymxs import runtime as rt

                # User Confrim
                confirm = QMessageBox.question(
                    self,
                    "Delete Material",
                    f"Are you sure you want to delete material '{mat_name}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm != QMessageBox.Yes:
                    return

                # DELETE Material WITH MAX SCRIPT
                ms_code = f'''
                try (
                    local lib = loadTempMaterialLibrary @"{mat_path}"
                    for i = lib.count to 1 by -1 do (
                        if lib[i].name == "{mat_name}" then deleteItem lib i
                    )
                    saveTempMaterialLibrary lib @"{mat_path}"
                    true
                ) catch (
                    false
                )
                '''
                result = rt.execute(ms_code)
                print("[DEBUG] Delete Material Result:", result)

                if not result:
                    raise Exception("MaxScript failed")

                # Remove thumbnail
                thumb_dir = os.path.dirname(mat_path)
                thumb_found = None
                for fname in os.listdir(thumb_dir):
                    if fname.lower().endswith(mat_name.lower() + ".jpg"):
                        thumb_found = os.path.join(thumb_dir, fname)
                        break

                if thumb_found and os.path.isfile(thumb_found):
                    try:
                        os.remove(thumb_found)
                        print(f"[DEBUG] Thumbnail deleted: {thumb_found}")
                    except Exception as e:
                        print(f"[WARNING] Failed to delete thumbnail: {e}")

                # Refresh
                self.load_folder(self.current_path)
                self.show_status_message(f"Deleted '{mat_name}' and thumbnail.", "orange")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete material:\n{e}")
        
        # ORBX Right CLick
        if is_orbx and action == import_orbx_action:
            try:
                from pymxs import runtime as rt
                orbx_file = path.split("::")[0].replace("\\", "/")

                print(f"[DEBUG] Importing ORBX: {orbx_file}")
                rt.execute(f'Octane_LoadORBXFile @"{orbx_file}"')

                self.show_status_message(f"ORBX imported: {os.path.basename(orbx_file)}", "green")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import ORBX:\n{e}")
        
        # Move To Folders        
        elif is_mat and action == move_action:
            QTimer.singleShot(100, self.move_selected_materials_to_folder)
            
# ==========================
# Filter Items
# ==========================
    def filter_items(self, query):
        query = query.strip().lower()
        self.asset_list.clear()

        if not query:
            self.load_folder(self.current_path)
            return

        engine = self.active_render_engine
        allowed_classes = [c.lower() for c in self.allowed_classes.get(engine, [])]

        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.lower().endswith(".mat"):
                    mat_name = os.path.splitext(file)[0]
                    if query in mat_name.lower():
                        mat_path = os.path.join(root, file).replace("\\", "/")
                        thumbnail_path = os.path.join(root, f"{mat_name}.jpg").replace("\\", "/")

                        # ??????? ?? ???? ??????:
                        if any(self.asset_list.item(i).text() == mat_name for i in range(self.asset_list.count())):
                            continue

                        mat_class = self.material_class_cache.get(mat_path.lower(), "unknown")
                        if mat_class.lower() != "unknown" and mat_class.lower() not in allowed_classes:
                            continue

                        icon = QIcon(thumbnail_path) if os.path.exists(thumbnail_path) else QIcon()
                        item = QListWidgetItem(icon, mat_name)
                        item.setData(Qt.UserRole, f"{mat_path}::{mat_name}")
                        self.asset_list.addItem(item)





# ==========================
# Filter Items get_mat_class
# ==========================
    def get_mat_class(self, mat_path):
        try:
            from pymxs import runtime as rt

            if not os.path.exists(mat_path):
                print(f"[SKIP] File not found: {mat_path}")
                return None

            matlib = rt.loadTempMaterialLibrary(mat_path)

            if not matlib or matlib.count == 0:
                print(f"[WARN] No materials in: {mat_path}")
                return None

            mat = matlib[1]  # ?? max ?? 1 ???? ?????
            mat_class = rt.classOf(mat).name
            print(f"[DEBUG] Mat class from {mat_path}: {mat_class}")
            return mat_class

        except Exception as e:
            print(f"[ERROR] get_mat_class() failed for {mat_path}: {e}")
            return None

       
                    
# ==========================
# open_settings
# ==========================
    def open_settings(self):
        dlg = SettingsDialog(self, self.config)
        dlg.exec()
        self.root_path = self.config.get("material_root", DEFAULT_MATERIAL_ROOT)
        self.load_folder(self.root_path)



# ==========================
# Run inside 3ds Max
# ==========================
def show_in_max():
    try:
        from qtmax import GetQMaxMainWindow
    except ImportError:
        raise ImportError("qtmax module not available. This must be run inside 3ds Max 2022+.")

    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()

    main_window = GetQMaxMainWindow()

    for widget in app.allWidgets():
        if isinstance(widget, QDockWidget) and widget.windowTitle() == "Octane Folder Explorer":
            widget.close()

    dock = AssetBrowserDock(parent=main_window)
    app.installEventFilter(dock.shelf_tool)  # ? ???? ???????
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
    dock.show()


class DockableShelf(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Octane Asset Browser")
        self.shelf_tool = AssetBrowserWidget()
        self.setWidget(self.shelf_tool)


from qtmax import GetQMaxMainWindow

main_window = GetQMaxMainWindow()
dockable_window = DockableShelf()
main_window.addDockWidget(Qt.RightDockWidgetArea, dockable_window)
dockable_window.show()
