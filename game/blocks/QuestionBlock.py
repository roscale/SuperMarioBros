from typing import Type

from game.Resources import Resources
from game.blocks.Block import Block, HitUpperEnemies
from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World


class QuestionBlock(Block):
	def init(self, item: Type = None, *args, **kwargs):
		super().init(*args, **kwargs)
		self.itemClass = item
		if self.itemClass is None:
			self.itemClass = RotatingCoin

		self.hit = False

		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["questionBlock"])

		self.getComponent(Collider).size = spriteRenderer.size
		self.getComponent(Input).size = spriteRenderer.size

	def trigger(self):
		if not self.hit:
			self.hit = True
			self.getComponent(SpriteRenderer).setImage(Resources.theme[self.theme]["questionBlockHit"])

			World.instantiate(self.itemClass, self.transform.position)
			# World.instantiate(RotatingCoin, (), self.transform.position)

			self.getScript(HitUpperEnemies).hit()

	def smallHit(self):
		super().smallHit()
		self.trigger()

	def bigHit(self):
		super().bigHit()
		self.trigger()



class RotatingCoin(GameObject):
	def init(self):
		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.rotatingCoin)
		spriteRenderer.order = 3

		self.addComponent(Physics).addForce((0, 350))

		World.destroy(self, 500)

		World.findByTag("Coins")[0].increment()

		Resources.coin.play().volume = 0.05