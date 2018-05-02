from pyglet.gl import glClearColor, glTexParameterf, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, \
	GL_TEXTURE_MAG_FILTER, glColor4f, GL_COLOR_MATERIAL, glEnable, gluOrtho2D, glMatrixMode, GL_MODELVIEW, \
	glLoadIdentity, glViewport, GL_PROJECTION, glTranslatef

from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.components.Label import Label
from gameengine.core.FrustumCulling import FrustumCulling
from gameengine.managers.CameraManager import CameraManager
from gameengine.managers.Manager import Manager
from gameengine.util.Singleton import Singleton


@Singleton
class DrawingManager(Manager[SpriteRenderer]):
	def __init__(self):
		super().__init__()

		self.frustumCulling = FrustumCulling()
		self.GUI = set() # IDrawable objects

	def remove(self, object):
		super().remove(object)

		if isinstance(object, SpriteRenderer):
			self.frustumCulling.remove(object)

	def draw(self):
		for camera in CameraManager().collection:
			glClearColor(camera.backgroundColor[0] / 255,
			             camera.backgroundColor[1] / 255,
			             camera.backgroundColor[2] / 255,
			             camera.backgroundColor[3] / 255)

			camera.worldProjection()

			sprites = self.frustumCulling.intersect((*camera.transform.position, *(camera.transform.position + camera.size / camera.zoom)))

			for sprite in sprites:
				sprite.draw()

				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		###

		for elem in self.GUI:
			for camera in CameraManager().collection:
				camera.hudProjection()

				elem.draw()

				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		# for textRenderer in self.collection:
		# 	if isinstance(textRenderer, TextRenderer):
		# 		for camera in CameraManager().collection:
		# 			if textRenderer.hud:
		# 				camera.hudProjection()
		#
		# 			else:
		# 				glMatrixMode(GL_MODELVIEW)
		# 				glLoadIdentity()
		# 				glViewport(int(camera._windowPosition.x), int(camera._windowPosition.y), int(camera._size.x),
		# 				           int(camera._size.y))
		#
		# 				glMatrixMode(GL_PROJECTION)
		# 				glLoadIdentity()
		#
		# 				inverseZoom = 1 / camera.zoom
		#
		# 				# gluOrtho2D(-halfWidth * inverseZoom, halfWidth * inverseZoom, -halfHeight * inverseZoom, halfHeight * inverseZoom)
		# 				gluOrtho2D(0, camera._size.x * inverseZoom, 0, camera._size.y * inverseZoom)
		# 				glTranslatef(-camera.transform.position.x, -camera.transform.position.y, 0)
		#
		# 			coords = textRenderer.gameObject.transform.position
		#
		# 			textRenderer.x = int(coords.x)
		# 			textRenderer.y = int(coords.y)
		# 			textRenderer.draw()
		#
		# 			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		# 			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)