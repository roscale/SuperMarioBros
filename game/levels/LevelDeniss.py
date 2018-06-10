from game.Player import Player
from game.Resources import tileSizeNum, tileSize, Resources, setBgMusic
from game.hud.Coins import Coins
from game.hud.Level import Level
from game.hud.Score import Score
from game.hud.Time import Time
from game.levels.Level1_1 import getClassByName
from game.scripts import FollowPlayer
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.loaders.LevelLoader import LevelLoader


class LevelDeniss(Scene):
	def onLoad(self):
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

		World.findByTag("Level")[0].major = 1
		World.findByTag("Level")[0].minor = 42

		World.findByTag("Time")[0].fastMusic = Resources.owMusicFast
		setBgMusic(Resources.owMusic).play()

		LevelLoader.loadMap("res/maps/levelDeniss.tmx", getClassByName)

		if not World.findByTag("Player"):
			onGroundY = tileSize.y * 2
			player = World.instantiate(Player, (tileSizeNum * 5, onGroundY))
			# player = World.instantiate(Player, (tileSizeNum * 77, onGroundY + tileSizeNum * 8))
			# player = World.instantiate(Player, (tileSizeNum * 120, onGroundY + tileSizeNum * 8))
			player.keepBetweenScenes = True

		self.mainCamera.addScript(FollowPlayer, 180)
		self.mainCamera.zoom = 3
		self.mainCamera.backgroundColor = (107, 140, 255, 0)
		self.mainCamera.transform.position = (-8, 0)
