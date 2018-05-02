from game.Resources import Resources, setBgMusic
from gameengine.components.Label import Label
from gameengine.core.GameObject import GameObject
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.managers.DrawingManager import DrawingManager


class Time(Label):
	def init(self, *args, **kwargs):
		self.tags.append("Time")

		self.time = 999

		self.font_name = "Emulogic"
		self.font_size = 18
		self.text = "TIME\n{:03d}".format(self.time)
		self.width = 100
		self.multiline = True
		self.set_style("align", "right")

		self.countdown = Timer.add(self.decrement, (), 400, 400, -1)
		self.fastMusic = None

		DrawingManager().GUI.add(self)

	def decrement(self):
		self.time -= 1
		self.text = "TIME\n{:03d}".format(self.time)

		if self.time == 100:
			Resources.bgMusic.pause()
			p = Resources.hurryUp.play()
			p.volume = 0.15

			def f():
				setBgMusic(self.fastMusic).play()
				Resources.bgMusic.pitch = 1.05

			p.set_handler("on_player_eos", f)

		if self.time <= 0:
			Timer.remove(self.countdown)
			players = World.findByTag("Player")
			for player in players:
				# TODO: Just die
				player.state.downgrade()

	def stop(self):
		Timer.remove(self.countdown)

	def prepareDestroy(self):
		self.stop()