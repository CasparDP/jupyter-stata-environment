# Getting Stata Kernel to Work in VSCode

## Quick Fix

Run this command to configure VSCode:
```bash
poetry run python fix_vscode_kernel.py
```

Then restart VSCode completely.

## Manual Setup (if the script doesn't work)

### 1. Get the Poetry Environment Python Path

```bash
# Find the Poetry environment path
poetry env info --path

# This will output something like:
# /Users/casparm4/Library/Caches/pypoetry/virtualenvs/jupyter-stata-environment-IHKJBeOb-py3.13
```

### 2. Set VSCode to Use the Correct Python Interpreter

1. Open VSCode in the project folder
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type: `Python: Select Interpreter`
4. Choose: **Enter interpreter path...**
5. Browse to or paste: `[POETRY_ENV_PATH]/bin/python`
   
   For example:
   ```
   /Users/casparm4/Library/Caches/pypoetry/virtualenvs/jupyter-stata-environment-IHKJBeOb-py3.13/bin/python
   ```

### 3. Install Stata Kernel for the Poetry Environment

```bash
# Activate the environment
poetry shell

# Set Stata path
export STATA_PATH="/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp"

# Install the kernel
python -m nbstata.install

# Verify it's installed
jupyter kernelspec list
```

### 4. Create VSCode Workspace Settings

Create a file `.vscode/settings.json` with:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "jupyter.jupyterServerType": "local",
  "notebook.kernelPicker.type": "all",
  "terminal.integrated.env.osx": {
    "STATA_PATH": "/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp"
  },
  "terminal.integrated.env.linux": {
    "STATA_PATH": "/usr/local/stata17/stata-mp"
  },
  "terminal.integrated.env.windows": {
    "STATA_PATH": "C:\\Program Files\\Stata17\\StataMP-64.exe"
  }
}
```

### 5. Install Jupyter Extension in VSCode

Make sure you have the Jupyter extension installed:
1. Open VSCode Extensions (Cmd+Shift+X / Ctrl+Shift+X)
2. Search for "Jupyter"
3. Install the official Microsoft Jupyter extension

### 6. Restart VSCode

**Important**: Completely quit and restart VSCode (don't just reload the window).

### 7. Select the Kernel in a Notebook

1. Open any `.ipynb` file
2. In the top-right corner, click on the kernel selector (might say "Python 3.x.x")
3. Choose **"Select Another Kernel..."**
4. Choose **"Jupyter Kernel..."**
5. Look for **"Stata"** or **"Stata (Poetry)"**

## Alternative: Use Jupyter Server

If the kernel still doesn't show up, you can connect VSCode to a running Jupyter server:

### Terminal 1: Start Jupyter Server
```bash
poetry run jupyter lab --no-browser
```

Copy the URL with the token (like `http://localhost:8888/lab?token=...`)

### In VSCode:
1. Open a notebook
2. Click the kernel selector
3. Choose **"Select Another Kernel..."**
4. Choose **"Existing Jupyter Server..."**
5. Paste the URL from Terminal 1
6. Now the Stata kernel should be available

## Troubleshooting

### Kernel Not Showing Up

1. **Check kernel is installed for the right Python:**
   ```bash
   poetry run jupyter kernelspec list
   ```
   Should show `stata` kernel.

2. **Check VSCode is using the right Python:**
   - Bottom-left of VSCode should show the Poetry environment Python
   - If not, use `Python: Select Interpreter` again

3. **Clear VSCode cache:**
   - Press Cmd+Shift+P / Ctrl+Shift+P
   - Run: `Jupyter: Clear Cache and Restart`

4. **Check kernel.json location:**
   ```bash
   # Find where the kernel is installed
   poetry run jupyter kernelspec list
   
   # Check the kernel.json file
   cat ~/.local/share/jupyter/kernels/stata/kernel.json
   ```

### Environment Variable Issues

VSCode might not pick up the `STATA_PATH` variable. You can:

1. **Set it in your shell profile** (`~/.zshrc` or `~/.bashrc`):
   ```bash
   export STATA_PATH="/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp"
   ```

2. **Or modify the kernel.json directly:**
   ```bash
   # Find kernel location
   poetry run jupyter kernelspec list
   
   # Edit the kernel.json to include the env variable
   nano ~/.local/share/jupyter/kernels/stata/kernel.json
   ```
   
   Add the env section:
   ```json
   {
     "argv": [...],
     "display_name": "Stata",
     "language": "stata",
     "env": {
       "STATA_PATH": "/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp"
     }
   }
   ```

## Working Setup Verification

Once everything is working, you should:
1. See "Stata" in the kernel picker
2. Be able to run Stata code cells
3. See Stata output properly formatted

## If All Else Fails

Use the terminal-based Jupyter Lab which we know works:
```bash
poetry run jupyter lab
```

Then access it in your browser. The Stata kernel works reliably there.

## VSCode Jupyter Settings (Optional)

For better experience, you can add these to your VSCode settings:

```json
{
  "jupyter.askForKernelRestart": false,
  "jupyter.interactiveWindow.textEditor.executeSelection": true,
  "notebook.cellToolbarLocation": {
    "default": "right",
    "jupyter-notebook": "left"
  },
  "notebook.lineNumbers": "on",
  "notebook.output.textLineLimit": 100
}
```
