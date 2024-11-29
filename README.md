# LeetCode Automation Bot

This Python automation project helps you to complete your daily LeetCode challenges automatically and maintain your streak. The script utilizes `Selenium` for web automation and `BeautifulSoup` for scraping the necessary data. With this tool, you can easily stay on top of your daily practice and never miss a challenge!

![LeetCode Progress Image](https://preview.redd.it/what-ive-learned-from-7-months-of-leetcode-v0-od4xo623frzd1.png?width=834&format=png&auto=webp&s=49e4c3d1e11728f078d56f7f1e9af25ba6373b59)
 

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
