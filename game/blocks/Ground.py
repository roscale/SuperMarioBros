from game.blocks.Block import Block
from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer


class Ground(Block):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		spriteRenderer = self.getComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["ground"])

		self.getComponent(Collider).size = spriteRenderer.size

	def smallHit(self):
		pass

	def bigHit(self):
		pass