from gameengine.components.Label import Label
from gameengine.core.GameObject import GameObject
from gameengine.core.Timer import Timer
from gameengine.core.World import World


class Points(GameObject):
	def init(self, number, *args, **kwargs):
		self.number = str(number)

		tr = self.addComponent(Label)
		tr.fontName = "Emulogic"
		tr.fontSize = 6
		tr.text = self.number

		def f():
			World.destroy(self)

		Timer.add(f, (), 700, 0, 1)