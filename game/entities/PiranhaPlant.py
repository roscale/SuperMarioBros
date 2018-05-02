from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.Timer import Timer
from gameengine.util.Vector2 import Vector2


class PiranhaPlant(GameObject):
	def __init__(self):
		super().__init__()
		self.aggressive = False

	def init(self, theme="ow", *args, **kwargs):
		self.tags.append("Enemy")
		self.tags.append("PiranhaPlant")
		self.theme = theme

		self.addComponent(Physics).customGravity = Vector2()

		sr = self.addComponent(SpriteRenderer)
		sr.order = 2
		sr.setImage(Resources.theme[self.theme]["piranhaPlant"])
		sr.offset = (8, 0)

		collider = self.addComponent(Collider)
		collider.size = sr.size
		collider.offset = (8, 0)


		self.addScript(self.PiranhaPlantScript)




	class PiranhaPlantScript(Script):
		def init(self, *args):
			self._active = False
			self.showUpTimer = None
			self.hideTimer = None

			self.active = True

			self.startPositionY = self.gameObject.transform.position.y
			self.movingUp = True

		@property
		def active(self) -> bool:
			return self._active

		@active.setter
		def active(self, val):
			if val is True and self._active is False:
				Timer.remove(self.showUpTimer)

				def goUp():
					self.movingUp = True

				self.showUpTimer = Timer.add(goUp, (), 2000, 4000, -1)

				Timer.remove(self.hideTimer)

				def goDown():
					self.movingUp = False

				self.hideTimer = Timer.add(goDown, (), 0, 4000, -1)

			if val is False and self._active is True:
				Timer.remove(self.showUpTimer)
				Timer.remove(self.hideTimer)

			self._active = val

		def onUpdate(self):
			self.gameObject.aggressive = True

			if self.movingUp:
				if self.active:
					self.gameObject.getComponent(Physics).velocity = Vector2(0, 50)
				else:
					self.gameObject.aggressive = False

				if self.gameObject.transform.position.y >= self.startPositionY + 24:
					self.gameObject.getComponent(Physics).velocity = Vector2(0, 0)


			elif not self.movingUp:
				self.gameObject.getComponent(Physics).velocity = Vector2(0, -50)

				if self.gameObject.transform.position.y <= self.startPositionY:
					self.gameObject.getComponent(Physics).velocity = Vector2(0, 0)
					self.gameObject.aggressive = False

					if not self.active:
						Timer.remove(self.hideTimer)

		def onCollisionEnter(self, other, side):
			if self.gameObject.aggressive:
				if ("KoopaTroopa" in other.tags and "Bowling" in other.tags) or \
						("Fireball" in other.tags) or \
						("Player" in other.tags and "Invincible" in other.tags):
					from gameengine.core.World import World
					World.destroy(self.gameObject)

					Resources.kick.play().volume = 0.05

		def onDestroy(self):
			Timer.remove(self.showUpTimer)
			Timer.remove(self.hideTimer)
