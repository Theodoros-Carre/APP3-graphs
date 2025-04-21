# Social Network Analysis

This project analyzes social networks represented as directed or undirected graphs. It reads interaction data from CSV files and computes key insights like top leaders, most active followers, and shortest paths between nodes. It also visualizes the graph, highlighting the most influential individuals.

## ✅ Features

- **Graph construction** from CSV files (directed or undirected)
- **Adjacency matrix generation** and export
- **Leader detection** (most followed nodes)
- **Follower discovery** per leader
- **Top followers** detection (most outgoing links)
- **Shortest path** computation between top leaders
- **Graph visualization** with color-coded leaders and improved layout

## 🧰 Installation

Before running the app, install the required Python packages:

```bash
pip install numpy matplotlib networkx pyqt5
```

## 🚀 How to Run

```bash
python APP3_final.py
```

The GUI will launch automatically.

## 📋 How to Use the App

### 1. Select Your File
- Choose file type (`CSV` or `TXT`)
- Click **“Select File”**
- Pick your dataset file (e.g., `students.csv`, `club.txt`)

### 2. Choose Graph Settings
- Select graph type:
  - `Directed Graph`: arrows have direction (e.g., Twitter)
  - `Undirected Graph`: mutual links (e.g., Facebook)
- Set:
  - Number of **leaders**
  - Number of **best followers**

### 3. Run the Analysis
- Click **“Run Analysis”**
- View results in the right panel:
  - Leaders and their followers
  - Best followers
  - Shortest path (if it exists)

### 4. Save the Adjacency Matrix (Optional)
- Click **“Save Matrix”**
- Choose file format (`.txt` or `.csv`)

## 📊 Graph Visualization

- Red nodes = Leaders
- Sky blue nodes = Regular members
- Green = Shortest path (if found)
- Layout auto-adjusts for readability
- Warning appears if graph is too large to visualize (> 1000 nodes)

## 📥 Input Format

Your input file (CSV or TXT) should contain edges in the form:

```
id1,id2
0,1
1,2
3,4
...
```

- Each line represents an edge
- Headers like `id1,id2` are automatically ignored
- Nodes should be integers

## 🙌 Author

- CARRE Theodoros, JEYANESHAN Dacshayan, TANTER Thibaud, VUKOVIC Luka 
- Advanced Algorithms 3 | Social Network Project  
- ESME
