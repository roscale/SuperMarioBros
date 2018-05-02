from pyglet.sprite import pyglet

from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World

image = pyglet.image.load("image.png")
image.anchor_x = 0
image.anchor_y = 0

World.init("collider", False, 800, 600)

class DragScript(Script):
	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		self.gameObject.transform.position += (dx, dy)


class ChangeOrder(Script):
	def onKeyPress(self, symbol, modifiers):
		if symbol in range(65456, 65456 + 10):
			symbol -= 65456
			# self.gameObject.getComponent(Input).order = symbol
			self.gameObject.getComponent(SpriteRenderer).order = symbol


class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)
		input = self.addComponent(Input)
		input.size = (256, 256)
		self.addScript(DragScript)
		self.addScript(ChangeOrder)

class MyGameObject2(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)
		input = self.addComponent(Input)
		input.size = (256, 256)
		self.addScript(DragScript)

camera = Camera()

a = World.instantiate(MyGameObject, (), (50, 50))
b = World.instantiate(MyGameObject2, (400, 400))

b.getComponent(Input).order = 5
b.getComponent(SpriteRenderer).order = 5

World.run()