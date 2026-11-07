import unittest
from unittest.mock import patch
from io import StringIO

from main import (MAX_TOTAL, SUBJECTS, add_student, calculate_percentage, calculate_grade,
                  calculate_total, delete_student, is_passing, ranked_students,
                  print_report, run_menu, subject_statistics, update_student,
                  validate_mark)


def marks(value):
    return {subject: value for subject in SUBJECTS}


class GradeAnalyzerTests(unittest.TestCase):
    def test_totals_percentages_and_boundaries(self):
        self.assertEqual(calculate_total(marks(80)), 480)
        self.assertEqual(MAX_TOTAL, 600)
        self.assertEqual(calculate_percentage(marks(80)), 80)
        for value, grade in [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (50, "E"), (49.99, "F")]:
            self.assertEqual(calculate_grade(value), grade)

    def test_pass_requires_every_subject(self):
        self.assertTrue(is_passing(marks(35)))
        failing_marks = marks(100)
        failing_marks["English"] = 34.99
        self.assertFalse(is_passing(failing_marks))

    def test_mark_validation(self):
        self.assertEqual(validate_mark("80.5"), (True, 80.5))
        for value in ("-1", "101", "nan", "inf", "abc"):
            self.assertFalse(validate_mark(value)[0])

    def test_add_duplicate_blank_and_normalization(self):
        students = {}
        self.assertFalse(add_student(students, " ", "A", marks(50))[0])
        self.assertFalse(add_student(students, "S2", " ", marks(50))[0])
        self.assertTrue(add_student(students, " s1 ", "A", marks(50))[0])
        self.assertFalse(add_student(students, "S1", "B", marks(50))[0])

    def test_missing_ids_are_rejected(self):
        students = {}
        self.assertEqual(update_student(students, "MISSING", "A", marks(50)),
                         (False, "Student ID not found."))
        self.assertEqual(delete_student(students, "MISSING"),
                         (False, "Student ID not found."))

    def test_update_delete_and_rejected_update(self):
        students = {}
        add_student(students, "S1", "A", marks(50))
        before = students["S1"].copy()
        self.assertFalse(update_student(students, "S1", "", marks(50))[0])
        self.assertEqual(students["S1"], before)
        self.assertTrue(update_student(students, "S1", "B", marks(90))[0])
        self.assertTrue(delete_student(students, "S1")[0])
        self.assertFalse(delete_student(students, "S1")[0])

    def test_invalid_update_leaves_record_unchanged(self):
        students = {}
        add_student(students, "S1", "A", marks(50))
        original = {"name": students["S1"]["name"], "marks": students["S1"]["marks"].copy()}
        invalid_marks = marks(90)
        invalid_marks["Social"] = 101
        self.assertFalse(update_student(students, " s1 ", "A", invalid_marks)[0])
        self.assertEqual(students["S1"], original)

    def test_report_contains_all_subjects_and_total(self):
        students = {}
        add_student(students, "S1", "A", marks(50))
        with patch("sys.stdout", new_callable=StringIO) as output:
            print_report("S1", students["S1"])
        report = output.getvalue()
        for subject in SUBJECTS:
            self.assertIn(subject, report)
        self.assertIn("/ 600.00", report)

    def test_ranking_ties(self):
        students = {}
        add_student(students, "B", "Bee", marks(80))
        add_student(students, "A", "Ace", marks(80))
        add_student(students, "C", "See", marks(70))
        self.assertEqual([(row[0], row[1]) for row in ranked_students(students)], [(1, "A"), (1, "B"), (3, "C")])

    def test_statistics_ties_and_empty(self):
        self.assertEqual(subject_statistics({}), {})
        students = {}
        add_student(students, "A", "Ace", {subject: 50 for subject in SUBJECTS})
        add_student(students, "B", "Bee", {subject: 50 for subject in SUBJECTS})
        stats = subject_statistics(students)["Maths"]
        self.assertEqual(stats["highest_students"], ["A", "B"])
        self.assertEqual(stats["lowest_students"], ["A", "B"])

    def test_invalid_menu_choice_and_exit_confirmation(self):
        with patch("builtins.input", side_effect=["wrong", "9", "y"]), patch("sys.stdout", new_callable=StringIO) as output:
            run_menu()
        self.assertIn("Please choose a number from 1 to 9.", output.getvalue())
        self.assertIn("Goodbye!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
