from abc import ABC

from typing import Generic, TypeVar, List

T = TypeVar("T")
class Manager(ABC, Generic[T]):
	def __init__(self):
		self.collection: List[T] = []

	def add(self, object: T):
		self.collection.append(object)
		object.managers.append(self)

		self.collectionChanged()

	def remove(self, object: T):
		if object in self.collection:
			self.collection.remove(object)
			object.managers.remove(self)

			self.collectionChanged()

	def collectionChanged(self):
		pass

	def onUpdate(self, dt: float):
		pass