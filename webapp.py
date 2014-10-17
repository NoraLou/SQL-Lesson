from flask import Flask, render_template, request
import hackbright_app


app = Flask(__name__)

@app.route("/student/")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    first_name = row[0]
    last_name = row[1]
    github = row[2]
    html = render_template("student_info.html", first_name=first_name,
        last_name=last_name, github=github)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

if __name__ == "__main__":
    app.run(debug=True)