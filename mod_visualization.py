# mod_visualization.py

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import networkx as nx

class Visualization(QOpenGLWidget):
    def __init__(self, tree, settings):
        super(Visualization, self).__init__()
        self.tree = tree
        self.settings = settings
        self.zoom = -100  # Initial zoom level
        self.rotation = [0, 0, 0]  # Rotation angles for x, y, z axes
        self.setMinimumSize(800, 600)
    
    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Background color from settings
        glEnable(GL_DEPTH_TEST)
        glPointSize(self.settings['visualization_params']['node_size'])
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h) if h != 0 else 1, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Move back to see the scene
        glTranslatef(0.0, 0.0, self.zoom)
        # Apply rotations
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw the tree
        self.draw_tree()
        
        # Trigger label painting
        self.update()
    
    def draw_tree(self):
        # Draw edges
        glColor3f(0.7, 0.7, 0.7)  # Light gray for edges
        glLineWidth(1)
        glBegin(GL_LINES)
        for edge in self.tree.edges(data=True):
            node1, node2, data = edge
            pos1 = self.tree.nodes[node1]['pos']
            pos2 = self.tree.nodes[node2]['pos']
            glVertex3f(*pos1)
            glVertex3f(*pos2)
        glEnd()
        
        # Draw nodes
        glColor3f(1.0, 0.0, 0.0)  # Red color for nodes
        glPointSize(self.settings['visualization_params']['node_size'])
        glBegin(GL_POINTS)
        for node in self.tree.nodes():
            pos = self.tree.nodes[node]['pos']
            glVertex3f(*pos)
        glEnd()
    
    def paintEvent(self, event):
        super(Visualization, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0))
        font = QFont('Arial', 10)
        painter.setFont(font)
        
        # Project 3D coordinates to 2D screen coordinates
        for node in self.tree.nodes():
            pos = self.tree.nodes[node]['pos']
            x, y, z = pos
            screen_pos = self.project_position(x, y, z)
            if screen_pos:
                px, py = screen_pos
                painter.drawText(px, py, node)
        
        painter.end()
    
    def project_position(self, x, y, z):
        """
        Projects 3D coordinates to 2D screen coordinates.

        Parameters:
            x, y, z (float): 3D coordinates.

        Returns:
            tuple or None: 2D screen coordinates or None if not visible.
        """
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        window_coords = gluProject(x, y, z, modelview, projection, viewport)
        if window_coords:
            win_x, win_y, win_z = window_coords
            # Convert OpenGL coordinates to Qt coordinates
            qt_y = self.height() - win_y
            return (int(win_x), int(qt_y))
        return None
    
    # Methods to update view based on interactions
    def update_zoom(self, delta):
        self.zoom += delta
        self.update()
    
    def update_rotation(self, axis, angle):
        self.rotation[axis] += angle
        self.update()
