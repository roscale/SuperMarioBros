from abc import ABC

from game.Resources import Resources
from game.scripts import DestroyOutOfWorld
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides


class PowerUp(GameObject, ABC):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("PowerUp")

		self.addComponent(SpriteRenderer).order = 3
		self.theme = "ow"

		self.addComponent(Collider)
		self.addComponent(Physics)

		self.addScript(DestroyOutOfWorld)
		self.addScript(self.PowerUpScript)

		self.popped = False

		Resources.powerupAppears.play().volume = 0.05


	class PowerUpScript(Script):
		def onCollisionEnter(self, other, side):
			physics = self.gameObject.getComponent(Physics)

			if "Solid" in other.tags:
				if side == Sides.BOTTOM_SIDE:
					physics.velocity.y = 0

				else:
					physics.velocity.x *= -1

			elif "Platform" in other.tags:
				if side == Sides.BOTTOM_SIDE:
					physics.velocity.y = 0

			elif "PowerUp" in other.tags:
				if side == Sides.LEFT_SIDE or side == Sides.RIGHT_SIDE:
					physics.velocity.x *= -1


		def onCollisionStay(self, other):
			if "Player" in other.tags and self.gameObject.popped:
				World.destroy(self.gameObject)

				Resources.powerup.play().volume = 0.05
