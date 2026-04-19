from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QListWidget, QListWidgetItem, QWidget)
from PySide6.QtCore import Qt, QSize
import style

class TagManagerDialog(QDialog):
    def __init__(self, parent=None, current_tags=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Tags")
        self.setFixedSize(380, 350) 
        self.setStyleSheet(style.MAIN_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Tags List
        self.tag_list = QListWidget()
        self.tag_list.setFlow(QListWidget.LeftToRight)
        self.tag_list.setWrapping(True)
        self.tag_list.setResizeMode(QListWidget.Adjust)
        self.tag_list.setSpacing(8)
        self.tag_list.setStyleSheet(style.TAG_LIST_STYLE)
        layout.addWidget(self.tag_list)

        # Add Tag
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Enter a tag...")
        self.tag_input.setStyleSheet(style.TAG_INPUT_STYLE) 
        self.tag_input.returnPressed.connect(self.add_tag)

        self.btn_add = QPushButton("Add")
        self.btn_add.setFixedWidth(60)
        self.btn_add.setFixedHeight(32)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self.add_tag)

        input_layout.addWidget(self.tag_input)
        input_layout.addWidget(self.btn_add)
        layout.addLayout(input_layout)

        # 3. Save Tags
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save Tags")
        self.btn_save.setFixedHeight(35)
        self.btn_save.setStyleSheet(style.BTN_ACTION)
        self.btn_save.clicked.connect(self.accept)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        self.tags = []
        if current_tags:
            for tag in current_tags:
                self._create_tag_item(tag)

    def add_tag(self):
        text = self.tag_input.text().strip().lower()
        if not text:
            return
        
        
        new_tags = [t.strip() for t in text.split(",") if t.strip()]
        for tag in new_tags:
            if tag not in self.tags:
                self._create_tag_item(tag)
        
        self.tag_input.clear()

    def _create_tag_item(self, tag_text):
        self.tags.append(tag_text)
        item = QListWidgetItem(self.tag_list)
        
        tag_widget = QWidget()
        tag_layout = QHBoxLayout(tag_widget)
        tag_layout.setContentsMargins(2, 2, 2, 2)
        tag_layout.setSpacing(1)
        tag_widget.setStyleSheet(style.TAG_CHIP_STYLE)

        lbl = QLabel(tag_text)        
        lbl.adjustSize() 
        
        btn_remove = QPushButton("×")
        btn_remove.setFixedSize(20, 20)
        btn_remove.clicked.connect(lambda: self.remove_tag(item, tag_text))

        tag_layout.addWidget(lbl)
        tag_layout.addWidget(btn_remove)
        tag_layout.activate() 
        dynamic_size = tag_widget.sizeHint()
        
        item.setSizeHint(QSize(dynamic_size.width() + 10, dynamic_size.height() + 15))

        self.tag_list.addItem(item)
        self.tag_list.setItemWidget(item, tag_widget)

    def remove_tag(self, item, tag_text):
        if tag_text in self.tags:
            self.tags.remove(tag_text)
        row = self.tag_list.row(item)
        self.tag_list.takeItem(row)

    def get_tags(self):
        return self.tags