import os
import shutil
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QComboBox,
    QPushButton,
    QMessageBox,
)


class OptionsWindow(QDialog):
    def __init__(self, current_project_directory, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setGeometry(200, 200, 700, 400)
        self.project_directory = current_project_directory
        self.destination_directory = None  # Variable to store the selected destination directory

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

        self.copy_button = QPushButton("Copy Tutorial to Current Project")
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
            self.options_combo.setToolTip(
                "LaplacianFoam is a solver in OpenFOAM for solving Laplace's equation and similar problems in fluid dynamics and heat transfer.")
            subdirectories = ["flange", "implicitAMI"]
        elif selected_option == "potentialFoam":
            subdirectories = ["cylinder", "pitzDaily"]
            self.options_combo.setToolTip(
                "potentialFoam is a solver in OpenFOAM for simulating electric potential and electrostatic fields in electrostatic problems.")
        elif selected_option == "scalarTransportFoam":
            self.options_combo.setToolTip(
                "scalarTransportFoam is an OpenFOAM solver for modeling the transport of scalar quantities (e.g., temperature, concentration) in fluid flows, used in various applications from heat transfer to chemical reactions.")
            subdirectories = [""]
        elif selected_option == "rhoCentralFoam":
            self.options_combo.setToolTip(
                "rhoCentralFoam is an OpenFOAM solver for simulating compressible, transient, and turbulent flows using a central-upwind scheme for density-based solvers.")
            subdirectories = ["biconic25-55Run35", "LadenburgJet60psi", "shockTube"]
        elif selected_option == "rhoPimpleFoam":
            self.options_combo.setToolTip(
                "rhoPimpleFoam is an OpenFOAM solver that's suitable for transient, incompressible flows with turbulence modeling, using the PIMPLE (PISO-SIMPLE) algorithm to solve the Navier-Stokes equations.")
            subdirectories = [""]
        elif selected_option == "rhoPorousSimpleFoam":
            self.options_combo.setToolTip(
                "rhoPorousSimpleFoam is an OpenFOAM solver designed for modeling flows through porous media with incompressible, turbulent fluid flow, suitable for various applications involving porous materials like filters or packed beds.")
            subdirectories = [""]
        elif selected_option == "rhoSimpleFoam":
            self.options_combo.setToolTip(
                "rhoSimpleFoam is an OpenFOAM solver for steady-state, incompressible flows, using the SIMPLE (Semi-Implicit Method for Pressure-Linked Equations) algorithm to solve the Navier-Stokes equations.")
            subdirectories = [""]
        elif selected_option == "icoFoam":
            self.options_combo.setToolTip(
                "icoFoam is an OpenFOAM solver designed for simulating incompressible, steady-state flows using a PISO (Pressure-Implicit with Splitting of Operators) algorithm, making it suitable for a wide range of fluid flow applications.")
            subdirectories = ["cavity/cavity"]

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
            self.destination_directory = os.path.join(self.project_directory, selected_option, selected_subdirectory)

            try:
                shutil.copytree(source_directory, self.destination_directory, symlinks=True, dirs_exist_ok=True)
                QMessageBox.information(self, "Success", f'Tutorial copied to: {self.destination_directory}')
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f'Failed to copy tutorial. Error: {str(e)}')