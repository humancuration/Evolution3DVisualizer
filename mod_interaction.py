# mod_interaction.py

class Interaction:
    def __init__(self, visualization, ui):
        self.viz = visualization
        self.ui = ui
        self.connect_signals()
    
    def connect_signals(self):
        # Zoom buttons
        self.ui.zoom_in_button.clicked.connect(self.zoom_in)
        self.ui.zoom_out_button.clicked.connect(self.zoom_out)
        self.ui.reset_view_button.clicked.connect(self.reset_view)
        # load data button
        self.ui.load_data_button.clicked.connect(self.load_data)

        
        # Rotation buttons
        self.ui.rotate_x_pos_button.clicked.connect(lambda: self.rotate_view(axis=0, angle=5))
        self.ui.rotate_x_neg_button.clicked.connect(lambda: self.rotate_view(axis=0, angle=-5))
        self.ui.rotate_y_pos_button.clicked.connect(lambda: self.rotate_view(axis=1, angle=5))
        self.ui.rotate_y_neg_button.clicked.connect(lambda: self.rotate_view(axis=1, angle=-5))
        self.ui.rotate_z_pos_button.clicked.connect(lambda: self.rotate_view(axis=2, angle=5))
        self.ui.rotate_z_neg_button.clicked.connect(lambda: self.rotate_view(axis=2, angle=-5))
    
    def zoom_in(self):
        self.viz.update_zoom(10)  # Adjust zoom increment as needed
    
    def zoom_out(self):
        self.viz.update_zoom(-10)  # Adjust zoom decrement as needed
    
    def load_data(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
        self.viz,
        "Open Data File",
        "",
        "CSV Files (*.csv);;JSON Files (*.json)",
        options=options
    )
        try:
            raw_data = load_data(file_name)
            processed_data = process_data(raw_data)
            tree = generate_tree(processed_data)
            self.viz.update_tree(tree)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.viz, "Error", f"Failed to load data:\n{e}")


    def reset_view(self):
        self.viz.zoom = -100
        self.viz.rotation = [0, 0, 0]
        self.viz.update()
    
    def rotate_view(self, axis, angle):
        """
        Rotates the view around the specified axis by the given angle.

        Parameters:
            axis (int): 0 for x, 1 for y, 2 for z.
            angle (float): Angle to rotate in degrees.
        """
        self.viz.update_rotation(axis, angle)

    def update_time(self, value):
        # Update the visualization based on the selected time
        self.viz.update_time(value)
