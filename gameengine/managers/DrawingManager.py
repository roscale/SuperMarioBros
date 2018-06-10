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
