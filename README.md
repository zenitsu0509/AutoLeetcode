# AutoLeetcode

This project is designed to automate the process of solving your daily LeetCode problem and help you maintain your streak effortlessly. It provides a user-friendly application that allows you to monitor your LeetCode account and track your progress. The script uses **Selenium** for web automation to interact with the LeetCode website and **BeautifulSoup** for scraping necessary data. The user interface (UI) is built using **PyQt5** for the desktop application, while **HTML** and **CSS** are used for styling the interface. With this tool, you can easily stay on top of your daily practice and ensure you never miss a challenge.

#

![LeetCode Progress Image](https://i.ibb.co/GP1gTp2/my-42-yr-old-dad-journey-with-912-problems-solved-on-v0-mswt5ewza94e1-ezgif-com-webp-to-jpg-converte.jpg)

# SETUP
## Cloning Repo
```bash
# clone the repo
git clone https://github.com/Its-Vaibhav-2005/AutoLeetcode.git
# change the directory
cd AutoLeetcode
# downloading the requirements
pip install -r requirements.txt
# run script
python -u "app.py"
```
# Code Explaination
## 1. **Overview**
This section explains the key components of the **AutoLeetcode** script. It provides a breakdown of the different functions and how they interact to automate the process of solving and submitting the "Question of the Day."
## 2. **Application**
The UI is developed using `PyQt5` as the platform, while the remaining parts are built with `HTML5` and `CSS`. The UI fetches basic details from the LeetCode account using `Selenium` and displays them in the application. Additionally, users can manually run the script if it is not working automatically. A code snippet is provided below.
```python
class App(QMainWindow):
    def __init__(self, content):
        super().__init__()
        self.page = QWebEngineView()
        self.page.setHtml(content)
        self.setCentralWidget(self.page)
        self.setWindowTitle("LeetCode Dashboard")
        self.initMenuBar()
    def initMenuBar(self):
        menu = self.menuBar()
        menuOpt = menu.addMenu('Operation')

        chngUrl = QAction("Change Url", self)
        chngUrl.triggered.connect(self.change)

        runScript = QAction("Run Script", self)
        runScript.triggered.connect(self.run)

        menuOpt.addAction(chngUrl)
        menuOpt.addAction(runScript)
    def change(self):
        # further Code . . .
    def run(self):
        # further code . . .
    def resize(self, event):
        self.page.resize(event.size())
```
## 3. **Browser Setup**
For the current version of **AutoLeetcode**, it is necessary to use **Chrome**. The user must be logged into their **Leetcode** account in **Chrome**. The system will retrieve the user's login credentials from there system from (`C:\Users\<Device_login_name>\AppData\Local\Google\Chrome\User Data`) and continue with the automation process.
```python
def chromeBrowser():
   options = Options()
   dataDir = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
   options.add_argument(f"--user-data-dir={dataDir}")
   options.add_argument("--profile-directory=Default")
   return webdriver.Chrome(options=options)
```
## 4. **Navigating to "Question of the Day"**
The script navigates to the "Question of the Day" page on LeetCode, by fetching the current date from users system
```python
xpath = f"/html/body/div[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]/a[{datetime.date.today().day}]"
qnsTab = WebDriverWait(driver, 60).until(
   ec.element_to_be_clickable((By.XPATH, xpath))
)
qnsTab.click()
```
## 5. **Solution**
As `Leetcode` provides the solution in 3 languages `(C++, Python3, Java)`, so we go with `C++` as default by accessing the leetcode-playground and copying the code.
```python
retries = 5
content = ""
while retries > 0:
   try:
         solDiv = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[5]/div/div[2]/div/div[2]/div/div'))
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
driver.get(iFrame[-1])
copyBtn = WebDriverWait(driver, 10).until(
   ec.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[1]/div[2]/button"))
)
copyBtn.click()
```
## 6. **Submit Code**
Let's be honest—how many of us have spent those precious few minutes copying and pasting code manually? 🙄 It's like the universe just wants us to waste time on this instead of actually building something cool! But fear not, my cool developer friends! I took that mind-numbing task and automated it so **YOU** don’t have to suffer anymore. 🚀

This script? It’s a speed demon, taking just **~40 seconds** to do what would normally waste your valuable time. ⏱️ While it’s busy doing the heavy lifting, **YOU** can actually focus on what matters—developing, innovating, and looking like a coding wizard. ✨

Go ahead, let the script work its magic while you do **YOUR** thing. 🎩💻

# Information
## Features
- **Dashboard**: 
A user friendly and cool dashboard to show `Leetcode` analysis.
- **Automates the "Question of the Day"**: Automatically solves and submits the problem of the day.
- **Maintains your streak**: Keeps track of your streak and ensures you don't miss any day.
- **Saves time**: No need to manually solve the questions; this bot handles everything for you.

## Prerequisites

Before you run this project, ensure you have the following installed:

- Python 3.x
- Chrome (depending on your configuration)
- Internet Connection (10Mbs)

## Python Libraries

To install the required Python libraries, run the following command:

- selenium
- beautifulsoup4
- PyQt5
- matplotlib

## Setup and Configuration

1. **Clone the repository** 
Clone repo apply any changes if required and enjoy the process of development.
   
2. **Set up your LeetCode account credentials**:
Login to the leetcode in your chrome and provide the profile url to the application.


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

## Acknowledgments

- [Selenium](https://www.selenium.dev/) for browser automation.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [LeetCode](https://leetcode.com/) solving problem
- [Qt](https://doc.qt.io/qtforpython-6/) for platform design
- [Icecream](https://github.com/gruns/icecream) for code debuging

---
Happy coding, and may your streak stay as unbreakable as your coffee addiction! ☕💻 Keep crushing it and let no bug stand in your way! 💥🚀
