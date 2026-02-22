from flask import Flask, render_template, request, redirect, session, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import PyPDF2

app = Flask(__name__)
app.secret_key = "secret123"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- MODELS ---------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(10))


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    file = db.Column(db.String(200))
    skills = db.Column(db.String(500))
    status = db.Column(db.String(50))
    score = db.Column(db.Integer)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills_required = db.Column(db.String(500))


# ---------- INIT ---------- #

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        db.session.add(User(username="admin", password="admin", role="admin"))
        db.session.commit()


# ---------- AUTH ---------- #

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect("/admin")
            return redirect("/user")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")


# ---------- USER ---------- #

@app.route("/user", methods=["GET", "POST"])
def user_dashboard():
    if request.method == "POST":
        file = request.files["resume"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = extract_text(path)
        skills = extract_skills(text)

        score, status = calculate_score(skills)

        resume = Resume(
            user_id=session["user_id"],
            file=path,
            skills=", ".join(skills),
            status="Received",
            score=score
        )

        db.session.add(resume)
        db.session.commit()

    resumes = Resume.query.filter_by(user_id=session["user_id"]).all()
    return render_template("user_dashboard.html", resumes=resumes)


# ---------- ADMIN ---------- #

@app.route("/admin", methods=["GET", "POST"])
def admin():
    filter_type = request.args.get("filter")

    if request.method == "POST":
        new_skills = request.form["skills"].lower().split(",")

        job = Job.query.first()

        if job:
            existing = job.skills_required.split(",")
            updated = list(set(existing + [s.strip() for s in new_skills]))
            job.skills_required = ",".join(updated)
        else:
            job = Job(skills_required=",".join(new_skills))
            db.session.add(job)

        db.session.commit()

    # update matching
    resumes_all = Resume.query.all()
    for r in resumes_all:
        skills = r.skills.split(",")
        score, status = calculate_score(skills)
        r.score = score
        r.status = status
    db.session.commit()

    if filter_type == "shortlisted":
        resumes = Resume.query.filter_by(status="Matched").order_by(Resume.score.desc()).all()
    else:
        resumes = Resume.query.order_by(Resume.score.desc()).all()

    users = User.query.all()
    job = Job.query.first()

    return render_template("admin.html", resumes=resumes, users=users, job=job)


@app.route("/delete-skill/<skill>")
def delete_skill(skill):
    job = Job.query.first()
    skills = job.skills_required.split(",")

    skills = [s for s in skills if s != skill]
    job.skills_required = ",".join(skills)

    db.session.commit()
    return redirect("/admin")


@app.route("/view-resume/<int:id>")
def view_resume(id):
    resume = Resume.query.get(id)
    return send_file(resume.file)


# ---------- LOGIC ---------- #

def extract_text(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()


def extract_skills(text):
    skills_db = ["python", "java", "sql", "html", "css", "javascript"]
    return [s for s in skills_db if s in text]


def calculate_score(resume_skills):
    job = Job.query.first()

    if not job:
        return 0, "Pending"

    job_skills = [s.strip() for s in job.skills_required.split(",")]

    match = set(resume_skills) & set(job_skills)
    score = int((len(match) / len(job_skills)) * 100)

    if len(match) >= 1:
        return score, "Matched"
    return score, "Not Matched"


# ---------- RUN ---------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)