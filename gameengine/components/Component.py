from abc import ABC

from typing import List

from gameengine.interfaces.IManageable import IManageable
from gameengine.managers.Manager import Manager


class Component(IManageable, ABC):
	def __init__(self):
		self.gameObject = None
		self._managers: List[Manager] = []

	def attachGameObject(self, gameObject):
		self.gameObject = gameObject

	def init(self, *args):
		pass

	@property
	def managers(self) -> List[Manager]:
		return self._managers

	def destroy(self):
		for manager in self._managers:
			manager.remove(self)

		self._managers = None
		self.gameObject = None