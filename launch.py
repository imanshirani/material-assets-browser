import os
import sys
import importlib
from PySide6.QtWidgets import QDockWidget, QApplication
from PySide6.QtCore import Qt


current_folder = os.path.dirname(os.path.realpath(__file__))
if current_folder not in sys.path:
    sys.path.insert(0, current_folder)


for mod in ["style", "logic", "ui"]:
    if mod in sys.modules:
        del sys.modules[mod]

try:
    import style
    import logic
    import ui
    importlib.reload(style)
    importlib.reload(logic)
    importlib.reload(ui)
    from ui import AssetBrowserWidget
    print(f"[SUCCESS] Modules loaded from: {current_folder}")
except Exception as e:
    print(f"[CRITICAL ERROR] Failed to load modules: {e}")

def show_in_max():
    from qtmax import GetQMaxMainWindow
    app = QApplication.instance()
    main_window = GetQMaxMainWindow()

    
    for widget in app.allWidgets():
        if isinstance(widget, QDockWidget) and widget.windowTitle() == "Octane Asset Browser":
            widget.close()
            widget.deleteLater()

    class DockableShelf(QDockWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Octane Asset Browser")
            self.setObjectName("OctaneAssetBrowserDock")
            self.shelf_tool = AssetBrowserWidget()
            self.setWidget(self.shelf_tool)

    dock = DockableShelf(parent=main_window)
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
    dock.show()

if __name__ == "__main__":
    show_in_max()