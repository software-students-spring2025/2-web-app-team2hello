import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)
            
config = dotenv_values()
app.config.from_mapping(config)

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]


try:
    cxn.admin.command("ping")
    print(" *", "Connected to MongoDB!")
except Exception as e:
    print(" * MongoDB connection error:", e)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get_courses", methods=["GET"])
def get_courses():
    courses = list(db.courses.find({}, {"_id": 0, "name": 1}))
    return jsonify(courses)

@app.route("/add_course", methods=["POST"])
def add_course():
    try:
        data = request.json
        course_name = data.get("courseName")

        if not course_name:
            return jsonify({"error": "Course name is required"}), 400

        new_course = {"name": course_name}
        db.courses.insert_one(new_course)

        return jsonify({"message": "Course added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_students", methods=["GET"])
def get_students():
    students = list(db.students.find({}, {"_id": 0, "name": 1, "student_id": 1, "assignments": 1}))
    return jsonify(students)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()

    student_name = data.get('name')
    student_id = data.get('student_id')

    if not student_name or not student_id:
        return jsonify({"error": "Student name and ID are required"}), 400

    existing_student = db.students.find_one({"student_id": student_id})
    if existing_student:
        return jsonify({"error": "Student with this ID already exists"}), 400

    new_student = {
        "name": student_name,
        "student_id": student_id,
        "assignments": []
    }
    db.students.insert_one(new_student)
    
    return jsonify({"message": "Student added successfully"}), 201

@app.route('/search_student', methods=['GET'])
def search_student():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({"error": "Please provide a student name or ID"}), 400

    student = db.students.find_one({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},  
            {"student_id": query}  
        ]
    })

    if student:
        return jsonify({"student_id": student["student_id"]})
    else:
        return jsonify({"error": "No student found"}), 404

@app.route("/get_student_details/<student_id>", methods=["GET"])
def get_student_details(student_id):
    student = db.students.find_one({"student_id": student_id})

    if student:
        student_details = {
            "name": student["name"],
            "student_id": student["student_id"],
            "assignments": student["assignments"]
        }
        return jsonify(student_details)
    else:
        return jsonify({"error": "Student not found"}), 404


@app.route("/add_assignment/<student_id>", methods=["POST"])
def add_assignment(student_id):
    data = request.json
    assignment_name = data.get("assignmentName")
    grade = data.get("grade")

    student = db.students.find_one({"student_id": student_id})
    if student:
        student["assignments"].append({"name": assignment_name, "grade": grade})
        db.students.update_one({"student_id": student_id}, {"$set": {"assignments": student["assignments"]}})
        return jsonify({"message": "Assignment added successfully!"})
    return jsonify({"error": "Student not found"}), 404

@app.route("/update_grade/<student_id>", methods=["POST"])
def update_grade(student_id):
    data = request.json
    assignment_name = data.get("assignmentName")
    new_grade = data.get("newGrade")

    student = db.students.find_one({"student_id": student_id})
    if student:
        for assignment in student["assignments"]:
            if assignment["name"] == assignment_name:
                assignment["grade"] = new_grade
                break
        db.students.update_one({"student_id": student_id}, {"$set": {"assignments": student["assignments"]}})
        return jsonify({"message": "Grade updated successfully!"})
    return jsonify({"error": "Student not found"}), 404

@app.route("/delete_assignment/<student_id>", methods=["POST"])
def delete_assignment(student_id):
    data = request.json
    assignment_name = data.get("assignmentName")

    student = db.students.find_one({"student_id": student_id})
    if student:
        student["assignments"] = [assignment for assignment in student["assignments"] if assignment["name"] != assignment_name]
        db.students.update_one({"student_id": student_id}, {"$set": {"assignments": student["assignments"]}})
        return jsonify({"message": "Assignment deleted successfully!"})
    return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_ENV = os.getenv("FLASK_ENV")
    print(f"FLASK_ENV: {FLASK_ENV}, FLASK_PORT: {FLASK_PORT}")

    app.run(port=FLASK_PORT)
