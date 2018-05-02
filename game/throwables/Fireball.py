from game.Resources import Resources
from game.scripts import DestroyOutOfWorld
from game.particles.FireballExplosion import FireballExplosion
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides


class Fireball(GameObject):
	def init(self, toRight=True):
		self.tags.append("Fireball")

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.fireBall)
		collider = self.addComponent(Collider)
		collider.size = spriteRenderer.size
		collider.offset = (4, 4)

		self.addComponent(Physics).addAcceleration((250 if toRight else -250, 0))

		self.addScript(DestroyOutOfWorld)
		self.addScript(self.FireballScript)

		Resources.fireball.play().volume = 0.05

	class FireballScript(Script):
		def onCollisionEnter(self, other, side):
			if "Solid" in other.tags:
				if side == Sides.BOTTOM_SIDE:
					self.gameObject.getComponent(Physics).velocity.y = 200

				else:
					World.destroy(self.gameObject)

					Resources.bump.play().volume = 0.05

			elif "Platform" in other.tags:
				if side == Sides.BOTTOM_SIDE:
					self.gameObject.getComponent(Physics).velocity.y = 200

			elif "Enemy" in other.tags:
				if "PiranhaPlant" in other.tags:
					if other.aggressive:
						World.destroy(self.gameObject)

				else:
					World.destroy(self.gameObject)

		def onDestroy(self):
			World.instantiate(FireballExplosion, self.gameObject.transform.position)


