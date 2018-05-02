from gameengine.components.Component import Component
from gameengine.interfaces.IOrderable import IOrderable
from gameengine.interfaces.IResizable import IResizable
from gameengine.util.Rect import Rect
from gameengine.util.Vector2 import Vector2


class Input(Component, IResizable, IOrderable):
	def __init__(self):
		super().__init__()

		self._rect = Rect()
		self._offset = Vector2()
		self._order = 0

		from gameengine.managers.InputManager import InputManager
		InputManager().add(self)

	def init(self):
		self.updateRect()

	def attachGameObject(self, gameObject):
		super().attachGameObject(gameObject)

		def transformPosChanged(sender, oldPos, newPos):
			self.updateRect()

		gameObject.transform.position.hasChanged += transformPosChanged

	@property
	def rect(self) -> Rect:
		return self._rect

	def updateRect(self):
		self._rect.topLeft = self.gameObject.transform.position + self._offset

	@property
	def offset(self) -> Vector2:
		return self._offset

	@offset.setter
	def offset(self, v):
		self._offset = v
		self.updateRect()

	@property
	def size(self) -> Vector2:
		return self._rect.size

	@size.setter
	def size(self, v):
		self._rect.size = v

	@property
	def order(self) -> int:
		return self._order

	@order.setter
	def order(self, val):
		self._order = val

		from gameengine.managers.InputManager import InputManager
		InputManager().sortByOrder()