from game.scripts import DestroyOutOfWorld
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World


class BrickPieces(GameObject):
	def init(self, sprite, velocity):
		self.addComponent(SpriteRenderer).setImage(sprite)
		self.addComponent(Physics).velocity.set(velocity)

		self.addScript(DestroyOutOfWorld)
