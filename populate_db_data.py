import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()  # load environment variables from .env file

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]


def populate_courses():
    """
    Populates the courses collection with sample data.
    """
    courses = [
        {
            "name": "Math 101",
        },
        {
            "name": "Physics 202",
        },
        {
            "name": "Chemistry 303",
        },
        {
            "name": "Biology 404",
        },
    ]

    db.courses.insert_many(courses)



def populate_students_and_assignments():
    """
    Populates the students collection with sample data.
    student_id can be redundat because we have object id, but we're keeping it for convenience.
    """
    students = [
        {
            "name": "John Doe", 
            "student_id": "12345",
            "assignments": [
                {"name": "Math Homework 1", "grade": 85},
                {"name": "Science Project", "grade": 92}
            ]
        },
        {
            "name": "Jane Smith", 
            "student_id": "67890",
            "assignments": [
                {"name": "Math Homework 1", "grade": 90},
                {"name": "Science Project", "grade": 88}
            ]
        },
        {
            "name": "Michael Johnson", 
            "student_id": "11223",
            "assignments": [
                {"name": "Math Homework 1", "grade": 78},
                {"name": "Science Project", "grade": 85}
            ]
        },
        {
            "name": "Emily Brown", 
            "student_id": "44556",
            "assignments": [
                {"name": "Math Homework 1", "grade": 92},
                {"name": "Science Project", "grade": 95}
            ]
        },
        {
            "name": "Alice Williams", 
            "student_id": "78901",
            "assignments": [
                {"name": "Math Homework 1", "grade": 88},
                {"name": "Science Project", "grade": 91}
            ]
        }
    ]

    db.students.insert_many(students)

if __name__ == "__main__":
    populate_students_and_assignments()
    
