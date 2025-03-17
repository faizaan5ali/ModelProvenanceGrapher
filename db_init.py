import csv
import os
import uuid
from datetime import datetime
import matplotlib
import networkx

# Paths to CSV files
DATASETS_CSV = "datasets.csv"
MODELS_CSV = "models.csv"
EDGES_CSV = "edges.csv"


def initialize_csv():
    for file, headers in [
        (DATASETS_CSV, ["dataset_id", "name", "creator", "license"]),
        (MODELS_CSV, ["model_id", "name", "params", "trained_on", "timestamp"]),
        (EDGES_CSV, ["start_node", "end_node", "relationship"])
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)