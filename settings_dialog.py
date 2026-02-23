from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import webbrowser
import os
import style  
import constants 

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, current_path=""):
        super().__init__(parent)
        self.setWindowTitle(f"Settings - {constants.PRODUCT_NAME}")
        self.setFixedWidth(450)
        self.setStyleSheet(style.MAIN_STYLE)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(20)

        # --- About & Product Info ---
        self.group_about = QtWidgets.QGroupBox("Product Information")
        about_layout = QtWidgets.QVBoxLayout(self.group_about)
        about_layout.setContentsMargins(15, 25, 15, 15)
        
        
        self.title_label = QtWidgets.QLabel(constants.PRODUCT_NAME)
        self.title_label.setObjectName("SystemInfoLabel") 
        
        
        info_text = (
            f"<span style='color:#888;'>Version:</span> <span style='color:#ddd;'>{constants.VERSION}</span><br>"
            f"<span style='color:#888;'>Author:</span> <span style='color:#ddd;'>{constants.AUTHOR}</span>"
        )
        self.info_label = QtWidgets.QLabel(info_text)
        self.info_label.setStyleSheet("font-size: 11px; line-height: 160%;")
        
        # (GitHub & PayPal)
        link_layout = QtWidgets.QHBoxLayout()
        link_layout.setSpacing(8)
        
        self.btn_git = QtWidgets.QPushButton(" GitHub Repository")
        self.btn_git.setFixedHeight(32)
        self.btn_git.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_git.setStyleSheet(style.BTN_GITHUB)
        
        self.btn_pay = QtWidgets.QPushButton(" Support (PayPal)")
        self.btn_pay.setFixedHeight(32)
        self.btn_pay.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_pay.setStyleSheet(style.BTN_DONATE)
        
        link_layout.addWidget(self.btn_git)
        link_layout.addWidget(self.btn_pay)
        
        about_layout.addWidget(self.title_label)
        about_layout.addWidget(self.info_label)
        about_layout.addSpacing(10)
        about_layout.addLayout(link_layout)
        
        self.main_layout.addWidget(self.group_about)

        # --- Configuration ---
        self.group_config = QtWidgets.QGroupBox("Library Configuration")
        config_layout = QtWidgets.QVBoxLayout(self.group_config)
        config_layout.setContentsMargins(15, 25, 15, 15)
        
        path_label = QtWidgets.QLabel("Root Library Path:")
        path_label.setStyleSheet("color: #888; font-size: 11px;")
        
        self.path_h_layout = QtWidgets.QHBoxLayout()
        self.path_edit = QtWidgets.QLineEdit(current_path)
        self.path_edit.setReadOnly(True) 
        
        self.btn_browse = QtWidgets.QPushButton("Browse")
        self.btn_browse.setFixedWidth(70)
        
        self.path_h_layout.addWidget(self.path_edit)
        self.path_h_layout.addWidget(self.btn_browse)
        
        config_layout.addWidget(path_label)
        config_layout.addLayout(self.path_h_layout)
        
        self.main_layout.addWidget(self.group_config)
        
        # ---  Apply Changes ---
        self.btn_save = QtWidgets.QPushButton("Apply Changes")
        self.btn_save.setFixedHeight(35)
        self.btn_save.setStyleSheet(style.BTN_ACTION) 
        self.btn_save.clicked.connect(self.accept)
        
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.btn_save)

        # --- (Connections) ---
        self.btn_browse.clicked.connect(self.browse_folder)
        self.btn_git.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(constants.GITHUB_URL)))
        self.btn_pay.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(constants.DONATION_LINK)))

    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Library Folder", self.path_edit.text()
        )
        if folder:
            self.path_edit.setText(folder)

    def get_path(self):
        return self.path_edit.text()