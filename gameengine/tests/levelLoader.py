from pyglet.image import AbstractImage
from pyglet.sprite import pyglet
from pytmx import TiledMap, TiledObjectGroup
from pytmx.util_pyglet import load_pyglet

from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.loaders.LevelLoader import LevelLoader
from gameengine.util.Vector2 import Vector2

def getRegion(image: AbstractImage, x, y, size: Vector2) -> AbstractImage:
	image = image.get_region(x, int(image.height - size.y - y), *size.toIntTuple())
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return image

image = pyglet.image.load("tileset.png")
image.anchor_x = 0
image.anchor_y = 0

ground = getRegion(image, 0, 0, Vector2(16, 16))

class Ground(GameObject):
	def init(self, argument=None):
		if argument is not None:
			self.addScript(self.S, (argument,))

		self.addComponent(SpriteRenderer).setImage(ground)

	class S(Script):
		def init(self, argument):
			self.argument = argument

		def onUpdate(self):
			print(self, self.argument)

def getClassByName(name: str) -> type:
	if name == "Ground":
		return Ground

World.init("levelLoader", True, 800, 600)

camera = Camera()
# World.instantiate(Ground, (0, 0))
# World.instantiate(Ground, (16, 0))

LevelLoader.loadMap("map.tmx", getClassByName)

World.run()