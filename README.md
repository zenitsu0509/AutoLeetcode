# AutoLeetcode

This Python automation project helps you to complete your daily LeetCode challenges automatically and maintain your streak. The script utilizes `Selenium` for web automation and `BeautifulSoup` for scraping the necessary data. With this tool, you can easily stay on top of your daily practice and never miss a challenge!

![LeetCode Progress Image](https://preview.redd.it/what-ive-learned-from-7-months-of-leetcode-v0-od4xo623frzd1.png?width=834&format=png&auto=webp&s=49e4c3d1e11728f078d56f7f1e9af25ba6373b59)

# SETUP
## Cloning Repo
```bash
# clone the repo
git clone https://github.com/Its-Vaibhav-2005/AutoLeetcode.git
# change the directory
cd AutoLeetcode
# downloading the requirements
pip install -r requirements.txt
```
## Change BAT file
After cloning the repo apply these changes to `leetcode.bat` file
```leetcode.bat
@echo off
REM Execute Python script with unbuffered output
python -u "<path_to_the_scriptFolder>\main.py"
exit
```
after applying the changes paste the `BAT` file at 
`C:\Users\<YourUsername>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`.
Now the script is ready to run automatically when the system turns on.

# Code Explaination
## 1. **Overview**
This section explains the key components of the **AutoLeetcode** script. It provides a breakdown of the different functions and how they interact to automate the process of solving and submitting the "Question of the Day."
## 2. **Browser Setup**
Here as browser we have two options `Chrome` as deafault and `Edge` as secondary choice. Both browser proceeds with the browser information from the system.
### 2. **Chrome**
```pyhton
def chromeBrowser():
   options = Options()
   dataDir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
   options.add_argument(f"--user-data-dir={dataDir}")
   options.add_argument("--profile-directory=Default")
   return webdriver.Chrome(options=options)
```
### 1. **Edge** (Under development !!!)
```python
def edgeBrowser():
   options = Options.EdgeOptions()
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument("--no-sandbox")
   options.add_argument("--disable-gpu")
   # Enable verbose logging for debugging
   options.add_argument("--enable-logging")
   options.add_argument("--v=1")
   options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
   driver_path = r"<path_to>\msedgedriver.exe"
   return webdriver.Edge(executable_path=driver_path, options=options)
```
## 3. **Navigating to "Question of the Day"**
The script navigates to the "Question of the Day" page on LeetCode, by fetching the current date from users system
```python
xpath = f"/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]/a[{datetime.date.today().day}]"
qnsTab = WebDriverWait(driver, 60).until(
   ec.element_to_be_clickable((By.XPATH, xpath))
)
qnsTab.click()
```
## 4. **Solution**
As `Leetcode` provides the solution in 3 languages `(C++, Python3, Java)`, so we go with `C++` as default by accessing the leetcode-playground and copying the code.
```python
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
```
## 5. **Submit Code**
After getting everything it just simply copy paste the code 😂 most of us do it manually. So I just automated the task, so that everyone focus on devlopment part rather than wasting our some `minutes` on this. This script harldy took `40sec` to execute. While the script is doing it's work u can do yours.

# Information
## Features

- **Automates the "Question of the Day"**: Automatically solves and submits the problem of the day.
- **Maintains your streak**: Keeps track of your streak and ensures you don't miss any day.
- **Saves time**: No need to manually solve the questions; this bot handles everything for you.

## Prerequisites

Before you run this project, ensure you have the following installed:

- Python 3.x
- Chrome or Edge browser (depending on your configuration)
- ChromeDriver or MicrosoftedgeDriver (depending on the browser you are using)

### Python Libraries

To install the required Python libraries, run the following command:

- selenium
- beautifulsoup4

Additionally, you may need to install `webdriver-manager` for managing the browser drivers.

## Setup and Configuration

1. **Clone the repository** (or create your own script if you are building this from scratch).
   
2. **Set up your LeetCode account credentials**:  
   You will need to input your LeetCode username and password in the script to log in and automate the tasks. Make sure to handle sensitive data (e.g., credentials) securely.

3. **Configure the WebDriver**:
   - Ensure you have either ChromeDriver or GeckoDriver installed depending on the browser you're using.
   - You can specify the path to your driver, or use the `webdriver-manager` to automatically manage this.

## How to Use

### Running the Script

1. Navigate to the folder where your script is located.

2. Run the Python script to automate the completion of the "Question of the Day".

3. The script will:
   - Navigate to loged in leetcode account.
   - Automatically access the "Question of the Day."
   - Submit a solution present in "Editorial" section.
   - Maintain your streak by submitting the answer on time.

### Note:
- Ensure that you have your answers ready for the questions or modify the script to solve the problems programmatically. This automation currently helps with the submission process.

## How It Works

1. **Leetcode**: Browse to your leetcode account
2. **Navigate to the Question of the Day**: Using `Selenium`, the script opens the LeetCode page for the current day's problem.
3. **Solution Submission**: The script can either directly submit a pre-coded solution or use some predefined mechanism to automate the solution submission (e.g., simulated clicks).
4. **Streak Maintenance**: The streak is updated automatically with each successful submission.

## Customization

You can easily modify the script to:
- Work with different problem categories or difficulty levels.
- Add additional features like tracking progress, emailing reports, etc.

## Troubleshooting

- **Driver Not Found**: Ensure you have the correct WebDriver for your browser version.
- **Login Issues**: Login to your leetcode from edge before running the script
- **Dependencies**: Make sure all libraries are correctly installed, and you're using a compatible Python version.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request! You can:
- Report issues or bugs
- Suggest new features
- Improve the documentation

## Acknowledgments

- [Selenium](https://www.selenium.dev/) for browser automation.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [LeetCode](https://leetcode.com/) for the awesome platform!

---

Happy coding, and may your streak stay unbroken!
