from typing import Type

from game.Resources import Resources
from game.blocks.Block import Block, HitUpperEnemies
from game.particles.BrickPieces import BrickPieces
from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.World import World
from gameengine.util.Rect import Rect


class Brick(Block):
	def init(self, item: Type = None, *args, **kwargs):
		super().init(*args, **kwargs)
		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["brick"])

		self.getComponent(Collider).size = spriteRenderer.size
		self.getComponent(Input).size = spriteRenderer.size

		self.itemClass = item

		from game.blocks.QuestionBlock import RotatingCoin
		self.tenCoinBlock = self.itemClass == RotatingCoin

		self.triggered = False
		self.hits = 0

	def smallHit(self):
		super().smallHit()
		if self.itemClass is not None:
			self.trigger()

		if not self.triggered:
			self.getScript(HitUpperEnemies).hit()

		self.getCoinAbove()

	def bigHit(self):
		super().bigHit()
		if self.itemClass is None:
			World.destroy(self)

			velX = 50

			World.instantiate(BrickPieces, self.transform.position - (4, 4), Resources.theme[self.theme]["brickPieces"][0], (-velX, 250))
			World.instantiate(BrickPieces, self.transform.position + (8, 0) - (4, 4), Resources.theme[self.theme]["brickPieces"][1], (velX, 250))
			World.instantiate(BrickPieces, self.transform.position + (0, 8) - (4, 4), Resources.theme[self.theme]["brickPieces"][2], (-velX, 300))
			World.instantiate(BrickPieces, self.transform.position + (8, 8) - (4, 4), Resources.theme[self.theme]["brickPieces"][3], (velX, 300))

			Resources.breakblock.play().volume = 0.05

		else:
			self.trigger()

		if not self.triggered:
			self.getScript(HitUpperEnemies).hit()

		self.getCoinAbove()

	def trigger(self):
		if not self.triggered:
			World.instantiate(self.itemClass, self.transform.position)

			if self.tenCoinBlock:
				self.hits += 1
				if self.hits >= 10:
					self.triggered = True
					self.getComponent(SpriteRenderer).setImage(Resources.theme[self.theme]["questionBlockHit"])

			else:
				self.triggered = True
				self.getComponent(SpriteRenderer).setImage(Resources.theme[self.theme]["questionBlockHit"])

	def getCoinAbove(self):
		from gameengine.managers.CollisionManager import CollisionManager
		above: set = CollisionManager().quadtree.intersect(bbox=Rect(self.transform.position + (0, 20), 1, 1).bbox())
		if above:
			go = above.pop().gameObject
			if "Coin" in go.tags:
				from game.blocks.QuestionBlock import RotatingCoin
				World.instantiate(RotatingCoin, (go.transform.position))
				World.destroy(go)
