
import os
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QListWidgetItem, QLabel
from PySide6.QtGui import QIcon, QPixmap


class BatchLoader:
    def __init__(self, browser_widget, items_per_page=20):
        self.browser = browser_widget
        self.items_per_page = items_per_page
        self.all_items = []
        self.current_index = 0

    def setup(self, items):
        self.all_items = items
        self.current_index = 0
        self.load_next() 
        
        
        if len(items) > self.items_per_page:
            self.browser.show_status_message(f"Loaded {self.items_per_page} items. Scroll down to load more...", "orange")

    def load_next(self):
        
        if self.current_index >= len(self.all_items):
            self.browser.show_status_message("All materials loaded.", "green")
            return

        print(f">>> [DEBUG] Loading Batch: {self.current_index} to {self.current_index + self.items_per_page}")

        
        scrollbar = self.browser.asset_list.verticalScrollBar()
        current_scroll_position = scrollbar.value()        
        self.browser.asset_list.setUpdatesEnabled(False)    
        
        end = self.current_index + self.items_per_page
        batch = self.all_items[self.current_index:end]
        
        for mat_path in batch:
            self.browser.split_material_library(mat_path)
            self.browser.add_material_item(mat_path) 
            
        self.current_index = end
        
        
        self.browser.asset_list.setUpdatesEnabled(True)

        
        scrollbar.setValue(current_scroll_position)

        self.browser.show_status_message(f"Loading materials: {end} of {len(self.all_items)}", "orange")


