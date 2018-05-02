from gameengine.components.Label import Label
from gameengine.core.GameObject import GameObject
from gameengine.managers.DrawingManager import DrawingManager


class Level(Label):
	def init(self, major=1, minor=1, *args, **kwargs):
		self.tags.append("Level")

		self._major = major
		self._minor = minor

		self.font_name = "Emulogic"
		self.font_size = 18

		self.width = 150
		self.multiline = True
		self.set_style("align", "center")

		self.updateText()

		DrawingManager().GUI.add(self)

	def updateText(self):
		self.text = "WORLD\n{}-{}".format(str(self._major), str(self._minor))

	@property
	def major(self) -> int:
		return self._major

	@major.setter
	def major(self, val):
		self._major = val
		self.updateText()

	@property
	def minor(self) -> int:
		return self.minor

	@minor.setter
	def minor(self, val):
		self._minor = val
		self.updateText()

