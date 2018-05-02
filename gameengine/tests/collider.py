from pyglet.sprite import pyglet

from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.CollisionManager import Sides

image = pyglet.image.load("image.png")
image.anchor_x = 0
image.anchor_y = 0

World.init("collider", True, 800, 600)

class DragScript(Script):
	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		self.gameObject.getComponent(Physics).addAcceleration((dx, dy))

	def onCollisionEnter(self, other, side):
		# physics = self.gameObject.getComponent(Physics)
		#
		# if side == Sides.TOP_SIDE or side == Sides.BOTTOM_SIDE:
		# 	physics.velocity.y = 0
		#
		# elif side == Sides.LEFT_SIDE or side == Sides.RIGHT_SIDE:
		# 	physics.velocity.x = 0

		print("onCollisionEnter", other, side)

	def onCollisionStay(self, other):
		print("onCollisionStay", other)

	def onCollisionExit(self, other):
		print("onCollisionExit", other)


class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)
		input = self.addComponent(Input)
		input.size = (256, 256)
		self.addComponent(Collider).size = (256, 256)
		self.addComponent(Physics).customGravity = (0, 0)

		self.addScript(DragScript)


class MyGameObject2(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)
		input = self.addComponent(Input)
		input.size = (256, 256)
		# input.offset = (256, 256)

		collider = self.addComponent(Collider)
		collider.size = (256, 256)
		# collider.offset = (256, 256)
		self.addComponent(Physics).customGravity = (0, 0)

		self.addScript(DragScript)

def collisionListener(this, other, side):
	if isinstance(this, MyGameObject) and isinstance(other, MyGameObject2):
		return True

	if isinstance(this, MyGameObject2) and isinstance(other, MyGameObject):
		return True

	return False

World._collisionListener = collisionListener


camera = Camera()

World.instantiate(, MyGameObject, (200, 400), ()
World.instantiate(, MyGameObject2, (50, 50), ()
World.instantiate(, MyGameObject2, (500, 200), ()

World.run()