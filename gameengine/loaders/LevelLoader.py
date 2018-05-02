from abc import ABC
from typing import Callable, Type

from pyglet.image import AbstractImage
from pytmx.pytmx import *
from pytmx.util_pyglet import *

from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World


class Image(GameObject):
	def init(self, image: AbstractImage, *args, **kwargs):
		print("image")

		sr = self.addComponent(SpriteRenderer)
		sr.setImage(image)
		sr.order = 999


class LevelLoader(ABC):
	@classmethod
	def loadMap(cls, filename: str, getClassByName: Callable[[str], Type]):
		map: TiledMap = load_pyglet(filename)

		for layer in map.layers:
			if isinstance(layer, TiledTileLayer):
				for x, y, gid in layer:
					if gid != 0:
						properties = map.get_tile_properties_by_gid(gid)
						if properties is None:
							continue

						properties: dict = properties.copy()
						properties.pop("width")
						properties.pop("height")
						properties.pop("frames")

						name = properties["type"]
						properties.pop("type")

						cls.classifyAndNullify(properties, getClassByName)

						Class = getClassByName(name)
						if Class is None:
							print("Couldn't get class '{}'".format(name))

						invertY = (map.height-1 - y)

						print(properties)
						World.instantiate(Class, (x * map.tilewidth, invertY * map.tileheight), **properties)

			elif isinstance(layer, TiledObjectGroup):
				for object in layer:
					properties: dict = object.properties.copy()
					properties.pop("width")
					properties.pop("height")
					properties.pop("frames")

					name = properties["type"]
					properties.pop("type")

					cls.classifyAndNullify(properties, getClassByName)

					Class = getClassByName(name)
					if Class is None:
						print("Couldn't get class '{}'".format(name))

					invertY = (map.tileheight * (map.height-1) - object.y)

					World.instantiate(Class, (object.x, invertY), **properties)

			elif isinstance(layer, TiledImageLayer):
				properties: dict = layer.properties.copy()
				properties.pop("type")

				cls.classifyAndNullify(properties, getClassByName)

				try:
					y = map.height * map.tileheight - layer.image.height - layer.offsety
					World.instantiate(Image, (layer.offsetx-8, y-8), image=layer.image)

				except AttributeError:
					World.instantiate(Image, (-8, -8), image=layer.image, **properties)

	@classmethod
	def classifyAndNullify(cls, properties: dict, getClassByName: Callable[[str], Type]):
		for key in properties.keys():
			if properties[key] == "":
				properties[key] = None

			else:
				if properties[key][0] == '<' and properties[key][-1] == '>':
					properties[key] = getClassByName(properties[key][1:-1])

