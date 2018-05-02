from game.Resources import Resources
from game.powerups.PowerUp import PowerUp
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides
from gameengine.util.Vector2 import Vector2


class SuperStar(PowerUp):
	def init(self, *args, **kwargs):
		super().init()
		self.tags.append("SuperStar")

		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["superStar"])
		self.getComponent(Collider).size = spriteRenderer.size

		physics = self.getComponent(Physics)
		physics.customGravity = Vector2(0, 0)
		physics.velocity.y = 20

		self.removeScript(self.getScript(PowerUp.PowerUpScript))
		self.addScript(self.SuperStarScript)


	class SuperStarScript(Script):
		def init(self, *args, **kwargs):
			self.ignoreFirstBlock = True

		def onCollisionExit(self, other):
			if not self.gameObject.popped and "Solid" in other.tags:
				physics = self.gameObject.getComponent(Physics)
				physics.customGravity = None
				physics.velocity.y = 0
				physics.velocity.x = 75

				self.gameObject.popped = True

		def onCollisionEnter(self, other, side):
			physics = self.gameObject.getComponent(Physics)

			if "Solid" in other.tags:
				if side == Sides.BOTTOM_SIDE:
					physics.velocity.y = 450

				elif side == Sides.TOP_SIDE:
					if not self.ignoreFirstBlock:
						physics.velocity.y = 0

					else:
						self.ignoreFirstBlock = False

				else:
					physics.velocity.x *= -1

			elif "PowerUp" in other.tags:
				if side == Sides.LEFT_SIDE or side == Sides.RIGHT_SIDE:
					physics.velocity.x *= -1

		def onCollisionStay(self, other):
			if "Player" in other.tags and self.gameObject.popped:
				World.destroy(self.gameObject)

