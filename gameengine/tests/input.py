from pyglet.sprite import pyglet

from gameengine.components.Input import Input
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World

image = pyglet.image.load("image.png")
image.anchor_x = 0
image.anchor_y = 0

World.init("input", False, 800, 600)


class Keyboard(Script):
	def onKeyPress(self, symbol, modifiers):
		print("onKeyPress", symbol, modifiers)

	def onKeyRelease(self, symbol, modifiers):
		print("onKeyPress", symbol, modifiers)


class Mouse(Script):
	def onMouseMotion(self, x, y, dx, dy):
		print("onMouseMotion", x, y, dx, dy)

	def onMousePress(self, x, y, button, modifiers):
		print("onMousePress", x, y, button, modifiers)

	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		print("onMouseDrag", x, y, dx, dy, buttons, modifiers)

	def onMouseRelease(self, x, y, button, modifiers):
		print("onMouseRelease", x, y, button, modifiers)

	def onMouseScroll(self, x, y, scroll_x, scroll_y):
		print("onMouseScroll", x, y, scroll_x, scroll_y)


class DragScript(Script):
	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		self.gameObject.transform.position += (dx, dy)


class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.da = 0

		self.addComponent(SpriteRenderer).setImage(image)
		self.addComponent(Input).size = (256, 256)

		self.addScript(Keyboard)
		self.addScript(Mouse)
		self.addScript(DragScript)


camera = Camera()
camera.windowPosition = (0, 0)
camera.size = (400, 600)
camera.zoom = 0.3

camera = Camera()
camera.windowPosition = (400, 0)
camera.size = (400, 600)
camera.zoom = 0.7

World.instantiate(MyGameObject, (100, 50))

World.run()


