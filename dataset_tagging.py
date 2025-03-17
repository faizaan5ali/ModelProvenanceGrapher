import json
import hashlib
from datetime import datetime, timezone
import uuid

# Predefined licenses for selection, add more if necessary?
LICENSES = {
    "CC-BY": "Creative Commons Attribution",
    "CC-BY-SA": "Creative Commons Attribution-ShareAlike",
    "MIT": "MIT License",
    "GPL-3.0": "GNU General Public License v3.0",
    "Apache-2.0": "Apache License 2.0"
}


def generate_dataset_id(file_path):
    """Generate a unique ID based on file hash."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def create_metadata(dataset_path, title, author, description, license_key):
    """Create JSON-LD metadata for the dataset."""

    if license_key not in LICENSES:
        raise ValueError(f"Invalid license key. Choose from: {list(LICENSES.keys())}")

    dataset_id = generate_dataset_id(dataset_path)
    creation_date = datetime.now(timezone.utc).isoformat()

    metadata = {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "identifier": dataset_id,
        "name": title,
        "author": author,
        "dateCreated": creation_date,
        "description": description,
        "license": {
            "@type": "CreativeWork",
            "name": LICENSES[license_key],
            "url": f"https://opensource.org/licenses/{license_key}"
        },
        "sourceFile": dataset_path
    }

    # Save metadata as JSON-LD
    metadata_file = f"{uuid.uuid4()}_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Metadata saved to: {metadata_file}")
    return metadata_file


# Example Usage
if __name__ == "__main__":
    file_path = input("Enter dataset file path: ")
    title = input("Enter dataset title: ")
    author = input("Enter author's name: ")
    description = input("Enter dataset description: ")

    print("\nAvailable Licenses:")
    for key, value in LICENSES.items():
        print(f"- {key}: {value}")

    license_key = input("Choose a license (e.g., CC-BY, MIT, GPL-3.0): ").strip()

    try:
        metadata_file = create_metadata(file_path, title, author, description, license_key)
        print(f"Metadata successfully created and stored in {metadata_file}")
    except ValueError as e:
        print(f"❌ Error: {e}")
