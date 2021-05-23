from collections import defaultdict, namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))


class Subject:
    def __init__(self):
        self.grades = []

    def report_grade(self, score, weight):
        self.grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self.grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self.subjects = defaultdict(Subject)

    def get_subject(self, subject):
        return self.subjects[subject]

    def average_grade(self):
        total, count = 0, 0
        for subject in self.subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class GradeBook:
    def __init__(self):
        self.students = defaultdict(Student)

    def get_student(self, name):
        return self.students[name]


book = GradeBook()
albert = book.get_student('알버트 아인슈타인')
math = albert.get_subject('수학')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('체육')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
