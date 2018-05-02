from game.Resources import Resources
from game.scripts import DestroyOutOfWorld
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World


class FireballExplosion(GameObject):
	def init(self):
		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.fireBallExplosion)

		def f():
			World.destroy(self)

		spriteRenderer.sprite.on_animation_end = f