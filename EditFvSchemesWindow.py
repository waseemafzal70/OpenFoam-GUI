from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox


class EditFvSchemesWindow(QDialog):
    def __init__(self, fv_schemes_path):
        super().__init__()
        self.setWindowTitle("Edit fvSchemes")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.ddt_schemes_label = QLabel("ddtSchemes:")
        self.ddt_schemes_combobox = QComboBox()
        self.ddt_schemes_combobox.addItems(["Euler", "localEuler", "CrankNicholson", "backward", "steadyState"])
        self.layout.addWidget(self.ddt_schemes_label)
        self.layout.addWidget(self.ddt_schemes_combobox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_fv_schemes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.fv_schemes_path = fv_schemes_path

        # Load and display the current value of ddtSchemes
        self.load_fv_schemes_values()

    def load_fv_schemes_values(self):
        ddt_schemes_found = False
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    ddt_schemes_found = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.ddt_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'ddtSchemes'.")

        if not ddt_schemes_found:
            print("Warning: 'ddtSchemes' not found in the file.")

    def save_fv_schemes(self):
        # Get the selected ddtScheme from the combobox
        selected_scheme = self.ddt_schemes_combobox.currentText()

        # Update the fvSchemes file with the edited value
        updated_lines = []
        ddt_schemes_found = False
        inside_ddt_schemes_block = False
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    ddt_schemes_found = True
                    inside_ddt_schemes_block = True
                    try:
                        updated_lines.append(f"ddtSchemes\n{{\n    default         {selected_scheme};\n}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'ddtSchemes'.")
                elif inside_ddt_schemes_block and line.strip() == "}":
                    inside_ddt_schemes_block = False
                elif not inside_ddt_schemes_block:
                    updated_lines.append(line)

        if not ddt_schemes_found:
            print("Warning: 'ddtSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nddtSchemes\n{{\n    default         {selected_scheme};\n}}\n")

        with open(self.fv_schemes_path, 'w') as file:
            file.writelines(updated_lines)

        self.accept()
