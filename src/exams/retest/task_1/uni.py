from dataclasses import dataclass


@dataclass
class Course:
    title: str
    id: int
    lector: int
    students: list[int]


@dataclass
class Student:
    name: str
    id: int
    courses: dict[int, int]


@dataclass
class Lector:
    name: str
    id: int
    courses: list[int]


class Uni:
    def __init__(self) -> None:
        self.students: dict[int, Student] = {}
        self.lectors: dict[int, Lector] = {}
        self.courses: dict[int, Course] = {}

    def _check_student(self, student_id: int, name: str) -> None:
        if student_id not in self.students:
            raise ValueError(f"{name} not registered")

    def _check_course(self, course_id: int, name: str) -> None:
        if course_id not in self.courses:
            raise ValueError(f"{name} not registered")

    def _check_lector(self, lector_id: int, name: str) -> None:
        if lector_id not in self.lectors:
            raise ValueError(f"{name} not registered")

    def show_all_courses(self) -> list[Course]:
        return list(self.courses.values())

    def get_courses_of_student(self, name: str) -> list[Course]:
        student_id = hash(name)
        self._check_student(student_id, name)
        courses = self.students[student_id].courses
        return [self.courses[course] for course in courses.keys()]

    def get_courses_of_lector(self, name: str) -> list[Course]:
        lector_id = hash(name)
        self._check_lector(lector_id, name)
        courses = self.lectors[lector_id].courses
        return [self.courses[course] for course in courses]

    def get_score_of_student(self, name: str) -> float:
        student_id = hash(name)
        self._check_student(student_id, name)
        courses = self.students[student_id].courses
        return sum(courses.values()) / len(courses)

    def get_lector_of_course(self, name: str) -> Lector:
        course_id = hash(name)
        self._check_course(course_id, name)
        course = self.courses[course_id]
        return self.lectors[course.lector]

    def get_students_of_course(self, name: str) -> list[Student]:
        course_id = hash(name)
        self._check_course(course_id, name)
        course = self.courses[course_id]
        return [self.students[student_id] for student_id in course.students]

    def add_course(self, course_name: str) -> None:
        course_id = hash(course_name)
        if course_id in self.courses:
            raise ValueError("Course already exists")
        course = Course(course_name, course_id, 0, [])
        self.courses.update({course_id: course})

    def add_lector(self, name: str) -> None:
        lector_id = hash(name)
        if lector_id in self.lectors:
            raise ValueError("Lector already exists")
        lector = Lector(name, lector_id, [])
        self.lectors.update({lector_id: lector})

    def add_student(self, name: str) -> None:
        student_id = hash(name)
        if student_id in self.students:
            raise ValueError("Student already exists")
        student = Student(name, student_id, {})
        self.students.update({student_id: student})

    def add_lector_to_course(self, course_name: str, lector_name: str) -> None:
        lector_id = hash(lector_name)
        course_id = hash(course_name)
        self._check_course(course_id, course_name)
        self._check_lector(lector_id, lector_name)
        lector = self.lectors[lector_id]
        course = self.courses[course_id]
        course.lector = lector_id
        lector.courses.append(course_id)

    def add_student_to_course(self, student_name: str, mark: int, course_name: str) -> None:
        student_id = hash(student_name)
        course_id = hash(course_name)
        self._check_course(course_id, course_name)
        self._check_student(student_id, student_name)
        student = self.students[student_id]
        course = self.courses[course_id]
        course.students.append(student_id)
        student.courses.update({course_id: mark})
