from abc import ABC, abstractmethod

from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.managers.CollisionManager import Sides


class IBlock(ABC):
	@abstractmethod
	def smallHit(self):
		Resources.bump.play().volume = 0.05

	@abstractmethod
	def bigHit(self):
		Resources.bump.play().volume = 0.05

class Block(GameObject, IBlock, ABC):
	def init(self, theme="ow", *args, **kwargs):
		self.tags.extend(["Block", "Solid"])

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.order = 2
		self.theme = theme

		self.addComponent(Collider)
		self.addScript(HitUpperEnemies)


class HitUpperEnemies(Script):
	def init(self):
		self.upperEnemies = []

	def onUpdate(self):
		self.upperEnemies.clear()

	def onCollisionEnter(self, other, side):
		if "MovingEnemy" in other.tags and side == Sides.TOP_SIDE:
			self.upperEnemies.append(other)

	def hit(self):
		for enemy in self.upperEnemies:
			flipSide = Sides.LEFT_SIDE if enemy.getComponent(Physics).velocity.x < 0 else Sides.RIGHT_SIDE
			enemy.flip(flipSide)