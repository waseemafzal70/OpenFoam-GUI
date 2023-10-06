# OpenFOAM GUI with PyQt6 for Windows using WSL

This project aims to create a graphical user interface (GUI) for OpenFOAM, a popular open-source computational fluid dynamics (CFD) software, using PyQt6 on the Windows operating system with the Windows Subsystem for Linux (WSL). This GUI provides an intuitive way to interact with OpenFOAM, making it easier for users to set up and run simulations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [WSL Installation](#wsl-installation)
  - [OpenFOAM Installation](#openfoam-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before running this project, make sure you have the following prerequisites installed on your system:

1. Windows 10 or later (64-bit).
2. Windows Subsystem for Linux (WSL) with Ubuntu or a compatible Linux distribution installed. You can follow the official Microsoft documentation to set up WSL: [Windows Subsystem for Linux Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install).
3. OpenFOAM already installed in your WSL environment. You can install OpenFOAM by following the instructions below.

## Installation

### WSL Installation

You can install WSL with a single command. Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting "Run as administrator," then enter the following command:

```bash
wsl --install
```

After running this command, restart your machine.

### OpenFOAM Installation

To install OpenFOAM in your WSL environment, follow these steps:

1. Add the OpenFOAM repository:

   ```bash
   curl https://dl.openfoam.com/add-debian-repo.sh | sudo bash
   ```

2. Update the repository information:

   ```bash
   sudo apt-get update
   ```

3. Install your preferred OpenFOAM package. For example:

   ```bash
   sudo apt-get install openfoam2306-default
   ```

4. Use the OpenFOAM shell session:

   ```bash
   openfoam2306
   ```

## Usage

To run the OpenFOAM GUI with PyQt6 on Windows using WSL in PyCharm, follow these steps:

1. Open PyCharm and navigate to the project directory where you cloned this repository.

2. Install the required Python packages:

   ```bash
   pip install PyQt6
   ```

3. Run the GUI application:

   - Open the `main.py` file in PyCharm.
   - Click the "Run" button or use the keyboard shortcut to execute the script.

4. The GUI application will open, allowing you to interact with OpenFOAM. You can use it to set up and run simulations.

## Contributing

We welcome contributions to this project. If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/new-feature
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push your changes to your fork:

   ```bash
   git push origin feature/new-feature
   ```

5. Create a pull request from your fork to the main repository, explaining your changes and why they are necessary.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it according to the terms of the license.
