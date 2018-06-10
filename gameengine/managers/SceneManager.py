from typing import Type

from queue import Queue

from gameengine.core.Camera import Camera
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.util.Singleton import Singleton


@Singleton
class SceneManager:
	def __init__(self):
		self.currentScene = None

	def loadScene(self, Class: Type[Scene], *args, **kwargs):
		for gameObject in World.gameObjects:
			if not gameObject.keepBetweenScenes:
				World.destroy(gameObject)

		scene = Class()
		scene.mainCamera = World.instantiate(Camera, (0, 0))
		scene.mainCamera.tags.append("MainCamera")
		scene.onLoad(*args, **kwargs)
		self.currentScene = scene
