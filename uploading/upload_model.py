import csv
import os
import uuid
from datetime import datetime

# Paths to CSV files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up one level
DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATASETS_CSV = os.path.join(DATABASE_DIR, "datasets.csv")
MODELS_CSV = os.path.join(DATABASE_DIR, "models.csv")
EDGES_CSV = os.path.join(DATABASE_DIR, "edges.csv")


# Ensure CSV files exist
def initialize_csv():
    for file, headers in [
        (MODELS_CSV, ["model_id", "name", "params", "trained_on", "timestamp"]),
        (EDGES_CSV, ["start_node", "end_node", "relationship"])
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)


# Load datasets from the CSV
def load_datasets():
    datasets = {}
    if not os.path.exists(DATASETS_CSV):
        print("No datasets found. Please upload datasets first.")
        return datasets

    with open(DATASETS_CSV, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            datasets[row[0]] = {"name": row[1], "creator": row[2], "license": row[3]}

    return datasets


# Select datasets for training
def select_datasets(datasets):
    print("Available Datasets for Training:")
    for key, details in datasets.items():
        print(f"{key}: {details['name']} (Creator: {details['creator']}, License: {details['license']})")

    selected = input("Enter dataset numbers to use for training (comma-separated): ").split(",")
    return {key: datasets[key] for key in selected if key in datasets}


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


# Main function for model creation
def main():
    initialize_csv()
    datasets = load_datasets()
    if not datasets:
        return

    selected_datasets = select_datasets(datasets)
    if not selected_datasets:
        print("No valid datasets selected. Exiting.")
        return

    model = create_model(selected_datasets)
    save_model_and_edges(model, selected_datasets)

    print(f"\nModel '{model['name']}' added with ID: {model['model_id']}")
    print("Model has been linked to the selected datasets:")
    print(f"\t", end="")
    for dataset in selected_datasets.values():
        print(dataset["name"], end=" ")
    print()


if __name__ == "__main__":
    main()
