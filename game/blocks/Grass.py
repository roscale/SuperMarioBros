from game.Resources import Resources
from game.blocks.Block import Block
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject


class Pillar(GameObject):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		sr = self.addComponent(SpriteRenderer)
		sr.order = 2
		sr.setImage(Resources.theme["ow"]["pillar"])


class GrassLeft(Block):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		sr = self.getComponent(SpriteRenderer)
		sr.setImage(Resources.theme[self.theme]["grassLeft"])

		self.getComponent(Collider).size = sr.size

	def smallHit(self):
		pass

	def bigHit(self):
		pass


class GrassMiddle(Block):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		sr = self.getComponent(SpriteRenderer)
		sr.setImage(Resources.theme[self.theme]["grassMiddle"])

		self.getComponent(Collider).size = sr.size

	def smallHit(self):
		pass

	def bigHit(self):
		pass


class GrassRight(Block):
	def init(self, *args, **kwargs):
		super().init(*args, **kwargs)
		sr = self.getComponent(SpriteRenderer)
		sr.setImage(Resources.theme[self.theme]["grassRight"])

		self.getComponent(Collider).size = sr.size

	def smallHit(self):
		pass

	def bigHit(self):
		pass