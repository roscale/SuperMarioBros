from typing import List

from pyglet.gl import *

from gameengine.core.GameObject import GameObject
from gameengine.core.World import World
from gameengine.interfaces.IManageable import IManageable
from gameengine.managers.Manager import Manager
from gameengine.util.Vector2 import Vector2


class Camera(GameObject, IManageable):
	def __init__(self):
		super().__init__()
		self._managers: List[Manager] = []

		self._windowPosition = Vector2()
		self._size = Vector2(World.window.width, World.window.height)
		self.zoom = 1.0
		self.backgroundColor = (0, 0, 0, 0)
		self._order = 0

		from gameengine.managers.CameraManager import CameraManager
		CameraManager().add(self)

	@property
	def managers(self) -> List[Manager]:
		return self._managers

	@property
	def windowPosition(self) -> Vector2:
		return self._windowPosition

	@windowPosition.setter
	def windowPosition(self, v):
		self._windowPosition.set(*v)

	@property
	def size(self) -> Vector2:
		return self._size

	@size.setter
	def size(self, v):
		self._size.set(*v)

	@property
	def order(self) -> int:
		return self._order

	@order.setter
	def order(self, val):
		self._order = val

		from gameengine.managers.CameraManager import CameraManager
		CameraManager().sortByOrder()

	def worldProjection(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glViewport(int(self._windowPosition.x), int(self._windowPosition.y), int(self._size.x), int(self._size.y))

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		inverseZoom = 1/self.zoom

		# gluOrtho2D(-halfWidth * inverseZoom, halfWidth * inverseZoom, -halfHeight * inverseZoom, halfHeight * inverseZoom)
		gluOrtho2D(0, self._size.x * inverseZoom, 0, self._size.y * inverseZoom)
		glTranslatef(-self.transform.position.x, -self.transform.position.y, 0)

	def hudProjection(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, self._size.x, 0, self._size.y)

	def windowToWorldCoords(self, vec: Vector2) -> Vector2:
		relToCamera = vec - self.windowPosition
		return self.transform.position + relToCamera / self.zoom

	def worldToWindowCoords(self, vec: Vector2) -> Vector2:
		relToCamera: Vector2 = (vec - self.transform.position) * self.zoom
		return relToCamera + self.windowPosition

	def prepareDestroy(self):
		from gameengine.managers.CameraManager import CameraManager
		CameraManager().remove(self)