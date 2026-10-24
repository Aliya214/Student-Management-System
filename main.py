import json
import os

class Student:
    def __init__(self, student_id, name, age, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.__marks = marks

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        if 0 <= value <= 100:
            self.__marks = value
        else:
            raise ValueError("Marks must be between 0 and 100")

    def calculate_grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 75:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 40:
            return "D"
        else:
            return "F"

    def display(self):
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Marks: {self.marks:g}")
        print(f"Grade: {self.calculate_grade()}")

class RecordManager:
    def __init__(self):
        self.students = []

class StudentManager(RecordManager):
    def __init__(self):
        super().__init__()
        self.filename = "students.json"
        self.load_students()

    def load_students(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                student = Student(
                    item["student_id"],
                    item["name"],
                    item["age"],
                    item["marks"]
                )
                self.students.append(student)

        except (json.JSONDecodeError, OSError, KeyError,
                TypeError, ValueError):
            print("Unable to load student records.")

    def save_students(self):
        data = []

        for student in self.students:
            data.append({
                "student_id": student.student_id,
                "name": student.name,
                "age": student.age,
                "marks": student.marks
            })

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def add_student(self):
        print("\n--- Add Student ---")

        student_id = input("Enter student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return

        if self.find_student(student_id):
            print("Student ID already exists.")
            return

        name = input("Enter student name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter age: "))
            marks = float(input("Enter marks (0-100): "))

            if age <= 0:
                print("Age must be greater than zero.")
                return

            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return

            student = Student(student_id, name, age, marks)
            self.students.append(student)
            self.save_students()

            print("Student added successfully!")

        except ValueError:
            print("Please enter valid numbers for age and marks.")

        except OSError:
            print("Unable to save student record.")

    def view_students(self):
        print("\n--- All Students ---")

        if not self.students:
            print("No student records found.")
            return

        for student in self.students:
            print("-" * 30)
            student.display()

    def search_student(self):
        student_id = input("Enter student ID to search: ").strip()
        student = self.find_student(student_id)

        if student:
            student.display()
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter student ID to update: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep the existing value.")

        name = input(f"New name [{student.name}]: ").strip()
        age_text = input(f"New age [{student.age}]: ").strip()
        marks_text = input(f"New marks [{student.marks:g}]: ").strip()

        try:
            new_name = name if name else student.name
            new_age = int(age_text) if age_text else student.age
            new_marks = float(marks_text) if marks_text else student.marks

            if not new_name:
                print("Name cannot be empty.")
                return

            if new_age <= 0:
                print("Age must be greater than zero.")
                return

            if not 0 <= new_marks <= 100:
                print("Marks must be between 0 and 100.")
                return

            old_values = (student.name, student.age, student.marks)

            student.name = new_name
            student.age = new_age
            student.marks = new_marks

            try:
                self.save_students()
                print("Student updated successfully!")
            except OSError:
                student.name, student.age, student.marks = old_values
                print("Could not save changes.")

        except ValueError:
            print("Invalid age or marks.")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        confirm = input(
            f"Delete {student.name}? Type yes to confirm: "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            return

        self.students.remove(student)

        try:
            self.save_students()
            print("Student deleted successfully!")
        except OSError:
            self.students.append(student)
            print("Could not save changes. Record restored.")

    def show_statistics(self):
        print("\n--- Student Statistics ---")

        if not self.students:
            print("No student records found.")
            return

        total = len(self.students)
        average = sum(s.marks for s in self.students) / total
        highest = max(self.students, key=lambda s: s.marks)
        lowest = min(self.students, key=lambda s: s.marks)

        print(f"Total students: {total}")
        print(f"Average marks: {average:.2f}")
        print(f"Highest scorer: {highest.name} ({highest.marks:g})")
        print(f"Lowest scorer: {lowest.name} ({lowest.marks:g})")

def main():
    manager = StudentManager()

    while True:
        print("\n================================")
        print("   STUDENT MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Student Statistics")
        print("7. Exit")
        print("================================")

        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                manager.add_student()
            elif choice == "2":
                manager.view_students()
            elif choice == "3":
                manager.search_student()
            elif choice == "4":
                manager.update_student()
            elif choice == "5":
                manager.delete_student()
            elif choice == "6":
                manager.show_statistics()
            elif choice == "7":
                print("Thank you for using the application!")
                break
            else:
                print("Invalid choice. Please enter 1 to 7.")

        except OSError:
            print("File error. Please check your project folder.")

if __name__ == "__main__":
    main()