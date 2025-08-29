# Quick NBGrader Workflow for Stata

## Test the Example Assignment

### 1. Generate Student Version
```bash
poetry run nbgrader generate_assignment assignment1_stata --force
```

### 2. View Student Version
```bash
poetry run jupyter lab release/assignment1_stata/assignment1_stata.ipynb
```
You'll see that solutions are removed and replaced with `* YOUR CODE HERE`

### 3. Test Autograding
```bash
# Use the helper script for full workflow
poetry run python nbgrader_helper.py workflow assignment1_stata
```

## Create Your Own Assignment

### Step 1: Create Assignment
```bash
poetry run python nbgrader_helper.py create my_assignment
```

### Step 2: Edit in Jupyter Lab
```bash
poetry run jupyter lab source/my_assignment.ipynb
```

### Step 3: Add NBGrader Cell Metadata

In Jupyter Lab, use the toolbar or View → Cell Toolbar → Create Assignment to add:
- **Autograded answer**: Check "Autograded answer" for solution cells
- **Autograded tests**: Check "Autograded tests" + set points for test cells
- **Read-only**: Check for setup cells students shouldn't modify

### Step 4: Test Your Assignment
```bash
poetry run python nbgrader_helper.py workflow my_assignment
```

## Cell Examples

### Solution Cell (Students write code here)
```stata
* YOUR CODE HERE
gen new_var = old_var * 2
```
**Metadata**: `"solution": true`

### Test Cell (Auto-graded)
```stata
* TEST CELL - DO NOT MODIFY
capture confirm variable new_var
assert _rc == 0
display "Test passed!"
```
**Metadata**: `"grade": true, "points": 2, "locked": true`

## Common Stata Test Patterns

### Check Variable Exists
```stata
capture confirm variable varname
assert _rc == 0
```

### Check Scalar Value
```stata
capture scalar list scalar_name
assert _rc == 0
assert abs(scalar_name - expected_value) < 0.01
```

### Check Regression
```stata
quietly regress y x
assert abs(_b[x] - expected_coef) < 0.001
```

### Check Count
```stata
quietly count if condition
assert r(N) == expected_count
```

## Grading Multiple Students

### Submit Assignments
Place student notebooks in:
```
submitted/
├── student1/
│   └── assignment1_stata/
│       └── assignment1_stata.ipynb
├── student2/
│   └── assignment1_stata/
│       └── assignment1_stata.ipynb
```

### Grade All
```bash
poetry run nbgrader autograde assignment1_stata --force
```

### View Grades
```bash
poetry run nbgrader export
```

## Tips

1. **Test First**: Always test your assignment with the workflow before distributing
2. **Clear Output**: Clear all output before saving source notebooks
3. **Use Assertions**: Stata's `assert` command is perfect for automated testing
4. **Partial Credit**: Split tests into multiple assert statements for partial credit
5. **Hidden Tests**: Add tests students can't see in the source version

## Quick Commands Reference

| Task | Command |
|------|---------|
| Create assignment | `poetry run python nbgrader_helper.py create NAME` |
| Edit assignment | `poetry run jupyter lab source/NAME.ipynb` |
| Generate for students | `poetry run nbgrader generate_assignment NAME` |
| Test workflow | `poetry run python nbgrader_helper.py workflow NAME` |
| Grade submissions | `poetry run nbgrader autograde NAME` |
| Export grades | `poetry run nbgrader export` |
| Manual grading UI | `poetry run nbgrader formgrade` |

## Troubleshooting

### Stata kernel not selected
- Check kernel in top-right corner of notebook
- Must say "Stata" not "Python"

### Tests fail unexpectedly
- Check if data is loaded in setup cell
- Verify variable/scalar names match exactly
- Add `display` statements for debugging

### Can't find assignment
- Assignments must be in `source/` directory
- Filename must end with `.ipynb`
