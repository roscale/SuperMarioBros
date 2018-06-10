from gameengine.components.Label import Label
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.managers.DrawingManager import DrawingManager


class Instructions(Label):
	def init(self, *args, **kwargs):
		self.tags.append("Instructions")

		self.font_name = "Emulogic"
		self.font_size = 16
		self.text = "Deplacement : fleches\nCourir/jeter des boules de feu : SHIFT"
		self.width = 1000
		self.multiline = True
		self.set_style("align", "left")

		DrawingManager().GUI.add(self)

		def f():
			DrawingManager().remove(self)
			DrawingManager().GUI.remove(self)
			World.destroy(self)

		Timer.add(f, (), 5000, 0, 1)