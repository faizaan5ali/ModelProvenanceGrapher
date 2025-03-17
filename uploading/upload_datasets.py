import csv
import os
import uuid  # Generate unique dataset IDs

# Path to datasets CSV file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up one level
DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATASETS_CSV = os.path.join(DATABASE_DIR, "datasets.csv")


# Ensure datasets.csv exists
def initialize_csv():
    if not os.path.exists(DATASETS_CSV):
        with open(DATASETS_CSV, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["dataset_id", "name", "creator", "license"])


# Append a dataset to the CSV
def append_dataset(dataset_id, name, creator, license_type):
    with open(DATASETS_CSV, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([dataset_id, name, creator, license_type])


# Main function for dataset upload
def upload_datasets():
    initialize_csv()

    while True:
        print("\nEnter dataset details")
        name = input("Dataset Name: ").strip()
        creator = input("Creator: ").strip()
        license_type = input("License: ").strip()

        dataset_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
        append_dataset(dataset_id, name, creator, license_type)

        print(f"Dataset '{name}' added successfully with ID: {dataset_id}")

        cont = input("Do you want to add another dataset? (y/n): ").strip().lower()
        if cont != "y":
            break


if __name__ == "__main__":
    upload_datasets()
