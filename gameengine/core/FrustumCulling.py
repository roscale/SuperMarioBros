from pyglet.graphics import Batch
from pyglet.image import AbstractImage, Animation
from pyglet.sprite import Sprite
from typing import List

from gameengine.util.Vector2 import Vector2
from gameengine.util.pyqtree import Index


# TODO: Take scale in consideration
class FrustumCulling:
	def __init__(self):
		self.quadtree = Index((0, 0, 5000, 5000))

	def insert(self, spriteRenderer):
		sprite = spriteRenderer.sprite

		if isinstance(sprite.image, AbstractImage):
			self.quadtree.insert(spriteRenderer, self.getActualBBox(sprite, sprite.image))

		elif isinstance(sprite.image, Animation):
			image = sprite.image.frames[0].image
			self.quadtree.insert(spriteRenderer, self.getActualBBox(sprite, image))

	def remove(self, spriteRenderer):
		sprite = spriteRenderer.sprite

		if isinstance(sprite.image, AbstractImage):
			self.quadtree.remove(spriteRenderer, self.getActualBBox(sprite, sprite.image))

		elif isinstance(sprite.image, Animation):
			image = sprite.image.frames[0].image
			self.quadtree.remove(spriteRenderer, self.getActualBBox(sprite, image))

	def intersect(self, bbox) -> List[Sprite]:
		spriteRenderers = list(self.quadtree.intersect(bbox))

		def _byOrder(spriteRenderer):
			return spriteRenderer._order

		spriteRenderers.sort(key=_byOrder, reverse=True)

		return [spriteRenderer.sprite for spriteRenderer in spriteRenderers]

	@staticmethod
	def getActualBBox(sprite: Sprite, image: AbstractImage) -> tuple:
		pos = Vector2(sprite.position)
		anchor = Vector2(image.anchor_x, image.anchor_y)
		actualPos = pos - anchor

		return (*actualPos, *(actualPos + (sprite.width, sprite.height)))