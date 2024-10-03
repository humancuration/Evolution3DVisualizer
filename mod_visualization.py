from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
import sys
import networkx as nx
import numpy as np

class Visualization(QOpenGLWidget):
    def __init__(self, tree, settings):
        super(Visualization, self).__init__()
        self.node_id_map = {}
        self.tree = tree
        self.settings = settings
        self.zoom = -100  # Initial zoom level
        self.rotation = [0, 0, 0]  # Rotation angles for x, y, z axes
        self.setMinimumSize(800, 600)
        self.last_mouse_pos = None
        self.setFocusPolicy(Qt.StrongFocus)
    
    def initializeGL(self):
        # Background color and other initial settings
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        glEnable(GL_DEPTH_TEST)
        glPointSize(self.settings['visualization_params']['node_size'])
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 1, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

        # Create Vertex Buffer Object (VBO) for efficient rendering
        self.create_vbo()

    def create_vbo(self):
        # Prepare vertex data for VBO
        vertices = []
        for node in self.tree.nodes():
            pos = self.tree.nodes[node]['pos']
            vertices.extend(pos)
        self.node_vbo = vbo.VBO(np.array(vertices, dtype='f'))

    def draw_tree(self, select_mode=False):
        # Draw nodes using VBO
        glPointSize(self.settings['visualization_params']['node_size'])
        glBegin(GL_POINTS)
        for idx, node in enumerate(self.tree.nodes()):
            pos = self.tree.nodes[node]['pos']
            if select_mode:
                glLoadName(idx + 1)
                self.node_id_map[idx + 1] = node
            else:
                # Assign color based on node attribute
                attr = self.tree.nodes[node].get('attribute', 'default')
                glColor3f(*self.get_color_for_attribute(attr))
            glVertex3f(*pos)
        glEnd()

        # Draw edges (light gray)
        glColor3f(0.7, 0.7, 0.7)
        glLineWidth(1)
        glBegin(GL_LINES)
        for edge in self.tree.edges(data=True):
            node1, node2, data = edge
            pos1 = self.tree.nodes[node1]['pos']
            pos2 = self.tree.nodes[node2]['pos']
            glVertex3f(*pos1)
            glVertex3f(*pos2)
        glEnd()

    def get_color_for_attribute(self, attr):
        # Assign color based on attribute
        color_map = {
            'attribute_value_1': (1.0, 0.0, 0.0),  # Red
            'attribute_value_2': (0.0, 1.0, 0.0),  # Green
            'default': (0.5, 0.5, 0.5),            # Gray
        }
        return color_map.get(attr, color_map['default'])

    def resizeGL(self, w, h):
        # Resize the OpenGL viewport and set the perspective
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h) if h != 0 else 1, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Clear the screen and reset the view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Move back to see the scene
        glTranslatef(self.pan[0], self.pan[1], self.zoom)
        # Apply rotations
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw the tree
        self.draw_tree()
        self.update()

    def project_position(self, x, y, z):
        # Convert 3D coordinates to 2D screen coordinates for label rendering
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        window_coords = gluProject(x, y, z, modelview, projection, viewport)
        if window_coords:
            win_x, win_y, win_z = window_coords
            qt_y = self.height() - win_y
            return (int(win_x), int(qt_y))
        return None

    def mousePressEvent(self, event):
        # Store mouse press position
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        # Handle mouse dragging for rotation and panning
        if self.last_mouse_pos is None:
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        if event.buttons() & Qt.LeftButton:
            # Rotate view with left button drag
            self.rotation[0] += dy * 0.5
            self.rotation[1] += dx * 0.5
        elif event.buttons() & Qt.RightButton or (event.buttons() & Qt.LeftButton and event.modifiers() & Qt.ShiftModifier):
            # Pan view with right button drag or Shift + left button drag
            self.pan[0] += dx * 0.01
            self.pan[1] -= dy * 0.01

        self.last_mouse_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        # Reset mouse press position on release
        self.last_mouse_pos = None

    def wheelEvent(self, event):
        # Zoom in or out using the mouse wheel
        delta = event.angleDelta().y() / 120  # Each notch is 120 units
        self.update_zoom(delta * 5)  # Adjust zoom sensitivity

    def mouseDoubleClickEvent(self, event):
        # Handle node selection on double-click
        x = event.x()
        y = self.height() - event.y()
        selected_node = self.pick_node(x, y)
        if selected_node:
            self.show_node_info(selected_node)

    def pick_node(self, x, y):
        # Node picking using OpenGL selection mode
        buffer_size = 512
        select_buffer = glSelectBuffer(buffer_size)
        glRenderMode(GL_SELECT)
        glInitNames()
        glPushName(0)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        viewport = glGetIntegerv(GL_VIEWPORT)
        gluPickMatrix(x, y, 5, 5, viewport)
        gluPerspective(45, viewport[2] / viewport[3], 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(self.pan[0], self.pan[1], self.zoom)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        self.draw_tree(select_mode=True)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glFlush()

        hits = glRenderMode(GL_RENDER)
        if hits:
            closest_hit = min(hits, key=lambda hit: hit.near)
            node_id = closest_hit.names[0]
            node_name = self.node_id_map.get(node_id)
            return node_name
        return None

    def show_node_info(self, node_name):
        # Display node information in a message box
        info = f"Selected Node: {node_name}\nAdditional Info: ..."
        QtWidgets.QMessageBox.information(self, "Node Information", info)

    def update_zoom(self, delta):
        # Update zoom level and refresh the view
        self.zoom += delta
        self.update()

    def update_rotation(self, axis, angle):
        # Update rotation for the specified axis
        self.rotation[axis] += angle
        self.update()
    
    def update_tree(self, new_tree):
        self.tree = new_tree
        self.create_vbo()
        self.update()
        
    def update_time(self, time_value):
        # Filter or modify the tree based on time_value
        # Update VBOs or data structures accordingly
        self.update()
