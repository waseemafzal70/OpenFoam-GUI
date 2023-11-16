from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit


class EditControlDictWindow(QDialog):
    def __init__(self, control_dict_path):
        super().__init__()
        self.setWindowTitle("Edit controlDict")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.start_time_label = QLabel("Start Time:")
        self.start_time_edit = QLineEdit()
        self.layout.addWidget(self.start_time_label)
        self.layout.addWidget(self.start_time_edit)

        self.end_time_label = QLabel("End Time:")
        self.end_time_edit = QLineEdit()
        self.layout.addWidget(self.end_time_label)
        self.layout.addWidget(self.end_time_edit)

        self.delta_t_label = QLabel("Delta T:")
        self.delta_t_edit = QLineEdit()
        self.layout.addWidget(self.delta_t_label)
        self.layout.addWidget(self.delta_t_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_control_dict)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.control_dict_path = control_dict_path

        # Load and display the current values of startTime, endTime, and deltaT
        self.load_control_dict_values()

    def load_control_dict_values(self):
        with open(self.control_dict_path, 'r') as file:
            for line in file:
                if line.startswith("startTime"):
                    self.start_time_edit.setText(line.split()[1].strip(';'))
                elif line.startswith("endTime"):
                    self.end_time_edit.setText(line.split()[1].strip(';'))
                elif line.startswith("deltaT"):
                    self.delta_t_edit.setText(line.split()[1].strip(';'))

    def save_control_dict(self):
        # Read the user's input for startTime, endTime, and deltaT
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()
        delta_t = self.delta_t_edit.text()

        # Update the controlDict file with the edited values
        updated_lines = []
        with open(self.control_dict_path, 'r') as file:
            for line in file:
                if line.startswith("startTime"):
                    updated_lines.append(f"startTime {start_time};\n")
                elif line.startswith("endTime"):
                    updated_lines.append(f"endTime {end_time};\n")
                elif line.startswith("deltaT"):
                    updated_lines.append(f"deltaT {delta_t};\n")
                else:
                    updated_lines.append(line)

        with open(self.control_dict_path, 'w') as file:
            file.writelines(updated_lines)

        self.accept()
