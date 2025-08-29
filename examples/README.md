# Example Notebooks

This directory contains example notebooks demonstrating various features.

## Notebooks

### `stata_basics.ipynb`
- Pure Stata notebook
- Basic data manipulation and analysis
- Regression examples
- Visualization with Stata

### `python_stata_mixed.ipynb`
- Mixed Python and Stata workflow
- Data preparation in Python
- Statistical analysis in Stata
- Using `%%stata` magic commands

### `assignment_template.ipynb`
- NBGrader assignment template
- Shows how to structure auto-graded questions
- Includes test cells with assertions
- Ready to use as starting point

## How to Use

1. **For learning:** Open notebooks in Jupyter Lab and run cells
2. **For assignments:** Copy `assignment_template.ipynb` to `source/` folder and modify
3. **For reference:** Use as examples when creating your own notebooks

## Running Examples

```bash
# Start Jupyter Lab
poetry run jupyter lab

# Navigate to examples/ folder
# Open any notebook
# Select Stata kernel (for Stata notebooks)
```

## Creating Your Own

1. Copy a template
2. Modify for your needs
3. Save in appropriate directory:
   - `notebooks/` for working notebooks
   - `source/` for NBGrader assignments
