from game.Resources import Resources
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World


class Castle(GameObject):
	class FirstPart(GameObject):
		def init(self):
			spriteRenderer = self.addComponent(SpriteRenderer)
			spriteRenderer.setImage(Resources.castle1)
			spriteRenderer.order = 1

	class SecondPart(GameObject):
		def init(self):
			spriteRenderer = self.addComponent(SpriteRenderer)
			spriteRenderer.setImage(Resources.castle2)
			spriteRenderer.order = -1


	def init(self):
		World.instantiate(self.FirstPart, self.transform.position)
		World.instantiate(self.SecondPart, self.transform.position + (40, 0))