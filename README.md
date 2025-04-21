# Social Network Analysis

This project analyzes social networks represented as directed or undirected graphs. It reads interaction data from CSV files and computes key insights like top leaders, most active followers, and shortest paths between nodes. It also visualizes the graph, highlighting the most influential individuals.

## 📁 Project Files

- `students.csv`, `club.txt`, `anybeatAnonymized.csv`, etc. — input data files representing social networks.
- `network_analysis.py` — main Python script (your code).
- `adjacency_matrix.txt` — output adjacency matrix (saved after analysis).
- Generated graph visualization — shown using `matplotlib`.

## ✅ Features

- **Graph construction** from CSV files (directed or undirected)
- **Adjacency matrix generation** and export
- **Leader detection** (most followed nodes)
- **Follower discovery** per leader
- **Top followers** detection (most outgoing links)
- **Shortest path** computation between top leaders
- **Graph visualization** with color-coded leaders and improved layout

## 🧠 How It Works

1. Load a CSV file of edges (e.g., `students.csv`)
2. Build the graph and adjacency matrix
3. Detect leaders based on incoming connections
4. Detect best followers based on outgoing connections
5. Compute shortest path between top 2 leaders
6. Visualize the graph with:
   - Red nodes = leaders
   - Blue nodes = others
   - Arrows (if directed)

## 🔧 Configuration

Inside the script, you can configure:

```python
filename = 'students.csv'         # File to analyze
directed = False                  # True = directed graph, False = undirected
top_n_leaders = 3                 # Number of top leaders to identify
top_n_followers = 5               # Number of best followers to find
```

## 📊 Visualization

The graph is visualized using `networkx` and `matplotlib`. Leaders appear in red, other nodes in sky blue. Spacing is optimized with `spring_layout` using:

```python
pos = nx.spring_layout(G, k=0.5, iterations=100)
```

This improves readability, even for more complex networks.

## 📦 Dependencies

Make sure to install:

```bash
pip install numpy matplotlib networkx
```

Optionally, for large graphs:

```bash
pip install scipy
```

## 🏁 Running the Script

```bash
python network_analysis.py
```

The script will print:
- Top leaders and their followers
- Best followers
- Shortest path between top leaders
- It will also display a graph window

## 📥 Input File Format

The CSV should contain two columns with node IDs (integers):

```
id1,id2
0,1
1,2
3,2
...
```

Header is optional — if present, it will be ignored.

## 📌 Notes

- The adjacency matrix is saved to `adjacency_matrix.txt`
- The graph visualization is shown in a pop-up window
- Directed graphs show arrows, undirected graphs use two-way connections

## 👨‍🎓 Final Thoughts

This project meets the full requirements of a social network analysis assignment using core algorithms and graph theory. It’s modular, readable, and easily extendable. 🎉
