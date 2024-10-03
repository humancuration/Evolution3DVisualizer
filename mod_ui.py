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
        
        self.legend_label = QtWidgets.QLabel("Legend:")
        layout.addWidget(self.legend_label)

        # Add colored labels
        legend_layout = QHBoxLayout()
        for attr_value, color in self.get_legend_items():
            color_label = QtWidgets.QLabel()
            color_label.setFixedSize(20, 20)
            color_label.setStyleSheet(f"background-color: rgb({color[0]*255}, {color[1]*255}, {color[2]*255});")
            text_label = QtWidgets.QLabel(attr_value)
            legend_layout.addWidget(color_label)
            legend_layout.addWidget(text_label)
        layout.addLayout(legend_layout)

        # Zoom Buttons
        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_out_button = QPushButton('Zoom Out')
        self.reset_view_button = QPushButton('Reset View')
        self.load_data_button = QPushButton('Load Data')
        
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)
        layout.addWidget(self.reset_view_button)
        layout.addWidget(self.load_data_button)
        
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

        self.time_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(100)  # Adjust based on your data
        self.time_slider.valueChanged.connect(self.update_time)
        layout.addWidget(self.time_slider)

        
        layout.addLayout(rotate_layout)
        
        self.setLayout(layout)
  
    def get_legend_items(self):
        return [
            ('attribute_value_1', (1.0, 0.0, 0.0)),
            ('attribute_value_2', (0.0, 1.0, 0.0)),
            # Add more items
        ]
