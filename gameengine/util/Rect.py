from gameengine.util.EventDispatcher import EventDispatcher
from gameengine.util.Vector2 import Vector2


class Rect:
    def __init__(self, left=.0, top=.0, width=.0, height=.0):
        self._topLeft = Vector2(left, top)
        self._size = Vector2(width, height)

        self.hasChanged = EventDispatcher(self)

        def topLeftChanged(sender, old, new):
            self.hasChanged(Rect(*new, *self._size), self)

        def sizeChanged(sender, old, new):
            self.hasChanged(Rect(*self._topLeft, *new), self)

        self._topLeft.hasChanged += topLeftChanged
        self._size.hasChanged += sizeChanged

    def tuple(self):
        return (*self._topLeft.x, *self._size)

    def bbox(self):
        return (*self._topLeft, *(self._topLeft + self._size))

    def __getitem__(self, item):
        if item == 0:
            return self._topLeft.x
        elif item == 1:
            return self._topLeft.y
        elif item == 2:
            return self._size.x
        elif item == 3:
            return self._size.y
        else:
            raise IndexError

    def __setitem__(self, key, value: float):
        if key == 0:
            self._topLeft.x = float(value)
        elif key == 1:
            self._topLeft.y = float(value)
        elif key == 2:
            self._size.x = float(value)
        elif key == 3:
            self._size.y = float(value)
        else:
            raise IndexError

    @property
    def size(self) -> Vector2:
        return self._size
    @size.setter
    def size(self, value: Vector2):
        self._size.set(value)

    @property
    def width(self) -> float:
        return self._size.x
    @width.setter
    def width(self, value):
        self._size.x = value

    @property
    def height(self) -> float:
        return self._size.y
    @height.setter
    def height(self, value):
        self._size.y = value

    @property
    def top(self) -> float:
        return self._topLeft.y
    @top.setter
    def top(self, value):
        self._topLeft.y = value

    @property
    def left(self) -> float:
        return self._topLeft.x
    @left.setter
    def left(self, value):
        self._topLeft.x = value

    @property
    def x(self) -> float:
        return self.left
    @x.setter
    def x(self, value):
        self.left = value

    @property
    def y(self) -> float:
        return self.top
    @y.setter
    def y(self, value):
        self.top = value


    @property
    def bottom(self) -> float:
        return self._topLeft.y + self._size.y
    @bottom.setter
    def bottom(self, value):
        self._topLeft.y = value - self._size.y

    @property
    def right(self) -> float:
        return self._topLeft.x + self._size.x
    @right.setter
    def right(self, value):
        self._topLeft.x = value - self._size.x


    @property
    def topLeft(self) -> Vector2:
        return self._topLeft
    @topLeft.setter
    def topLeft(self, value):
        self._topLeft.set(value)

    @property
    def bottomLeft(self) -> Vector2:
        return self._topLeft + Vector2(0, self._size.y)
    @bottomLeft.setter
    def bottomLeft(self, value):
        self.left = value.x
        self.bottom = value.y

    @property
    def topRight(self) -> Vector2:
        return self._topLeft + Vector2(self._size.x, 0)
    @topRight.setter
    def topRight(self, value):
        self.right = value.x
        self.top = value.y

    @property
    def bottomRight(self) -> Vector2:
        return self._topLeft + self._size
    @bottomRight.setter
    def bottomRight(self, value):
        self.right = value.x
        self.bottom = value.y


    @property
    def midTop(self) -> Vector2:
        return self._topLeft + Vector2(self._size.x / 2, 0)
    @midTop.setter
    def midTop(self, value):
        self.left = value.x - (self._size.x / 2)
        self.top = value.y

    @property
    def midLeft(self) -> Vector2:
        return self._topLeft + Vector2(0, self._size.y / 2)
    @midLeft.setter
    def midLeft(self, value):
        self.left = value.x
        self.top = value.y - (self._size.y / 2)

    @property
    def midBottom(self) -> Vector2:
        return self._topLeft + Vector2(self._size.x / 2, self._size.y)
    @midBottom.setter
    def midBottom(self, value):
        self.left = value.x - (self._size.x / 2)
        self.bottom = value.y

    @property
    def midRight(self) -> Vector2:
        return self._topLeft + Vector2(self._size.x, self._size.y / 2)
    @midRight.setter
    def midRight(self, value):
        self.right = value.x
        self.top = value.y - (self._size.y / 2)


    @property
    def center(self) -> Vector2:
        return self._topLeft + (self._size / 2)
    @center.setter
    def center(self, value):
        self._topLeft.set(value - (self._size / 2))

    @property
    def centerX(self) -> float:
        return self.center.x
    @centerX.setter
    def centerX(self, value):
        self._topLeft.x = value - (self._size.x / 2)

    @property
    def centerY(self) -> float:
        return self.center.y
    @centerY.setter
    def centerY(self, value):
        self._topLeft.y = value - (self._size.y / 2)


    def copy(self):
        return Rect(*self._topLeft, *self._size)

    def move(self, dx: float, dy: float):
        self._topLeft += Vector2(dx, dy)

    def inflate(self, dw, dh):
        self._size += Vector2(dw, dh)

    def collidePoint(self, x, y):
        return self.left <= x < self.right and \
               self.top <= y < self.bottom

    def collideRect(self, other):
        return self.left < other.right and \
               self.top < other.bottom and \
               self.right > other.left and \
               self.bottom > other.top

    def __str__(self):
        return "[{}, {}, {}, {}]".format(*self._topLeft, *self._size)