# Using NBGrader with Stata

This guide explains how to create, distribute, and grade Stata assignments using NBGrader.

## Quick Start

### 1. Create an Assignment

```bash
# Create assignment in source/ directory
# Edit source/assignment1_stata.ipynb using Jupyter Lab
poetry run jupyter lab source/assignment1_stata.ipynb
```

### 2. Generate Student Version

```bash
# Generate the student version (removes solutions)
poetry run nbgrader generate_assignment assignment1_stata --force

# The student version is now in release/assignment1_stata/
```

### 3. After Students Submit

```bash
# Students submit to submitted/student_id/assignment1_stata/

# Autograde submissions
poetry run nbgrader autograde assignment1_stata --force

# Generate feedback
poetry run nbgrader generate_feedback assignment1_stata --force
```

## Cell Types in NBGrader

### 1. Read-only Cells (Setup/Instructions)
- **Purpose**: Provide data, functions, or instructions that students cannot modify
- **Metadata**: `"deletable": false, "editable": false`
- **Example**: Loading datasets, defining helper functions

### 2. Solution Cells
- **Purpose**: Where students write their code
- **Metadata**: `"solution": true`
- **In Source**: Contains your solution
- **In Release**: Contains `* YOUR CODE HERE` placeholder

### 3. Test Cells (Autograded)
- **Purpose**: Automatically test student solutions
- **Metadata**: `"grade": true, "points": X`
- **Must be**: Read-only (`"locked": true`)
- **Use**: Stata assert statements

### 4. Manual Grade Cells
- **Purpose**: For written answers or code that needs human review
- **Metadata**: `"grade": true, "solution": false, "task": true`

## Writing Stata Tests

### Basic Assertions

```stata
* Check if variable exists
capture confirm variable varname
assert _rc == 0

* Check if scalar exists
capture scalar list scalar_name
assert _rc == 0

* Check values
assert price > 0
assert abs(computed_value - expected_value) < 0.001

* Check counts
quietly count if condition
assert r(N) == expected_count

* Check regression results
quietly regress y x1 x2
assert e(N) > 0
assert e(r2) > 0.5
```

### Test Patterns

#### Pattern 1: Variable Creation Test
```stata
* Test if student created a binary variable correctly
capture confirm variable expensive
assert _rc == 0

quietly count if price > 6000 & expensive != 1
assert r(N) == 0
quietly count if price <= 6000 & expensive != 0
assert r(N) == 0
```

#### Pattern 2: Calculation Test
```stata
* Test if student calculated statistics correctly
capture scalar list student_mean
assert _rc == 0

quietly summarize price
assert abs(student_mean - r(mean)) < 0.01
```

#### Pattern 3: Regression Test
```stata
* Test if student ran correct regression
capture scalar list rsq
assert _rc == 0

quietly regress price mpg weight
assert abs(rsq - e(r2)) < 0.001
```

## Complete Workflow Example

### Step 1: Set Up Course

```bash
# Initialize nbgrader for your course
poetry run nbgrader quickstart my_stata_course
```

### Step 2: Configure NBGrader

Edit `nbgrader_config.py`:

```python
c.NbGrader.course_id = "stata_econometrics"
c.ClearSolutions.code_stub = {
    "python": "# YOUR CODE HERE\nraise NotImplementedError()",
    "stata": "* YOUR CODE HERE\ndisplay \"Not implemented\""
}
```

### Step 3: Create Assignment Structure

```bash
# Create directories
mkdir -p source/assignment1
mkdir -p submitted
mkdir -p autograded
```

### Step 4: Add Students (Optional)

```bash
# Add students to database
poetry run nbgrader db student add student1 --first-name "John" --last-name "Doe"
poetry run nbgrader db student add student2 --first-name "Jane" --last-name "Smith"
```

### Step 5: Assignment Lifecycle

```bash
# 1. Create assignment (edit in Jupyter Lab)
poetry run jupyter lab source/assignment1_stata.ipynb

# 2. Validate the source notebook
poetry run nbgrader validate source/assignment1_stata.ipynb

# 3. Generate student version
poetry run nbgrader generate_assignment assignment1_stata --force

# 4. Distribute to students (they get release/assignment1_stata/)
cp -r release/assignment1_stata/ send_to_students/

# 5. Collect submissions
cp student_submission.ipynb submitted/student1/assignment1_stata/

# 6. Autograde
poetry run nbgrader autograde assignment1_stata --force

# 7. Manual grading (if needed)
poetry run nbgrader formgrade

# 8. Generate feedback
poetry run nbgrader generate_feedback assignment1_stata --force

# 9. Export grades
poetry run nbgrader export
```

## Tips for Stata Assignments

### 1. Data Persistence
Stata maintains state across cells, so:
- Load data in a setup cell (read-only)
- Be careful about variable modifications affecting later questions
- Consider using `preserve/restore` for independent questions

### 2. Error Handling
```stata
* Use capture for commands that might fail
capture drop temp_var
if _rc == 0 {
    display "Variable dropped"
}

* Clear any existing variables/scalars before testing
capture scalar drop test_scalar
capture drop test_var
```

### 3. Hidden Tests
You can add tests that don't show output:
```stata
* Hidden test - output suppressed
quietly {
    count if condition
    assert r(N) == expected
}
```

### 4. Partial Credit
Structure tests to give partial credit:
```stata
* Test 1: Variable exists (1 point)
capture confirm variable result
if _rc == 0 {
    display "✓ Variable created"
}
else {
    display "✗ Variable not found"
    assert _rc == 0  // This will fail
}

* Test 2: Values correct (1 point)
* Only runs if variable exists
if _rc == 0 {
    quietly count if result != expected
    assert r(N) == 0
}
```

## Example Test Cell Templates

### Template 1: Variable Existence and Type
```stata
* Check variable exists and has correct type
capture confirm variable varname
assert _rc == 0, "Variable 'varname' does not exist"

describe varname
assert r(vartype) == "byte" | r(vartype) == "int", "Variable type incorrect"
```

### Template 2: Summary Statistics
```stata
* Check if student calculated correct statistics
capture scalar list student_stat
assert _rc == 0, "Scalar 'student_stat' not found"

* Recalculate to verify
quietly summarize variable
local true_stat = r(mean)
assert abs(student_stat - `true_stat') < 0.01, "Calculated value incorrect"
```

### Template 3: Regression Results
```stata
* Check regression was performed correctly
quietly regress depvar indepvars
matrix correct_b = e(b)

* Check student's results match
assert mreldif(student_b, correct_b) < 0.01, "Regression coefficients incorrect"
```

## Debugging Student Code

If student code fails:

1. **Check Syntax Errors**: Stata will show line numbers
2. **Check Variable Names**: Students might use different names
3. **Check Missing Values**: Students might not handle missing data
4. **Add Diagnostic Output**:
   ```stata
   display "Debug: Variable exists = " _rc
   display "Debug: N = " _N
   display "Debug: Value = " scalar_name
   ```

## Common Issues and Solutions

### Issue 1: Stata Kernel Not Found
```bash
# Ensure Stata kernel is installed
poetry run python -m nbstata.install
poetry run jupyter kernelspec list
```

### Issue 2: Tests Pass Locally but Fail in Autograder
- Check for hardcoded paths
- Ensure data is loaded in setup cells
- Verify Stata version compatibility

### Issue 3: Unicode/Display Issues
```stata
* Use ASCII characters for better compatibility
display "OK" // instead of "✓"
display "FAIL" // instead of "✗"
```

## Advanced Features

### Custom Test Functions
Create a helper do-file:
```stata
* test_helpers.do
program define assert_near
    args val1 val2 tolerance
    if abs(`val1' - `val2') > `tolerance' {
        display "Assertion failed: " `val1' " != " `val2'
        exit 1
    }
end
```

### Automated Test Generation
Create Python script to generate test cells:
```python
def create_test_cell(var_name, expected_type):
    return f"""
capture confirm variable {var_name}
assert _rc == 0
describe {var_name}
assert r(vartype) == "{expected_type}"
"""
```

## Best Practices

1. **Clear Instructions**: Specify exact variable/scalar names students should create
2. **Incremental Testing**: Test step-by-step rather than all at once
3. **Meaningful Feedback**: Use display statements to show what passed/failed
4. **Robust Tests**: Handle edge cases and missing values
5. **Version Control**: Keep source notebooks in git
6. **Backup**: Regularly backup the gradebook database

## Sample Rubric

| Component | Points | Description |
|-----------|--------|-------------|
| Variable Creation | 2 | Create specified variables correctly |
| Calculations | 3 | Perform statistical calculations |
| Regression | 3 | Run and interpret regression |
| Data Manipulation | 2 | Transform and clean data |
| **Total** | **10** | |

## Resources

- [NBGrader Documentation](https://nbgrader.readthedocs.io/)
- [Stata Assert Documentation](https://www.stata.com/help.cgi?assert)
- [Jupyter Notebook Metadata](https://nbformat.readthedocs.io/)
