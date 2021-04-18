# problem 1
# 직사각형 1개와 정사각형 1개 만들기
# 너비(width), 높이(height), 색상(color)를 한번에 설정 할 수 있는
# 메서드를 만들고, 다음 값으로 각 객체의 속성값을 변경한 후
# 사각형 너비와 색상도 함께 출력하기

class Quadrangle:

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def get_area(self):
        return self.width * self.height


square1 = Quadrangle(10, 5, 'red')
square2 = Quadrangle(7, 7, 'blue')

print(square1.get_area())
print(square2.get_area())


class Quadrangle:
    def __init__(self, width, height, color):
        self.__width = width
        self.__height = height
        self.__color = color

    def get_area(self):
        return self.__width * self.__height

    def __set_area(self, width, height):
        self.__width = width
        self.__height = height



square = Quadrangle(5, 5, "black")
dir(square)


square = Quadrangle(5, 5, 'black')
print(square.__set_area(10, 10))



print(square.get_area())
print(square._width)
square._width = 10
print(square.get_area())
square._set_area(3, 3)
print(square.get_area())


