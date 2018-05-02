from game.Resources import Resources, tileSizeNum
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.util.Vector2 import Vector2


class Platform(GameObject):
	def init(self, script, *args, **kwargs):
		self.tags.extend(["Platform"])

		sr = self.addComponent(SpriteRenderer)
		sr.setImage(Resources.platform)
		sr.order = 1

		from gameengine.components.Physics import Physics
		physics = self.addComponent(Physics)
		physics.customGravity = Vector2()
		physics.mass = 999

		col = self.addComponent(Collider)
		col.size = sr.size
		col.offset = Vector2(8, 8)

		self.addScript(script, *args, **kwargs)

	class UpOrDown(Script):
		def init(self, velocity):
			self.gameObject.getComponent(Physics).velocity.set(velocity)

		def onCollisionEnter(self, other, side):
			from gameengine.managers.CollisionManager import Sides
			if side == Sides.TOP_SIDE and "Player" in other.tags:
				from gameengine.components.Physics import Physics
				other.getComponent(Physics).velocity.y = self.gameObject.getComponent(Physics).velocity.y

		def onUpdate(self):
			if self.gameObject.transform.position.y < -8:
				self.gameObject.transform.position.y = tileSizeNum * 15

			elif self.gameObject.transform.position.y > tileSizeNum * 15:
				self.gameObject.transform.position.y = -8

	class SmoothUpDown(Script):
		def init(self, yLimit):
			self.goingUp = True
			self.middle = yLimit / 2.0

		def onCollisionEnter(self, other, side):
			from gameengine.managers.CollisionManager import Sides
			if side == Sides.TOP_SIDE and "Player" in other.tags:
				from gameengine.components.Physics import Physics
				other.getComponent(Physics).velocity.y = self.gameObject.getComponent(Physics).velocity.y

		def onUpdate(self):
			self.goingUp = True if self.gameObject.transform.position.y < self.middle else False

			physics = self.gameObject.getComponent(Physics)
			physics.acceleration += (0, 1) if self.goingUp else (0, -1)

	class SmoothLeftRight(Script):
		def init(self, xLimit):
			self.goingRight = True
			xStart = self.gameObject.transform.position.x
			self.middle = (xLimit - xStart) / 2.0 + xStart

			print(self.middle, flush=True)

		def onCollisionEnter(self, other, side):
			from gameengine.managers.CollisionManager import Sides
			if side == Sides.TOP_SIDE and "Player" in other.tags:
				pass
				# from gameengine.components.Physics import Physics
				# other.getComponent(Physics).acceleration += (2, 0) if self.goingRight else (-2, 0)
				# FIXME Move Player with the platform

		def onUpdate(self):
			self.goingRight = True if self.gameObject.transform.position.x < self.middle else False

			physics = self.gameObject.getComponent(Physics)
			physics.acceleration += (1, 0) if self.goingRight else (-1, 0)

		def onLateUpdate(self):
			pass