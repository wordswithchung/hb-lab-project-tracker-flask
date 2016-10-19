from flask import Flask, request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import hackbright

db = SQLAlchemy()

app = Flask(__name__)


@app.route("/")
def home():
    """Homepage with listing of students and projects."""

    _ALL_STUDENTS_SQL = "SELECT * FROM students"
    _ALL_PROJECTS_SQL = "SELECT * FROM projects"

    student_session = db.session.execute(_ALL_STUDENTS_SQL)
    students = student_session.fetchall()

    project_session = db.session.execute(_ALL_PROJECTS_SQL)
    projects = project_session.fetchall()

    return render_template("home.html", 
                           students=students, 
                           projects=projects)


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

    rows = hackbright.get_grades_by_title(title)    

    return render_template("project.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           rows=rows)


@app.route("/create")
def create():
    """Form to make new project."""

    return render_template("project_form.html")


@app.route("/create-project", methods=["POST"])
def create_project():
    """Add a new project and print confirmation.

    From the HTML web form, get a title, description, and maximum grade and 
    add that info to the database and print a confirmation message.
    """

    _ADD_PROJECT = """
                   INSERT INTO projects (title, description, max_grade)
                   VALUES (:title, :description, :max_grade)
                   """
    
    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = int(request.form.get('max_grade'))

    db.session.execute(_ADD_PROJECT, {'title': title,
                                      'description': description,
                                      'max_grade': max_grade})
    db.session.commit()
    
    return """
          Successfully added project: 
          Title: {}
          Description: {}
          Max grade: {}""".format(title, description, max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
