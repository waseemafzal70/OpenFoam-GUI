from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox


class EditFvSchemesWindow(QDialog):
    def __init__(self, fv_schemes_path):
        super().__init__()
        self.setWindowTitle("Edit fvSchemes")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        # Add ddtSchemes section
        self.ddt_schemes_label = QLabel("ddtSchemes:")
        self.ddt_schemes_combobox = QComboBox()
        self.ddt_schemes_combobox.addItems(["Euler", "localEuler", "CrankNicholson", "backward", "steadyState"])
        self.layout.addWidget(self.ddt_schemes_label)
        self.layout.addWidget(self.ddt_schemes_combobox)

        # Add gradSchemes section
        self.grad_schemes_label = QLabel("gradSchemes:")
        self.grad_schemes_combobox = QComboBox()
        self.grad_schemes_combobox.addItems(["corrected", "uncorrected", "limited", "bounded", "fourth"])
        self.layout.addWidget(self.grad_schemes_label)
        self.layout.addWidget(self.grad_schemes_combobox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_fv_schemes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.fv_schemes_path = fv_schemes_path

        # Load and display the current values of ddtSchemes and gradSchemes
        self.load_fv_schemes_values()

    def load_fv_schemes_values(self):
        schemes_found = {"ddtSchemes": False, "gradSchemes": False}
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    schemes_found["ddtSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.ddt_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'ddtSchemes'.")
                elif line.startswith("gradSchemes"):
                    schemes_found["gradSchemes"] = True
                    try:
                        current_scheme = line.split()[1].strip(';')
                        self.grad_schemes_combobox.setCurrentText(current_scheme)
                    except IndexError:
                        print("Error: Index out of range while reading 'gradSchemes'.")

        if not schemes_found["ddtSchemes"]:
            print("Warning: 'ddtSchemes' not found in the file.")

        if not schemes_found["gradSchemes"]:
            print("Warning: 'gradSchemes' not found in the file.")

    def save_fv_schemes(self):
        # Get the selected ddtScheme and gradScheme from the comboboxes
        selected_ddt_scheme = self.ddt_schemes_combobox.currentText()
        selected_grad_scheme = self.grad_schemes_combobox.currentText()

        # Update the fvSchemes file with the edited values
        updated_lines = []
        schemes_found = {"ddtSchemes": False, "gradSchemes": False}
        inside_ddt_schemes_block = False
        inside_grad_schemes_block = False
        with open(self.fv_schemes_path, 'r') as file:
            for line in file:
                if line.startswith("ddtSchemes"):
                    schemes_found["ddtSchemes"] = True
                    inside_ddt_schemes_block = True
                    try:
                        updated_lines.append(f"ddtSchemes\n{{\n    default         {selected_ddt_scheme};\n}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'ddtSchemes'.")
                elif line.startswith("gradSchemes"):
                    schemes_found["gradSchemes"] = True
                    inside_grad_schemes_block = True
                    try:
                        updated_lines.append(f"gradSchemes\n{{\n    default         {selected_grad_scheme};\n    grad(p)         Gauss linear;}}\n")
                        next(file)  # Skip the existing block
                    except IndexError:
                        print("Error: Index out of range while updating 'gradSchemes'.")
                elif inside_ddt_schemes_block and line.strip() == "}":
                    inside_ddt_schemes_block = False
                elif inside_grad_schemes_block and line.strip() == "}":
                    inside_grad_schemes_block = False
                elif not inside_ddt_schemes_block and not inside_grad_schemes_block:
                    updated_lines.append(line)

        if not schemes_found["ddtSchemes"]:
            print("Warning: 'ddtSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\nddtSchemes\n{{\n    default         {selected_ddt_scheme};\n}}\n")

        if not schemes_found["gradSchemes"]:
            print("Warning: 'gradSchemes' not found in the file. Adding it at the end.")
            updated_lines.append(f"\ngradSchemes\n{{\n    default         {selected_grad_scheme};\n}}\n")

        with open(self.fv_schemes_path, 'w') as file:
            file.writelines(updated_lines)

        self.accept()
