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

# Predefined dataset library
DATASET_LIBRARY = {
    "1": {"name": "ImageNet", "creator": "Stanford", "license": "CC BY 4.0"},
    "2": {"name": "COCO", "creator": "Microsoft", "license": "CC BY 4.0"},
    "3": {"name": "MNIST", "creator": "Yann LeCun", "license": "Open Access"},
    "4": {"name": "CIFAR-10", "creator": "Krizhevsky", "license": "MIT"},
    "5": {"name": "OpenImages", "creator": "Google", "license": "CC BY 4.0"}
}


# Ensure CSV files exist
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


# Select datasets
def select_datasets():
    print("Available Datasets:")
    for key, details in DATASET_LIBRARY.items():
        print(f"{key}: {details['name']} (Creator: {details['creator']}, License: {details['license']})")

    selected = input("Enter dataset numbers (comma-separated): ").split(",")
    selected_datasets = {key: DATASET_LIBRARY[key] for key in selected if key in DATASET_LIBRARY}

    return selected_datasets


# Create a mock model
def create_model(selected_datasets):
    model_id = str(uuid.uuid4())[:8]
    model_name = input("Enter model name: ")
    model_params = input("Enter model parameters (e.g., 'LR=0.01, Epochs=10'): ")
    trained_on = ", ".join([d["name"] for d in selected_datasets.values()])
    timestamp = datetime.now().isoformat()

    return {
        "model_id": model_id,
        "name": model_name,
        "params": model_params,
        "trained_on": trained_on,
        "timestamp": timestamp
    }


# Append to CSV files
def append_to_csv(filename, row):
    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


# Save the new model and relationships
def save_model_and_edges(model, selected_datasets):
    # Append model to models.csv
    append_to_csv(MODELS_CSV,
                  [model["model_id"], model["name"], model["params"], model["trained_on"], model["timestamp"]])

    # Append edges to edges.csv
    for dataset_id in selected_datasets.keys():
        append_to_csv(EDGES_CSV, [dataset_id, model["model_id"], "Used for training"])


# Main function
def main():
    initialize_csv()
    selected_datasets = select_datasets()
    if not selected_datasets:
        print("No valid datasets selected. Exiting.")
        return

    model = create_model(selected_datasets)
    save_model_and_edges(model, selected_datasets)

    print(f"\nModel '{model['name']}' added with ID: {model['model_id']}")
    print("Model has been linked to the selected datasets.\n")


if __name__ == "__main__":
    main()
