from abc import ABC
from typing import TypeVar, List, Type

from queue import Queue

from gameengine.components.Collider import Collider
from gameengine.components.Component import Component
from gameengine.components.Transform import Transform
from gameengine.core.Script import Script

C = TypeVar("C")
S = TypeVar("S")

class GameObject(ABC):
	def __init__(self):
		self.keepBetweenScenes = False

		self.tags: List[str] = []

		self.components: List[Component] = []
		self.scripts: List[Script] = []

		self.transform = self.addComponent(Transform)

	def init(self, *args, **kwargs):
		pass

	def getComponent(self, Class: Type[C]) -> C:
		if isinstance(Class, type):
			for component in self.components:
				if isinstance(component, Class):
					return component
		return None

	def addComponent(self, Class: Type[C]) -> C:
		if isinstance(Class, type):
			existent = self.getComponent(Class)
			if existent:
				return existent

			component = Class()
			component.attachGameObject(self)
			component.init()

			self.components.append(component)

			return component

		return None

	def removeComponent(self, component):
		def f():
			if component.gameObject is None:
				return

			component.destroy()
			self.components.remove(component)

		from gameengine.core.World import World
		World.callableQueue.put(f)

	def getScript(self, Class: Type[S]) -> S:
		if isinstance(Class, type):
			for script in self.scripts:
				if isinstance(script, Class):
					return script
		return None

	def addScript(self, Class: Type[S], *args, **kwargs) -> S:
		if isinstance(Class, type):
			script = Class()
			script.attachGameObject(self)

			script.init(*args, **kwargs)

			def f():
				self._sortScripts()

			self.scripts.append(script)

			return script

	def removeScript(self, script):
		def f():
			script.onDestroy()
			self.scripts.remove(script)

		from gameengine.core.World import World
		World.callableQueue.put(f)

	def _sortScripts(self):
		from gameengine.core.Script import Script
		self.scripts.sort(key=Script._byOrder)

	def prepareDestroy(self):
		for script in self.scripts:
			self.removeScript(script)

		for component in self.components:
			self.removeComponent(component)
