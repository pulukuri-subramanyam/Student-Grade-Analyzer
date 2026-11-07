# Student Grade Analyzer

A beginner-friendly terminal Python program that keeps student records in memory and calculates totals, percentages, grades, pass/fail status, rankings, and subject statistics.

## Requirements and commands

Use Python 3.9 or newer. From this folder, run:

```text
python main.py
python -m unittest -v
```

## Rules

Each record is stored under an uppercase student ID and contains a name plus marks for Telugu, Hindi, English, Maths, Science, and Social. Marks must be finite numbers from 0 to 100. Grade uses the unrounded percentage: A (90+), B (80–89.99), C (70–79.99), D (60–69.99), E (50–59.99), F (below 50). A student passes only when every subject is at least 35, so a high percentage can still be a fail.

Rankings sort by total, use competition ranking (1, 2, 2, 4), and use ID as the tie display order. Subject statistics show percentages, extremes, and every tied student.

## Menu and example

The menu lets you add, view, search, update, delete, print a report card, show rankings, and show subject statistics. A short session looks like:

```text
Welcome to the Student Grade Analyzer!
Students currently stored: 0
Choose an option: 1
Student ID: s01
Student name: Anika
  Telugu: 85
  Hindi: 92
  English: 88
  Maths: 90
  Science: 87
  Social: 84
Student added.
Choose an option: 6
Student ID: s01
==========================================
Report Card: Anika (S01)
==========================================
Subject              Marks
--------------------------
Telugu               85.00
Hindi                92.00
English              88.00
Maths                90.00
Science              87.00
Social               84.00
--------------------------
Total               526.00 / 600.00
Percentage    87.67%
Grade         B
Status        Pass
Choose an option: 9
Are you sure you want to exit? (y/n): y
Goodbye!
```

The project uses variables, strings, numbers, booleans, conditions, loops, functions, dictionaries, lists, sorting, formatting, imports, and basic exception handling. Records are deliberately stored only in memory, so they disappear when the program closes.
