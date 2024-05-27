from random import randint

import pytest
from faker import Faker

from src.exams.retest.task_1.uni import Uni


class SetUpper:
    def __init__(self):
        fake = Faker()
        lectors = [fake.name() for _ in range(3)]
        courses = ["Linear Algebra", "Computer Science", "Progs"]
        students = [fake.name() for _ in range(30)]
        self.students = students
        self.lectors = lectors
        self.courses = courses
        self.uni = Uni()

    def set_up(self):
        for student in self.students:
            self.uni.add_student(student)
        for course in self.courses:
            self.uni.add_course(course)
        for lector in self.lectors:
            self.uni.add_lector(lector)
        return self.uni

    def place(self, uni: Uni):
        students_score = {}
        for i in range(3):
            uni.add_lector_to_course(self.courses[i], self.lectors[i])

        for student in self.students:
            marks = []
            for i in range(3):
                mark = randint(1, 5)
                marks.append(mark)
                uni.add_student_to_course(student, mark, self.courses[i])
            students_score.update({student: sum(marks) / len(marks)})

        return uni, students_score


class TestUni:
    upper = SetUpper()
    uni = upper.set_up()
    uni, students_score = upper.place(uni)

    def test_find_student_exception(self):
        with pytest.raises(ValueError):
            self.uni._check_student(hash("123"), "123")

    def test_find_lector_exception(self):
        with pytest.raises(ValueError):
            self.uni._check_lector(hash("123"), "123")

    def test_find_course_exception(self):
        with pytest.raises(ValueError):
            self.uni._check_course(hash("123"), "123")

    def test_add_student_exception(self):
        with pytest.raises(ValueError):
            self.uni.add_student(self.upper.students[0])

    def test_add_lector_exception(self):
        with pytest.raises(ValueError):
            self.uni.add_lector(self.upper.lectors[0])

    def test_add_course_exception(self):
        with pytest.raises(ValueError):
            self.uni.add_course(self.upper.courses[0])

    def test_show_func(self):
        names = [course.title for course in self.uni.show_all_courses()]
        assert names == self.upper.courses

    def test_students_score(self):
        for student in self.students_score:
            assert self.uni.get_score_of_student(student) == self.students_score[student]

    def test_student_courses(self):
        for student in self.students_score:
            courses_names = [course.title for course in self.uni.get_courses_of_student(student)]
            assert courses_names == self.upper.courses

    def test_course_students(self):
        for course in self.upper.courses:
            students_names = [student.name for student in self.uni.get_students_of_course(course)]
            assert students_names == self.upper.students
