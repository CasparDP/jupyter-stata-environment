# Template Setup Checklist

## For Template Creators (You)

Before making this a GitHub template:

- [ ] Remove `poetry.lock` (let users generate their own)
- [ ] Clear any personal data from notebooks
- [ ] Update author information in `pyproject.toml`
- [ ] Remove `.vscode/settings.json` if it contains personal paths
- [ ] Clear `source/` directory (keep only README)
- [ ] Clear `notebooks/` directory (keep only README)

## For Template Users

After creating repository from template:

### 1. Initial Setup
- [ ] Clone your new repository
- [ ] Run `python setup.py`
- [ ] Enter Stata path when prompted (or skip)

### 2. Start Working
- [ ] Run start script (`start_jupyter.sh` / `start_jupyter.bat`)
- [ ] Open browser to http://localhost:8888
- [ ] Create first notebook

### 3. For VSCode Users
- [ ] Start Jupyter server
- [ ] Open notebook in VSCode
- [ ] Connect to existing server (http://localhost:8888)
- [ ] Select Stata kernel

### 4. For Instructors
- [ ] Customize `nbgrader_config.py`
- [ ] Create assignments in `source/`
- [ ] Test grading workflow

## Platform-Specific Notes

### Windows
- Use `start_jupyter.bat` or PowerShell script
- Stata typically in `C:\Program Files\Stata17\`

### macOS
- Use `start_jupyter.sh`
- Stata typically in `/Applications/Stata/`

### Linux
- Use `start_jupyter.sh`
- Stata typically in `/usr/local/stata17/`

## Support

- Check `QUICK_START.md` for commands
- Check `docs/` for detailed guides
- Check `examples/` for notebook examples
- Check `tools/` for troubleshooting scripts
