from abc import abstractmethod

from game.Resources import Resources
from game.scripts import DestroyOutOfWorld
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides


class Enemy(GameObject):
	def init(self, theme = "ow", *args, **kwargs):
		self.tags.append("Enemy")
		self.tags.append("MovingEnemy")
		self.addComponent(SpriteRenderer).order = 1
		self.theme = theme

		self.addComponent(Physics)
		self.addComponent(Collider)

		self.addScript(DestroyOutOfWorld)
		self.addScript(InverseXVelocity)

		self.getComponent(Physics).velocity.set(-30, 0)

	@abstractmethod
	def playerSmash(self):
		pass

	@abstractmethod
	def flip(self, flipSide):
		Resources.kick.play().volume = 0.05


class InverseXVelocity(Script):
	def init(self, ignoreEntities=False):
		self.ignoreEntities = ignoreEntities

	def onCollisionEnter(self, other, side):
		if not ("Solid" in other.tags or ("MovingEnemy" in other.tags and not self.ignoreEntities)):
			return

		physics = self.gameObject.getComponent(Physics)

		if "Solid" in other.tags:
			if (side == Sides.RIGHT_SIDE and physics.velocity.x > 0) or \
				(side == Sides.LEFT_SIDE and physics.velocity.x < 0):
				physics.velocity.x *= -1

			elif (side == Sides.TOP_SIDE and physics.velocity.y > 0) or \
				(side == Sides.BOTTOM_SIDE and physics.velocity.y < 0):
				physics.velocity.y = 0

		elif "Platform" in other.tags:
			if side == Sides.BOTTOM_SIDE and physics.velocity.y < 0:
				physics.velocity.y = 0