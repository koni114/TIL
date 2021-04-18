from abc import *
from abc import ABC


class Character(object, metaclass=ABCMeta):
    def __init__(self, name='yourname', health_point=100, striking_power=3, defensive_power=3):
        self.name = name
        self.health_point = health_point
        self.striking_power = striking_power
        self.defensive_power = defensive_power

    def info(self):
        print(self.name, self.health_point, self.striking_power, self.defensive_power)

    @abstractmethod
    def attack(self, obj):
        pass

    @abstractmethod
    def receive(self, obj):
        pass


class Warrior(Character):
    def attack(self, obj):
        print("칼로 찌르다")
        obj.receive(self.striking_power)

    def receive(self, striking_point):
        if self.health_point <= striking_point:
            self.health_point = 0
            print("죽었음")
        else:
            self.health_point = self.health_point - striking_point


class Elf(Character):
    def __init__(self, name='yourname', health_point=100, striking_power=3, defensive_power=3):
        super().__init__(name, health_point, striking_power, defensive_power)
        self.wear_manteau = 1

    def attack(self, obj):
        print("마법을 쓰다")
        obj.receive(self.striking_power)

    def receive(self, obj):
        if self.wear_manteau == 1:
            self.wear_manteau = 0
            pass
        if self.health_point <= obj.striking_power:
            self.health_point = 0
            print("죽었음")
        else:
            self.health_point = self.health_point - obj.striking_power


class Wizard(Elf):
    def use_wizard(self):
        self.health_point += 3


warrior1 = Warrior()
warrior2 = Warrior()
elf1 = Elf(name='efl1', health_point=100, striking_power=1, defensive_power=3)
warrior1.attack(warrior2)
print(warrior2.health_point)


# 나쁜예
# 학생성적과 수강하는 코스를 한개의 class에서 다루는 예
# 한 클래스에서 두개의 책임을 갖기 때문에, 수정이 용이하지 않음
class StudentScoreAndCourseManager(object):
    def __init__(self):
        scores = {}
        courses = {}

    def get_score(self, student_name, course):
        pass

    def get_courses(self, student_name):
        pass


# 변경예
class ScoreManager(object):
    def __init__(self):
        scores = {}

    def get_scores(self, student_name, course):
        pass


class CourseManager(object):
    def __init__(self):
        courses = {}

    def get_courses(self, student_name):
        pass


# 나쁜 예
class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


# 나쁜예
class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


class AreaCalculator(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def total_area(self):
        total = 0
        for shape in self.shapes:
            total += shape.area()
        return total


shapes = [Rectangle(2, 3), Rectangle(1, 6), Circle(5), Circle(7)]
calculator = AreaCalculator(shapes)
print("The total Area is : ", calculator.total_area())


# bubble_sort의 이름이 바뀌면, 상속 클래스인 SortManager의 BubbleSort도 바뀌어야 함
class BubbleSort:
    def sort(self):
        print("bubble_sort")
        # sorting algorithm
        pass


class QuickSort:
    def sort(self):
        print("Quick_sort")
        pass


class SortManager:
    def __init__(self, sort_method):
        self.sort_method = sort_method

    def begin_sort(self):
        self.sort_method.sort()

