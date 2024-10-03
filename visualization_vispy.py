# visualization_vispy.py

import vispy
from vispy import app, scene
from vispy.visuals import transforms
import networkx as nx
import numpy as np

class VispyVisualization(app.Canvas):
    def __init__(self, tree, settings):
        app.Canvas.__init__(self, title='Evolution 3D Visualizer with VisPy', keys='interactive')
        self.tree = tree
        self.settings = settings

        # Create a 3D scene
        self.view = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
        self.view.camera = scene.cameras.TurntableCamera(up='z', fov=60)

        # Add a grid
        grid = self.view.central_widget.add_grid()

        # Create a scatter plot for nodes
        self.node_positions = np.array([self.tree.nodes[node]['pos'] for node in self.tree.nodes()])
        self.node_colors = np.array([self.get_color_for_attribute(self.tree.nodes[node].get('attribute', 'default')) for node in self.tree.nodes()])
        self.scatter = scene.visuals.Markers()
        self.scatter.set_data(self.node_positions, face_color=self.node_colors, size=5)
        self.view.add(self.scatter)

        # Create a line plot for edges
        edges = []
        edge_colors = []
        for edge in self.tree.edges():
            start_pos = self.tree.nodes[edge[0]]['pos']
            end_pos = self.tree.nodes[edge[1]]['pos']
            edges.append([start_pos, end_pos])
            edge_colors.append([0.5, 0.5, 0.5, 1.0])  # RGBA color for edges

        self.edge_segments = np.array(edges)
        self.lines = scene.visuals.Line(pos=self.edge_segments.reshape(-1, 3), connect='segments', color=edge_colors)
        self.view.add(self.lines)

        # Show the canvas
        self.show()

    def get_color_for_attribute(self, attr):
        color_map = {
            'attribute_value_1': [1.0, 0.0, 0.0, 1.0],  # Red
            'attribute_value_2': [0.0, 1.0, 0.0, 1.0],  # Green
            'default': [0.5, 0.5, 0.5, 1.0],            # Gray
        }
        return color_map.get(attr, color_map['default'])

    def on_draw(self, event):
        gloo.clear('white')
        self.view.draw()

if __name__ == '__main__':
    # Assume 'tree' and 'settings' are already defined
    vis = VispyVisualization(tree, settings)
    vispy.app.run()
