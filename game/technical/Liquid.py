from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject


class Wave(GameObject):
	def init(self, theme, *args, **kwargs):
		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.theme[theme]["wave"])
		self.addComponent(Collider).size = sr.size

class Liquid(GameObject):
	def init(self, theme, *args, **kwargs):
		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.theme[theme]["liquid"])
		self.addComponent(Collider).size = sr.size