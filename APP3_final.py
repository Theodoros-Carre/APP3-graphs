import sys
import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFileDialog, QComboBox, QSpinBox, 
                             QGroupBox, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SocialNetworkAnalyzer(QMainWindow):
    """Main application window for social network analysis."""
    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        self.setWindowTitle("Social Network Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for controls
        control_panel = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        
        # File selection
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["CSV File", "Text File"])
        
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_file)
        
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setWordWrap(True)
        
        file_layout.addWidget(QLabel("File Type:"))
        file_layout.addWidget(self.file_type_combo)
        file_layout.addWidget(self.select_file_btn)
        file_layout.addWidget(self.file_path_label)
        file_group.setLayout(file_layout)
        
        # Parameters
        param_group = QGroupBox("Analysis Parameters")
        param_layout = QVBoxLayout()
        
        self.directed_combo = QComboBox()
        self.directed_combo.addItems(["Directed Graph", "Undirected Graph"])
        
        self.leaders_spin = QSpinBox()
        self.leaders_spin.setRange(1, 10)
        self.leaders_spin.setValue(3)
        
        self.followers_spin = QSpinBox()
        self.followers_spin.setRange(1, 10)
        self.followers_spin.setValue(5)
        
        param_layout.addWidget(QLabel("Graph Type:"))
        param_layout.addWidget(self.directed_combo)
        param_layout.addWidget(QLabel("Number of Leaders:"))
        param_layout.addWidget(self.leaders_spin)
        param_layout.addWidget(QLabel("Number of Best Followers:"))
        param_layout.addWidget(self.followers_spin)
        param_group.setLayout(param_layout)
        
        # Action buttons
        button_group = QGroupBox("Actions")
        button_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("Run Analysis")
        self.run_btn.clicked.connect(self.run_analysis)
        
        self.save_matrix_btn = QPushButton("Save Matrix")
        self.save_matrix_btn.clicked.connect(self.save_matrix)
        self.save_matrix_btn.setEnabled(False)  # Disabled until analysis is run
        
        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(self.save_matrix_btn)
        button_group.setLayout(button_layout)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        
        # Add widgets to control panel
        control_layout.addWidget(file_group)
        control_layout.addWidget(param_group)
        control_layout.addWidget(button_group)
        control_layout.addWidget(self.results_text)
        control_layout.addStretch()
        control_panel.setLayout(control_layout)
        
        # Right panel for graph visualization
        graph_panel = QGroupBox("Graph Visualization")
        graph_layout = QVBoxLayout()
        
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        
        # Add label for large graph warning
        self.graph_warning_label = QLabel()
        self.graph_warning_label.setWordWrap(True)
        self.graph_warning_label.setStyleSheet("color: red; font-weight: bold;")
        self.graph_warning_label.setAlignment(Qt.AlignCenter)
        
        graph_layout.addWidget(self.canvas)
        graph_layout.addWidget(self.graph_warning_label)
        graph_panel.setLayout(graph_layout)
        
        # Add panels to main layout
        main_layout.addWidget(control_panel, stretch=1)
        main_layout.addWidget(graph_panel, stretch=2)
        
        # Initialize variables
        self.file_path = ""
        self.nodes = []
        self.edges = []
        self.matrix = None
        self.MAX_NODES_FOR_VISUALIZATION = 1000  # Threshold for graph visualization
    
    def select_file(self):
        """Open a file dialog to select input data file (CSV or TXT)."""
        file_type = self.file_type_combo.currentText()
        if file_type == "CSV File":
            file_filter = "CSV Files (*.csv);;All Files (*)"
        else:
            file_filter = "Text Files (*.txt);;All Files (*)"
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(file_path)
    
    def read_csv_graph(self, filename, directed=True):
        """Read graph data from a CSV or text file."""
        edges = []
        nodes = set()
        try:
            with open(filename, 'r') as file:
                if filename.endswith('.csv') or filename.endswith('.txt'):
                    reader = csv.reader(file)
                
                for row in reader:
                    if not row or row[0].lower() == 'id1':
                        continue  # skip empty rows and headers
                    try:
                        u, v = int(row[0]), int(row[1]) 
                        edges.append((u, v))
                        nodes.update([u, v])
                        if not directed:
                            edges.append((v, u))
                    except ValueError:
                        print(f"Skipping invalid row: {row}")
            return list(nodes), edges
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")
            return [], []
    
    def create_adjacency_matrix(self, nodes, edges):
        """Create an adjacency matrix from nodes and edges."""
        size = max(nodes) + 1
        matrix = np.zeros((size, size), dtype=int)
        for u, v in edges:
            matrix[u][v] = 1
        return matrix
    
    def save_matrix(self):
        """Save the adjacency matrix to a file (CSV or TXT format)."""
        if self.matrix is None:
            QMessageBox.warning(self, "Warning", "No matrix to save. Please run analysis first.")
            return
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                 "Save Matrix File",
                                                 "adjacency_matrix.txt",
                                                 "Text Files (*.txt);;CSV Files (*.csv)",
                                                 options=options)
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    np.savetxt(file_path, self.matrix, fmt='%d', delimiter=',')
                else:
                    np.savetxt(file_path, self.matrix, fmt='%d')
                QMessageBox.information(self, "Success", f"Matrix saved successfully to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save matrix: {str(e)}")
    
    def find_leaders(self, matrix, directed=True, top_n=2):
        """Identify the most influential nodes (leaders) in the network.
            Directed Graphs: Counts how many nodes point to each node (column sums).
            Undirected Graphs: Counts connections per node (row sums, same as column sums)."""
        if directed:
            incoming = np.sum(matrix, axis=0)
        else:
            incoming = np.sum(matrix, axis=1)
        leaders = np.argsort(-incoming)[:top_n]
        return leaders.tolist(), incoming
    
    def find_followers(self, matrix, node, directed=True):
        """Find all followers of a specific node.
            Directed: Checks the node's column for 1s (who follows it).
            Undirected: Checks the node's row ( same as neighbors)"""
        if directed:
            return list(np.where(matrix[:, node] == 1)[0])
        else:
            return list(np.where(matrix[node, :] == 1)[0])
    
    def find_best_followers(self, matrix, top_n=2):
        """Identify nodes with the most outgoing connections.
            Counts how many nodes each node points to row sums"""
        outgoing = np.sum(matrix, axis=1)
        best_followers = np.argsort(-outgoing)[:top_n]
        return best_followers.tolist(), outgoing
    
    def bfs_shortest_path(self, matrix, start, goal):
        """Find shortest path between nodes using BFS"""
        if start == goal:
            return [start]
        
        visited = set()
        queue = deque([[start]])
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node not in visited:
                neighbors = np.where(matrix[node] == 1)[0]
                
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    
                    if neighbor == goal:
                        return new_path
                    
                    queue.append(new_path)
                
                visited.add(node)
        
        return None
    
    def draw_graph(self, nodes, edges, leaders, path=None):
        """Attempt to draw the graph, or show warning if too large"""
        self.figure.clear()
        self.graph_warning_label.clear()
        
        # Check if graph is too large for visualization
        if len(nodes) > self.MAX_NODES_FOR_VISUALIZATION:
            self.graph_warning_label.setText(
                f"Graph too large for visualization ({len(nodes)} nodes).\n"
                "Only showing textual results.\n"
                "Check terminal for complete output."
            )
            print("\nGraph too large for visualization. Showing textual results only.")
            print(f"Number of nodes: {len(nodes)}")
            print(f"Number of edges: {len(edges)}")
            return
        
        try:
            directed = self.directed_combo.currentIndex() == 0
            G = nx.DiGraph() if directed else nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            ax = self.figure.add_subplot(111)
            pos = nx.spring_layout(G, k=0.5, iterations=100)
            color_map = ['red' if node in leaders else 'skyblue' for node in G.nodes()]
            node_size = [800 if node in leaders else 300 for node in G.nodes()]

            nx.draw(G, pos, ax=ax, node_color=color_map, with_labels=True, 
                   node_size=node_size, arrowsize=10, font_size=8)
            
            # Only draw path if one exists
            if path and len(path) > 1:
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                      edge_color='green', width=2, ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=path,
                                     node_color='green', node_size=500, ax=ax)

            ax.set_title("Social Network Graph", fontsize=14)
            self.canvas.draw()
        except Exception as e:
            self.graph_warning_label.setText(
                f"Error visualizing graph: {str(e)}\n"
                "Showing textual results only.\n"
                "Check terminal for complete output."
            )
            print(f"\nError during graph visualization: {str(e)}")
    
    def run_analysis(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first")
            return
        
        try:
            directed = self.directed_combo.currentIndex() == 0
            top_n_leaders = self.leaders_spin.value()
            top_n_followers = self.followers_spin.value()
            
            # Read and process the graph
            self.nodes, self.edges = self.read_csv_graph(self.file_path, directed)
            if not self.nodes:
                QMessageBox.warning(self, "Warning", "No valid data found in the file")
                return
                
            self.matrix = self.create_adjacency_matrix(self.nodes, self.edges)
            self.save_matrix_btn.setEnabled(True)  # Enable save button after analysis
            
            # Find leaders and followers
            leaders, _ = self.find_leaders(self.matrix, directed, top_n_leaders)
            best_followers, _ = self.find_best_followers(self.matrix, top_n_followers)
            
            # Prepare results text
            results = []
            results.append(f"Analysis Results for {self.file_path}")
            results.append(f"Graph Type: {'Directed' if directed else 'Undirected'}")
            results.append(f"Number of nodes: {len(self.nodes)}")
            results.append(f"Number of edges: {len(self.edges)}")
            results.append("\nLeaders:")
            
            for i, leader in enumerate(leaders):
                followers = [int(f) for f in self.find_followers(self.matrix, leader, directed)]
                results.append(f"Leader {i+1} (node {leader}) followers: {followers}")
                print(f"Leader {i+1} (node {leader}) followers: {followers}")
            
            results.append("\nBest Followers:")
            results.append(f"{[int(bf) for bf in best_followers]}")
            print(f"Best Followers: {[int(bf) for bf in best_followers]}")
            
            # Find path between leaders if possible
            if len(leaders) >= 2:
                path = self.bfs_shortest_path(self.matrix, leaders[0], leaders[1])
                if path:
                    results.append(f"\nShortest path between leaders {leaders[0]} and {leaders[1]}:")
                    results.append(f"{[int(p) for p in path]}")
                    print(f"Shortest path between leaders {leaders[0]} and {leaders[1]}: {[int(p) for p in path]}")
                else:
                    results.append(f"\nNo path exists between leader {leaders[0]} and {leaders[1]}")
                    print(f"No path exists between leader {leaders[0]} and {leaders[1]}")
            else:
                results.append("\nNot enough leaders to find a path")
                print("Not enough leaders to find a path")
            
            self.results_text.setPlainText("\n".join(results))
            
            # Draw the graph (or show warning if too large)
            path_to_draw = None
            if len(leaders) >= 2:
                path_to_draw = self.bfs_shortest_path(self.matrix, leaders[0], leaders[1])
            self.draw_graph(self.nodes, self.edges, leaders, path_to_draw)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during analysis:\n{str(e)}")
            print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialNetworkAnalyzer()
    window.show()
    sys.exit(app.exec_())