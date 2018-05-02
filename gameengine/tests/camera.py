from pyglet.sprite import pyglet

from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World

image = pyglet.image.load("image.png")

World.init("camera", False, 800, 600)


class DragScript(Script):
	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		self.gameObject.transform.position += (dx, dy)


class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)
		self.addComponent(Input).size = (256, 256)
		self.addScript(DragScript)

camera = Camera()
camera.windowPosition = (0, 0)
camera.size = (400, 300)
camera.zoom = 0.3

# class MoveCamera(Script):
# 	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
# 		self.gameObject.transform.position -= (dx, dy)
#
# input = camera.addComponent(Input)
# input.size = camera.size / camera.zoom
# camera.addScript(MoveCamera)

camera = Camera()
camera.windowPosition = (400, 0)
camera.size = (400, 300)
camera.zoom = 0.7

camera = Camera()
camera.windowPosition = (0, 300)
camera.size = (400, 300)
camera.zoom = 0.7

camera = Camera()
camera.windowPosition = (400, 300)
camera.size = (400, 300)
camera.zoom = 0.7

World.instantiate(MyGameObject, (0, 0))

World.run()