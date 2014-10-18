from flask import Flask, render_template, request
import hackbright_app


app = Flask(__name__)

@app.route("/student/")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    rows = hackbright_app.get_grade_by_project_given_github(student_github)
    html = render_template("student_info.html", rows=rows, github= student_github)
    return html


@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/projects/<title>")
def get_projects(title):
    hackbright_app.connect_to_db()
    projectrows = hackbright_app.get_grade_by_project(title)
    print projectrows
    html = render_template("project_info.html", rows= projectrows, title = title)
    return html





if __name__ == "__main__":
    app.run(debug=True)