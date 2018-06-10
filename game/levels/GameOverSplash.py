from gameengine.components.Label import Label
from gameengine.core.Scene import Scene
from gameengine.core.Timer import Timer
from gameengine.core.World import World
from gameengine.managers.DrawingManager import DrawingManager
from gameengine.managers.SceneManager import SceneManager


class GameOverSplash(Scene):
	def onLoad(self, *args, **kwargs):
		self.mainCamera.backgroundColor = (0, 0, 0, 0)
		self.mainCamera.zoom = 3

		# players = World.findByTag("Player")
		# if players:
		# 	from gameengine.components.Physics import Physics
		# 	players[0].getComponent(Physics).customGravity = (0, 0)

		from game.Player import Player
		Player.lives = 3

		gameOverLabel = World.instantiate(Label, (500, 400))
		gameOverLabel.text = "Game Over"
		gameOverLabel.font_name = "Emulogic"
		gameOverLabel.font_size = 22
		gameOverLabel.set_style("align", "center")
		DrawingManager().GUI.add(gameOverLabel)

		scoreLabel = World.instantiate(Label, (400, 330))
		scoreLabel.text = "final score: {}".format(World.findByTag("Score")[0].score)
		scoreLabel.font_name = "Emulogic"
		scoreLabel.font_size = 22
		scoreLabel.set_style("align", "center")
		DrawingManager().GUI.add(scoreLabel)

		def loadNextLevel():
			DrawingManager().remove(gameOverLabel)
			DrawingManager().GUI.remove(gameOverLabel)

			DrawingManager().remove(scoreLabel)
			DrawingManager().GUI.remove(scoreLabel)

			World.findByTag("Score")[0].reset()
			World.findByTag("Coins")[0].reset()
			from game.levels.Level1_1 import Level1_1
			SceneManager().loadScene(Level1_1)

		Timer.add(loadNextLevel, (), 4000, 0, 1)