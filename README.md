ghostenv 👻
Temporary, disposable virtual environments for testing pip packages

⚠️ Development Status: This project is still in active development and may contain bugs or unexpected behavior. Use with caution in production environments.

What is ghostenv?
ghostenv is a command-line tool that creates temporary, isolated Python virtual environments for quickly testing pip packages without cluttering your system or main development environment. Perfect for:

Testing new packages before adding them to your project
Experimenting with different package versions
Running one-off scripts with specific dependencies
Learning new libraries in a clean environment

Features

🚀 Quick package testing - Install and test packages in seconds
🧹 Automatic cleanup - Environments are deleted by default (unless you choose to keep them)
📝 Smart test file generation - Creates sample code for common packages
🔧 IDE integration - Opens test files in your preferred editor
📦 Requirements file support - Install from requirements.txt
🐍 Interactive REPL - Drop into a Python shell with packages pre-installed
🖥️ Cross-platform - Works on Windows, macOS, and Linux

Installation

⚠️ Note: This package is not yet published to PyPI. For now, you'll need to install from source.

Install from source
bashgit clone https://github.com/yourusername/ghostenv.git
cd ghostenv
pip install -e .
Future PyPI installation (not available yet)
bash# This will work once published to PyPI
pip install ghostenv
Quick Start
Test a single package
bashghostenv run requests
Test multiple packages
bashghostenv run requests pandas numpy
Install from requirements file
bashghostenv run --requirements requirements.txt
Run a specific script
bashghostenv run requests --run my_script.py
Keep the environment after testing
bashghostenv run pandas --keep
Open test file in IDE
bashghostenv run matplotlib --ide
Usage
Basic Commands
bashghostenv run [PACKAGES] [OPTIONS]
ghostenv version
Options

--keep - Keep the temporary environment after exit
--run SCRIPT - Python script to run in the environment
--requirements FILE - Requirements file to install from
--ide - Open test file in IDE instead of REPL
--help - Show help message

Examples
Quick package exploration
bash# Test requests library
ghostenv run requests

# This will:

# 1. Create a temporary virtual environment

# 2. Install requests

# 3. Generate a test file with sample HTTP requests

# 4. Open your preferred IDE or Python REPL

# 5. Clean up when you're done

Development workflow
bash# Test dependencies for a new project
ghostenv run flask sqlalchemy pytest --keep

# The --keep flag saves the environment so you can:

# 1. Test your packages

# 2. Copy working code to your main project

# 3. Activate the environment later if needed

Script testing
bash# Run a script with specific dependencies
ghostenv run beautifulsoup4 lxml --run scraper.py
Supported IDEs
ghostenv automatically detects and supports these editors:

Visual Studio Code (code, code-insiders)
PyCharm (pycharm, pycharm64)
Sublime Text (subl)
Atom (atom)
Vim/Neovim (vim, nvim)
Emacs (emacs)
Notepad++ (notepad++)
IDLE (idle)
Spyder (spyder)

If no IDE is found or selected, ghostenv falls back to an interactive Python REPL.
Smart Test File Generation
When you install packages, ghostenv creates a test file with relevant sample code:
For requests:
pythonimport requests

# Test HTTP requests

response = requests.get('https://httpbin.org/json')
print('Response:', response.json())
print('Status:', response.status_code)
For pandas:
pythonimport pandas as pd

# Test pandas DataFrame

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print('DataFrame:')
print(df)
For numpy:
pythonimport numpy as np

# Test numpy array

arr = np.array([1, 2, 3, 4, 5])
print('Array:', arr)
print('Mean:', np.mean(arr))
Requirements

Python 3.7 or higher
pip (included with Python)

Development Status & Known Issues
⚠️ This project is still in development. Known limitations:

Limited test file templates (currently supports requests, pandas, numpy)
IDE detection may not work on all systems
Some package installations may fail due to system dependencies
Windows path handling may need improvements
Error messages could be more informative

Contributing
This project is in early development and contributions are welcome! Areas that need work:

More comprehensive test file templates
Better error handling and user feedback
Improved IDE detection
Package dependency resolution
Configuration file support
Better Windows compatibility

License
[Add your license here]
Changelog
Current Version

Initial release with basic functionality
Support for package installation and IDE integration
Automatic cleanup and keep options
Requirements file support

Note: This tool creates temporary directories and virtual environments. Always review the packages you're installing and be cautious with unknown or untrusted packages.
