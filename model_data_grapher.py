import csv
import networkx as nx
import matplotlib.pyplot as plt

# CSV file paths
DATASETS_CSV = "database/datasets.csv"
MODELS_CSV = "database/models.csv"
EDGES_CSV = "database/edges.csv"


def load_all():
    datasets = {}
    with open(DATASETS_CSV, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            datasets[row[0]] = row[1]  # dataset_id -> name
    edges = []
    with open(EDGES_CSV, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            edges.append((row[0], row[1], row[2]))  # (start_node, end_node, relationship)
    models = {}
    with open(MODELS_CSV, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            models[row[0]] = row[1]  # model_id -> name
    return datasets, edges, models


# Build and visualize the graph
def visualize_graph():
    datasets, edges, models = load_all()

    G = nx.DiGraph()

    # Add dataset nodes
    for dataset_id, name in datasets.items():
        G.add_node(dataset_id, label=name, type="dataset")

    # Add model nodes
    for model_id, name in models.items():
        G.add_node(model_id, label=name, type="model")

    # Add edges
    for start, end, relationship in edges:
        G.add_edge(start, end, label=relationship)

    # Draw the graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42, k=0.7)

    # Define node colors
    node_colors = ["lightblue" if G.nodes[n]["type"] == "dataset" else "lightcoral" for n in G.nodes]

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, "label"), node_color=node_colors,
            edge_color="gray", node_size=2000, font_size=10, font_weight="bold", arrowsize=12)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="black")

    plt.title("Dataset-Model Relationship Graph")
    plt.show()


# Run visualization
if __name__ == "__main__":
    visualize_graph()
