import pyglet

from gameengine.components.Component import Component
from gameengine.interfaces.IOrderable import IOrderable
from gameengine.util.Vector2 import Vector2


class SpriteRenderer(Component, IOrderable):
	def __init__(self):
		super().__init__()

		self.sprite: pyglet.sprite.Sprite = None
		self._order = 0
		self._opacity = 255

		self._offset = Vector2()

		from gameengine.managers.DrawingManager import DrawingManager
		DrawingManager().add(self)

	def init(self):
		def changedPos(sender, old, new):
			from gameengine.managers.DrawingManager import DrawingManager

			if self.sprite is not None:
				DrawingManager().frustumCulling.remove(self)
				self.sprite.position = new + self.offset
				DrawingManager().frustumCulling.insert(self)

		self.gameObject.transform.position.hasChanged += changedPos

	@property
	def offset(self) -> Vector2:
		return self._offset

	@offset.setter
	def offset(self, value):
		self.offset.set(value)

		if self.sprite is not None:
			from gameengine.managers.DrawingManager import DrawingManager
			DrawingManager().frustumCulling.remove(self)
			self.sprite.position = self.gameObject.transform.position + self.offset
			DrawingManager().frustumCulling.insert(self)

	@property
	def size(self) -> Vector2:
		if self.sprite is not None:
			return Vector2(self.sprite.width, self.sprite.height)
		return Vector2()

	@property
	def order(self):
		return self._order

	@order.setter
	def order(self, val: int):
		self._order = val

	def setImage(self, image):
		from gameengine.managers.DrawingManager import DrawingManager

		if self.sprite is not None:
			if image == self.sprite.image:
				return
			else:
				DrawingManager().frustumCulling.remove(self)
				self.sprite.batch = None
				self.sprite.delete()

		self.sprite = pyglet.sprite.Sprite(image, *(self.gameObject.transform.position + self.offset))
		DrawingManager().frustumCulling.insert(self)

		self.sprite.opacity = self._opacity

	@property
	def opacity(self) -> int:
		return self._opacity

	@opacity.setter
	def opacity(self, val):
		self._opacity = val
		self.sprite.opacity = val