from abc import ABC, abstractmethod

from gameengine.core.Camera import Camera
from gameengine.interfaces.IOrderable import IOrderable


class IDrawable(IOrderable, ABC):
	@abstractmethod
	def draw(self):
		pass