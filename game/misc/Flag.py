from typing import Callable

from game.Resources import Resources
from game.levels.LevelSplash import LevelSplash
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides
from gameengine.managers.SceneManager import SceneManager
from gameengine.util.Vector2 import Vector2


class Flag(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("Flag")

		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.theme[theme]["flag"])
		sr.order = 1

		self.addComponent(Physics).customGravity = Vector2()
		self.addComponent(Collider).size = sr.size

		self.nextScene = None
		self.nextSceneArgs = args
		self.nextSceneKwargs = kwargs

		self.prepareNextLevel: Callable = None

	def setNextScene(self, nextScene, *args, **kwargs):
		self.nextScene = nextScene
		self.nextSceneArgs = args
		self.nextSceneKwargs = kwargs

	def pull(self):
		if self.getScript(self.FlagScript) is None:
			self.addScript(self.FlagScript)

	class FlagScript(Script):
		def init(self, *args):
			self.gameObject.getComponent(Physics).velocity.y = -120

			Resources.bgMusic.pause()
			Resources.flagpole.play().volume = 0.05
			World.findByTag("Time")[0].stop()

			World.findByTag("Score")[0].add(5000)

			def goToNextLevel():
				if self.gameObject.prepareNextLevel:
					self.gameObject.prepareNextLevel()
				if self.gameObject.nextScene:
					SceneManager().loadScene(self.gameObject.nextScene, *self.gameObject.nextSceneArgs, *self.gameObject.nextSceneKwargs)

			Timer.add(goToNextLevel, (), 2000, 0, 1)

		def onCollisionEnter(self, other, side):
			if "Solid" in other.tags and side == Sides.BOTTOM_SIDE:
				self.gameObject.getComponent(Physics).velocity.y = 0


class FlagPoleHead(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.theme[theme]["flagPoleHead"])
		sr.order = 2

		collider = self.addComponent(Collider)
		collider.size = (8, 8)
		collider.offset = (4, 0)

		self.addScript(self.FlagPoleHeadScript)

	class FlagPoleHeadScript(Script):
		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				World.findByTag("Flag")[0].pull()


class FlagPoleBody(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.theme[theme]["flagPoleBody"])
		sr.order = 2

		collider = self.addComponent(Collider)
		collider.size = (2, 16)
		collider.offset = (7, 0)

		self.addScript(self.FlagPoleBodyScript)

	class FlagPoleBodyScript(Script):
		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				World.findByTag("Flag")[0].pull()

