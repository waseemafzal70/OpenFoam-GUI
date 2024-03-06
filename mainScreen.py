import sys

from PyQt6.QtCore import QProcess
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QPushButton, QFormLayout, QLineEdit, QDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.setWindowTitle('MainWindow')

        self.init_ui()

    def init_ui(self):
        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create start button
        self.start_button = QPushButton('Start Command', self)
        self.start_button.clicked.connect(self.run_command)

        # Create layout for start button
        button_layout = QFormLayout()
        button_layout.addRow('Command:', self.start_button)

        # Create central widget
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.text_edit)
        central_layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        save_action = QAction('Save Progress', self)
        save_action.triggered.connect(self.save_progress)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        # Config edit action (you can replace 'ConfigEditDialog' with your actual config editing class)
        config_edit_action = QAction('Configure', self)
        config_edit_action.triggered.connect(self.show_config_edit)
        edit_menu.addAction(config_edit_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('PyQt6 Progress Demo')
        self.show()

    def save_progress(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, 'Save Progress', '', 'Text Files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def run_command(self):
        # Replace 'your_command' with the actual command you want to run
        command = 'your_command'
        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.update_output)
        process.start(command)

    def update_output(self):
        process = self.sender()
        output = process.readAllStandardOutput().data().decode('utf-8')
        self.text_edit.append(output)

    def show_config_edit(self):
        # Replace 'ConfigEditDialog' with your actual config editing class
        config_dialog = ConfigEditDialog(self)
        config_dialog.exec()


# Example ConfigEditDialog class (replace with your actual implementation)
class ConfigEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        # Add your configuration editing widgets here
        layout = QVBoxLayout(self)
        layout.addWidget(QLineEdit('Configuration Edit'))
        self.setWindowTitle('Config Edit')
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
