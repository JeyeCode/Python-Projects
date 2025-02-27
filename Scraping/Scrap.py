
#JEyCode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import requests

def download_image(img_url, folder_name, image_name):
    # Clean invalid filename characters
    image_name = "".join([c if c.isalnum() else "_" for c in image_name])
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Get file extension
    file_extension = img_url.split('.')[-1].split('?')[0]
    valid_extensions = ['png', 'jpg', 'jpeg', 'svg', 'gif', 'webp']
    if file_extension.lower() not in valid_extensions:
        file_extension = 'jpg'  # Default to jpg if extension is not recognized
    
    filename = f"{image_name}.{file_extension}"
    filepath = os.path.join(folder_name, filename)
    
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.get('https://www.digikala.com/product-list/plp_228477160/?sort=7&promo_name=%D9%BE%D8%A7%D8%B1%D8%AA%D9%86%D8%B1%D8%B4%DB%8C%D9%BE-%D8%B1%DB%8C+%D8%A8%D9%86&promo_position=home_middle&promo_creative=194139&bCode=194139/')  # Replace with the actual URL

# Function to scroll down and load more products
def scroll_to_load_products():
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()
    max_wait_time = 60  # Maximum time to wait for new products (in seconds)
    scroll_delay = 2  # Time to wait after each scroll (in seconds)
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)  # Wait for new products to load
        
        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # No more products to load
            # Check if we've waited long enough
            if time.time() - start_time > max_wait_time:
                print("No new products loaded for 1 minute. Stopping scroll.")
                break
        else:
            # Reset the timer if new products are loaded
            start_time = time.time()
            last_height = new_height

# Scroll to load all products
scroll_to_load_products()

# Wait for products to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-list_ProductList__pagesContainer__zAhrX")))
except Exception as e:
    print("Loading timeout:", e)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the parent container - CORRECTED SELECTOR
parent_container = soup.find('div', class_='product-list_ProductList__pagesContainer__zAhrX')

if not parent_container:
    print("Parent container not found!")
    driver.quit()
    exit()

# Find product containers inside the parent container
products = parent_container.find_all('div', class_='product-list_ProductList__item__LiiNI')

print(f"Found {len(products)} products")

# Add a delay between downloading images (optional)
download_delay = 1  # Time to wait between downloading images (in seconds)

for product in products:
    # Extract product name - CORRECTED SELECTOR
    name_element = product.find('h3', class_='styles_VerticalProductCard__productTitle__6zjjN')
    if name_element:
        product_name = name_element.text.strip()
        product_name = "".join([c if c.isalnum() else "_" for c in product_name])
    else:
        product_name = "Unnamed_Product"
    
    # Extract main image URL - CORRECTED SELECTOR
    img_tag = product.find('img')
    if img_tag:
        img_url = img_tag.get('src')
        if img_url:
            # Convert to absolute URL
            if not img_url.startswith(('http', 'https')):
                img_url = f'https:{img_url}'
            
            print(f"Product: {product_name}")
            print(f"Main Image URL: {img_url}")
            download_image(img_url, 'digikala_products', product_name)
            time.sleep(download_delay)  # Add delay between downloads
        else:
            print(f"No valid main image found for {product_name}")
    else:
        print(f"No main image tag found for {product_name}")
    
    # Extract additional image URLs from <picture> and <source> tags
    picture_tag = product.find('picture')
    if picture_tag:
        additional_images = picture_tag.find_all('source')
        for idx, source in enumerate(additional_images):
            img_url = source.get('srcset')
            if img_url:
                # Convert to absolute URL
                if not img_url.startswith(('http', 'https')):
                    img_url = f'https:{img_url}'
                
                print(f"Additional Image {idx + 1} URL: {img_url}")
                download_image(img_url, 'digikala_products', f"{product_name}_additional_{idx + 1}")
                time.sleep(download_delay)  # Add delay between downloads
            else:
                print(f"No valid additional image found for {product_name}")
    else:
        print(f"No <picture> tag found for {product_name}")
    
    # Extract price - CORRECTED SELECTOR
    price_element = product.find('span', {'data-testid': 'price-final'})
    if price_element:
        price = price_element.text.strip()
        print(f"Price: {price}")
    else:
        print("Price not found")
    
    # Extract discounted price (if available)
    discounted_price_element = product.find('span', class_='text-neutral-300 line-through self-end mr-auto text-body-2')
    if discounted_price_element:
        discounted_price = discounted_price_element.text.strip()
        print(f"Discounted Price: {discounted_price}")
    else:
        print("Discounted price not found")

driver.quit()

#END
