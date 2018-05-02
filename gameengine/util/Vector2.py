from gameengine.util.EventDispatcher import EventDispatcher


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, Vector2) or isinstance(x, tuple):
            self._x = x[0]
            self._y = x[1]
        else:
            self._x = float(x)
            self._y = float(y)

        self.hasChanged = EventDispatcher(self)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: float):
        if value != self._x:
            old = Vector2(self)

            self._x = float(value)
            self.hasChanged(old, self)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: float):
        if value != self._y:
            old = Vector2(self)

            self._y = float(value)
            self.hasChanged(old, self)

    def set(self, x: float, y: float=None):
        if isinstance(x, Vector2) or isinstance(x, tuple):
            if x != self:
                old = Vector2(self)

                self._x = x[0]
                self._y = x[1]

                self.hasChanged(old, self)

        else:
            if x != self._x or y != self._y:
                old = Vector2(self)

                self._x = float(x)
                self._y = float(y)

                self.hasChanged(old, self)

    def tuple(self):
        return self._x, self._y

    def toIntTuple(self):
        return int(self._x), int(self._y)

    def __eq__(self, other):
        if other is None:
            return self is None
        return self._x == other[0] and self._y == other[1]

    def __bool__(self):
        return self != Vector2(0, 0)

    def __add__(self, other):
        return Vector2(self._x + other[0], self._y + other[1])

    def __iadd__(self, other):
        if other != Vector2(0, 0):
            old = Vector2(self)

            self._x += other[0]
            self._y += other[1]

            self.hasChanged(old, self)

        return self

    def __sub__(self, other):
        return Vector2(self._x - other[0], self._y - other[1])

    def __isub__(self, other):
        if other != Vector2(0, 0):
            old = Vector2(self)

            self._x -= other[0]
            self._y -= other[1]

            self.hasChanged(old, self)

        return self

    def __mul__(self, other):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            return Vector2(self._x * other[0], self._y * other[1])
        else:
            return Vector2(self._x * other, self._y * other)

    def __imul__(self, other):
        old = Vector2(self)

        if isinstance(other, Vector2) or isinstance(other, tuple):
            self._x *= other[0]
            self._y *= other[1]
        else:
            self._x *= other
            self._y *= other

        if self != old:
            self.hasChanged(old, self)

        return self

    def __pow__(self, other, modulo=None):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            return Vector2(self._x ** other[0], self._y ** other[1])
        else:
            return Vector2(self._x ** other, self._y ** other)

    def __ipow__(self, other):
        old = Vector2(self)

        if isinstance(other, Vector2) or isinstance(other, tuple):
            self._x **= other[0]
            self._y **= other[1]
        else:
            self._x **= other
            self._y **= other

        if self != old:
            self.hasChanged(old, self)

        return self

    def __truediv__(self, other):
        if isinstance(other, Vector2) or isinstance(other, tuple):
            return Vector2(self._x / other[0], self._y / other[1])
        else:
            return Vector2(self._x / other, self._y / other)

    def __idiv__(self, other):
        old = Vector2(self)

        if isinstance(other, Vector2) or isinstance(other, tuple):
            self._x /= other[0]
            self._y /= other[1]
        else:
            self._x /= other
            self._y /= other

        if self != old:
            self.hasChanged(old, self)

        return self

    def __neg__(self):
        return Vector2(-self._x, -self._y)

    def __getitem__(self, item):
        if item == 0:
            return self._x
        elif item == 1:
            return self._y
        else:
            raise IndexError

    def __setitem__(self, key, value: float):
        if key == 0:
            self._x = float(value)
        elif key == 1:
            self._y = float(value)
        else:
            raise IndexError

    def __repr__(self):
        return "<Vector2({}, {})>".format(self._x, self._y)

    def __str__(self):
        return "[{}, {}]".format(self._x, self._y)