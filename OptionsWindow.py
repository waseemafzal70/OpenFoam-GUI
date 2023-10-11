import os
import shutil
import subprocess

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QRadioButton, QButtonGroup, \
    QMessageBox, QApplication, QTextEdit


class OptionsWindow(QDialog):
    def __init__(self, project_directory):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(200, 200, 700, 400)
        self.project_directory = project_directory

        self.layout = QVBoxLayout()

        self.label = QLabel("Select an option:")
        self.layout.addWidget(self.label)

        self.button_group = QButtonGroup(self)
        self.basic_radio = QRadioButton("Basic CFD codes:")
        self.compressible_radio = QRadioButton("Compressible flow:")
        self.incompressible_radio = QRadioButton("Incompressible:")

        self.layout.addWidget(self.basic_radio)
        self.layout.addWidget(self.compressible_radio)
        self.layout.addWidget(self.incompressible_radio)

        self.button_group.addButton(self.basic_radio)
        self.button_group.addButton(self.compressible_radio)
        self.button_group.addButton(self.incompressible_radio)

        self.options_combo = QComboBox()
        self.layout.addWidget(self.options_combo)

        self.subdirectory_combo = QComboBox()
        self.layout.addWidget(self.subdirectory_combo)

        self.basic_radio.toggled.connect(self.update_options)
        self.compressible_radio.toggled.connect(self.update_options)
        self.incompressible_radio.toggled.connect(self.update_options)
        self.options_combo.currentIndexChanged.connect(self.update_subdirectories)

        self.copy_button = QPushButton("Next")
        self.copy_button.clicked.connect(self.copy_selected_option)
        self.layout.addWidget(self.copy_button)

        self.setLayout(self.layout)

    def update_options(self):
        selected_radio = self.button_group.checkedButton()
        if selected_radio == self.basic_radio:
            options = ["laplacianFoam", "potentialFoam", "scalarTransportFoam"]
        elif selected_radio == self.compressible_radio:
            options = ["rhoCentralFoam", "rhoPimpleFoam", "rhoPorousSimpleFoam", "rhoSimpleFoam"]
        elif selected_radio == self.incompressible_radio:
            options = ["icoFoam"]
        else:
            options = []

        self.options_combo.clear()
        self.options_combo.addItems(options)

    def update_subdirectories(self):
        selected_option = self.options_combo.currentText()
        subdirectories = []

        if selected_option == "laplacianFoam":
            subdirectories = ["flange", "implicitAMI"]
        elif selected_option == "potentialFoam":
            subdirectories = ["cylinder", "pitzDaily"]
        elif selected_option == "scalarTransportFoam":
            subdirectories = [""]
        elif selected_option == "rhoCentralFoam":
            subdirectories = [""]
        elif selected_option == "rhoPimpleFoam":
            subdirectories = [""]
        elif selected_option == "rhoPorousSimpleFoam":
            subdirectories = [""]
        elif selected_option == "rhoSimpleFoam":
            subdirectories = [""]
        elif selected_option == "icoFoam":
            subdirectories = ["cavity"]

        self.subdirectory_combo.clear()
        self.subdirectory_combo.addItems(subdirectories)

    def copy_selected_option(self):
        selected_option = self.options_combo.currentText()
        selected_subdirectory = self.subdirectory_combo.currentText()

        if not selected_option or not selected_subdirectory:
            QMessageBox.critical(self, "Error", "Please select both an option and a subdirectory.")
            return

        source_directory = ""

        if selected_option == "laplacianFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\basic\laplacianFoam"
        elif selected_option == "potentialFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\basic\potentialFoam"
        elif selected_option == "scalarTransportFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\basic\scalarTransportFoam"
        elif selected_option == "rhoCentralFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\compressible\rhoCentralFoam"
        elif selected_option == "rhoPimpleFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\compressible\rhoPimpleFoam"
        elif selected_option == "rhoPorousSimpleFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\compressible\rhoPorousSimpleFoam"
        elif selected_option == "rhoSimpleFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\compressible\rhoSimpleFoam"
        elif selected_option == "icoFoam":
            source_directory = r"\\wsl.localhost\Ubuntu\usr\lib\openfoam\openfoam2306\tutorials\incompressible\icoFoam"

        if source_directory:
            source_directory = os.path.join(source_directory, selected_subdirectory)
            destination_directory = os.path.join(self.project_directory, selected_option, selected_subdirectory)

            try:
                shutil.copytree(source_directory, destination_directory, symlinks=True, dirs_exist_ok=True)
                self.accept()
                # QMessageBox.information(self, "Success",
                #                         f"Copying {selected_option}/{selected_subdirectory} successful.")

                # After copying, change the current directory to the destination and run "./Allrun" in WSL
                print(destination_directory)
                wsl_path = '/mnt/c/' + destination_directory.replace('\\', '/').lstrip('C:').lstrip('/')

                # Build the WSL command to run "./Allrun" and capture the output
                wsl_command = "cd '{}' && source /usr/lib/openfoam/openfoam2306/etc/bashrc && ./Allrun && foamToVTK".format(
                    wsl_path)

                # Launch a cmd window while running the WSL command and capturing the output
                cmd_command = f"wsl -e bash -c \"{wsl_command}\""
                process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                           text=True)

                # Create a dialog to display the progress
                progress_dialog = QDialog(self)
                progress_dialog.setWindowTitle("Progress")
                progress_dialog.setGeometry(200, 200, 700, 400)
                progress_layout = QVBoxLayout(progress_dialog)
                progress_label = QLabel("Running WSL command:")
                progress_layout.addWidget(progress_label)
                progress_text = QTextEdit(progress_dialog)
                progress_text.setReadOnly(True)
                progress_layout.addWidget(progress_text)
                progress_dialog.setLayout(progress_layout)
                progress_dialog.show()

                # Read and display the output while the process is running
                while process.poll() is None:
                    output_line = process.stdout.readline()
                    progress_text.append(output_line)
                    QApplication.processEvents()

                # Capture any remaining output
                output, error = process.communicate()
                progress_text.append(output)
                progress_text.append(error)

                QMessageBox.information(self, "Success",
                                        "Please open VTK file from your project directory in Paraview")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error copying directory: {e}")
