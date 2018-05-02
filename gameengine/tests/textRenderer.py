import pyglet
from pyglet.font.freetype import FreeTypeFace

from gameengine.components.Input import Input
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.components.Label import Label
from gameengine.core.Camera import Camera
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World

World.init("textRenderer", True, 800, 600)

image = pyglet.image.load("image.png")
# image.anchor_x = image.width // 2
# image.anchor_y = image.height // 2

c = Camera()
# c.transform.position = (200, 200)
c.zoom = 3

class MyGameObject(Label):
	def __init__(self):
		super().__init__()

		sr = self.addComponent(SpriteRenderer)
		sr.setImage(image)

		ip = self.addComponent(Input)
		ip.size = sr.size
		self.addScript(self.DragScript)

		self._text = "Test Font"

		# FIXME loading local ttf file doesn't work
		pyglet.font.add_file("emulogic.ttf")
		self._fontName = "Emulogic"

		self._fontSize = 18
		self._color = (255, 255, 255, 255)

	class DragScript(Script):
		def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
			self.gameObject.transform.position += (dx, dy)

		def onUpdate(self):
			self.gameObject.transform.position += (0.9, 0.9)
			print(self.gameObject.transform.position)


World.instantiate(MyGameObject, (0, 0))


World.run()
