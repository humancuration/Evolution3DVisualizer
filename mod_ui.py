# mod_ui.py

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSlider, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)

class LogViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Viewer")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.refresh_button = QPushButton("Refresh Logs")
        self.refresh_button.clicked.connect(self.load_logs)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        with open("app.log", "r") as f:
            self.log_text.setPlainText(f.read())

class UserInterface(QWidget):
    def __init__(self, settings, visualization, event_manager):
        super().__init__()
        self.settings = settings
        self.viz = visualization
        self.event_manager = event_manager
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
        
        # Add node size slider
        self.node_size_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.node_size_slider.setRange(1, 20)
        self.node_size_slider.setValue(self.settings['visualization_params']['node_size'])
        self.node_size_slider.valueChanged.connect(self.update_node_size)
        layout.addWidget(QtWidgets.QLabel("Node Size"))
        layout.addWidget(self.node_size_slider)
        
        # Add LOD slider
        self.lod_slider = QSlider(Qt.Horizontal)
        self.lod_slider.setRange(10, 200)
        self.lod_slider.setValue(50)
        self.lod_slider.valueChanged.connect(self.update_lod)
        layout.addWidget(QLabel("Level of Detail"))
        layout.addWidget(self.lod_slider)
        
        self.show_logs_button = QPushButton("Show Logs")
        self.show_logs_button.clicked.connect(self.show_logs)
        layout.addWidget(self.show_logs_button)

        self.setLayout(layout)

    def setup_search_bar(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a node...")
        self.search_bar.returnPressed.connect(self.search_node)
        self.layout().addWidget(self.search_bar)

    def search_node(self):
        query = self.search_bar.text()
        self.event_manager.emit('search_node', query)
  
    def get_legend_items(self):
        return [
            ('attribute_value_1', (1.0, 0.0, 0.0), "Description for attribute 1"),
            ('attribute_value_2', (0.0, 1.0, 0.0), "Description for attribute 2"),
            # Add more items with descriptions
        ]
    
    def create_legend(self):
        for attr_value, color, description in self.get_legend_items():
            color_label = QLabel()
            color_label.setFixedSize(20, 20)
            color_label.setStyleSheet(f"background-color: rgb({color[0]*255}, {color[1]*255}, {color[2]*255});")
            color_label.setToolTip(description)
            text_label = QLabel(attr_value)
            text_label.setToolTip(description)
            self.legend_layout.addWidget(color_label)
            self.legend_layout.addWidget(text_label)

    def update_node_size(self, value):
        self.settings['visualization_params']['node_size'] = value
        self.viz.update()

    def update_lod(self, value):
        self.event_manager.emit('update_lod', value)

    def show_logs(self):
        self.log_viewer = LogViewer()
        self.log_viewer.show()

    def update_time(self, value):
        # Update time logic here
        pass