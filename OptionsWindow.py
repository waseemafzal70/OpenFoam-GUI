import os
import shutil
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QRadioButton, QButtonGroup, \
    QMessageBox


class OptionsWindow(QDialog):
    def __init__(self, project_directory):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(300, 300, 400, 250)  # Increased height for the progress bar
        self.project_directory = project_directory

        self.layout = QVBoxLayout()

        self.label = QLabel("Select an option:")
        self.layout.addWidget(self.label)

        # Create radio buttons
        self.button_group = QButtonGroup(self)
        self.basic_radio = QRadioButton("Basic CFD codes:")  # Fixed typo
        self.compressible_radio = QRadioButton("Compressible flow:")  # Fixed typo

        # Add radio buttons to layout
        self.layout.addWidget(self.basic_radio)
        self.layout.addWidget(self.compressible_radio)

        # Add radio buttons to button group
        self.button_group.addButton(self.basic_radio)
        self.button_group.addButton(self.compressible_radio)

        self.options_combo = QComboBox()
        self.layout.addWidget(self.options_combo)

        # Connect radio button signals to update options
        self.basic_radio.toggled.connect(self.update_options)
        self.compressible_radio.toggled.connect(self.update_options)

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
        else:
            options = []  # Empty list if neither radio button is selected

        self.options_combo.clear()
        self.options_combo.addItems(options)

    def copy_selected_option(self):
        selected_option = self.options_combo.currentText()
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

        if source_directory:
            destination_directory = os.path.join(self.project_directory, selected_option)
            try:
                shutil.copytree(source_directory, destination_directory, symlinks=True, dirs_exist_ok=True)
                self.accept()  # Close the window after copying
                QMessageBox.information(self, "Success", f"Copying {selected_option} successful.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error copying directory: {e}")
