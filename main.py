import os
import time
import json
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


# Setting browser driver and data
def setBrowser():
    options = Options()
    dataDir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
    options.add_argument(f"--user-data-dir={dataDir}")
    options.add_argument("--profile-directory=Default")
    return webdriver.Chrome(options=options)
# Data management
def dataManagement(file, date, status=None):
    try:
        with open(file, "r") as f:
            dateData = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dateData = {}
    if status is None:
        if date in dateData:
            print("qns solved . . .")
            return None
        return dateData
    dateData[date] = status
    with open(file, "w") as f:
        json.dump(dateData, f, indent=4)
    return None
# main script . . .
def main():
    file = "leetcodeStreak.json"
    date = datetime.date.today().isoformat()
    dateData = dataManagement(file, date)
    if dateData is None:
        return
    driver = setBrowser()
    try:
        # setting the link
        driver.get("https://leetcode.com/problemset/")
        # waiting to load the qns pannel
        WebDriverWait(driver, 60).until(
            ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]"))
        )
        #navigate to the problem of the day
        while True:
            try:
                # Construct the dynamic XPath
                xpath = f"/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]/a[{datetime.date.today().day}]"
                qnsTab = WebDriverWait(driver, 60).until(
                    ec.element_to_be_clickable((By.XPATH, xpath))
                )
                qnsTab.click()
                break  
            except Exception as e:
                print(f"Retrying on qns of the day, Error: {e}")
        # switiching the tab, controll given to new tab . . .
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        # opening editorial section . . .
        while True:
            try:
                editorialSec = WebDriverWait(driver,20).until(
                    ec.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[1]/div[1]/div[1]/div/div[3]/div"))
                )
                editorialSec.click()
                driver.execute_script("arguments[0].scrollIntoView(true);", editorialSec)
                break
            except Exception as e:
                print(e) 
        # getting playground link . . .
        retries = 5
        content = ""
        while retries > 0:
            try:
                solDiv = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[5]/div/div[2]/div/div[1]/div/div'))
                )
                content = driver.execute_script("return arguments[0].innerHTML;", solDiv)
                if content.strip():  # Break if non-empty content is retrieved
                    break
            except Exception as e:
                retries -= 1
                time.sleep(2)
        # getting list of all solutions . . .
        soup = BeautifulSoup(content, "html.parser")
        iFrames = soup.find_all("iframe")
        iFrame = []
        for i, iframe in enumerate(iFrames, 1):
            src = iframe.get("src", "No src attribute found")
            iFrame.append(src)
        # opening playground to copy code . . .
        driver.get(iFrame[0])
        copyBtn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/button"))
        )
        copyBtn.click()
        driver.back() # back to the qns of the day tab . . .
        # for selecting the writing section . . .
        writerDiv = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[5]"))
        )
        writerDiv.click()
        driver.implicitly_wait(2)
        # pasting the copied code . . .
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        # submit the code . . .
        submit = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div[3]/div/button"))
        )
        submit.click()
        #saving the data . . .
        dataManagement(file, date, "solved")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        time.sleep(30)
        driver.quit()
if __name__ == "__main__":
    main()
