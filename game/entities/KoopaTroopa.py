from typing import Callable

from game.entities.Enemy import Enemy, InverseXVelocity
from game.Resources import Resources
from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.interfaces.IEvents import IEvents
from gameengine.managers.CollisionManager import Sides
from gameengine.util.Vector2 import Vector2


class KoopaTroopa(Enemy):
	def init(self, smart=False, *args, **kwargs):
		super().init(*args, **kwargs)
		self.tags.append("KoopaTroopa")

		if smart:
			self.color = "red"
			self.addScript(AlwaysOnPlatform)
		else:
			self.color = "green"

		collider = self.getComponent(Collider)
		collider.size = (16, 16)

		self.addScript(KoopaTroopaScript)



	def playerSmash(self):
		pass

	def flip(self, flipSide):
		super().flip(flipSide)

		self.removeComponent(self.getComponent(Collider))

		alwaysOnPlatform = self.getScript(AlwaysOnPlatform)
		if alwaysOnPlatform is not None:
			self.removeScript(alwaysOnPlatform)

		if flipSide == Sides.LEFT_SIDE:
			self.getComponent(Physics).velocity.set(-50, 250)
		else:
			self.getComponent(Physics).velocity.set(50, 250)

		spriteRenderer = self.getComponent(SpriteRenderer)
		# spriteRenderer.setImage(Resources.goombaFlipped)
		spriteRenderer.sprite.scale_y = -1

		World.destroy(self, 1000)


class KoopaTroopaScript(Script):
	def init(self):
		self.state = self.Walk(self)

	def onUpdate(self):
		self.state.onUpdate()

	def onCollisionEnter(self, other, side):
		self.state.onCollisionEnter(other, side)

		if ("KoopaTroopa" in other.tags and "Bowling" in other.tags) or \
		     ("Fireball" in other.tags) or \
		     ("Player" in other.tags and "Invincible" in other.tags):

			flipSide = Sides.LEFT_SIDE if other.getComponent(Physics).velocity.x < 0 else Sides.RIGHT_SIDE
			self.gameObject.flip(flipSide)

	def onDestroy(self):
		if isinstance(self.state, self.Stomped) or isinstance(self.state, self.Recovering):
			self.state.onDestroy()


	class Walk(IEvents):
		def __init__(self, script):
			self.script = script
			self.koopaTroopa = script.gameObject

			self.koopaTroopa.getComponent(SpriteRenderer).setImage(Resources.theme[self.koopaTroopa.theme][self.koopaTroopa.color]["koopaTroopaWalking"])
			self.koopaTroopa.getComponent(Collider).offset = (0, -4)

			self.koopaTroopa.getScript(InverseXVelocity).ignoreEntities = False

		def onUpdate(self):
			physics = self.koopaTroopa.getComponent(Physics)
			self.koopaTroopa.getComponent(SpriteRenderer).sprite.scale_x = 1 if physics.velocity.x < 0 else -1

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags and side == Sides.TOP_SIDE:
				self.koopaTroopa.transform.position -= (0, 4)
				self.script.state = KoopaTroopaScript.Stomped(self.script)


	class Stomped(IEvents):
		def __init__(self, script):
			self.script = script
			self.koopaTroopa = script.gameObject

			self.koopaTroopa.getComponent(Physics).velocity.x = 0

			self.koopaTroopa.getComponent(SpriteRenderer).setImage(Resources.theme[self.koopaTroopa.theme][self.koopaTroopa.color]["koopaTroopaStomped"])
			self.koopaTroopa.getComponent(Collider).offset = (0, 0)

			Resources.stomp.play().volume = 0.05

			def recover():
				self.script.state = KoopaTroopaScript.Recovering(self.script)

			self.recoverTimer = Timer.add(recover, (), 2500, 0, 1)

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				Timer.remove(self.recoverTimer)
				self.script.state = KoopaTroopaScript.Bowling(self.script, other)

		def onDestroy(self):
			Timer.remove(self.recoverTimer)


	class Recovering(IEvents):
		def __init__(self, script):
			self.script = script
			self.koopaTroopa = script.gameObject

			self.koopaTroopa.getComponent(SpriteRenderer).setImage(Resources.theme[self.koopaTroopa.theme][self.koopaTroopa.color]["koopaTroopaRecovering"])

			def walk():
				self.koopaTroopa.transform.position += (0, 4)
				self.script.state = KoopaTroopaScript.Walk(self.script)

				players = World.findByTag("Player")
				if not players:
					return
				player = players[0]

				self.koopaTroopa.getComponent(Physics).velocity.x = \
					-30 if player.transform.position.x < self.koopaTroopa.transform.position.x else 30


			self.walkTimer = Timer.add(walk, (), 2000, 0, 1)

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags:
				Timer.remove(self.walkTimer)

				if side == Sides.TOP_SIDE:
					self.script.state = KoopaTroopaScript.Stomped(self.script)
				else:
					self.script.state = KoopaTroopaScript.Bowling(self.script, other)

		def onDestroy(self):
			Timer.remove(self.walkTimer)


	class Bowling(IEvents):
		def __init__(self, script, player):
			self.script = script
			self.koopaTroopa = script.gameObject
			self.koopaTroopa.tags.append("Bowling")

			self.koopaTroopa.getComponent(SpriteRenderer).setImage(Resources.theme[self.koopaTroopa.theme][self.koopaTroopa.color]["koopaTroopaStomped"])

			playerMiddle = player.getComponent(Collider).rect.centerX
			koopaTroopaMiddle = self.koopaTroopa.getComponent(Collider).rect.centerX

			physics = self.koopaTroopa.getComponent(Physics)
			force = 250
			physics.velocity.x = force if playerMiddle < koopaTroopaMiddle else -force

			self.koopaTroopa.getScript(InverseXVelocity).ignoreEntities = True

			Resources.kick.play().volume = 0.05

		def onCollisionEnter(self, other, side):
			if "Player" in other.tags and side == Sides.TOP_SIDE:
				self.koopaTroopa.tags.remove("Bowling")
				self.script.state = KoopaTroopaScript.Stomped(self.script)

			elif "Block" in other.tags and (side == Sides.LEFT_SIDE or side == Sides.RIGHT_SIDE):
				other.bigHit()


class AlwaysOnPlatform(Script):

	class Trigger(GameObject):
		def init(self, follow: GameObject, offset, exitCallback: Callable[[], None], *args, **kwargs):
			self.follow = follow
			self.offset = offset
			self.callback = exitCallback

			self.addComponent(Collider).size = (5, 5)
			self.addComponent(Physics).customGravity = Vector2(0, 0)

			self.transform.position = self.follow.transform.position + offset

			# from pyglet import image
			# square = image.load("res/sprites/" + "square5x5.png")
			# sr = self.addComponent(SpriteRenderer)
			# sr.setImage(square)
			# sr.order = 50


			self.addScript(self.TriggerScript)

		class TriggerScript(Script):
			def onUpdate(self):
				self.gameObject.getComponent(Physics).velocity.set(self.gameObject.follow.getComponent(Physics).velocity)

			def onCollisionExit(self, other):
				if "Solid" in other.tags and not self.gameObject.getComponent(Collider).isColliding: # TODO verify isColliding
					self.gameObject.callback()


	def init(self, *args):
		self.triggers = []

		def invertVelocity():
			if not isinstance(self.gameObject.getScript(KoopaTroopaScript).state, KoopaTroopaScript.Bowling):
				self.gameObject.getComponent(Physics).velocity *= -1

		self.triggers.append(World.instantiate(self.Trigger, self.gameObject.transform.position, follow=self.gameObject, offset=(0, -10), exitCallback=invertVelocity))
		self.triggers.append(World.instantiate(self.Trigger, self.gameObject.transform.position, follow=self.gameObject, offset=(10, -10), exitCallback=invertVelocity))



	def onDestroy(self):
		for trigger in self.triggers:
			World.destroy(trigger)







