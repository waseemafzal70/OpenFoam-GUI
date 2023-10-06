import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, \
    QLineEdit

from OptionsWindow import OptionsWindow


class ProjectManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager")
        self.setGeometry(200, 200, 700, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        original_pixmap = QPixmap("OpenFOAM.png")

        # Resize the image to the desired size
        width = 256*2  # Replace with your desired width
        height = 183  # Replace with your desired height
        scaled_pixmap = original_pixmap.scaled(width, height)

        logo_pixmap = QPixmap(scaled_pixmap)  # Replace "logo.png" with your logo file path
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        self.layout.addWidget(logo_label)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Welcome to the openFoam Project Manager!")
        self.layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter Project Name")
        self.layout.addWidget(self.project_name_input)

        self.new_project_button = QPushButton("Create New Project")
        self.new_project_button.clicked.connect(self.create_new_project)
        self.layout.addWidget(self.new_project_button)

        self.open_project_button = QPushButton("Open Existing Project")
        self.open_project_button.clicked.connect(self.open_existing_project)
        self.layout.addWidget(self.open_project_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.open_next_window)
        self.layout.addWidget(self.next_button)
        self.next_button.setEnabled(False)

        self.project_directory_label = QLabel("Project Directory:")
        self.layout.addWidget(self.project_directory_label)

        self.central_widget.setLayout(self.layout)

        self.current_project_directory = None
        self.current_project_name = None

    def create_new_project(self):
        self.current_project_name = self.project_name_input.text()
        if not self.current_project_name:
            self.label.setText("Please enter a project name.")
            return

        directory = QFileDialog.getExistingDirectory(self, "Select Directory for New Project")
        if directory:
            self.current_project_directory = os.path.join(directory, self.current_project_name)
            os.makedirs(self.current_project_directory, exist_ok=True)
            self.project_directory_label.setText(f"Project Directory: {self.current_project_directory}")
            self.next_button.setEnabled(True)

    def open_existing_project(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Existing Project Directory")
        if directory:
            self.current_project_directory = directory
            self.project_directory_label.setText(f"Project Directory: {directory}")
            self.next_button.setEnabled(True)

    def open_next_window(self):
        # You can add code here to open the next window or perform other actions.
        # For example:
        # next_window = NextWindow(self.current_project_directory, self.current_project_name)
        # next_window.show()
        options_window = OptionsWindow(self.current_project_directory)
        options_window.exec()


def main():
    app = QApplication(sys.argv)
    window = ProjectManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
