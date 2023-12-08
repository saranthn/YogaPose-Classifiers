# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get('https://www.nasa.gov')

# headlines = driver.find_element("name", "headline")
# for headline in headlines:
#     print(headline.text.strip())
# driver.close()

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def download_image(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print('File saved to', destination)
    except requests.exceptions.RequestException as e:
        print('Error downloading image:', e)

def google_search_and_save_images(search):
    print(f'Searching images for: {search}')

    query = f'yoga {search} pose'
    url = f'https://www.google.com/search?q={quote_plus(query)}&tbm=isch'
    print(url)

    driver = webdriver.Chrome()  # You need to have ChromeDriver installed
    driver.get(url)

    # Simulate scrolling to load more results
    for _ in range(5):  # Adjust the number of scrolls as needed
        driver.find_element('tag name', 'body').send_keys(Keys.END)
        time.sleep(2)  # Adjust the sleep duration as needed

    # Get the updated page source after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    image_results = soup.find_all('img')

    print(f'Image result count: {len(image_results)}')

    if len(image_results) > 0:
        # Create directory folder for the current search term
        root_dir = './poses'
        search_dir = f'{root_dir}/{search}'
        train_dir = f'{search_dir}/train'

        os.makedirs(root_dir, exist_ok=True)
        os.makedirs(search_dir, exist_ok=True)
        os.makedirs(train_dir, exist_ok=True)

        count = 0

        # Save image results
        for image_result in image_results:
            if 'class' in image_result.attrs:
                img_class = image_result['class']
                # print(img_class)
                if len(img_class) == 2:
                    if image_result.get('src'):
                        dest_dir = train_dir
                        img_url = image_result['src']
                        destination = f'./{dest_dir}/{count}.png'

                        download_image(img_url, destination)

                        count += 1
    else:
        print("Couldn't find image results!")

if __name__ == "__main__":
    # Yoga pose search term list
    search_term_list = ["tree", "warrior 2", "mountain", "plank", "down dog"]
    # search_term_list = ["down dog"]

    # Loop through search terms
    for term in search_term_list:
        google_search_and_save_images(term)
