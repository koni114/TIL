class MetaClass(type):
    def __new__(meta, name, bases, class_dict):
        print(f"실행 : {name}, 메타 {meta}.__new__")
        print(f"기반 클래스들 : {bases}")
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases:
            if class_dict['sides']  < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(metaclass=ValidatePolygon):
    sides = None


class Triangle(Polygon):
    sides = 3