import os
from datasets import Dataset, Features, ClassLabel, Image

def load_data(image_folder):
    data = {
        'image': [],
        'label': []
    }
    
    # Traverse through the folders (labels)
    for label in os.listdir(image_folder):
        label_folder = os.path.join(image_folder, label)
        if os.path.isdir(label_folder):
            print(f"Processing folder: {label_folder}")  # Debug print
            # Traverse through the images in the folder
            for image_name in os.listdir(label_folder):
                if image_name.endswith('.jpg'):
                    image_path = os.path.join(label_folder, image_name)
                    data['image'].append(image_path)
                    data['label'].append(label)
                    print(f"Added {image_name} to dataset")  # Debug print
    return data

def create_dataset():
    # Define the folder where the images are stored
    image_folder = r"/home/bs2021/e2546794/Desktop/image-scraper/persian_food_dataset"
    
    # Check if the folder exists
    if not os.path.exists(image_folder):
        print(f"Error: The folder {image_folder} does not exist.")
        return None

    # Load the data
    print("Loading data...")
    data = load_data(image_folder)
    
    # Check if data was loaded properly
    if not data['image'] or not data['label']:
        print("Error: No data found in the folder.")
        return None
    
    # Print the structure of the data to verify it's correct
    print(f"Data loaded: {len(data['image'])} images and {len(data['label'])} labels.")  # Debug print
    print("First 3 entries in the dataset:")
    print(f"Images: {data['image'][:3]}")
    print(f"Labels: {data['label'][:3]}")
    
    # Define dataset features
    features = Features({
        'image': Image(),
        'label': ClassLabel(names=os.listdir(image_folder))  # List class names (labels)
    })

    # Create the dataset
    print("Creating dataset...")
    dataset = Dataset.from_dict(data, features=features)

    return dataset

# Main execution
if __name__ == "__main__":
    dataset = create_dataset()
    
    if dataset:
        # Save the dataset to disk
        print("Saving dataset to disk...")
        dataset.save_to_disk(r"/home/bs2021/e2546794/Desktop/image-scraper/persian_food_dataset/dataset")
        print("Dataset saved successfully.")
    else:
        print("Dataset creation failed.")
