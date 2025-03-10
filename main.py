import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
import time

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scroll_down(driver, scroll_pause_time=2, scroll_limit=5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(scroll_limit):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_all_images(driver):
    try:
        images = driver.find_elements(By.TAG_NAME, 'img')
        image_urls = []
        for img in images:
            image_url = img.get_attribute('src') or img.get_attribute('data-src')
            if image_url and "data:image/gif" not in image_url:
                width = int(img.get_attribute('width') or 0)
                height = int(img.get_attribute('height') or 0)
                if width >= 100 and height >= 100:
                    image_urls.append(image_url)
        return image_urls
    except Exception as e:
        print(f"Error scraping images: {e}")
        return []

def save_image(image_url, folder_name, file_name, retry_count=3):
    try:
        file_path =os.path.join(folder_name, f"{file_name}.jpg")

        if image_url.startswith('data:image/'):
            header, encoded = image_url.split(',', 1)
            image_data = base64.b64decode(encoded)
            with open(file_path, 'wb') as f:
                f.write(image_data)

        else:
            for attempt in range(retry_count):
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    break
                else:
                    print(f"Failed attempt {attempt+1} for image: {image_url}")
                    time.sleep(2)
    except Exception as e:
        print(f"Error saving image {file_name}: {e}")

def scrape_and_save_images(base_folder, search_term, index, num_images=10):
    folder_path = os.path.join(base_folder, '_'.join(search_term.split()))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    driver = create_driver()
    driver.get(f"https://www.google.com/search?q={search_term}&tbm=isch")
    time.sleep(5)
    scroll_down(driver)
    image_urls = scrape_all_images(driver)
    image_urls = image_urls[:num_images]
    for index, image_url in enumerate(image_urls, start=1):
        file_name = f'{search_term}_{index}'
        save_image(image_url, folder_path, f"{'_'.join(search_term.split())}_{index}")
    print(f"Finished scraping")
    driver.quit()

if __name__ == "__main__":
    base_folder = r"/home/bs2021/e2546794/Desktop/image-scraper/photos"
    persian_foods = [
    "Kebab", 
    "Fesenjan", 
    "Ghormeh Sabzi", 
    "Tahdig", 
    "Khoresht-e Bademjan", 
    "Ash Reshteh", 
    "Kuku Sabzi", 
    "Zereshk Polo", 
    "Joojeh Kebab", 
    "Dolmeh", 
    "Baghali Polo", 
    "Shirin Polow", 
    "Sabzi Khordan", 
    "Abgoosht", 
    "Sabzi Polo", 
    "Gheymeh", 
    "Beryani", 
    "Tahchin", 
    "Kashk-e Bademjan", 
    "Eshkeneh", 
    "Kebab Tabei", 
    "Abdoogh Khiar", 
    "Saffron Ice Cream", 
    "Nan-e Barbari", 
    "Faloodeh", 
    "Sambusa", 
    "Saffron Rice with Raisins", 
    "Khoresht Gheymeh", 
    "Shirin Kebab", 
    "Kalam Polo", 
    "Mast-o-Khiar"
]
    for i in range(len(persian_foods)):
        scrape_and_save_images(base_folder, persian_foods[i], i, num_images=300)