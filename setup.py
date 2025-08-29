#!/usr/bin/env python
"""
Universal Setup Script for Jupyter-Stata Environment
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path


class JupyterStataSetup:
    def __init__(self):
        self.system = platform.system()
        self.stata_path = None
        self.env_path = None
        
    def run_command(self, command, shell=False):
        """Run a shell command and return the result."""
        try:
            if isinstance(command, str):
                command = command.split()
            result = subprocess.run(
                command, 
                shell=shell, 
                check=True, 
                capture_output=True, 
                text=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except FileNotFoundError:
            return False, "Command not found"
    
    def check_python(self):
        """Check Python version."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            print(f"❌ Python {version.major}.{version.minor} detected. Python 3.9+ is required!")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def check_poetry(self):
        """Check if Poetry is installed."""
        success, output = self.run_command("poetry --version")
        if not success:
            print("❌ Poetry is not installed!")
            print("\nTo install Poetry:")
            if self.system == "Windows":
                print("  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -")
            else:
                print("  curl -sSL https://install.python-poetry.org | python3 -")
            print("\nOr visit: https://python-poetry.org/docs/#installation")
            return False
        print(f"✅ {output}")
        return True
    
    def find_stata(self):
        """Try to find Stata installation."""
        stata_paths = {
            "Darwin": [  # macOS
                "/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp",
                "/Applications/Stata/StataSE.app/Contents/MacOS/stata-se",
                "/Applications/Stata/StataBE.app/Contents/MacOS/stata",
                "/Applications/Stata/Stata.app/Contents/MacOS/stata",
                "/Applications/StataMP.app/Contents/MacOS/stata-mp",
                "/Applications/StataSE.app/Contents/MacOS/stata-se",
                "/Applications/StataBE.app/Contents/MacOS/stata",
                "/Applications/Stata.app/Contents/MacOS/stata",
            ],
            "Linux": [
                "/usr/local/stata18/stata-mp",
                "/usr/local/stata18/stata-se",
                "/usr/local/stata18/stata",
                "/usr/local/stata17/stata-mp",
                "/usr/local/stata17/stata-se",
                "/usr/local/stata17/stata",
                "/usr/local/stata16/stata-mp",
                "/usr/local/stata16/stata-se",
                "/usr/local/stata16/stata",
                "/usr/local/stata/stata-mp",
                "/usr/local/stata/stata-se",
                "/usr/local/stata/stata",
                "/opt/stata/stata-mp",
                "/opt/stata/stata-se",
                "/opt/stata/stata",
            ],
            "Windows": [
                r"C:\Program Files\Stata18\StataMP-64.exe",
                r"C:\Program Files\Stata18\StataSE-64.exe",
                r"C:\Program Files\Stata18\Stata-64.exe",
                r"C:\Program Files\Stata17\StataMP-64.exe",
                r"C:\Program Files\Stata17\StataSE-64.exe",
                r"C:\Program Files\Stata17\Stata-64.exe",
                r"C:\Program Files\Stata16\StataMP-64.exe",
                r"C:\Program Files\Stata16\StataSE-64.exe",
                r"C:\Program Files\Stata16\Stata-64.exe",
                r"C:\Program Files (x86)\Stata18\StataMP.exe",
                r"C:\Program Files (x86)\Stata18\StataSE.exe",
                r"C:\Program Files (x86)\Stata18\Stata.exe",
                r"C:\Program Files (x86)\Stata17\StataMP.exe",
                r"C:\Program Files (x86)\Stata17\StataSE.exe",
                r"C:\Program Files (x86)\Stata17\Stata.exe",
            ]
        }
        
        if self.system in stata_paths:
            for path in stata_paths[self.system]:
                if Path(path).exists():
                    return path
        return None
    
    def install_dependencies(self):
        """Install Python dependencies via Poetry."""
        print("\n📦 Installing dependencies...")
        success, output = self.run_command("poetry install")
        if success:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(output)
            return False
    
    def get_poetry_env(self):
        """Get Poetry environment path."""
        success, output = self.run_command("poetry env info --path")
        if success:
            self.env_path = output
            return output
        return None
    
    def setup_stata_kernel(self):
        """Configure nbstata with Stata path."""
        if not self.stata_path:
            self.stata_path = self.find_stata()
        
        if not self.stata_path:
            print("\n⚠️  Stata installation not found automatically")
            print("Please enter the full path to your Stata executable:")
            if self.system == "Windows":
                print("  Example: C:\\Program Files\\Stata17\\StataMP-64.exe")
            elif self.system == "Darwin":
                print("  Example: /Applications/Stata/StataMP.app/Contents/MacOS/stata-mp")
            else:
                print("  Example: /usr/local/stata17/stata-mp")
            
            user_path = input("Stata path (or press Enter to skip): ").strip()
            if user_path and Path(user_path).exists():
                self.stata_path = user_path
            else:
                print("⚠️  Skipping Stata configuration")
                return False
        
        print(f"\n🔧 Configuring nbstata with Stata at: {self.stata_path}")
        
        # Set environment variable
        os.environ["STATA_PATH"] = self.stata_path
        
        # Try to install kernel
        success, output = self.run_command("poetry run python -m nbstata.install")
        
        if success or "already exists" in output.lower():
            print("✅ Stata kernel installed")
            return True
        else:
            print("⚠️  Could not install Stata kernel automatically")
            return False
    
    def create_vscode_config(self):
        """Create VSCode configuration."""
        if not self.env_path:
            self.env_path = self.get_poetry_env()
        
        if not self.env_path:
            return
        
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        # Determine Python path based on OS
        if self.system == "Windows":
            python_path = str(Path(self.env_path) / "Scripts" / "python.exe")
        else:
            python_path = str(Path(self.env_path) / "bin" / "python")
        
        settings = {
            "python.defaultInterpreterPath": python_path,
            "jupyter.jupyterServerType": "local",
            "notebook.kernelPicker.type": "all",
            "files.exclude": {
                "**/__pycache__": True,
                "**/.ipynb_checkpoints": True,
                "**/*.pyc": True
            }
        }
        
        # Add Stata path to environment if available
        if self.stata_path:
            for os_type in ["osx", "linux", "windows"]:
                settings[f"terminal.integrated.env.{os_type}"] = {
                    "STATA_PATH": self.stata_path
                }
        
        settings_file = vscode_dir / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(f"✅ Created VSCode configuration in {settings_file}")
    
    def create_jupyter_config(self):
        """Create Jupyter configuration for easy server start."""
        config_content = """c = get_config()  # noqa

# Jupyter Lab configuration
c.ServerApp.open_browser = False
c.ServerApp.port = 8888
c.ServerApp.ip = '127.0.0.1'

# Automatically set token (optional - remove for security)
# c.ServerApp.token = 'your-secret-token'

# Enable nbgrader extensions
c.ServerApp.jpserver_extensions = {
    'nbgrader': True
}
"""
        
        config_file = Path("jupyter_lab_config.py")
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print("✅ Created Jupyter Lab configuration")
    
    def create_start_scripts(self):
        """Create platform-specific start scripts."""
        
        # Unix/Mac script
        unix_script = """#!/bin/bash
# Start Jupyter Lab server

echo "Starting Jupyter Lab server..."
echo "="*50

# Set Stata path if available
if [ -f .stata_path ]; then
    export STATA_PATH=$(cat .stata_path)
    echo "Stata path: $STATA_PATH"
fi

# Start server
poetry run jupyter lab --config=jupyter_lab_config.py

echo ""
echo "Server stopped."
"""
        
        # Windows script
        windows_script = """@echo off
REM Start Jupyter Lab server

echo Starting Jupyter Lab server...
echo ==================================================

REM Set Stata path if available
if exist .stata_path (
    set /p STATA_PATH=<.stata_path
    echo Stata path: %STATA_PATH%
)

REM Start server
poetry run jupyter lab --config=jupyter_lab_config.py

echo.
echo Server stopped.
pause
"""
        
        # PowerShell script
        ps_script = """# Start Jupyter Lab server

Write-Host "Starting Jupyter Lab server..." -ForegroundColor Green
Write-Host ("=" * 50)

# Set Stata path if available
if (Test-Path .stata_path) {
    $env:STATA_PATH = Get-Content .stata_path
    Write-Host "Stata path: $env:STATA_PATH"
}

# Start server
poetry run jupyter lab --config=jupyter_lab_config.py

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
"""
        
        # Create scripts
        with open("start_jupyter.sh", 'w', newline='\n') as f:
            f.write(unix_script)
        
        with open("start_jupyter.bat", 'w', newline='\r\n') as f:
            f.write(windows_script)
        
        with open("start_jupyter.ps1", 'w', newline='\r\n') as f:
            f.write(ps_script)
        
        # Make Unix script executable
        if self.system != "Windows":
            os.chmod("start_jupyter.sh", 0o755)
        
        print("✅ Created start scripts")
    
    def save_stata_path(self):
        """Save Stata path for future use."""
        if self.stata_path:
            with open(".stata_path", 'w') as f:
                f.write(self.stata_path)
    
    def show_next_steps(self):
        """Show user what to do next."""
        print("\n" + "="*60)
        print("✨ Setup Complete!")
        print("="*60)
        
        print("\n📋 Quick Start Guide:")
        print("-" * 40)
        
        print("\n1️⃣  Start Jupyter Lab server:")
        if self.system == "Windows":
            print("   Option A: Double-click 'start_jupyter.bat'")
            print("   Option B: Run in PowerShell: .\\start_jupyter.ps1")
            print("   Option C: Run in terminal: poetry run jupyter lab")
        else:
            print("   Option A: Run: ./start_jupyter.sh")
            print("   Option B: Run: poetry run jupyter lab")
        
        print("\n2️⃣  Access Jupyter Lab:")
        print("   Open browser: http://localhost:8888")
        print("   (Copy the token from the terminal if prompted)")
        
        print("\n3️⃣  For VSCode users:")
        print("   • Open a notebook (.ipynb file)")
        print("   • Click kernel selector (top-right)")
        print("   • Choose: Select Another Kernel → Existing Jupyter Server")
        print("   • Enter: http://localhost:8888")
        print("   • Enter the token if prompted")
        print("   • Select the Stata kernel")
        
        print("\n📚 Documentation:")
        print("   • README.md - General documentation")
        print("   • QUICK_START.md - Quick reference")
        print("   • examples/ - Example notebooks")
        
        if self.stata_path:
            print(f"\n✅ Stata configured at: {self.stata_path}")
        else:
            print("\n⚠️  Stata not configured - you can set it up later")
        
        print("\n" + "="*60)
    
    def run(self):
        """Run the complete setup."""
        print("="*60)
        print("Jupyter-Stata Environment Setup")
        print(f"OS: {self.system}")
        print("="*60)
        
        # Check prerequisites
        if not self.check_python():
            return False
        
        if not self.check_poetry():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            print("\n⚠️  Setup incomplete. Please check the errors above.")
            return False
        
        # Get Poetry environment
        self.get_poetry_env()
        
        # Setup Stata (optional)
        self.setup_stata_kernel()
        
        # Save Stata path
        self.save_stata_path()
        
        # Create configurations
        self.create_vscode_config()
        self.create_jupyter_config()
        self.create_start_scripts()
        
        # Show next steps
        self.show_next_steps()
        
        return True


def main():
    setup = JupyterStataSetup()
    success = setup.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
