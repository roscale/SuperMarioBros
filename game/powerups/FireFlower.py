from game.Resources import Resources
from game.powerups.PowerUp import PowerUp
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Script import Script
from gameengine.util.Vector2 import Vector2


class FireFlower(PowerUp):
	def init(self, *args, **kwargs):
		super().init()
		self.tags.append("FireFlower")

		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["fireFlower"])
		self.getComponent(Collider).size = spriteRenderer.size

		physics = self.getComponent(Physics)
		physics.customGravity = Vector2(0, 0)
		physics.velocity.y = 20

		self.addScript(self.FireFlowerScript)


	class FireFlowerScript(Script):
		def onCollisionExit(self, other):
			if "Solid" in other.tags and not self.gameObject.popped:
				physics = self.gameObject.getComponent(Physics)
				physics.customGravity = None
				physics.velocity.y = 0

				self.gameObject.popped = True