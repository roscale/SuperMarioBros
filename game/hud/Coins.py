from gameengine.components.Label import Label
from gameengine.managers.DrawingManager import DrawingManager


class Coins(Label):
	def init(self, *args, **kwargs):
		self.tags.append("Coins")

		self.coins = 0

		self.font_name = "Emulogic"
		self.font_size = 18
		self.text = "coins\n*00"
		self.width = 150
		self.multiline = True
		self.set_style("align", "center")

		DrawingManager().GUI.add(self)

	def increment(self):
		self.coins += 1
		if self.coins >= 100:
			self.coins = 0
			from game.Player import Player
			Player.lives += 1

			from game.Resources import Resources
			p = Resources.oneup.play()
			p.volume = 0.15

		self.text = "coins\n*{:02d}".format(self.coins)

	def reset(self):
		self.coins = 0
		self.text = "coins\n*{:02d}".format(self.coins)