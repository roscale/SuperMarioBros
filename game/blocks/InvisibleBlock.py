from typing import Type

from game.Resources import Resources
from game.blocks.Block import Block, HitUpperEnemies
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.World import World


class InvisibleBlock(Block):
	def init(self, item: Type = None, *args, **kwargs):
		super().init(*args, **kwargs)
		self.tags.append("Invisible")

		self.getComponent(Collider).size = (16, 16)

		self.itemClass = item
		self.triggered = False

	def trigger(self):
		if not self.triggered:
			self.tags.remove("Invisible")
			self.getComponent(SpriteRenderer).setImage(Resources.theme[self.theme]["questionBlockHit"])
			self.triggered = True

			World.instantiate(self.itemClass, self.transform.position)

			self.getScript(HitUpperEnemies).hit()

	def smallHit(self):
		super().smallHit()
		self.trigger()

	def bigHit(self):
		super().bigHit()
		self.trigger()
