from gameengine.components.Label import Label
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World
from gameengine.managers.DrawingManager import DrawingManager


class Coins(Label):
	def init(self, *args, **kwargs):
		self.tags.append("Coins")

		self.coins = 0

		self.font_name = "Emulogic"
		self.font_size = 18
		self.text = "\n*00"
		self.width = -1
		self.multiline = True

		DrawingManager().GUI.add(self)

	def increment(self):
		self.coins += 1
		self.text = "\n*{:02d}".format(self.coins)