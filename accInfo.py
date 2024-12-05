from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Correct import for QWebEngineView
from PyQt5.QtCore import Qt
import sys

class App(QMainWindow):
    def __init__(self, content):
        super().__init__()

        # Initialize the web engine view
        self.page = QWebEngineView()
        self.page.setHtml(content)
        self.setCentralWidget(self.page)
        
        # Set window title
        self.setWindowTitle("LeetCode Dashboard")

        # Set up the menu bar
        self.init_menu_bar()

    def init_menu_bar(self):
        menu_bar = self.menuBar()  # Create a menu bar

        # Add a menu to the bar
        file_menu = menu_bar.addMenu('File')

        # Create an action for the button
        action_button = QAction('Click Me', self)  # Action for the menu item
        action_button.triggered.connect(self.on_button_click)  # Connect to the function

        # Add the action to the 'File' menu
        file_menu.addAction(action_button)

    def on_button_click(self):
        print("Button clicked!")  # This function is triggered when the menu item is clicked

# HTML content for the web engine view
content = "<h1>Hi!</h1>"

app = QApplication(sys.argv)
window = App(content)
window.show()
sys.exit(app.exec_())
