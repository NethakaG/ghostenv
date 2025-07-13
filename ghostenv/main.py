import os
import sys
import tempfile
import shutil
import subprocess
import venv
import json
from pathlib import Path
from typing import List, Optional

import typer

app = typer.Typer(help="Temporary, disposable virtual environments for testing pip packages")

def check_python_version():
    """Check if Python version is 3.7 or higher."""
    if sys.version_info < (3, 7):
        typer.echo("⚠️  Warning: Python version is below 3.7. Some features may not work correctly.", err=True)
        return False
    return True

def create_virtual_environment(env_path: Path) -> bool:
    """Create a virtual environment at the specified path."""
    try:
        print(f"🔧 Creating virtual environment at {env_path}")
        venv.create(env_path, with_pip=True)
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_python_executable(env_path: Path) -> Path:
    """Get the Python executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return env_path / "Scripts" / "python.exe"
    else:  # Unix-like systems
        return env_path / "bin" / "python"

def get_pip_executable(env_path: Path) -> Path:
    """Get the pip executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return env_path / "Scripts" / "pip.exe"
    else:  # Unix-like systems
        return env_path / "bin" / "pip"

def install_packages(env_path: Path, packages: List[str]) -> bool:
    """Install packages in the virtual environment."""
    pip_executable = get_pip_executable(env_path)
    
    try:
        print(f"📦 Installing packages: {', '.join(packages)}")
        cmd = [str(pip_executable), "install"] + packages
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_from_requirements(env_path: Path, requirements_file: str) -> bool:
    """Install packages from a requirements file."""
    pip_executable = get_pip_executable(env_path)
    
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    try:
        print(f"📦 Installing from requirements file: {requirements_file}")
        cmd = [str(pip_executable), "install", "-r", requirements_file]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print(f"Error output: {e.stderr}")
        return False

def run_script(env_path: Path, script_path: str) -> int:
    """Run a Python script in the virtual environment."""
    python_executable = get_python_executable(env_path)
    
    if not os.path.exists(script_path):
        print(f"❌ Script file not found: {script_path}")
        return 1
    
    try:
        print(f"🚀 Running script: {script_path}")
        cmd = [str(python_executable), script_path]
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to run script: {e}")
        return 1

def detect_ides():
    """Detect available IDEs/editors on the system."""
    ides = []
    
    # Common IDE/editor executables and their display names
    ide_candidates = [
        # VSCode - check multiple possible locations
        ("code", "Visual Studio Code"),
        ("code-insiders", "Visual Studio Code (Insiders)"),
        # PyCharm
        ("pycharm", "PyCharm"),
        ("pycharm64", "PyCharm"),
        # Sublime Text
        ("subl", "Sublime Text"),
        ("sublime_text", "Sublime Text"),
        # Atom
        ("atom", "Atom"),
        # Vim/Neovim
        ("nvim", "Neovim"),
        ("vim", "Vim"),
        # Emacs
        ("emacs", "Emacs"),
        # Notepad++
        ("notepad++", "Notepad++"),
        ("notepad", "Notepad"),
        # IDLE
        ("idle", "IDLE"),
        # Spyder
        ("spyder", "Spyder"),
        ("spyder3", "Spyder"),
    ]
    
    # Check standard PATH first
    for executable, display_name in ide_candidates:
        if shutil.which(executable):
            ides.append((executable, display_name))
    
    # On Windows, check common VSCode installation paths
    if os.name == 'nt':
        vscode_paths = [
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME')),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
        ]
        
        for path in vscode_paths:
            if os.path.exists(path) and not any(ide[0] == path for ide in ides):
                ides.append((path, "Visual Studio Code"))
                break
    
    return ides

def choose_ide():
    """Let user choose which IDE to use."""
    ides = detect_ides()
    
    if not ides:
        print("❌ No supported IDEs found. Falling back to REPL.")
        return None
    
    print("\n📝 Available IDEs/Editors:")
    for i, (executable, display_name) in enumerate(ides, 1):
        print(f"  {i}. {display_name}")
    
    print(f"  {len(ides) + 1}. Python REPL (default)")
    
    while True:
        try:
            choice = input(f"\nChoose IDE (1-{len(ides) + 1}) [default: REPL]: ").strip()
            
            if not choice:  # Default to REPL
                return None
            
            choice_num = int(choice)
            if choice_num == len(ides) + 1:  # REPL option
                return None
            elif 1 <= choice_num <= len(ides):
                return ides[choice_num - 1][0]  # Return executable name
            else:
                print(f"❌ Please enter a number between 1 and {len(ides) + 1}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n🛑 Cancelled by user")
            return None

def create_test_file(temp_dir: Path, packages: List[str]) -> Path:
    """Create a test Python file with sample code for the installed packages."""
    test_file = temp_dir / "test_script.py"
    
    # Generate sample code based on installed packages
    sample_code = []
    sample_code.append("# Test script for ghostenv")
    sample_code.append("# This file will be automatically deleted when you exit\n")
    
    for package in packages:
        if package.lower() == "requests":
            sample_code.extend([
                "import requests",
                "",
                "# Test HTTP requests",
                "response = requests.get('https://httpbin.org/json')",
                "print('Response:', response.json())",
                "print('Status:', response.status_code)",
                ""
            ])
        elif package.lower() == "pandas":
            sample_code.extend([
                "import pandas as pd",
                "",
                "# Test pandas DataFrame",
                "df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})",
                "print('DataFrame:')",
                "print(df)",
                ""
            ])
        elif package.lower() == "numpy":
            sample_code.extend([
                "import numpy as np",
                "",
                "# Test numpy array",
                "arr = np.array([1, 2, 3, 4, 5])",
                "print('Array:', arr)",
                "print('Mean:', np.mean(arr))",
                ""
            ])
        else:
            # Generic import for unknown packages
            sample_code.extend([
                f"import {package}",
                f"print('{package} imported successfully')",
                f"print('{package} version:', getattr({package}, '__version__', 'Unknown'))",
                ""
            ])
    
    sample_code.append("# Add your test code here!")
    sample_code.append("# When you're done testing, this file will be automatically deleted")
    
    with open(test_file, 'w') as f:
        f.write('\n'.join(sample_code))
    
    return test_file

def open_file_in_ide(file_path: Path, ide_executable: str) -> subprocess.Popen:
    """Open a file in the specified IDE."""
    try:
        # Different IDEs have different command line arguments
        if ide_executable in ["code", "code-insiders"]:
            # VSCode: wait for the window to be closed
            return subprocess.Popen([ide_executable, str(file_path), "--wait"])
        elif ide_executable == "subl":
            # Sublime Text: wait for the window to be closed
            return subprocess.Popen([ide_executable, str(file_path), "--wait"])
        else:
            # Generic approach for other editors
            return subprocess.Popen([ide_executable, str(file_path)])
    except Exception as e:
        print(f"❌ Failed to open file in {ide_executable}: {e}")
        return None

def start_repl(env_path: Path) -> int:
    """Start an interactive Python REPL in the virtual environment."""
    python_executable = get_python_executable(env_path)
    
    try:
        print("🐍 Starting Python REPL (type 'exit()' to quit)")
        print(f"Virtual environment: {env_path}")
        print("=" * 50)
        
        # Use os.system for better interactive experience
        if os.name == 'nt':  # Windows
            return os.system(f'"{python_executable}"')
        else:  # Unix-like systems
            return os.system(f'"{python_executable}"')
    except Exception as e:
        print(f"❌ Failed to start REPL: {e}")
        return 1

@app.command()
def run(
    packages: Optional[List[str]] = typer.Argument(None, help="Package names to install"),
    keep: bool = typer.Option(False, "--keep", help="Keep the temporary environment after exit"),
    run_script: Optional[str] = typer.Option(None, "--run", help="Python script to run in the environment"),
    requirements: Optional[str] = typer.Option(None, "--requirements", help="Requirements file to install from"),
    ide: bool = typer.Option(False, "--ide", help="Open test file in IDE instead of REPL")
):
    """Create a temporary virtual environment and install packages."""
    
    # Check Python version
    check_python_version()
    
    # Create temporary directory
    temp_dir = None
    test_file = None
    ide_process = None
    
    try:
        temp_dir = tempfile.mkdtemp(prefix="ghostenv_")
        env_path = Path(temp_dir) / "venv"
        
        print(f"🏗️  Creating temporary environment in: {temp_dir}")
        
        # Create virtual environment
        if not create_virtual_environment(env_path):
            return 1
        
        # Install packages from requirements file if provided
        if requirements:
            if not install_from_requirements(env_path, requirements):
                return 1
        
        # Install specified packages
        if packages:
            if not install_packages(env_path, packages):
                return 1
        elif not requirements:
            # If no packages and no requirements file, show error
            print("❌ Error: You must specify either packages or a requirements file")
            print("Examples:")
            print("  ghostenv run requests")
            print("  ghostenv run --requirements requirements.txt")
            return 1
        
        # Determine what packages were installed (for test file generation)
        installed_packages = packages or []
        
        # Run script, open IDE, or start REPL
        exit_code = 0
        if run_script:
            exit_code = run_script(env_path, run_script)
        elif ide or (packages and not run_script):
            # Create test file with sample code
            test_file = create_test_file(Path(temp_dir), installed_packages)
            print(f"📝 Created test file: {test_file}")
            
            # Choose IDE
            chosen_ide = choose_ide()
            
            if chosen_ide:
                print(f"🚀 Opening test file in {chosen_ide}...")
                ide_process = open_file_in_ide(test_file, chosen_ide)
                
                if ide_process:
                    print("✅ IDE opened successfully!")
                    print("💡 Edit your test file, then close the IDE or press Ctrl+C here when done.")
                    
                    try:
                        # Wait for the IDE process or user interrupt
                        if chosen_ide in ["code", "code-insiders", "subl"]:
                            # These IDEs support --wait flag
                            ide_process.wait()
                        else:
                            # For other IDEs, just wait for user interrupt
                            print("Press Ctrl+C when you're done testing...")
                            while True:
                                import time
                                time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n🛑 Testing session ended by user")
                        if ide_process and ide_process.poll() is None:
                            ide_process.terminate()
                else:
                    print("⚠️  Failed to open IDE, falling back to REPL")
                    exit_code = start_repl(env_path)
            else:
                print("⚠️  No IDE selected, falling back to REPL")
                exit_code = start_repl(env_path)
        else:
            exit_code = start_repl(env_path)
        
        # Handle cleanup or keeping the environment
        if keep:
            print(f"🔒 Environment saved at: {temp_dir}")
            print(f"To activate later: {env_path}\\Scripts\\activate.bat (Windows) or source {env_path}/bin/activate (Linux/Mac)")
            if test_file:
                print(f"📝 Test file saved at: {test_file}")
        else:
            print("🧹 Cleaning up temporary environment...")
            shutil.rmtree(temp_dir)
            print("✅ Cleanup complete")
            
        return exit_code
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        if ide_process and ide_process.poll() is None:
            ide_process.terminate()
        if temp_dir and not keep:
            print("🧹 Cleaning up...")
            shutil.rmtree(temp_dir, ignore_errors=True)
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if ide_process and ide_process.poll() is None:
            ide_process.terminate()
        if temp_dir and not keep:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return 1

@app.command()
def version():
    """Show version information."""
    from ghostenv import __version__
    print(f"ghostenv version {__version__}")

if __name__ == "__main__":
    app()