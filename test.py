
from datasets import load_from_disk

def test_loaded_dataset():
    dataset_path = r"/home/bs2021/e2546794/Desktop/image-scraper/persian_food_dataset/dataset"

    print("Loading dataset from disk...")
    dataset = load_from_disk(dataset_path)

    print(f"Dataset loaded: {dataset}")
    print(f"Number of samples in dataset: {len(dataset)}")

    print("First sample in dataset:")
    print(dataset[0])
    image = dataset[0]['image']
    image.show()



if __name__ == "__main__":
    test_loaded_dataset()
