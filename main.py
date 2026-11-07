import math


SUBJECTS = ("Telugu", "Hindi", "English", "Maths", "Science", "Social")
GRADE_THRESHOLDS = ((90, "A"), (80, "B"), (70, "C"), (60, "D"), (50, "E"))
MAX_TOTAL = len(SUBJECTS) * 100


def normalize_student_id(student_id):
    return student_id.strip().upper()


def validate_student_id(student_id, students, current_id=None):
    normalized = normalize_student_id(student_id)
    if not normalized:
        return False, "Student ID cannot be blank."
    if normalized != current_id and normalized in students:
        return False, "That student ID already exists."
    return True, normalized


def validate_name(name):
    name = name.strip()
    return (bool(name), "Student name cannot be blank." if not name else name)


def validate_mark(mark):
    try:
        value = float(mark)
    except (TypeError, ValueError):
        return False, "Please enter a number from 0 to 100."
    if not math.isfinite(value) or not 0 <= value <= 100:
        return False, "Please enter a finite number from 0 to 100."
    return True, value


def calculate_total(marks):
    return sum(marks.values())


def calculate_percentage(marks):
    return calculate_total(marks) / len(SUBJECTS)


def calculate_grade(percentage):
    for threshold, grade in GRADE_THRESHOLDS:
        if percentage >= threshold:
            return grade
    return "F"


def is_passing(marks):
    return all(marks[subject] >= 35 for subject in SUBJECTS)


def student_summary(student):
    marks = student["marks"]
    percentage = calculate_percentage(marks)
    return {"total": calculate_total(marks), "percentage": percentage,
            "grade": calculate_grade(percentage), "passed": is_passing(marks)}


def add_student(students, student_id, name, marks):
    valid, result = validate_student_id(student_id, students)
    if not valid:
        return False, result
    normalized_id = result
    valid, result = validate_name(name)
    if not valid:
        return False, result
    checked_marks = {}
    for subject in SUBJECTS:
        valid, checked = validate_mark(marks.get(subject))
        if not valid:
            return False, f"{subject}: {checked}"
        checked_marks[subject] = checked
    students[normalized_id] = {"name": name.strip(), "marks": checked_marks}
    return True, normalized_id


def update_student(students, student_id, name, marks):
    student_id = normalize_student_id(student_id)
    if student_id not in students:
        return False, "Student ID not found."
    valid, checked_name = validate_name(name)
    if not valid:
        return False, checked_name
    checked_marks = {}
    for subject in SUBJECTS:
        valid, checked = validate_mark(marks.get(subject))
        if not valid:
            return False, f"{subject}: {checked}"
        checked_marks[subject] = checked
    students[student_id] = {"name": checked_name, "marks": checked_marks}
    return True, student_id


def delete_student(students, student_id):
    if student_id not in students:
        return False, "Student ID not found."
    del students[student_id]
    return True, student_id


def ranked_students(students):
    ordered = sorted(students.items(), key=lambda item: (-calculate_total(item[1]["marks"]), item[0]))
    result = []
    previous_total = None
    previous_rank = 0
    for position, (student_id, student) in enumerate(ordered, start=1):
        total = calculate_total(student["marks"])
        rank = previous_rank if total == previous_total else position
        result.append((rank, student_id, student))
        previous_total, previous_rank = total, rank
    return result


def subject_statistics(students):
    if not students:
        return {}
    statistics = {}
    for subject in SUBJECTS:
        values = {student_id: student["marks"][subject] for student_id, student in students.items()}
        highest = max(values.values())
        lowest = min(values.values())
        statistics[subject] = {"percentage": sum(values.values()) / len(values),
                               "highest": highest,
                               "lowest": lowest,
                               "highest_students": [sid for sid, mark in values.items() if mark == highest],
                               "lowest_students": [sid for sid, mark in values.items() if mark == lowest]}
    return statistics


def read_mark(prompt, allow_blank=False, existing=None):
    while True:
        value = input(prompt).strip()
        if allow_blank and not value:
            return existing
        valid, result = validate_mark(value)
        if valid:
            return result
        print(result)


def read_student_marks(prefix="  ", existing=None):
    marks = {}
    for subject in SUBJECTS:
        old = existing[subject] if existing else None
        suffix = f" [{old:.2f}]" if old is not None else ""
        marks[subject] = read_mark(f"{prefix}{subject}{suffix}: ", existing is not None, old)
    return marks


def print_report(student_id, student):
    summary = student_summary(student)
    print(f"\n{'=' * 42}\nReport Card: {student['name']} ({student_id})\n{'=' * 42}")
    print(f"{'Subject':<16}{'Marks':>10}")
    print("-" * 26)
    for subject in SUBJECTS:
        print(f"{subject:<16}{student['marks'][subject]:>10.2f}")
    print("-" * 26)
    print(f"{'Total':<16}{summary['total']:>10.2f} / {MAX_TOTAL:.2f}")
    print(f"{'Percentage':<16}{summary['percentage']:>9.2f}%")
    print(f"{'Grade':<16}{summary['grade']:>10}")
    print(f"{'Status':<16}{'Pass' if summary['passed'] else 'Fail':>10}")


def run_menu():
    students = {}
    print("Welcome to the Student Grade Analyzer!")
    while True:
        print("\n" + "=" * 34)
        print("       STUDENT GRADE ANALYZER")
        print("=" * 34)
        print("1. Add a student\n2. View all students\n3. Search by ID\n4. Update a student\n5. Delete a student\n6. Display report card\n7. Display rankings\n8. Subject statistics\n9. Exit")
        print(f"\nStudents currently stored: {len(students)}")
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if choice == "1":
            student_id = input("Student ID: ")
            name = input("Student name: ")
            valid, message = validate_student_id(student_id, students)
            if not valid:
                print(message)
                continue
            valid, message = validate_name(name)
            if not valid:
                print(message)
                continue
            ok, message = add_student(students, student_id, name, read_student_marks())
            print("Student added." if ok else message)
        elif choice == "2":
            if not students:
                print("No students have been added yet.")
            else:
                print(f"\nAll Students ({len(students)})")
                print(f"{'ID':<12}{'Name':<20}{'Total':>10}{'Percentage':>14}")
                print("-" * 56)
            for student_id in sorted(students):
                student = students[student_id]
                summary = student_summary(student)
                print(f"{student_id:<12} {student['name']:<20} Total: {summary['total']:>7.2f}  Percentage: {summary['percentage']:>6.2f}%\n")
        elif choice in ("3", "6"):
            student_id = normalize_student_id(input("Student ID: "))
            if student_id not in students:
                print("Student ID not found.")
            elif choice == "3":
                print(f"{student_id}: {students[student_id]['name']}")
            else:
                print_report(student_id, students[student_id])
        elif choice == "4":
            student_id = normalize_student_id(input("Student ID: "))
            if student_id not in students:
                print("Student ID not found.")
                continue
            student = students[student_id]
            name = input(f"Name [{student['name']}]: ").strip() or student["name"]
            ok, message = update_student(students, student_id, name, read_student_marks(existing=student["marks"]))
            print("Student updated." if ok else message)
        elif choice == "5":
            student_id = normalize_student_id(input("Student ID: "))
            if student_id in students and input("Delete this student? (y/n): ").strip().lower() == "y":
                delete_student(students, student_id)
                print("Student deleted.")
            else:
                print("Deletion cancelled. No records were changed.")
        elif choice == "7":
            if not students:
                print("No students have been added yet.")
            else:
                print("\nRank  ID          Name                     Total   Percentage  Status")
                print("-" * 70)
            for rank, student_id, student in ranked_students(students):
                summary = student_summary(student)
                print(f"{rank:<5} {student_id:<12} {student['name']:<20} {summary['total']:>7.2f} {summary['percentage']:>7.2f}% {'Pass' if summary['passed'] else 'Fail'}")
        elif choice == "8":
            if not students:
                print("No students available for statistics.")
            else:
                for subject, stats in subject_statistics(students).items():
                    print(f"\n{subject}: percentage {stats['percentage']:.2f}%, highest {stats['highest']:.2f} ({', '.join(stats['highest_students'])}), lowest {stats['lowest']:.2f} ({', '.join(stats['lowest_students'])})")
        elif choice == "9":
            if input("Are you sure you want to exit? (y/n): ").strip().lower() == "y":
                print("Goodbye!")
                return
            print("Exit cancelled.")
        else:
            print("Please choose a number from 1 to 9.")


if __name__ == "__main__":
    run_menu()
