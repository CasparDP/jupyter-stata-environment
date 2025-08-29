"""NBGrader configuration file."""

c = get_config()  # noqa

# Configure the notebook grader
c.NbGrader.course_id = "example_course"
c.NbGrader.db_assignments = [
    dict(name="assignment1"),
    dict(name="assignment2"),
]
c.NbGrader.db_students = [
    dict(id="student1", first_name="Student", last_name="One"),
    dict(id="student2", first_name="Student", last_name="Two"),
]

# Exchange configuration
c.Exchange.root = "./exchange"
c.Exchange.course_id = "example_course"

# Assignment configuration
c.IncludeHeaderFooter.header = "source/header.ipynb"

# Autograder configuration
c.ExecutePreprocessor.timeout = 120
c.ExecutePreprocessor.interrupt_on_timeout = True

# Allow errors in student notebooks (useful for partial credit)
c.Execute.allow_errors = True

# Configure assignment directory structure
c.CourseDirectory.source_directory = "source"
c.CourseDirectory.release_directory = "release"
c.CourseDirectory.submitted_directory = "submitted"
c.CourseDirectory.autograded_directory = "autograded"
c.CourseDirectory.feedback_directory = "feedback"

# Database configuration
c.CourseDirectory.db_url = "sqlite:///gradebook.db"

# Optional: Configure for use with JupyterHub
# c.NbGrader.course_directory = "/srv/nbgrader/example_course"
# c.FormgradeApp.authenticator_class = "nbgrader.auth.hubauth.HubAuth"
# c.HubAuth.graders = ["instructor1", "ta1"]

# Optional: Late submission penalty
# c.LateSubmissionPlugin.penalty_method = "exponential"
# c.LateSubmissionPlugin.penalty_per_day = 0.1

# Configure toolbar
c.ClearSolutions.code_stub = {
    "python": "# YOUR CODE HERE\nraise NotImplementedError()",
    "stata": "* YOUR CODE HERE\ndisplay \"Not implemented\"",
}

# Validate extensions
c.Validator.ignore_checksums = False
