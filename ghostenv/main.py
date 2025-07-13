import os
import sys
import tempfile
import shutil
import subprocess
import venv
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

import typer

# --- Globals and Main App ---
app = typer.Typer(
    help="👻 ghostenv: Temporary, disposable virtual environments for testing pip packages."
)

# --- Helper for Formatted Output ---
def _print_panel(title: str, text: str, border_char: str = "-"):
    """A simple replacement for rich.Panel using standard print."""
    lines = text.splitlines()
    width = max(len(title), max(len(line) for line in lines) if lines else 0) + 4
    
    print(f"+{border_char * (width-2)}+")
    print(f"| {title.center(width-4)} |")
    print(f"+{border_char * (width-2)}+")
    for line in lines:
        print(f"| {line.ljust(width-4)} |")
    print(f"+{border_char * (width-2)}+")


# --- State Management ---
@dataclass
class GhostEnvState:
    """A dataclass to hold the state of the ghost environment."""
    temp_dir: Path
    env_path: Path = field(init=False)
    python_executable: Path = field(init=False)
    pip_executable: Path = field(init=False)
    test_script_path: Optional[Path] = None

    def __post_init__(self):
        self.env_path = self.temp_dir / "venv"
        bin_dir = "Scripts" if os.name == 'nt' else "bin"
        self.python_executable = self.env_path / bin_dir / "python"
        self.pip_executable = self.env_path / bin_dir / "pip"

# --- Core Logic Functions ---

def create_virtual_environment(state: GhostEnvState):
    print(f"🔧 Creating virtual environment at {state.env_path}...")
    try:
        venv.create(state.env_path, with_pip=True)
    except Exception as e:
        _print_panel("Error", f"❌ Failed to create virtual environment: {e}")
        raise typer.Exit(code=1)

def _run_pip_command(state: GhostEnvState, cmd: List[str], message: str):
    print(message)
    try:
        subprocess.run(
            cmd, capture_output=True, text=True, check=True, encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        error_text = (f"Failed to run command: `{' '.join(cmd)}`\n\nPip Output:\n{e.stderr}")
        _print_panel("Installation Error", error_text)
        raise typer.Exit(code=1)

def install_packages(state: GhostEnvState, packages: List[str]):
    message = f"📦 Installing packages: {', '.join(packages)}"
    cmd = [str(state.pip_executable), "install"] + packages
    _run_pip_command(state, cmd, message)
    print("✅ Packages installed successfully.")

def install_from_requirements(state: GhostEnvState, requirements_file: Path):
    message = f"📄 Installing from requirements file: {requirements_file}"
    cmd = [str(state.pip_executable), "install", "-r", str(requirements_file)]
    _print_panel("Installation Error", f"Failed to run command: `{' '.join(cmd)}`")
    _run_pip_command(state, cmd, message)
    print("✅ Requirements installed successfully.")

def run_python_script(state: GhostEnvState, script_path: Path):
    print(f"🚀 Running script: {script_path}")
    try:
        result = subprocess.run([str(state.python_executable), str(script_path)], check=False)
        return result.returncode
    except Exception as e:
        _print_panel("Error", f"Failed to run script: {e}")
        return 1

def start_repl(state: GhostEnvState):
    _print_panel("Interactive Session", "🐍 Starting Python REPL. Type `exit()` or `Ctrl+D` to quit.\n" f"Using python from: {state.python_executable}")
    try:
        return os.system(f'"{state.python_executable}"')
    except Exception as e:
        _print_panel("Error", f"Failed to start REPL: {e}")
        return 1

# --- THIS IS THE MODIFIED FUNCTION ---
def create_test_file(state: GhostEnvState, packages: List[str]):
    """Create a test Python file with sample code, ensuring UTF-8 encoding."""
    state.test_script_path = state.temp_dir / "ghost_test.py"
    sample_code = [
        "# Test script for ghostenv",
        "# You can edit this file to test your packages.\n"
    ]
    for pkg in packages:
        pkg_name = pkg.split('==')[0].split('>')[0].split('<')[0].split('[')[0].strip()
        if pkg_name:
            sample_code.append(f"import {pkg_name} # Test import")
    
    # Using standard ASCII for the print statement for maximum compatibility
    sample_code.extend(["", "# Add your test code below!", "print('Script setup complete.')"])
    
    # Crucial Fix: Save the file with explicit UTF-8 encoding
    state.test_script_path.write_text("\n".join(sample_code), encoding='utf-8')
    
    print(f"📝 Test script created at: {state.test_script_path}")


@app.command()
def run(
    packages: Optional[List[str]] = typer.Argument(None, help="Package names to install (e.g., requests pandas)."),
    requirements: Optional[Path] = typer.Option(None, "-r", "--requirements", help="Path to a requirements.txt file.", exists=True, file_okay=True, dir_okay=False, readable=True),
    script: Optional[Path] = typer.Option(None, "--run", help="Python script to run in the environment.", exists=True, file_okay=True, dir_okay=False, readable=True),
    keep: bool = typer.Option(False, "--keep", help="Keep the temporary environment after exiting."),
):
    """Creates a temporary virtual environment, installs packages, and starts a REPL."""
    state = None
    exit_code = 0
    try:
        temp_dir = tempfile.mkdtemp(prefix="ghostenv_")
        state = GhostEnvState(temp_dir=Path(temp_dir))
        _print_panel("ghostenv", f"👻 Created temporary environment in {state.temp_dir}")
        create_virtual_environment(state)

        if not packages and not requirements:
            print("\n❌ Error: You must specify packages to install or a requirements file.")
            print("Example: ghostenv run requests pandas")
            print("Example: ghostenv run -r requirements.txt\n")
            raise typer.Exit(code=1)

        if requirements:
            install_from_requirements(state, requirements)
        if packages:
            install_packages(state, packages)

        if script:
            exit_code = run_python_script(state, script)
        else:
            all_packages = packages or []
            create_test_file(state, all_packages)
            exit_code = start_repl(state)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
        exit_code = 130
    except typer.Exit as e:
        exit_code = e.exit_code
    finally:
        if state:
            if keep:
                activate_cmd = "source bin/activate" if os.name != 'nt' else "Scripts\\activate.bat"
                panel_text = (f"✅ Environment saved at: {state.temp_dir}\n" f"To activate it later, run:\ncd {state.temp_dir} && {activate_cmd}")
                if state.test_script_path:
                    panel_text += f"\n\n📝 Your test script is saved at:\n{state.test_script_path}"
                _print_panel("Environment Kept", panel_text)
            else:
                print("\n🧹 Cleaning up temporary environment...")
                shutil.rmtree(state.temp_dir, ignore_errors=True)
                print("✅ Cleanup complete.")
    sys.exit(exit_code)

@app.command()
def version():
    __version__ = "1.2.0"
    print(f"👻 ghostenv version {__version__}")

if __name__ == "__main__":
    app()
