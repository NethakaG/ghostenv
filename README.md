# ghostenv 👻  
Temporary, disposable virtual environments for testing pip packages

⚠️ Development Status: This project is still in active development and may contain bugs or unexpected behavior. Use with caution in production environments.

---

## What is ghostenv?  
ghostenv is a command-line tool that creates temporary, isolated Python virtual environments for quickly testing pip packages without cluttering your system or main development environment. Perfect for:

- Testing new packages before adding them to your project  
- Experimenting with different package versions  
- Running one-off scripts with specific dependencies  
- Learning new libraries in a clean environment  

---

## Features  
🚀 Quick package testing – Install and test packages in seconds  
🧹 Automatic cleanup – Environments are deleted by default (unless you choose to keep them)  
📝 Smart test file generation – Creates sample code for common packages  
🐍 Interactive REPL – Drop into a Python shell with packages pre-installed  
📦 Requirements file support – Install from requirements.txt  
🖥️ Cross-platform – Works on Windows, macOS, and Linux  

⚠️ Note: All testing currently happens in REPL only. Ghostenv no longer opens files in an IDE.

---

## Installation  
⚠️ Note: This package is not yet published to PyPI. For now, you'll need to install from source.

### Install from source
```bash
git clone https://github.com/yourusername/ghostenv.git  
cd ghostenv  
pip install -e .
```

### Future PyPI installation (not available yet)
```bash
# This will work once published to PyPI  
pip install ghostenv
```

---

## Quick Start

### Test a single package
```bash
ghostenv run requests
```

### Test multiple packages
```bash
ghostenv run requests pandas numpy
```

### Install from requirements file
```bash
ghostenv run --requirements requirements.txt
```

### Run a specific script
```bash
ghostenv run requests --run my_script.py
```

### Keep the environment after testing
```bash
ghostenv run pandas --keep
```

---

## Usage

### Basic Commands
```bash
ghostenv run [PACKAGES] [OPTIONS]  
ghostenv version
```

### Options
- `--keep` – Keep the temporary environment after exit  
- `--run SCRIPT` – Python script to run in the environment  
- `--requirements FILE` – Requirements file to install from  
- `--help` – Show help message  

---

## Examples

### Quick package exploration
```bash
# Test requests library  
ghostenv run requests
```

This will:  
- Create a temporary virtual environment  
- Install `requests`  
- Generate a test file with sample HTTP requests  
- Launch an interactive Python REPL  
- Clean up when you're done  

### Development workflow
```bash
# Test dependencies for a new project  
ghostenv run flask sqlalchemy pytest --keep
```

With `--keep`, you can:  
- Test your packages  
- Copy working code to your main project  
- Activate the environment later if needed  

### Script testing
```bash
# Run a script with specific dependencies  
ghostenv run beautifulsoup4 lxml --run scraper.py
```

---

## Smart Test File Generation

When you install packages, ghostenv creates a test file with relevant sample code:

### For `requests`:
```python
import requests

# Test HTTP requests
response = requests.get('https://httpbin.org/json')
print('Response:', response.json())
print('Status:', response.status_code)
```

### For `pandas`:
```python
import pandas as pd

# Test pandas DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print('DataFrame:')
print(df)
```

### For `numpy`:
```python
import numpy as np

# Test numpy array
arr = np.array([1, 2, 3, 4, 5])
print('Array:', arr)
print('Mean:', np.mean(arr))
```

---

## Development Status & Known Issues

⚠️ This project is still in development. Known limitations:

- Limited test file templates (currently supports requests, pandas, numpy)  
- Some package installations may fail due to system dependencies  
- Windows path handling may need improvements  
- Error messages could be more informative  
- Only supports REPL — IDE launching is not available in this version  

---

## Contributing  
This project is in early development and contributions are welcome! Areas that need work:

- More comprehensive test file templates  
- Better error handling and user feedback  
- Package dependency resolution  
- Configuration file support  
- Better Windows compatibility  

---

## License  

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for full details.

---

## Changelog

**Current Version**  
- Initial release with basic functionality  
- Support for package installation  
- Automatic cleanup and keep options  
- Requirements file support  

> Note: This tool creates temporary directories and virtual environments. Always review the packages you're installing and be cautious with unknown or untrusted packages.
