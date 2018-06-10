from abc import ABC, abstractmethod

from gameengine.core.Camera import Camera


class Scene(ABC):
	def __init__(self):
		self.mainCamera: Camera = None

	@abstractmethod
	def onLoad(self, *args, **kwargs):
		pass