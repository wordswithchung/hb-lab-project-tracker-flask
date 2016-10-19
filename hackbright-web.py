from flask import Flask, request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import hackbright

db = SQLAlchemy()

# def connect_to_db(app):
#     """Connect to database."""

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)

app = Flask(__name__)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github", "jhacks")
    first_name, last_name, github = hackbright.get_student_by_github(github)

    rows = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", 
                           github=github,
                           first=first_name,
                           last=last_name,
                           rows=rows)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    github = request.form.get("github")
    first_name = request.form.get("first")
    last_name = request.form.get("last")
    hackbright.make_new_student(first_name, last_name, github)

    return render_template("new_student.html", 
                            github=github,
                            first=first_name,
                            last=last_name)

@app.route("/project")
def project():
    """Project listing."""

    title = request.args.get("title", "Banana Cream Pie")
    title, description, max_grade = hackbright.get_project_by_title(title)

    github, grade = hackbright.get_grades_by_title(title)

    return render_template("project.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           github=github,
                           grade=grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
