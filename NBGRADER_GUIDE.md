# NBGrader Guide for Stata Assignments

## Creating Assignments

### Cell Types

1. **Read-only cells** (setup, instructions)
   - Metadata: `deletable: false, editable: false`

2. **Solution cells** (where students write code)
   - Metadata: `solution: true`
   - Contains your solution (removed in student version)

3. **Test cells** (auto-grading)
   - Metadata: `grade: true, points: X, locked: true`
   - Use Stata `assert` commands

### Common Test Patterns

```stata
* Check variable exists
capture confirm variable varname
assert _rc == 0

* Check scalar value
capture scalar list scalar_name
assert _rc == 0
assert abs(scalar_name - expected) < 0.01

* Check regression
quietly regress y x
assert abs(_b[x] - expected_coef) < 0.001

* Check count
quietly count if condition
assert r(N) == expected_count
```

## Workflow

### For Instructors

1. **Create assignment** in `source/` folder
2. **Add NBGrader metadata** via View → Cell Toolbar → Create Assignment
3. **Generate student version:**
   ```bash
   poetry run nbgrader generate_assignment assignment_name --force
   ```
4. **Distribute** `release/assignment_name/` to students
5. **Collect** submissions in `submitted/student_id/assignment_name/`
6. **Grade:**
   ```bash
   poetry run nbgrader autograde assignment_name --force
   ```
7. **Export grades:**
   ```bash
   poetry run nbgrader export
   ```

### For Students

1. **Get assignment** from `release/` folder
2. **Complete** the notebook
3. **Validate:**
   ```bash
   poetry run nbgrader validate assignment_name.ipynb
   ```
4. **Submit** to instructor

## Example Assignment

See `examples/assignment_template.ipynb` for a basic template.

## Tips

- Clear all output before saving source notebooks
- Use exact variable names in instructions
- Test your assignment before distributing
- Add helpful error messages in assertions
- Structure tests for partial credit
