from abc import ABC, abstractmethod

from gameengine.util.Rect import Rect
from gameengine.util.Vector2 import Vector2


class IResizable(ABC):
	@property
	@abstractmethod
	def rect(self) -> Rect:
		pass

	@abstractmethod
	def updateRect(self):
		pass

	@property
	@abstractmethod
	def offset(self) -> Vector2:
		pass

	@offset.setter
	@abstractmethod
	def offset(self, v):
		pass

	@property
	@abstractmethod
	def size(self) -> Vector2:
		pass

	@size.setter
	@abstractmethod
	def size(self, v):
		pass