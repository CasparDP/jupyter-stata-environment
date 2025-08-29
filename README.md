# Jupyter-Stata Environment Template

A cross-platform template for Jupyter Lab with Stata kernel and NBGrader support. Works reliably on Windows, macOS, and Linux.

## 🚀 Quick Start (All Operating Systems)

### 1. Create Your Repository from Template

Click "Use this template" on GitHub to create your own repository, then clone it:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Run Setup

```bash
python setup.py
```

This will:

- Check Python version (3.9+ required)
- Install all dependencies via Poetry
- Configure Stata integration (if Stata is installed)
- Create start scripts for your OS
- Set up VSCode configuration

### 3. Start Jupyter Lab

#### Windows

```batch
:: Double-click start_jupyter.bat
:: Or run in terminal:
start_jupyter.bat
```

#### macOS/Linux

```bash
./start_jupyter.sh
```

#### Any OS

```bash
poetry run jupyter lab
```

### 4. Access Jupyter Lab

Open your browser: **http://localhost:8888**

## 📝 Using with VSCode (Recommended Method)

The most reliable way to use Stata notebooks in VSCode:

1. **Start the Jupyter server** (see step 3 above)
2. **In VSCode:**
   - Open any `.ipynb` file
   - Click the kernel selector (top-right corner)
   - Choose **"Select Another Kernel..."**
   - Choose **"Existing Jupyter Server..."**
   - Enter: `http://localhost:8888`
   - Copy/paste the token if prompted (shown in terminal)
   - Select **"Stata"** kernel

## 📚 What's Included

### Core Features

- **Jupyter Lab** with extensions
- **Stata kernel** support via nbstata
- **NBGrader** for assignments and auto-grading
- **Cross-platform** scripts (Windows, macOS, Linux)
- **VSCode** configuration

### Python Packages

- Data Science: pandas, numpy, scipy, matplotlib, seaborn, statsmodels
- Development: black, flake8, pytest, mypy
- Jupyter: jupyterlab, ipykernel, nbgrader, nbstata

### Directory Structure

```
your-project/
├── notebooks/          # Your working notebooks
├── examples/           # Example notebooks
├── source/            # NBGrader source assignments
├── release/           # NBGrader student versions
├── submitted/         # NBGrader submissions
├── autograded/        # NBGrader graded assignments
└── feedback/          # NBGrader feedback
```

## 🎓 Creating Assignments with NBGrader

### Quick Example

1. **Create an assignment:**

   ```bash
   poetry run jupyter lab
   # Create new notebook in source/ folder
   # Add nbgrader metadata via View → Cell Toolbar → Create Assignment
   ```

2. **Generate student version:**

   ```bash
   poetry run nbgrader generate_assignment assignment_name --force
   ```

3. **Grade submissions:**
   ```bash
   poetry run nbgrader autograde assignment_name --force
   ```

See `examples/` folder for sample assignments.

## 💻 System Requirements

### Required

- **Python** 3.9 or higher
- **Poetry** (will be installed if missing)
- **Git** (to clone the template)

### Optional

- **Stata** (14 or higher) for Stata kernel
- **VSCode** with Jupyter extension

## 🔧 Troubleshooting

### Stata Kernel Not Found

1. Make sure Stata is installed
2. Re-run setup: `python setup.py`
3. Or set manually: `export STATA_PATH="/path/to/stata"`

### VSCode Kernel Issues

Always use the **"Existing Jupyter Server"** method described above - it's the most reliable approach.

### Port Already in Use

Change the port in `jupyter_lab_config.py`:

```python
c.ServerApp.port = 8889  # Or another port
```

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick command reference
- **[examples/](examples/)** - Example notebooks
- **[NBGRADER_GUIDE.md](NBGRADER_GUIDE.md)** - NBGrader with Stata guide

## 🔄 Updating Dependencies

```bash
# Update all packages
poetry update

# Add new package
poetry add package-name

# Add dev dependency
poetry add --group dev package-name
```

## 🤝 Contributing

This is a template repository. Feel free to:

1. Fork it
2. Create your own version
3. Submit improvements via pull requests

## 📄 License

This template is provided free for educational use. Stata is proprietary software and requires a separate license.

## ✨ Tips for New Courses

When starting a new course:

1. Click "Use this template" on GitHub
2. Name it after your course (e.g., "eco101-fall2024")
3. Clone and run `python setup.py`
4. Start creating assignments in the `source/` folder
5. Share the repository with students (they clone and run setup)

## 🆘 Need Help?

1. Check the [documentation](QUICK_START.md)
2. Look at [examples](examples/)
3. Create an issue on GitHub

## 🤖 AI Disclosures

This template was crafted with a little help from Claude (my friendly AI assistant) and a dash of wisdom from running the course last year. If you spot anything clever, it was probably Claude. If you spot any mistakes, well... that's probably me!
