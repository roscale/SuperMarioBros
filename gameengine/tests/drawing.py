from pyglet.sprite import pyglet

from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World

image = pyglet.image.load("image.png")
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2

World.init("drawing", True, 800, 600)

class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.addComponent(SpriteRenderer).setImage(image)


World.instantiate(MyGameObject, (400, 300))

Camera()

World.run()
