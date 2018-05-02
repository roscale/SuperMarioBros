from gameengine.components.Component import Component
from gameengine.util.Vector2 import Vector2


class Transform(Component):
	def __init__(self):
		super().__init__()

		self._position = Vector2()
		self.depth = 0.0

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, tup):
		self._position.set(tup)

	def translate(self, delta):
		self._position += delta