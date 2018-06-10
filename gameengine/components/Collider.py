from gameengine.components.Component import Component
from gameengine.interfaces.IResizable import IResizable
# from gameengine.managers.CollisionManager import CollisionManager
from gameengine.util.Rect import Rect
from gameengine.util.Vector2 import Vector2


class Collider(Component, IResizable):
	def __init__(self):
		super().__init__()

		self._rect = Rect()
		self._offset = Vector2()

	def transformPosChanged(self, sender, oldPos, newPos):
		self.updateRect()

	def attachGameObject(self, gameObject):
		super().attachGameObject(gameObject)

		gameObject.transform.position.hasChanged += self.transformPosChanged

	def init(self):
		self.updateRect()

		self._rect.topLeft.hasChanged += self.updateQuadTreeOnPosition
		self._rect.size.hasChanged += self.updateQuadTreeOnSize

		from gameengine.managers.CollisionManager import CollisionManager
		CollisionManager().add(self)

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
		self._offset.set(v)
		self.updateRect()

	@property
	def size(self) -> Vector2:
		return self._rect.size

	@size.setter
	def size(self, v):
		self._rect.size = v

	def updateQuadTreeOnPosition(self, sender, old, new):
		from gameengine.managers.CollisionManager import CollisionManager

		CollisionManager().quadtree.remove(self, (*old, *(old + self._rect.size)))
		CollisionManager().quadtree.insert(self, (*new, *(new + self._rect.size)))

	def updateQuadTreeOnSize(self, sender, old, new):
		from gameengine.managers.CollisionManager import CollisionManager
		CollisionManager().quadtree.remove(self, (*self._rect.topLeft, *(self._rect.topLeft + old)))
		CollisionManager().quadtree.insert(self, (*self._rect.topLeft, *(self._rect.topLeft + new)))

	def destroy(self):
		self.gameObject.transform.position.hasChanged -= self.transformPosChanged
		super().destroy()