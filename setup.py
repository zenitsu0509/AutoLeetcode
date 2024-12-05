from cx_Freeze import setup, Executable

setup(
    name="AuoLeetcode",  # name of the application
    options={
        "build_exe": {
            "packages": [
                "matplotlib",  # for plotting
                "numpy",  # for numerical operations
                "pymsgbox",  # for message box UI
                "PyQt5",  # for GUI framework
                "bs4",  # BeautifulSoup for web scraping
                "selenium",  # for web automation
                "os",  # built-in
                "time",  # built-in
                "json",  # built-in
                "re",  # built-in
                "shutil",  # built-in
                "subprocess",  # built-in
                "datetime",  # built-in
                "io",  # built-in
                "base64"  # built-in
            ],  
            "include_files": [
                r"main.py",
                r"requirements.txt"
            ]  # Include your other files (like Python scripts or text files)
        }
    },
    version="1.0",  # version of your application
    description="AutoLeetcode: Leetcode Automation Tool",  # description of the application
    executables=[
        Executable(
            r"app.py",  # path to the main Python file
            icon=r"leetcode.ico"
        )
    ],  # icon for the application
    shortcutName="autoleetcode",
    shortcutDir="DesktopFolder",  # the folder in which you will have your app shortcut
    base="Win32GUI"  # <- Write this if you want to make a GUI
)
