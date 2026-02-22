# 🚀 Smart Resume Screening System

## 📌 Description

The **Smart Resume Screening System** is a web-based application designed to automate the initial stages of the recruitment process. It allows candidates to upload their resumes and enables administrators to define job criteria, analyze resumes, and shortlist candidates efficiently.

The system extracts relevant skills from uploaded resumes and compares them with admin-defined job requirements to determine candidate suitability. It simplifies hiring by reducing manual effort and improving decision-making.

---

## 🎯 Key Features

### 👤 User Module

* Upload resume (PDF format)
* View application status (**Received**)
* Get professional update message regarding application progress

### 👨‍💼 Admin Module

* Add / update / remove job criteria (skills)
* View all uploaded resumes
* Resume ranking based on skill match
* Shortlist candidates (even with 1 matching skill)
* Filter shortlisted candidates
* View candidate email
* Open uploaded resume (PDF viewer)

---

## 🛠️ Technologies Used

### 🔹 Frontend

* HTML5
* CSS3
* Bootstrap 5 (for modern UI/UX)

### 🔹 Backend

* Python
* Flask (Web Framework)

### 🔹 Database

* SQLite (via Flask-SQLAlchemy)

### 🔹 Libraries

* PyPDF2 (Resume parsing)
* SQLAlchemy (ORM)

---

## ⚙️ System Workflow

1. **User Registration & Login**

   * Users create an account and log in to the system.

2. **Resume Upload**

   * Users upload their resume (PDF format).
   * The system extracts text and identifies key skills.

3. **Admin Defines Criteria**

   * Admin adds required skills for a job role.
   * Criteria can be updated dynamically.

4. **Resume Processing**

   * Extracted skills are compared with job criteria.
   * Matching logic calculates similarity.

5. **Shortlisting**

   * If at least one skill matches → candidate is shortlisted.
   * Candidates are ranked based on matching score.

6. **Admin Dashboard**

   * Admin can view:

     * Candidate email
     * Resume
     * Match status
     * Ranking

7. **User Dashboard**

   * Users see:

     * Status: **Received**
     * Message: Application under review

---

## ▶️ How to Setup & Run

### 🔹 Step 1: Clone the Repository

```bash
git clone <your-repo-link>
cd smart_resume
```

### 🔹 Step 2: Install Dependencies

```bash
pip install flask flask_sqlalchemy PyPDF2
```

### 🔹 Step 3: Remove Old Database (Important)

```bash
delete database.db
```

### 🔹 Step 4: Run the Application

```bash
python app.py
```

### 🔹 Step 5: Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Login

```
Username: admin
Password: admin
```

---

## 📄 Conclusion

This project demonstrates how automation and basic NLP techniques can streamline recruitment processes. It provides a scalable foundation for building intelligent hiring platforms with improved efficiency and accuracy.

---

