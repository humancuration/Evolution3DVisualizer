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
from sklearn.cluster import KMeans

class Visualization(QOpenGLWidget):
    def __init__(self, tree, settings, event_manager):
        super(Visualization, self).__init__()
        self.node_id_map = {}
        self.tree = tree
        self.settings = settings
        self.zoom = -100  # Initial zoom level
        self.rotation = [0, 0, 0]  # Rotation angles for x, y, z axes
        self.setMinimumSize(800, 600)
        self.last_mouse_pos = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.camera_pos = [0, 0, -100]  # Initial camera position
        self.lod_threshold = 50  # Initial LOD threshold
        self.selection_radius = 5  # Radius for node selection in pixels
        self.event_manager = event_manager
        self.event_manager.subscribe('search_node', self.highlight_searched_node)
        self.event_manager.subscribe('update_lod', self.update_lod_threshold)
        self.pan = [0, 0]  # Initialize pan
    
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

    def highlight_searched_node(self, node_name):
        if node_name in self.tree.nodes:
            self.highlighted_node = node_name
            self.center_view_on_node(node_name)
            self.update()

    def center_view_on_node(self, node_name):
        # Implement logic to center the view on the given node
        pass

    def create_vbo(self):
        # Prepare vertex data for VBO
        vertices = []
        for node in self.tree.nodes():
            pos = self.tree.nodes[node]['pos']
            vertices.extend(pos)
        self.node_vbo = vbo.VBO(np.array(vertices, dtype='f'))

    def cluster_nodes(self, n_clusters):
        positions = np.array([self.tree.nodes[node]['pos'] for node in self.tree.nodes()])
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(positions)
        for node, label in zip(self.tree.nodes(), labels):
            self.tree.nodes[node]['cluster'] = label

    def draw_tree(self, select_mode=False):
        # Draw edges with variable thickness
        max_weight = max([data['weight'] for _, _, data in self.tree.edges(data=True)])
        glBegin(GL_LINES)
        for edge in self.tree.edges(data=True):
            node1, node2, data = edge
            pos1 = self.tree.nodes[node1]['pos']
            pos2 = self.tree.nodes[node2]['pos']
            weight = data['weight']
            normalized_weight = (weight / max_weight)
            glLineWidth(1 + normalized_weight * 5)  # Adjust max thickness
            glColor3f(0.0, 0.0, 1.0 - normalized_weight)  # Blue to light blue
            glVertex3f(*pos1)
            glVertex3f(*pos2)
        glEnd()

        # Calculate visible nodes based on distance and LOD threshold
        for idx, node in enumerate(self.tree.nodes()):
            pos = self.tree.nodes[node]['pos']
            distance = np.linalg.norm([pos[0] - self.camera_pos[0],
                                       pos[1] - self.camera_pos[1],
                                       pos[2] - self.camera_pos[2]])
            if distance < self.lod_threshold:
                if select_mode:
                    glLoadName(idx + 1)
                    self.node_id_map[idx + 1] = node
                else:
                    # Assign color based on node attribute
                    attr = self.tree.nodes[node].get('attribute', 'default')
                    glColor3f(*self.get_color_for_attribute(attr))
                self.draw_node(pos)

        # Draw highlighted node
        if hasattr(self, 'highlighted_node') and self.highlighted_node and not select_mode:
            pos = self.tree.nodes[self.highlighted_node]['pos']
            glColor3f(1.0, 1.0, 0.0)  # Highlight color (yellow)
            self.draw_node(pos)

    def draw_node(self, pos):
        glPushMatrix()
        glTranslatef(*pos)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.settings['visualization_params']['node_size'] * 0.1, 16, 16)
        gluDeleteQuadric(quadric)
        glPopMatrix()

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
        self.draw_background()
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
        if event.button() == Qt.RightButton:
            x = event.x()
            y = self.height() - event.y()
            node_name = self.pick_node(x, y)
            if node_name:
                self.show_context_menu(event.globalPos(), node_name)
        else:
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
        self.highlight_node(event.x(), event.y())

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
        # Node picking using OpenGL selection mode with selection radius
        buffer_size = 512
        select_buffer = glSelectBuffer(buffer_size)
        glRenderMode(GL_SELECT)
        glInitNames()
        glPushName(0)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        viewport = glGetIntegerv(GL_VIEWPORT)
        gluPickMatrix(x, y, self.selection_radius, self.selection_radius, viewport)
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

    def animate_to(self, target_zoom=None, target_rotation=None):
        # Store the target values
        self.target_zoom = target_zoom if target_zoom is not None else self.zoom
        self.target_rotation = target_rotation if target_rotation is not None else self.rotation.copy()
        self.animation_step = 0
        self.total_steps = 60  # Adjust for animation speed
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # Approximately 60 FPS

    def update_animation(self):
        if self.animation_step < self.total_steps:
            t = self.animation_step / self.total_steps
            # Easing function (smoothstep)
            t = t * t * (3 - 2 * t)
            # Interpolate zoom
            self.zoom += (self.target_zoom - self.zoom) * t
            # Interpolate rotation
            self.rotation = [
                self.rotation[i] + (self.target_rotation[i] - self.rotation[i]) * t
                for i in range(3)
            ]
            self.animation_step += 1
            self.update()
        else:
            self.timer.stop()

    def draw_background(self):
        glDisable(GL_DEPTH_TEST)
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.3, 0.5)  # Top color
        glVertex2f(-1.0, 1.0)
        glVertex2f(1.0, 1.0)
        glColor3f(0.8, 0.9, 1.0)  # Bottom color
        glVertex2f(1.0, -1.0)
        glVertex2f(-1.0, -1.0)
        glEnd()
        glEnable(GL_DEPTH_TEST)

    def highlight_node(self, x, y):
        node_name = self.pick_node(x, self.height() - y)
        if node_name != getattr(self, 'highlighted_node', None):
            self.highlighted_node = node_name
            self.update()

    def show_context_menu(self, position, node_name):
        menu = QtWidgets.QMenu()
        zoom_action = menu.addAction("Zoom to Node")
        details_action = menu.addAction("Show Details")
        self.add_context_menu_actions(menu, node_name)
        action = menu.exec_(position)
        if action == zoom_action:
            self.zoom_to_node(node_name)
        elif action == details_action:
            self.show_node_info(node_name)

    def zoom_to_node(self, node_name):
        # Smoothly animate zooming to the selected node
        target_pos = self.tree.nodes[node_name]['pos']
        # Compute required transformations to center and zoom in on the node
        # Implement similar to animate_to method
        # Example:
        # self.animate_to(target_zoom=desired_zoom_level, target_rotation=desired_rotation)

    def save_screenshot(self, filename):
        width = self.width()
        height = self.height()
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = QtGui.QImage(data, width, height, QtGui.QImage.Format_RGBA8888)
        image = image.mirrored(False, True)  # Flip vertically
        image.save(filename)

    def update_lod_threshold(self, value):
        self.lod_threshold = value
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.update_zoom(5)
        elif event.key() == Qt.Key_Minus:
            self.update_zoom(-5)
        elif event.key() == Qt.Key_R:
            self.reset_view()
        elif event.key() == Qt.Key_Left:
            self.update_rotation(1, -5)
        elif event.key() == Qt.Key_Right:
            self.update_rotation(1, 5)
        elif event.key() == Qt.Key_Up:
            self.update_rotation(0, -5)
        elif event.key() == Qt.Key_Down:
            self.update_rotation(0, 5)
        self.update()

    def reset_view(self):
        self.zoom = -100
        self.rotation = [0, 0, 0]
        self.pan = [0, 0]
        self.update()

    def annotate_node(self, node_name, annotation):
        # Add an annotation to a node and display it
        if 'annotations' not in self.tree.nodes[node_name]:
            self.tree.nodes[node_name]['annotations'] = []
        self.tree.nodes[node_name]['annotations'].append(annotation)
        info = f"Annotated Node: {node_name}\nAnnotation: {annotation}"
        QtWidgets.QMessageBox.information(self, "Node Annotation", info)
        self.update()

    def delete_node(self, node_name):
        # Remove a node from the tree
        if node_name in self.tree.nodes:
            self.tree.remove_node(node_name)
            self.create_vbo()
            self.update()

    def add_context_menu_actions(self, menu, node_name):
        annotate_action = menu.addAction("Add Annotation")
        delete_action = menu.addAction("Delete Node")
        action = menu.exec_(QtGui.QCursor.pos())
        if action == annotate_action:
            annotation, ok = QtWidgets.QInputDialog.getText(self, "Add Annotation", f"Enter annotation for node {node_name}:")
            if ok and annotation:
                self.annotate_node(node_name, annotation)
        elif action == delete_action:
            self.delete_node(node_name)