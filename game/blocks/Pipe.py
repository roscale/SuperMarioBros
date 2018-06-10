from typing import Callable

from game.Resources import Resources
from game.entities.PiranhaPlant import PiranhaPlant
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides
from gameengine.util.Vector2 import Vector2


class PipeHead(GameObject):
	def init(self, teleport: Callable = lambda player: None, *args, **kwargs):
		self.teleport = teleport


class VPipeHead(PipeHead):
	def init(self, theme="ow", hasPiranhaPlant="False", *args, **kwargs):
		PipeHead.init(self, *args, **kwargs)

		self.tags.extend(["Solid", "PipeHead"])
		self.theme = theme
		self.hasPiranhaPlant = hasPiranhaPlant

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["vPipeHead"])
		spriteRenderer.order = 1
		spriteRenderer.offset = (8, 0)

		collider = self.addComponent(Collider)
		collider.size = spriteRenderer.size
		collider.size.x = 30
		collider.offset = Vector2(1, 0)

		self.piranhaPlant = None
		if self.hasPiranhaPlant == "True":
			self.piranhaPlant = World.instantiate(PiranhaPlant, self.transform.position - (0, 4), theme=self.theme)
			self.addScript(self.VPipeHeadScript)

		if "enter" in kwargs:
			self.tags.append("Enter")

	def playerCrouches(self, player):
		self.teleport(player)

	class VPipeHeadScript(Script):
		def onUpdate(self):
			script = self.gameObject.piranhaPlant.getScript(PiranhaPlant.PiranhaPlantScript)
			if script:
				script.active = True

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				script = self.gameObject.piranhaPlant.getScript(PiranhaPlant.PiranhaPlantScript)
				if script is not None:
					script.active = False


class VPipeBody(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("Solid")
		self.theme = theme

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["vPipeBody"])
		spriteRenderer.order = 1
		spriteRenderer.offset = (8, 0)

		collider = self.addComponent(Collider)
		collider.size = spriteRenderer.size
		collider.size.x = 30
		collider.offset = Vector2(1, 0)


class HPipeHead(PipeHead):
	def init(self, theme="ow", *args, **kwargs):
		PipeHead.init(self, *args, **kwargs)

		self.transform.position -= (0, 16)

		self.tags.extend(["Solid", "PipeHead"])
		self.theme = theme

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["hPipeHead"])
		spriteRenderer.order = 1
		spriteRenderer.offset = (0, 8)

		collider = self.addComponent(Collider)
		collider.size = spriteRenderer.size
		collider.size.y = 30
		collider.offset = (0, 1)

		if "exit" in kwargs:
			self.tags.append("Exit")

		self.addScript(self.HPipeHeadScript)

	class HPipeHeadScript(Script):
		def init(self, *args, **kwargs):
			self.player = None

		def onUpdate(self):
			self.player = None

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags and side == Sides.LEFT_SIDE:
				self.player = other

		def onLateUpdate(self):
			if not self.player:
				return

			from game.Player import Checks
			if self.player.getScript(Checks).onGround:
				self.gameObject.teleport(self.player)



class HPipeBody(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("Solid")
		self.theme = theme

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["hPipeBody"])
		spriteRenderer.order = 1
		spriteRenderer.offset = (0, 8)

		collider = self.addComponent(Collider)
		collider.size = spriteRenderer.size
		collider.size.y = 30
		collider.offset = (0, 1)


class HPipeConnection(GameObject):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("Solid")
		self.theme = theme

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["hPipeConnection"])
		spriteRenderer.order = 0.5
		spriteRenderer.offset = (0, 8)

		# collider = self.addComponent(Collider)
		# collider.size = spriteRenderer.size