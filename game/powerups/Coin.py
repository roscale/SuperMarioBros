from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World


class Coin(GameObject):
	def init(self, theme, *args, **kwargs):
		self.tags.append("Coin")

		self.theme = theme

		spriteRenderer = self.addComponent(SpriteRenderer)
		spriteRenderer.setImage(Resources.theme[self.theme]["coin"])

		self.addComponent(Collider).size = spriteRenderer.size
		self.addScript(self.CoinScript)

	class CoinScript(Script):
		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				World.destroy(self.gameObject)
				World.findByTag("Coins")[0].increment()

				Resources.coin.play().volume = 0.05