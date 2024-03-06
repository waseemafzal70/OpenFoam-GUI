import os
import subprocess
import sys
from PyQt6.QtCore import QProcess
from PyQt6.QtGui import QAction, QIcon, QTextCursor, QImage
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QPushButton,
    QFormLayout,
    QInputDialog, QLabel, QMessageBox,
)

from OptionsWindow import OptionsWindow
from EditControlDictWindow import EditControlDictWindow
from EditFvSchemesWindow import EditFvSchemesWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.open_foam_logo = QLabel(self)
        self.open_foam_logo.setText("")
        self.current_project_directory = None
        # Variable to store the current project directory

        self.setWindowTitle('MainWindow')

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('openfoam-logo.png'))
        # Create text editor widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        document = self.text_edit.document()
        cursor = QTextCursor(document)

        p1 = cursor.position()  # returns int
        cursor.insertImage(QImage("OpenFOAM.png").scaled(512, 183))

        # Add text to the text editor
        initial_text = '\n1. Create a new Project or open an existing project.\n' \
                       '2. Select a tutorial from Select dropdown menu.\n' \
                       '3. Edit the configuration files from Edit menu.\n' \
                       '4. Run your project.\n' \
                       '5. You can launch Paraview from Post processing menu to visualize the results.\n'

        self.text_edit.insertPlainText(initial_text)

        # Create start button
        self.start_button = QPushButton('Run Project', self)
        self.start_button.clicked.connect(self.run_command)

        # Create layout for start button
        button_layout = QFormLayout()
        button_layout.addRow('Command:', self.start_button)

        # Create central widget
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.open_foam_logo)
        central_layout.addWidget(self.text_edit)
        central_layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        new_project_action = QAction('New Project', self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)

        open_project_action = QAction('Open Existing Project', self)
        open_project_action.triggered.connect(self.open_existing_project)
        file_menu.addAction(open_project_action)

        save_action = QAction('Save Progress', self)
        save_action.triggered.connect(self.save_progress)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Select menu
        select_menu = menubar.addMenu('Select')

        select_tutorial_action = QAction('Select Tutorial', self)
        select_tutorial_action.triggered.connect(self.show_options_window)
        select_menu.addAction(select_tutorial_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        # ControlDict edit action
        control_dict_action = QAction('Edit ControlDict', self)
        control_dict_action.triggered.connect(self.edit_control_dict)
        edit_menu.addAction(control_dict_action)

        # fvSchemes edit action
        fv_schemes_action = QAction('Edit fvSchemes', self)
        fv_schemes_action.triggered.connect(self.edit_fv_schemes)
        edit_menu.addAction(fv_schemes_action)

        # Post processing menu
        post_process_menu = menubar.addMenu('Post Processing')

        # Paraview subAction
        paraview_action = QAction('Paraview', self)
        paraview_action.triggered.connect(self.launch_paraview)
        post_process_menu.addAction(paraview_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('OpenFoam GUI')
        self.show()

    def save_progress(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, 'Save Progress', '', 'Text Files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def run_command(self):
        if "rhoCentralFoam" in self.current_project_directory:
            wsl_path = '/mnt/c/' + self.current_project_directory.replace('\\', '/').lstrip('C:').lstrip('/')
            print(wsl_path)
            wsl_command = f"cd '{wsl_path}' && source /usr/lib/openfoam/openfoam2306/etc/bashrc && ./Allrun"
            print(wsl_command)
        elif "laplacianFoam" in self.current_project_directory:
            wsl_path = '/mnt/c/' + self.current_project_directory.replace('\\', '/').lstrip('C:').lstrip('/')
            print(wsl_path)
            wsl_command = f"cd '{wsl_path}' && source /usr/lib/openfoam/openfoam2306/etc/bashrc && ./Allrun"
            print(wsl_command)
        else:
            # Build the WSL command to run "./Allrun" and capture the output
            print(self.current_project_directory)
            wsl_path = '/mnt/c/' + self.current_project_directory.replace('\\', '/').lstrip('C:').lstrip('/')
            print(wsl_path)
            wsl_command = f"cd '{wsl_path}' && source /usr/lib/openfoam/openfoam2306/etc/bashrc && blockMesh && icoFoam && foamToVTK"

        print("Running command:", wsl_command)

        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.update_output)
        process.started.connect(lambda: print("Process started"))
        process.finished.connect(lambda exit_code, exit_status: print("Process finished with exit code:", exit_code))
        process.errorOccurred.connect(lambda error: print("Error occurred:", error))

        process.start(wsl_command)

        # Launch a cmd window while running the WSL command and capturing the output
        cmd_command = f"wsl -e bash -c \"{wsl_command}\""
        process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                   text=True)

        self.text_edit.clear()

        document = self.text_edit.document()
        cursor = QTextCursor(document)

        p1 = cursor.position()
        # returns int
        cursor.insertImage(QImage("OpenFOAM.png").scaled(512, 183))

        while process.poll() is None:
            output_line = process.stdout.readline()
            self.text_edit.append(output_line)
            # progress_text.append(output_line)
            QApplication.processEvents()

        # Capture any remaining output
        output, error = process.communicate()
        self.text_edit.append(output)
        self.text_edit.append(error)

    def update_output(self):
        process = self.sender()
        output = process.readAllStandardOutput().data().decode('utf-8')
        self.text_edit.append(output)

    #  self.text_edit.append(output)

    def new_project(self):
        # Show a dialog to get a new project name
        new_project_name, ok = QInputDialog.getText(self, 'New Project', 'Enter a name for the new project:')

        if ok and new_project_name:
            # Create a new directory using the specified name
            directory = QFileDialog.getExistingDirectory(self, 'Select New Project Directory',
                                                         self.current_project_directory)
            if directory and os.path.exists(directory):  # Check if the directory exists
                new_project_directory = os.path.join(directory, new_project_name)
                os.makedirs(new_project_directory, exist_ok=True)

                # Set the current project directory and update the UI
                self.current_project_directory = new_project_directory
                self.setWindowTitle(f'MainWindow - {new_project_directory}')
                print(f'New Project created in directory: {new_project_directory}')
                QMessageBox.information(self, "Success",
                                        "Step 1 is completed successfully, Please proceed to next step.")
            elif directory:
                print(f'Selected directory does not exist: {directory}')

    def open_existing_project(self):
        # Show a dialog to select an existing project directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Existing Project Directory',
                                                     self.current_project_directory)
        if directory and os.path.exists(directory):  # Check if the directory exists
            # Set the current project directory and update the UI
            self.current_project_directory = directory
            self.setWindowTitle(f'MainWindow - {directory}')
            print(f'Opened Existing Project in directory: {directory}')
        elif directory:
            print(f'Selected directory does not exist: {directory}')

    def show_options_window(self):
        options_window = OptionsWindow(self.current_project_directory, self)
        options_window.exec()

        # Update self.current_project_directory after the OptionsWindow is closed
        if options_window.destination_directory:
            self.current_project_directory = options_window.destination_directory
            self.setWindowTitle(f'MainWindow - {self.current_project_directory}')
            print(self.current_project_directory)
        QMessageBox.information(self, "Success",
                                "Step 2 is completed successfully, Please proceed to next step.")

    def edit_control_dict(self):
        if self.current_project_directory:
            control_dict_path = os.path.join(self.current_project_directory, 'system', 'controlDict')
            if os.path.isfile(control_dict_path):
                edit_control_dict_window = EditControlDictWindow(control_dict_path)
                edit_control_dict_window.exec()
                QMessageBox.information(self, "Success",
                                        "ControlDict edited successfully, Please proceed to next step.")
            else:
                print("ControlDict file not found.")

    def edit_fv_schemes(self):
        if self.current_project_directory:
            fv_schemes_path = os.path.join(self.current_project_directory, 'system', 'fvSchemes')
            if os.path.isfile(fv_schemes_path):
                edit_fv_schemes_window = EditFvSchemesWindow(fv_schemes_path)
                edit_fv_schemes_window.exec()
                QMessageBox.information(self, "Success",
                                        "fvSchemes edited successfully, Please proceed to next step.")
            else:
                print("fvSchemes file not found.")

    def launch_paraview(self):
        QMessageBox.information(self, "Success",
                                "Please wait, while Paraview is launching.")
        # Path to ParaView executable
        paraview_path = r"C:\Program Files\ParaView 5.11.1\bin\paraview.exe"

        # Check if ParaView executable exists
        if os.path.exists(paraview_path):
            # Launch ParaView
            subprocess.Popen(paraview_path)
        else:
            QMessageBox.critical(self, "Error", "ParaView executable not found.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())