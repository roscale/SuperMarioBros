from pyglet.graphics import Batch
from pyglet.image import AbstractImage, Animation
from pyglet.sprite import Sprite

from gameengine.util.Vector2 import Vector2
from gameengine.util.pyqtree import Index


# TODO: Take scale in consideration
class FrustumCulling:
	def __init__(self):
		self.quadtree = Index((0, 0, 5000, 5000))

		self.allSprites: [Sprite] = []
		self.idleBatches  = {}
		self.activeBatches = {}

	def insert(self, sprite):
		self.allSprites.append(sprite)

		if isinstance(sprite.image, AbstractImage):
			self.quadtree.insert(sprite, self.getActualBBox(sprite, sprite.image))

		elif isinstance(sprite.image, Animation):
			image = sprite.image.frames[0].image
			self.quadtree.insert(sprite, self.getActualBBox(sprite, image))


	def remove(self, sprite):
		self.allSprites.remove(sprite)

		if isinstance(sprite.image, AbstractImage):
			self.quadtree.remove(sprite, self.getActualBBox(sprite, sprite.image))

		elif isinstance(sprite.image, Animation):
			image = sprite.image.frames[0].image
			self.quadtree.remove(sprite, self.getActualBBox(sprite, image))

	def intersect(self, bbox) -> [Batch]:
		shownSprites = self.quadtree.intersect(bbox)

		for sprite in shownSprites:
			batch = None

			if sprite.image not in self.activeBatches.keys():
				batch = Batch()
				self.activeBatches[sprite.image] = batch
			else:
				batch = self.activeBatches[sprite.image]

			if sprite.batch != batch:
				sprite.batch = batch

		s = set(shownSprites)
		hiddenSprites = [x for x in self.allSprites if x not in s]

		for sprite in hiddenSprites:
			batch = None

			if sprite.image not in self.idleBatches.keys():
				batch = Batch()
				self.idleBatches[sprite.image] = batch
			else:
				batch = self.idleBatches[sprite.image]

			if sprite.batch != batch:
				sprite.batch = batch

		return list(self.activeBatches.values())

	@staticmethod
	def getActualBBox(sprite: Sprite, image: AbstractImage):
		pos = Vector2(sprite.position)
		anchor = Vector2(image.anchor_x, image.anchor_y)
		actualPos = pos - anchor

		return (*actualPos, *(actualPos + (sprite.width, sprite.height)))