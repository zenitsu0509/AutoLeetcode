import sys, os, time, matplotlib.pyplot as plt, numpy as np, io, base64, pymsgbox, re, json, shutil, subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

def batFile():
    mainFile = os.path.join(os.path.abspath(os.getcwd()),"main.py")
    req = os.path.join(os.path.abspath(os.getcwd()),"requirements.txt")
    batCont = f"""
@echo off
REM Execute Python script with unbuffered output
python -u "{mainFile}"
exit
    """
    if not os.path.exists("leetcode.bat"):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req])
            with open("leetcode.bat", "w") as batch_file:
                    batch_file.write(batCont)
            
        except:
            pass
    else:
        print("file exist")
def chrome():
    opt = Options()
    opt.add_argument(f"--user-data-dir={os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")}")
    opt.add_argument("--profile-directory=Default")
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--window-size=1920x1080")
    opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(opt)

def fetchDetails(url):
    details = {}
    xpaths = {
        "id":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div",
        "name":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div",
        "profilePic":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div[1]/div[1]/img",
        "rank":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[3]/span[2]",
        "qnsCard":"/html/body/div[1]/div[1]/div[4]/div/div[2]/div[1]/div[1]/div/div/div[2]",
        "countary":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/span[2]/div",
        "top3lang":"/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[6]",
    }
    driver = chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    # getting id
    try:
        id = WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.XPATH,xpaths['id']))
        )
        details['id'] = id.text
    except Exception as e:
        details['id'] = 'N/A'
        print(e)
    
    # getting name
    try:
        name = WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.XPATH,xpaths['name']))
        )
        details['name'] = name.text
    except Exception as e:
        details['name'] = 'N/A'
        print(e)

    # getting rank
    try:
        rank = WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.XPATH,xpaths['rank']))
        )
        details['rank'] = rank.text
    except Exception as e:
        details['rank'] = 'N/A'
        print(e) 

    # getting profile
    try:
        pic = WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.XPATH,xpaths['profilePic']))
        )
        details['profilePic'] = pic.get_attribute('src')
    except Exception as e:
        details['profilePic'] = '#'
        print(e)
    
    # getting countary
    try:
        countary = WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.XPATH,xpaths['countary']))
        )
        details['countary'] = countary.text
    except Exception as e:
        details['countary'] = 'N/A'
        print(e)
    
    # getting qns
    try:
        qns = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.XPATH, xpaths['qnsCard']))
        )
        content = driver.execute_script("return arguments[0].innerHTML;", qns)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            qnsLevel = []
            divs = soup.find_all('div', class_='rounded-sd-sm')  # Confirm this class exists
            for div in divs:
                score_div = div.find('div', class_='text-sd-foreground text-xs font-medium')
                if score_div:
                    score = score_div.get_text(strip=True)
                    scores = [s.strip() for s in score.split('/')] 
                    qnsLevel.append(scores)
            details['qnsCard'] = qnsLevel
        else:
            print("No content found in qnsCard")
            
    except Exception as e:
        details['qnsCard'] = [[], [], []]
        print(e)
    
    # top lang
    try:
        # Wait for the top3lang div to be present
        top3lang = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.XPATH, xpaths['top3lang']))
        )
        content = driver.execute_script("return arguments[0].innerHTML;", top3lang)
        soup = BeautifulSoup(content, 'html.parser')
        langs = []
        divs = soup.find_all('div', class_='text-xs')[:3] 
        for div in divs:
            lang = div.find('span')
            if lang and lang.text.strip():
                langs.append(lang.text.strip())
            else:
                langs.append("N/A")
        details['top3lang'] = langs
    except Exception as e:
        details['top3lang'] = 'N/A'
        print(f"Error getting top languages: {e}")
    driver.quit()
    return details
def getChart(data):
    level = ['Easy', 'Medium', 'Hard']
    solved = [int(d[0]) for d in data]
    total = [int(d[1]) for d in data]
    unsolved = [t - s for t, s in zip(total, solved)]
    x = np.arange(len(level))
    plt.figure(figsize=(8, 6))
    plt.bar(x, total, color='#CF8FF7', label='Unsolved Questions', width=0.4)
    plt.bar(x, solved, color='#A020F0', label='Solved Questions', width=0.4)
    for i in range(len(level)):
        ratio = (solved[i] / total[i]) * 100
        plt.text(
            x[i], solved[i] + 0.05 * total[i], 
            f"{solved[i]}/{total[i]} ( {ratio:.1f}% )", 
            ha='center', va='bottom', fontsize=10, color='black'
        )
    plt.xticks(x, level)
    plt.ylabel('Number of Questions')
    plt.title('Questions Solved vs Total Questions by Difficulty')
    plt.legend()
    # graph to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image

def genHtml(details):
    chart = getChart(details['qnsCard'])
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Dashboard</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            overflow-x: hidden;
        }}

        /* Profile Section */
        .profile-container {{
            width: 100%;
            background: white;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}

        .profile {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .profile-left {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .profile-left img {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #ccc;
            border: 1px solid black;
            margin: 10px;
        }}

        .profile-info {{
            line-height: 1.4;
        }}

        .profile-info h1 {{
            font-size: 18px;
            margin: 0;
        }}

        .profile-info span {{
            font-size: 14px;
            color: gray;
        }}

        .rank {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }}

        /* Content Section */
        .container {{
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 10px;
        }}

        .card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 20px;
            flex: 1 1 100%; 
            min-width: 300px;
        }}

        /* Make two cards per row on larger screens */
        @media (min-width: 768px) {{
            .card {{
                flex: 1 1 calc(50% - 20px); /* 50% minus gap between cards */
            }}
        }}

        /* Graph Container */
        .card .chart {{
            height: auto; /* Automatically adjust height */
            background-color: #f0f0f0;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: gray;
            overflow: hidden;
            max-width: 100%;
        }}

        /* Responsive Styling for Graph Image */
        .card .chart img {{
            width: 100%; /* Scale the image */
            height: auto; /* Maintain aspect ratio */
        }}

        /* Top Languages */
        .languages-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .languages-list li {{
            font-size: 14px;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .languages-list li span {{
            font-weight: bold;
        }}

        /* Mobile-First Adjustments */
        @media (max-width: 768px) {{
            .profile {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}

            .rank {{
                align-self: flex-end;
            }}
        }}

    </style>
</head>
<body>
    <!-- Profile Section -->
    <div class="profile-container">
        <div class="profile">
            <div class="profile-left">
                <img src="{details['profilePic']}" alt="User Avatar" />
                <div class="profile-info">
                    <h1>{details['name']}</h1>
                    <span>ID: {details['id']}<br>{details['countary']}</span>
                </div>
            </div>
            <div class="rank">Rank: {details['rank']}</div>
        </div>
    </div>

    <!-- Content Section -->
    <div class="container">
        <!-- Graph Card -->
        <div class="card">
            <h2>Questions Solved</h2>
            <div class="chart">
                <img src="data:image/png;base64,{chart}" alt="qns list">
            </div>
        </div>

        <!-- Top Languages Card -->
        <div class="card">
            <h2>Top Languages</h2>
            <ul class="languages-list">
                <li><span style="padding:5px 10px">1 </span> {details['top3lang'][0]}</li>
                <li><span style="padding:5px 10px">2 </span> {details['top3lang'][1]}</li>
                <li><span style="padding:5px 10px">3 </span> {details['top3lang'][2]}</li>
            </ul>
        </div>
    </div>
</body>
</html>

"""


class App(QMainWindow):
    def __init__(self, content):
        super().__init__()
        self.page = QWebEngineView()
        self.page.setHtml(content)
        self.setCentralWidget(self.page)
        self.setWindowTitle("LeetCode Dashboard")
        self.initMenuBar()

    def resizeEvent(self, event):
        self.page.resize(event.size())
    
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
        pass


    def run(self):
        os.system('leetcode.bat')
if __name__ == "__main__":
    leetcode = {}
    pattern = r"^https://leetcode\.com/u/[^/]+/$"
    url = ""
    jsonPath = os.path.join(os.getcwd(), "leetcode.json")
    batFile()
    try:
        with open(jsonPath, 'r') as f:
            leetcode = json.load(f)
            url = leetcode.get('url', '')
    except Exception as e:
        print(f"Error reading file: {e}")
    
    if not url:
        url = pymsgbox.prompt("Enter Leetcode Profile URL")

        if not re.match(pattern, url):
            pymsgbox.alert('Invalid Url', 'Leetcode finder!')
        else:
            leetcode['url'] = url
            bat = os.path.join(os.getcwd(), 'leetcode.bat')  # Replace this with your actual .bat file location
            dest = os.path.join(os.getenv('APPDATA'), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            try:
                shutil.copy(bat, dest)
            except Exception as e:
                print(f"Error copying the batch file: {e}")
            
            leetcode['moved'] = True
            with open(jsonPath, 'w') as f:
                json.dump(leetcode, f, indent=4)

    if re.match(pattern, url):
        details = fetchDetails(url)
        content = genHtml(details)
        app = QApplication(sys.argv)
        window = App(content)
        window.show()
        sys.exit(app.exec_())