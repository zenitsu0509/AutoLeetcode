from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time, os, json
from bs4 import BeautifulSoup

file = "date.json"
date = datetime.date.today().isoformat()
chromeCred = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"



with open(file, "a+") as f:
    f.seek(0)
    time.sleep(10)
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    if date not in data:
        # giving initial data to the browser driver . . .
        chromeOpt = Options()
        chromeOpt.add_argument(f"--user-data-dir={chromeCred}")
        chromeOpt.add_argument(f"--profile-directory=Default")

        try:

            # setting up browser driver . . .
            driver = webdriver.Chrome(options=chromeOpt)
            driver.get('https://leetcode.com/problemset/')

            # waiting for qns pannel to be open . . .
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]"))
            )

            # opening problem of the day . . .
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
                        print(f"Retrying due to: {e}")
            
            # switiching the tab controll to new tab . . .
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

            driver.back() # back to previous page . . .

            # for clearing the writing section . . .
            writerDiv = WebDriverWait(driver, 20).until(
                ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[5]"))
            )
            writerDiv.click()
            driver.implicitly_wait(2)
            # copy pasting the clipboard . . .
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            # submit the code . . .
            submit = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div[3]/div/button"))
            )
            submit.click()
            # saving the data to json file . . .
            data[date] = "solved"
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            time.sleep(30)
            driver.quit()
        except Exception as e:
            print(f"Error: {e}")

    else:
        print("qns already solved . . .")
