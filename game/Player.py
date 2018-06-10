import pyglet
from pyglet.window import key

from game.Resources import Resources, tileSizeNum
from game.entities.KoopaTroopa import KoopaTroopaScript
from game.throwables.Fireball import Fireball
from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.interfaces.IEvents import IEvents
from gameengine.managers.CollisionManager import Sides
from gameengine.managers.SceneManager import SceneManager
from gameengine.util.EventBus import EventBus
from gameengine.util.Vector2 import Vector2
from gameengine.util.util import clamp


class Player(GameObject):
	lives = 3

	def init(self):
		self.tags.append("Player")
		self.character = "mario"

		self.addComponent(SpriteRenderer).order = 0
		self.addComponent(Collider)
		self.addComponent(Physics)
		self.addComponent(Input)

		self.addScript(Checks)

		self.state = Small(self)
		self.addScript(MainScript)

		self.addScript(MovementScript)
		self.addScript(CancelVelocity)
		self.addScript(ApplyDrag)
		self.addScript(MetEnemy)
		self.addScript(HandlePowerUps)
		self.addScript(HandlePipes)

	def goPassive(self):
		self.tags.append("Passive")
		self.getComponent(SpriteRenderer).opacity = 127

		def f():
			self.tags.remove("Passive")
			self.getComponent(SpriteRenderer).opacity = 255

		Timer.add(f, (), 2000, 0, 1)

	def prepareDestroy(self):
		movementScript = self.getScript(MovementScript)
		if type(movementScript.state) != MovementScript.Die:
			self.state = Small(self)
			movementScript.state = MovementScript.Die(movementScript)


class Small(IEvents):
	def __init__(self, player):
		self.player = player
		self.player.spriteSet = Resources.playerSprites[self.player.character]["small"]

		collider = self.player.getComponent(Collider)
		collider.size = Resources.playerSmallSize - Vector2(6, 3)
		collider.offset = Vector2(3, 0)

	def onLateUpdate(self):
		nearestBlockHit = self.player.getScript(Checks).nearestBlockHit
		if nearestBlockHit is not None:
			nearestBlockHit.smallHit()

	def downgrade(self):
		mainScript = self.player.getScript(MovementScript)
		mainScript.state = MovementScript.Die(mainScript)

	def upgrade(self):
		self.player.state = Big(self.player)
		self.player.transform.position += (0, 8)

	def __str__(self):
		return "Small"


class Big(IEvents):
	def __init__(self, player):
		self.player = player
		self.player.spriteSet = Resources.playerSprites[self.player.character]["big"]

		collider = self.player.getComponent(Collider)
		collider.size = Resources.playerBigSize - Vector2(6, 3)
		collider.offset = Vector2(3, -8)

	def onLateUpdate(self):
		nearestBlockHit = self.player.getScript(Checks).nearestBlockHit
		if nearestBlockHit is not None:
			nearestBlockHit.bigHit()

	def downgrade(self):
		self.player.state = Small(self.player)
		self.player.goPassive()

		Resources.powerdown.play().volume = 0.05

	def upgrade(self):
		self.player.state = Fire(self.player)

	def __str__(self):
		return "Big"


class Fire(IEvents):
	def __init__(self, player):
		self.player = player
		self.player.spriteSet = Resources.playerSprites["fire"]

		collider = self.player.getComponent(Collider)
		collider.size = Resources.playerBigSize - Vector2(6, 3)
		collider.offset = Vector2(3, -8)

	def onLateUpdate(self):
		nearestBlockHit = self.player.getScript(Checks).nearestBlockHit
		if nearestBlockHit is not None:
			nearestBlockHit.bigHit()

	def onKeyPress(self, symbol, modifiers):
		if symbol == pyglet.window.key.LSHIFT:
			World.instantiate(Fireball, self.player.transform.position, self.player.getScript(Checks).movingRight)

	def downgrade(self):
		self.player.state = Small(self.player)
		self.player.goPassive()

		Resources.powerdown.play().volume = 0.05

	def upgrade(self):
		pass

	def __str__(self):
		return "Fire"


class MainScript(Script):
	def init(self):
		self.order = 1

	def onUpdate(self):
		# print(self.gameObject.transform.position / tileSizeNum)

		self.gameObject.state.onUpdate()

		if self.gameObject.transform.position.y < 0:
			World.destroy(self.gameObject)

	def onLateUpdate(self):
		self.gameObject.state.onLateUpdate()

	def onKeyPress(self, symbol, modifiers):
		self.gameObject.state.onKeyPress(symbol, modifiers)

		# import pyglet
		# if symbol == pyglet.window.key.F:
		# 	self.gameObject.state = Fire(self.gameObject)
		#
		# elif symbol == pyglet.window.key.B:
		# 	self.gameObject.transform.position += (0, 8)
		# 	self.gameObject.state = Big(self.gameObject)
		#
		# elif symbol == pyglet.window.key.S:
		# 	self.gameObject.state = Small(self.gameObject)

class Checks(Script):
	def init(self):
		self.order = 0

		self.onGround = True
		self.running = False
		self.movingRight = True

		self.blocksHit = []
		self.nearestBlockHit = None

	def onUpdate(self):
		self.blocksHit.clear()
		self.nearestBlockHit = None

		self.onGround = False
		self.running = World.keys[key.LSHIFT]

		physics = self.gameObject.getComponent(Physics)

		if physics.velocity.x > 0:
			self.movingRight = True
		elif physics.velocity.x < 0:
			self.movingRight = False

	def onCollisionEnter(self, other, side):
		if side == Sides.BOTTOM_SIDE and ("Solid" in other.tags or "Platform" in other.tags):
			self.onGround = True

		elif side == Sides.TOP_SIDE and "Block" in other.tags:
			self.blocksHit.append(other)

	def onLateUpdate(self):
		if not self.blocksHit:
			return

		nearestDistance = 9999
		for block in self.blocksHit:
			dist = abs(self.gameObject.transform.position.x - block.transform.position.x)
			if dist < nearestDistance:
				nearestDistance = dist
				self.nearestBlockHit = block


class MovementScript(Script):
	def init(self):
		self.order = 1
		self.state = self.Walk(self)

	def onKeyPress(self, symbol, modifiers):
		self.state.onKeyPress(symbol, modifiers)

	def onUpdate(self):
		self.state.onUpdate()

	def onCollisionEnter(self, other, side):
		self.state.onCollisionEnter(other, side)

	def onLateUpdate(self):
		self.state.onLateUpdate()

	class Walk(IEvents):
		def __init__(self, script):
			self.script = script
			self.player = script.gameObject

		def onKeyPress(self, symbol, modifiers):
			if symbol == key.UP:
				if self.player.getScript(Checks).onGround:
					self.script.state = MovementScript.Jump(self.script)


		def onUpdate(self):
			physics = self.player.getComponent(Physics)
			spriteRenderer = self.player.getComponent(SpriteRenderer)

			leftRight(physics)

			# Nullify small movements
			limit = 4
			if -limit < physics.velocity.x < limit:
				physics.velocity.x = 0
				spriteRenderer.setImage(self.player.spriteSet["stand"])

			if physics.velocity.x != 0:
				if ((physics.velocity.x > 0 and World.keys[key.LEFT]) or
				    (physics.velocity.x < 0 and World.keys[key.RIGHT])) and \
						self.player.getScript(Checks).running:

					spriteRenderer.setImage(self.player.spriteSet["break"])

				elif abs(physics.velocity.x) > 120 and self.player.getScript(Checks).running:
					spriteRenderer.setImage(self.player.spriteSet["run"])
				else:
					spriteRenderer.setImage(self.player.spriteSet["walk"])

			self.flipSpriteAccordingly(spriteRenderer)

		def flipSpriteAccordingly(self, spriteRenderer):
			spriteRenderer.sprite.scale_x = 1 if self.player.getScript(Checks).movingRight else -1

		def onLateUpdate(self):
			physics = self.player.getComponent(Physics)

			if (World.keys[key.LEFT] and physics.velocity.x > 0) or \
					(World.keys[key.RIGHT] and physics.velocity.x < 0):
				physics.velocity.x *= 0.95

			if World.keys[key.DOWN] and physics.velocity.x == 0:
				if self.player.getScript(Checks).onGround:
					self.script.state = MovementScript.Crouch(self.script)

			# print(self.player.transform.position)

	class Jump(IEvents):
		def __init__(self, script):
			self.script = script
			self.player = script.gameObject

			self.player.getComponent(Physics).velocity.y = 415

			if str(self.player.state) == "Small":
				Resources.jumpSmall.play().volume = 0.05
			else:
				Resources.jumpSuper.play().volume = 0.05

		def onUpdate(self):
			leftRight(self.player.getComponent(Physics))

			self.player.getComponent(SpriteRenderer).setImage(self.player.spriteSet["jump"])
			self.player.getComponent(SpriteRenderer).sprite.scale_x = 1 if self.player.getScript(
				Checks).movingRight else -1

		def onCollisionEnter(self, other, side):
			if ("Solid" in other.tags or "Platform" in other.tags) and side == Sides.BOTTOM_SIDE:
				self.script.state = MovementScript.Walk(self.script)

	class Crouch(IEvents):
		def __init__(self, script):
			self.script = script
			self.player = script.gameObject

			standingPipe = self.player.getScript(HandlePipes).standingPipe
			if standingPipe:
				standingPipe.playerCrouches(self.player)

		def onUpdate(self):
			spriteRenderer = self.player.getComponent(SpriteRenderer)
			spriteRenderer.setImage(self.player.spriteSet["crouch"])
			spriteRenderer.sprite.scale_x = 1 if self.player.getScript(Checks).movingRight else -1

			if not World.keys[key.DOWN]:
				self.script.state = MovementScript.Walk(self.script)


	class Die(IEvents):
		def __init__(self, script):
			self.script = script
			self.player = script.gameObject
			Player.lives -= 1

			collider = self.player.getComponent(Collider)
			print("die", collider.gameObject)

			self.player.removeComponent(collider)
			self.player.getComponent(SpriteRenderer).setImage(self.player.spriteSet["die"])

			Resources.bgMusic.pause()
			Resources.mariodie.play().volume = 0.2
			World.findByTag("Time")[0].stop()

			self.player.getComponent(Physics).customGravity = (0, 0)
			self.player.getComponent(Physics).velocity.set(0, 0)

			def f():
				self.player.getComponent(Physics).customGravity = None
				self.player.getComponent(Physics).velocity.set(0, 450)

			Timer.add(f, (), 500, 0, 1)

			def goToGameOver():
				from game.levels.GameOverSplash import GameOverSplash
				SceneManager().loadScene(GameOverSplash)

			def resetLevel():
				from game.levels.Level1_1 import Level1_1
				from game.levels.LevelSplash import LevelSplash
				World.findByTag("Time")[0].restart()

				currentLevelClass = type(SceneManager().currentScene)
				SceneManager().loadScene(LevelSplash, currentLevelClass, currentLevelClass.major, currentLevelClass.minor)

			if self.player.lives <= 0:
				Timer.add(goToGameOver, (), 4000, 0, 1)
			else:
				Timer.add(resetLevel, (), 4000, 0, 1)

class ApplyDrag(Script):
	def onLateUpdate(self):
		dragGround = 0.90
		dragAir = 0.99

		physics = self.gameObject.getComponent(Physics)

		if not World.keys[key.LEFT] and not World.keys[key.RIGHT]:
			if self.gameObject.getScript(Checks).onGround:
				physics.velocity.x *= dragGround
			else:
				physics.velocity.x *= dragAir


class MetEnemy(Script):
	def onCollisionEnter(self, other, side):
		if "MovingEnemy" in other.tags:
			physics = self.gameObject.getComponent(Physics)

			if "KoopaTroopa" in other.tags:
				script = other.getScript(KoopaTroopaScript)

				if isinstance(script.state, KoopaTroopaScript.Walk) or \
						isinstance(script.state, KoopaTroopaScript.Bowling):

					if side == Sides.BOTTOM_SIDE and "Invincible" not in self.gameObject.tags:
						physics.velocity.y = 200

					else:
						if ("Passive" not in self.gameObject.tags) and \
								("Invincible" not in self.gameObject.tags):
							self.gameObject.state.downgrade()

				elif isinstance(script.state, KoopaTroopaScript.Stomped):
					pass

				elif isinstance(script.state, KoopaTroopaScript.Recovering):
					if side == Sides.BOTTOM_SIDE and "Invincible" not in self.gameObject.tags:
						physics.velocity.y = 200

			else:
				if side == Sides.BOTTOM_SIDE and "Invincible" not in self.gameObject.tags:
					physics.velocity.y = 200

				else:
					if ("Passive" not in self.gameObject.tags) and \
							("Invincible" not in self.gameObject.tags):
						self.gameObject.state.downgrade()

		elif "PiranhaPlant" in other.tags and other.aggressive:
			if ("Passive" not in self.gameObject.tags) and \
					("Invincible" not in self.gameObject.tags):
				self.gameObject.state.downgrade()


class CancelVelocity(Script):
	def onCollisionEnter(self, other, side):
		phyisics = self.gameObject.getComponent(Physics)

		if "Solid" in other.tags:
			if "Invisible" in other.tags:
				if side == Sides.TOP_SIDE and phyisics.velocity.y > 0:
					phyisics.velocity.y = 0

			else:
				if (side == Sides.RIGHT_SIDE and phyisics.velocity.x > 0) or \
						(side == Sides.LEFT_SIDE and phyisics.velocity.x < 0):
					phyisics.velocity.x = 0

				elif (side == Sides.TOP_SIDE and phyisics.velocity.y > 0) or \
						(side == Sides.BOTTOM_SIDE and phyisics.velocity.y < 0):
					phyisics.velocity.y = 0

		elif "Platform" in other.tags:
			if side == Sides.BOTTOM_SIDE and phyisics.velocity.y < 0:
				phyisics.velocity.y = 0


class HandlePowerUps(Script):
	def onCollisionStay(self, other):
		if "PowerUp" in other.tags and other.popped:
			# print(World.frameCount)
			if "SuperMushroom" in other.tags or "FireFlower" in other.tags:
				self.gameObject.state.upgrade()

			elif "SuperStar" in other.tags:
				self.gameObject.tags.append("Invincible")

				Resources.bgMusic.pause()
				p = Resources.star.play()
				p.volume = 0.15

				def f():
					Resources.bgMusic.play()

				p.set_handler("on_player_eos", f)

				def f():
					self.gameObject.tags.remove("Invincible")
					state = str(self.gameObject.state)

					if state == "Small":
						self.gameObject.spriteSet = Resources.playerSprites[self.gameObject.character]["small"]
					elif state == "Big":
						self.gameObject.spriteSet = Resources.playerSprites[self.gameObject.character]["big"]
					elif state == "Fire":
						self.gameObject.spriteSet = Resources.playerSprites["fire"]

				Timer.add(f, (), 10000, 0, 1)



	def onUpdate(self):
		if "Invincible" in self.gameObject.tags:
			state = str(self.gameObject.state)

			if state == "Small":
				self.gameObject.spriteSet = Resources.playerSprites["invincible"]["small"]
			else:
				self.gameObject.spriteSet = Resources.playerSprites["invincible"]["big"]


class HandlePipes(Script):
	def init(self, *args, **kwargs):
		self.standingPipe = None

	def onUpdate(self):
		self.standingPipe = None

	def onCollisionEnter(self, other, side):
		if side == Sides.BOTTOM_SIDE and "PipeHead" in other.tags:
			thisRect = self.gameObject.getComponent(Collider).rect
			otherRect = other.getComponent(Collider).rect
			if thisRect.left - 5 > otherRect.left and thisRect.right + 5 < otherRect.right:
				self.standingPipe = other


def leftRight(physics):
	running = World.keys[key.LSHIFT]

	leftRight = 4
	if World.keys[key.LEFT]:
		physics.addForce((-leftRight, 0))
	elif World.keys[key.RIGHT]:
		physics.addForce((leftRight, 0))

	clampVal = 100 if not running else 200
	physics.velocity.x = clamp(physics.velocity.x, -clampVal, clampVal)
