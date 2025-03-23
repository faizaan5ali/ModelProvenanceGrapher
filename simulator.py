import csv
import os
import uuid
import random
from datetime import datetime

# Paths to CSV files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current script directory
DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATASETS_CSV = os.path.join(DATABASE_DIR, "datasets.csv")
MODELS_CSV = os.path.join(DATABASE_DIR, "models.csv")
EDGES_CSV = os.path.join(DATABASE_DIR, "edges.csv")

NUM_MODELS = 10  # Number of random models to generate


# Ensure CSV files exist
def initialize_csv():
    for file, headers in [
        (MODELS_CSV, ["model_id", "name", "params", "accuracy", "timestamp"]),
        (EDGES_CSV, ["dataset_id", "model_id", "relationship"])
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)


# Load datasets
def load_datasets():
    datasets = {}
    if not os.path.exists(DATASETS_CSV):
        print("No datasets found. Please add datasets first.")
        return datasets

    with open(DATASETS_CSV, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            datasets[row[0]] = row[1]  # dataset_id -> dataset_name

    return datasets


# Generate a random model
def generate_model(dataset_id):
    model_id = str(uuid.uuid4())[:8]
    model_name = f"Model_{random.randint(1000, 9999)}"
    model_params = f"LR={random.uniform(0.001, 0.1):.3f}, Epochs={random.randint(5, 50)}"
    accuracy = round(random.uniform(0.70, 0.99), 3)  # Accuracy between 70% and 99%
    timestamp = datetime.now().isoformat()

    return {
        "model_id": model_id,
        "name": model_name,
        "params": model_params,
        "accuracy": accuracy,
        "timestamp": timestamp,
        "dataset_id": dataset_id
    }


# Save a model and its relationship to a dataset
def save_model_and_edge(model):
    with open(MODELS_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([model["model_id"], model["name"], model["params"], model["accuracy"], model["timestamp"]])

    with open(EDGES_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([model["dataset_id"], model["model_id"], "trained_on"])


# Compute dataset statistics
def compute_dataset_statistics():
    datasets = load_datasets()
    models = {}
    dataset_accuracies = {}

    # Load models
    if os.path.exists(MODELS_CSV):
        with open(MODELS_CSV, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                models[row[0]] = {"name": row[1], "accuracy": float(row[3])}

    # Compute dataset-model relationships
    if os.path.exists(EDGES_CSV):
        with open(EDGES_CSV, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                dataset_id, model_id, relationship = row
                if relationship == "trained_on" and model_id in models:
                    accuracy = models[model_id]["accuracy"]
                    dataset_accuracies.setdefault(dataset_id, []).append(accuracy)

    # Compute average accuracies per dataset
    dataset_avg_accuracies = {
        datasets[d_id]: round(sum(acc_list) / len(acc_list), 3)
        for d_id, acc_list in dataset_accuracies.items()
    }

    return dataset_avg_accuracies


# Find best models
def get_best_models(top_n=3):
    best_models = []
    if os.path.exists(MODELS_CSV):
        with open(MODELS_CSV, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            best_models = sorted(reader, key=lambda row: float(row[3]), reverse=True)[:top_n]

    return best_models


# Run the simulation
def main():
    initialize_csv()
    datasets = load_datasets()
    if not datasets:
        print("No datasets available")
        return

    dataset_ids = list(datasets.keys())

    print(f"\nGenerating {NUM_MODELS} random models...\n")

    for _ in range(NUM_MODELS):
        dataset_id = random.choice(dataset_ids)  # Assign a model to a random dataset
        model = generate_model(dataset_id)
        save_model_and_edge(model)

    print("\nSimulation completed. Models and relationships saved.")

    # Display statistics
    print("\nTop Performing Models:")
    for model in get_best_models():
        print(f"  - {model[1]} (Accuracy: {model[3]})")

    print("\nAverage Accuracy per Dataset:")
    dataset_avg_accuracies = compute_dataset_statistics()
    for dataset, avg_acc in dataset_avg_accuracies.items():
        print(f"  - {dataset}: {avg_acc}")


if __name__ == "__main__":
    main()
