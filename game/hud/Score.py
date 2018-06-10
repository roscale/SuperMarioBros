import pyglet

from gameengine.components.Input import Input
from gameengine.components.Label import Label
from gameengine.core.Script import Script
from gameengine.managers.DrawingManager import DrawingManager
from gameengine.managers.SceneManager import SceneManager


class Score(Label):
	def init(self, *args, **kwargs):
		self.tags.append("Score")

		self.score = 0

		self.font_name = "Emulogic"
		self.font_size = 18
		self.text = "MARIO\n{:06d}".format(self.score)
		self.width = -1
		self.multiline = True

		DrawingManager().GUI.add(self)

		self.addComponent(Input)

	def add(self, val):
		self.score += val
		self.text = "MARIO\n{:06d}".format(self.score)

	def reset(self):
		self.score = 0
		self.text = "MARIO\n{:06d}".format(self.score)