import csv
import os
import json
import logging

#  Logging setup
logging.basicConfig(
    filename="student_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CSV_FILE = "students.csv"
JSON_FILE = "students.json"
FIELDNAMES = ["reg_no", "name", "gender", "age", "course", "score"]


# Custom Exception 
class StudentNotFoundError(Exception):
    def __init__(self, reg_no):
        self.reg_no = reg_no
        super().__init__(f"No student found with registration number: {reg_no}")


# CSV Layer 
def add_student_csv(student):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(student)


def view_students_csv():
    if not os.path.isfile(CSV_FILE):
        return []
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def search_student_csv(reg_no):
    for student in view_students_csv():
        if student["reg_no"] == reg_no:
            return student
    return None


def update_student_csv(reg_no, updated_fields):
    students = view_students_csv()
    updated = False
    for student in students:
        if student["reg_no"] == reg_no:
            student.update(updated_fields)
            updated = True
            break
    if updated:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(students)
    return updated


def delete_student_csv(reg_no):
    students = view_students_csv()
    new_list = [s for s in students if s["reg_no"] != reg_no]
    if len(new_list) == len(students):
        return False
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(new_list)
    return True


#  JSON Layer 
def load_json_data():
    if not os.path.isfile(JSON_FILE):
        return {}
    with open(JSON_FILE, "r") as f:
        return json.load(f)


def save_json_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_student_json(reg_no, extra_details):
    data = load_json_data()
    data[reg_no] = extra_details
    save_json_data(data)


def search_student_json(reg_no):
    return load_json_data().get(reg_no)


def update_student_json(reg_no, updated_fields):
    data = load_json_data()
    if reg_no not in data:
        return False
    data[reg_no].update(updated_fields)
    save_json_data(data)
    return True


def delete_student_json(reg_no):
    data = load_json_data()
    if reg_no not in data:
        return False
    del data[reg_no]
    save_json_data(data)
    return True


# - Menu Actions 
def menu_add_student():
    """Collect input and add a new student to both CSV and JSON."""
    print("\n--- Add New Student ---")
    reg_no = input("Reg No: ").strip()

    if search_student_csv(reg_no) is not None:
        print("A student with this reg no already exists.")
        logging.warning(f"Attempted duplicate add: {reg_no}")
        return

    name = input("Name: ").strip()
    gender = input("Gender: ").strip()

    # Input validation for age and score
    while True:
        try:
            age = int(input("Age: "))
            break
        except ValueError:
            print("Age must be a number. Try again.")

    course = input("Course: ").strip()

    while True:
        try:
            score = float(input("Score: "))
            break
        except ValueError:
            print("Score must be a number. Try again.")

    address = input("Address: ").strip()
    contact = input("Contact: ").strip()
    program = input("Program: ").strip()

    student = {
        "reg_no": reg_no, "name": name, "gender": gender,
        "age": age, "course": course, "score": score
    }
    extra = {"address": address, "contact": contact, "program": program}

    add_student_csv(student)
    add_student_json(reg_no, extra)

    print(f"Student {name} added successfully.")
    logging.info(f"Student added: {reg_no}")


def menu_view_students():
    """Display all students with their basic + extra info."""
    print("\n--- All Students ---")
    students = view_students_csv()

    if not students:
        print("No students found.")
        return

    for s in students:
        extra = search_student_json(s["reg_no"]) or {}
        print(f"\nReg No: {s['reg_no']} | Name: {s['name']} | Gender: {s['gender']}")
        print(f"Age: {s['age']} | Course: {s['course']} | Score: {s['score']}")
        print(f"Address: {extra.get('address', 'N/A')} | "
              f"Contact: {extra.get('contact', 'N/A')} | "
              f"Program: {extra.get('program', 'N/A')}")

    logging.info("Viewed all students.")


def menu_search_student():
    """Search for one student by reg_no, raising custom exception if missing."""
    print("\n--- Search Student ---")
    reg_no = input("Enter Reg No to search: ").strip()

    student = search_student_csv(reg_no)
    if student is None:
        logging.error(f"Search failed - not found: {reg_no}")
        raise StudentNotFoundError(reg_no)

    extra = search_student_json(reg_no) or {}
    print(f"\nReg No: {student['reg_no']} | Name: {student['name']} | Gender: {student['gender']}")
    print(f"Age: {student['age']} | Course: {student['course']} | Score: {student['score']}")
    print(f"Address: {extra.get('address', 'N/A')} | "
          f"Contact: {extra.get('contact', 'N/A')} | "
          f"Program: {extra.get('program', 'N/A')}")

    logging.info(f"Student searched: {reg_no}")


def menu_update_student():
    """Update an existing student's details."""
    print("\n--- Update Student ---")
    reg_no = input("Enter Reg No to update: ").strip()

    if search_student_csv(reg_no) is None:
        logging.error(f"Update failed - not found: {reg_no}")
        raise StudentNotFoundError(reg_no)

    print("Leave blank to keep current value.")
    name = input("New Name: ").strip()
    course = input("New Course: ").strip()

    score_input = input("New Score: ").strip()

    updated_fields = {}
    if name:
        updated_fields["name"] = name
    if course:
        updated_fields["course"] = course
    if score_input:
        try:
            updated_fields["score"] = float(score_input)
        except ValueError:
            print("Invalid score - skipping that field.")

    update_student_csv(reg_no, updated_fields)
    print("Student updated successfully.")
    logging.info(f"Student updated: {reg_no}")


def menu_delete_student():
    """Delete a student from both CSV and JSON."""
    print("\n--- Delete Student ---")
    reg_no = input("Enter Reg No to delete: ").strip()

    deleted_csv = delete_student_csv(reg_no)
    if not deleted_csv:
        logging.error(f"Delete failed - not found: {reg_no}")
        raise StudentNotFoundError(reg_no)

    delete_student_json(reg_no)
    print("Student deleted successfully.")
    logging.info(f"Student deleted: {reg_no}")


# Main Menu Loop 
def main():
    while True:
        print("\n===== Student Record Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                menu_add_student()
            elif choice == "2":
                menu_view_students()
            elif choice == "3":
                menu_search_student()
            elif choice == "4":
                menu_update_student()
            elif choice == "5":
                menu_delete_student()
            elif choice == "6":
                print("Goodbye!")
                logging.info("Program exited normally.")
                break
            else:
                print("Invalid choice. Please enter a number from 1-6.")

        except StudentNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            # Catches anything unexpected (file errors, etc.)
            print(f"An unexpected error occurred: {e}")
            logging.error(f"Unexpected error: {e}")

        finally:
            # Runs no matter what - good place for a consistent log/marker
            logging.info("Menu action completed.")


if __name__ == "__main__":
    main()