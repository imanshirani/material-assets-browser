import os
import sys
import importlib
import logic
import ui


importlib.reload(logic)
importlib.reload(ui)

from ui import AssetBrowserWidget

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

    dock = DockableShelf(parent=main_window)
    app.installEventFilter(dock.shelf_tool)  # DockableShelf
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