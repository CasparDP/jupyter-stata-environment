# Quick Command Reference

## Setup (First Time Only)
```bash
# Clone template
git clone https://github.com/yourusername/repo-name.git
cd repo-name

# Run setup
python setup.py
```

## Daily Use

### Start Jupyter Server
```bash
# Windows
start_jupyter.bat

# Mac/Linux
./start_jupyter.sh

# Any OS
poetry run jupyter lab
```

### Access in Browser
Open: http://localhost:8888

### Access in VSCode
1. Start server (above)
2. Open notebook
3. Select Kernel → Existing Jupyter Server
4. Enter: http://localhost:8888
5. Choose Stata kernel

## NBGrader Commands

### For Instructors
```bash
# Create assignment
poetry run jupyter lab source/my_assignment.ipynb

# Generate student version
poetry run nbgrader generate_assignment my_assignment --force

# Grade submissions
poetry run nbgrader autograde my_assignment --force

# Export grades
poetry run nbgrader export
```

### For Students
```bash
# Work on assignment
poetry run jupyter lab assignments/my_assignment.ipynb

# Validate before submitting
poetry run nbgrader validate my_assignment.ipynb
```

## Common Tasks

### Install New Package
```bash
poetry add package-name
```

### Update All Packages
```bash
poetry update
```

### List Installed Kernels
```bash
poetry run jupyter kernelspec list
```

### Clear Jupyter Cache
```bash
poetry run jupyter lab clean
```

## Stata in Notebooks

### Pure Stata Notebook
Select "Stata" kernel when creating notebook

### Python Notebook with Stata
```python
# Load extension
%load_ext nbstata

# Run Stata code
%%stata
sysuse auto
summarize
```

## Keyboard Shortcuts

### Jupyter Lab
- `Shift + Enter` - Run cell and move to next
- `Ctrl/Cmd + Enter` - Run cell and stay
- `Esc` then `A` - Insert cell above
- `Esc` then `B` - Insert cell below
- `Esc` then `DD` - Delete cell
- `Esc` then `M` - Change to Markdown
- `Esc` then `Y` - Change to Code

### VSCode
- `Ctrl/Cmd + Enter` - Run cell
- `Shift + Enter` - Run cell and move to next
- `Ctrl/Cmd + Shift + P` - Command palette
- `Ctrl/Cmd + K` then `V` - Markdown preview

## Troubleshooting

### Stata Kernel Missing
```bash
export STATA_PATH="/path/to/stata"  # Mac/Linux
set STATA_PATH="C:\path\to\stata.exe"  # Windows
poetry run python -m nbstata.install
```

### Server Won't Start
```bash
# Kill existing servers
jupyter notebook stop

# Try different port
poetry run jupyter lab --port=8889
```

### VSCode Can't Find Kernel
Always use "Existing Jupyter Server" method with http://localhost:8888
