# mod_ui.py

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

class UserInterface(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('User Interface')
        self.setGeometry(900, 100, 200, 600)
        
        layout = QVBoxLayout()
        
        # Zoom Buttons
        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_out_button = QPushButton('Zoom Out')
        self.reset_view_button = QPushButton('Reset View')
        
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)
        layout.addWidget(self.reset_view_button)
        
        # Rotation Buttons
        rotate_layout = QHBoxLayout()
        
        self.rotate_x_pos_button = QPushButton('Rotate +X')
        self.rotate_x_neg_button = QPushButton('Rotate -X')
        self.rotate_y_pos_button = QPushButton('Rotate +Y')
        self.rotate_y_neg_button = QPushButton('Rotate -Y')
        self.rotate_z_pos_button = QPushButton('Rotate +Z')
        self.rotate_z_neg_button = QPushButton('Rotate -Z')
        
        rotate_layout.addWidget(self.rotate_x_pos_button)
        rotate_layout.addWidget(self.rotate_x_neg_button)
        rotate_layout.addWidget(self.rotate_y_pos_button)
        rotate_layout.addWidget(self.rotate_y_neg_button)
        rotate_layout.addWidget(self.rotate_z_pos_button)
        rotate_layout.addWidget(self.rotate_z_neg_button)
        
        layout.addLayout(rotate_layout)
        
        self.setLayout(layout)
