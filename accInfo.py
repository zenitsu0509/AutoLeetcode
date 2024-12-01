import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setting up the browser with Selenium
def setBrowser():
    options = Options()
    dataDir = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data")
    options.add_argument(f"--user-data-dir={dataDir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")  # Disable GPU (recommended in headless mode)
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Edge(options=options)

# Initialize the browser driver
driver = setBrowser()
driver.get("https://leetcode.com/u/vaibhav_pandey_2005/")  # Target URL
print("Started fetching content...")

# Ensure page is fully loaded by scrolling
time.sleep(3)  # Wait for initial content to load
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Allow time for additional lazy-loaded content to load
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(3)
# Try to locate the desired div and extract its HTML
content = ""
try:
    infoCard = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[4]/div/div[2]/div[1]/div[1]/div/div/div[2]"))
    )
    # Extract the HTML content of the targeted div
    content = driver.execute_script("return arguments[0].innerHTML;", infoCard)
    print("Content fetched successfully!")
except Exception as e:
    print(f"Error: {e}")
    print("Printing page source for debugging...")
    # print(driver.page_source)  # Debugging: Print the full page HTML

# Save the full content to an output file for review
if content:
    soup = BeautifulSoup(content, 'html.parser')
else:
    print("Failed to fetch the full content.")

soup = BeautifulSoup(soup, 'html.parser')

# Find all relevant divs
difficulty_data = []
divs = soup.find_all('div', class_='rounded-sd-sm')

for div in divs:
    # Extract difficulty level
    difficulty = div.find('div', class_='text-xs font-medium').get_text(strip=True)
    # Extract the score (e.g., "28/839")
    score = div.find('div', class_='text-sd-foreground').get_text(strip=True)
    # Append as nested list
    difficulty_data.append([difficulty, score])

# Print the nested list
print(difficulty_data)


driver.quit()
