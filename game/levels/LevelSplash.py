from typing import Type

from game.hud.Coins import Coins
from game.hud.Level import Level
from game.hud.Score import Score
from game.hud.Time import Time
from gameengine.components.Label import Label
from gameengine.core.Scene import Scene
from gameengine.core.Script import Script
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.managers.DrawingManager import DrawingManager
from gameengine.managers.SceneManager import SceneManager


class LevelSplash(Scene):
	def onLoad(self, nextLevel: Type[Scene], major, minor):
		self.mainCamera.backgroundColor = (0, 0, 0, 0)
		self.mainCamera.zoom = 3

		if not World.findByTag("Score"):
			score = World.instantiate(Score, (80, self.mainCamera.size.y - 50))
			score.keepBetweenScenes = True

		if not World.findByTag("Coins"):
			coins = World.instantiate(Coins, (400, self.mainCamera.size.y - 50))
			coins.keepBetweenScenes = True

		if not World.findByTag("Level"):
			level = World.instantiate(Level, (800, self.mainCamera.size.y - 50))
			level.keepBetweenScenes = True

		if not World.findByTag("Time"):
			time = World.instantiate(Time, (1100, self.mainCamera.size.y - 50))
			time.keepBetweenScenes = True

		World.findByTag("Level")[0].major = major
		World.findByTag("Level")[0].minor = minor

		worldLabel = World.instantiate(Label, (500, 400))
		worldLabel.text = "World {}-{}".format(major, minor)
		worldLabel.font_name = "Emulogic"
		worldLabel.font_size = 22
		worldLabel.set_style("align", "center")
		DrawingManager().GUI.add(worldLabel)

		lifesLabel = World.instantiate(Label, (500, 325))

		# players = World.findByTag("Player")
		# player = players[0] if players else None

		from game.Player import Player
		lifesLabel.text = "lives * {}".format(Player.lives)
		lifesLabel.font_name = "Emulogic"
		lifesLabel.font_size = 22
		lifesLabel.set_style("align", "right")
		DrawingManager().GUI.add(lifesLabel)


		def loadNextLevel():
			DrawingManager().remove(worldLabel)
			DrawingManager().GUI.remove(worldLabel)

			DrawingManager().remove(lifesLabel)
			DrawingManager().GUI.remove(lifesLabel)

			SceneManager().loadScene(nextLevel)

		# Prevent player falling while loading level
		class KeepPlayerFromFalling(Script):
			def init(self, *args, **kwargs):
				self.player = None

				players = World.findByTag("Player")
				if players:
					self.player = players[0]

			def onUpdate(self):
				if self.player:
					from gameengine.components.Physics import Physics
					self.player.getComponent(Physics).velocity.y = 0

		from gameengine.core.GameObject import GameObject
		go = World.instantiate(GameObject, (0, 0))
		go.addScript(KeepPlayerFromFalling)

		Timer.add(loadNextLevel, (), 1500, 0, 1)
