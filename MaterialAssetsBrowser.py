import os
import sys
import importlib
from PySide6.QtWidgets import QDockWidget, QApplication
from PySide6.QtCore import Qt


script_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


if script_dir in sys.path:
    sys.path.remove(script_dir)
sys.path.insert(0, script_dir)


modules_to_clear = ["style", "logic", "ui", "loader_utils", "constants", "settings_dialog", "TagManagerDialog"] 
for mod in modules_to_clear:
    if mod in sys.modules:
        del sys.modules[mod]

try:
    import constants
    import style
    import logic
    import loader_utils
    import ui
    import settings_dialog
    import TagManagerDialog
    
    #load modules
    importlib.reload(constants)
    importlib.reload(style)
    importlib.reload(logic)
    importlib.reload(loader_utils)
    importlib.reload(ui)
    importlib.reload(settings_dialog)
    importlib.reload(TagManagerDialog)
    
    from ui import AssetBrowserWidget
    print(f"[SUCCESS] Modules loaded correctly from: {script_dir}")
except Exception as e:
    #"No module named browser_item"
    print(f"[CRITICAL ERROR] Failed to load modules: {e}")

def show_in_max():
    from qtmax import GetQMaxMainWindow
    app = QApplication.instance()
    main_window = GetQMaxMainWindow()

    # WINDOW_TITLE constants
    for widget in app.allWidgets():
        if isinstance(widget, QDockWidget) and widget.windowTitle() == constants.WINDOW_TITLE:
            widget.close()
            widget.deleteLater()

    class DockableShelf(QDockWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            #constants 
            self.setWindowTitle(constants.WINDOW_TITLE)
            self.setObjectName(constants.DOCK_OBJECT_NAME)
            
            self.shelf_tool = AssetBrowserWidget()
            self.setWidget(self.shelf_tool)

    
    dock = DockableShelf(parent=main_window)
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
    dock.setFloating(True) 
    dock.show()

if __name__ == "__main__":
    show_in_max()