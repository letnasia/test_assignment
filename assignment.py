from math import pi
from typing import Optional, List


class Shape:
    def get_area(self):
        raise NotImplemented()

    def get_perimeter(self):
        raise NotImplemented()

    def name(self) -> str:
        raise NotImplemented()

    def parse(self, parameters: List[str]) -> bool:
        raise NotImplemented()

    def parse_point(self, i: int, lst: List[str]):
        x = self._parse_int(lst[i + 1])
        y = self._parse_int(lst[i + 2])
        return x, y

    @staticmethod
    def _parse_int(text: str):
        try:
            return int(text)
        except:
            return None


class Rectangle(Shape):
    top = None
    right = None
    bottom = None
    left = None

    def get_area(self):
        a = self.top - self.bottom
        b = self.right - self.left
        return a * b

    def get_perimeter(self):
        a = self.top - self.bottom
        b = self.right - self.left
        return 2 * a + 2 * b

    def name(self) -> str:
        return "Rectangle"

    def parse_point(self, i: int, lst: List[str]):
        x = self._parse_int(lst[i + 1])
        y = self._parse_int(lst[i + 2])
        return x, y

    def parse(self, parameters: List[str]) -> bool:
        i = 0
        while i < len(parameters):
            if parameters[i] == "TopRight":
                if i + 2 >= len(parameters):
                    return False
                self.top, self.right = self.parse_point(i, parameters)
                i += 3
            elif parameters[i] == "BottomLeft":
                if i + 2 >= len(parameters):
                    return False
                self.bottom, self.left = self.parse_point(i, parameters)
                i += 3
            else:
                return False
        if (self.top is None
                or self.right is None
                or self.left is None
                or self.bottom is None):
            return False
        return self.bottom <= self.top and self.left <= self.right


class Square(Rectangle):
    side = None

    def name(self) -> str:
        return "Square"

    def parse(self, parameters: List[str]) -> bool:
        i = 0
        while i < len(parameters):
            if parameters[i] == "TopRight":
                if i + 2 >= len(parameters):
                    return False
                self.top, self.right = self.parse_point(i, parameters)
                i += 3
            elif parameters[i] == "Side":
                if i + 1 >= len(parameters):
                    return False
                self.side = self._parse_int(parameters[i + 1])
                i += 2
            else:
                return False
        is_valid = (self.top is not None
                    and self.right is not None
                    and self.side is not None)
        if is_valid:
            self.bottom = self.top - self.side
            self.left = self.right - self.side
        return is_valid


class Circle(Shape):
    x = None
    y = None
    radius = None

    def get_area(self):
        return pi * self.radius * self.radius

    def get_perimeter(self):
        return 2 * pi * self.radius

    def name(self) -> str:
        return "Circle"

    def parse(self, parameters: List[str]) -> bool:
        i = 0
        while i < len(parameters):
            if parameters[i] == "Center":
                if i + 2 >= len(parameters):
                    return False
                self.x = self._parse_int(parameters[i + 1])
                self.y = self._parse_int(parameters[i + 2])
                i += 3
            elif parameters[i] == "Radius":
                if i + 1 >= len(parameters):
                    return False
                self.radius = self._parse_int(parameters[i + 1])
                i += 2
            else:
                return False
        return (self.x is not None
                and self.y is not None
                and self.radius is not None)


ALL_SHAPES = {
    "Square": Square,
    "Rectangle": Rectangle,
    "Circle": Circle,
}


def find_shape(name: str) -> Optional[Shape]:
    if name in ALL_SHAPES:
        return ALL_SHAPES[name]()


def main():
    while True:
        text = input("Enter a shape and its parameters: ")
        tokens = text.strip().split()
        if not tokens:
            continue
        shape_name = tokens[0]
        shape_params = tokens[1:]
        shape = find_shape(shape_name)
        if shape is None:
            print(f"Unknown shape '{shape_name}'")
            continue
        if not shape.parse(shape_params):
            print("Invalid parameters for {shape_name}")
            continue
        perimeter = round(shape.get_perimeter(), 3)
        area = round(shape.get_area(), 3)
        print(f"{shape.name()}: Perimeter {perimeter} Area {area}")


def test():
    def test_shape_parse(cls, params):
        params = params.split()
        s = cls()
        if s.parse(params):
            return s

    assert test_shape_parse(Square, "TopRight 1 1 Side 1"), "Square: Valid"
    assert test_shape_parse(Square, "Side 1 TopRight 1 1"), "Square: Valid"
    assert not test_shape_parse(Square, "TopRight 1 1"), "Square: Invalid"
    assert not test_shape_parse(Square, "Side 1"), "Square: Invalid"
    assert not test_shape_parse(Square, "Side"), "Square: Invalid"
    assert not test_shape_parse(Square, "Side 1 TopRight 1"), "Square: Invalid"
    assert not test_shape_parse(Square, "Side 1 TopRight 1 1 Foo 3"), "Square: Invalid"
    assert not test_shape_parse(Square, "1 1 1"), "Square: Invalid"
    assert not test_shape_parse(Square, ""), "Square: Invalid"
    shape = test_shape_parse(Square, "TopRight 1 1 Side 1")
    assert shape.get_perimeter() == 4
    assert shape.get_area() == 1
    assert shape.top == 1
    assert shape.right == 1
    assert shape.bottom == 0
    assert shape.left == 0
    assert shape.side == 1
    shape = test_shape_parse(Square, "TopRight 2 2 Side 2")
    assert shape.top == 2
    assert shape.right == 2
    assert shape.bottom == 0
    assert shape.left == 0
    assert shape.side == 2
    assert shape.get_perimeter() == 8
    assert shape.get_area() == 4

    assert test_shape_parse(Rectangle, "TopRight 2 2 BottomLeft 1 1"), "Rectangle: Valid"
    assert test_shape_parse(Rectangle, "BottomLeft 1 1 TopRight 2 2"), "Rectangle: Valid"
    assert not test_shape_parse(Rectangle, "TopRight 1 1"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "BottomLeft 1 1"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "BottomLeft"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "BottomLeft 1 1 1 TopRight 1"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "BottomLeft 1  1 TopRight 1 1 Foo 3"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "1 1 1 1"), "Rectangle: Invalid"
    assert not test_shape_parse(Rectangle, "BottomLeft 2 2 TopRight 1 1"), "Rectangle: Invalid"
    shape = test_shape_parse(Rectangle, "TopRight 2 2 BottomLeft 1 1")
    assert shape.get_perimeter() == 4
    assert shape.get_area() == 1
    shape = test_shape_parse(Rectangle, "TopRight 4 4 BottomLeft 1 1")
    assert shape.get_perimeter() == 12
    assert shape.get_area() == 9

    assert test_shape_parse(Circle, "Center 1 1 Radius 2"), "Circle: Valid"
    assert test_shape_parse(Circle, "Radius 2 Center 1 1"), "Circle: Valid"
    assert not test_shape_parse(Circle, "Center 1 1"), "Circle: Invalid"
    assert not test_shape_parse(Circle, "Center 1"), "Circle: Invalid"
    assert not test_shape_parse(Circle, "Center"), "Circle: Invalid"
    assert not test_shape_parse(Circle, "Center 1 Radius 2"), "Circle: Invalid"
    assert not test_shape_parse(Circle, "Center 1 1 Radius 2 Foo 3"), "Circle: Invalid"
    assert not test_shape_parse(Circle, "1 1 2"), "Circle: Invalid"
    shape = test_shape_parse(Circle, "Radius 2 Center 1 1")
    assert round(shape.get_perimeter(), 3) == 12.566
    assert round(shape.get_area(), 3) == 12.566
    shape = test_shape_parse(Circle, "Radius 4 Center 1 1")
    assert round(shape.get_perimeter(), 3) == 25.133
    assert round(shape.get_area(), 3) == 50.265


if __name__ == "__main__":
    test()
    # main()

