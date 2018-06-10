from typing import List

import pyglet

from gameengine.core.GameObject import GameObject
from gameengine.interfaces.IDrawable import IDrawable
from gameengine.interfaces.IManageable import IManageable
from gameengine.managers.Manager import Manager


class Label(GameObject, pyglet.text.Label, IManageable, IDrawable):
	def __init__(self):
		GameObject.__init__(self)
		pyglet.text.Label.__init__(self, "placeholder", "Sans", 14, color=(255, 255, 255, 255))

		self._managers = []

		self._order = 0

		from gameengine.managers.DrawingManager import DrawingManager
		DrawingManager().add(self)

	@property
	def order(self) -> int:
		return self._order

	@order.setter
	def order(self, val: int):
		self._order = val

	@property
	def managers(self) -> List[Manager]:
		return self._managers

	def draw(self):
		coords = self.transform.position

		self.x = int(coords.x)
		self.y = int(coords.y)
		super().draw()
