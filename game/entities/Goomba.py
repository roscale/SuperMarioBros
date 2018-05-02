from game.entities.Enemy import Enemy
from game.Resources import Resources
from game.particles.Points import Points
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides


class Goomba(Enemy):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["goombaWalking"])

		self.getComponent(Collider).size = spriteRenderer.size

		self.addScript(GoombaScript)

	def playerSmash(self):
		self.getComponent(SpriteRenderer).setImage(Resources.theme[self.theme]["goombaSmashed"])
		self.removeComponent(self.getComponent(Collider))
		self.removeComponent(self.getComponent(Physics))
		World.destroy(self, 1000)

		Resources.stomp.play().volume = 0.05

		# World.instantiate(Points, self.transform.position + (0, 5), number=1000)

	def flip(self, flipSide):
		super().flip(flipSide)

		self.removeComponent(self.getComponent(Collider))

		if flipSide == Sides.LEFT_SIDE:
			self.getComponent(Physics).velocity.set(-70, 250)
		else:
			self.getComponent(Physics).velocity.set(70, 250)

		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["goombaFlipped"])
		spriteRenderer.sprite.scale_y = -1

		World.destroy(self, 1000)


class GoombaScript(Script):
	def onCollisionEnter(self, other, side):
		if (("Player" in other.tags) and "Invincible" not in other.tags) and side == Sides.TOP_SIDE:
			self.gameObject.playerSmash()

		elif ("KoopaTroopa" in other.tags and "Bowling" in other.tags) or \
				("Fireball" in other.tags) or \
				("Player" in other.tags and "Invincible" in other.tags):

			flipSide = Sides.LEFT_SIDE if other.getComponent(Physics).velocity.x < 0 else Sides.RIGHT_SIDE
			self.gameObject.flip(flipSide)