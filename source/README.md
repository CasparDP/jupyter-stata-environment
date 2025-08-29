# Source Directory (NBGrader)

This directory is for NBGrader source assignments (instructor version).

## Usage

1. **Create assignments here** with full solutions
2. **Add NBGrader metadata** to cells (View → Cell Toolbar → Create Assignment)
3. **Generate student versions** with:
   ```bash
   poetry run nbgrader generate_assignment assignment_name --force
   ```

Student versions will appear in `release/` directory.

## Cell Types

- **Read-only**: Setup cells, instructions (locked)
- **Solution**: Where students write code
- **Tests**: Auto-graded with assertions (include points)

## Example

See `examples/assignment_template.ipynb` for a template.

## Workflow

1. Create → 2. Generate → 3. Distribute → 4. Collect → 5. Grade

See `NBGRADER_GUIDE.md` for detailed instructions.
