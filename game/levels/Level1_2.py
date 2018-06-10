from game.Player import Player
from game.Resources import tileSize, tileSizeNum, setBgMusic, Resources
from game.entities.Goomba import Goomba
from game.entities.KoopaTroopa import KoopaTroopa
from game.entities.Platform import Platform
from game.hud.Coins import Coins
from game.hud.Level import Level
from game.hud.Score import Score
from game.hud.Time import Time
from game.levels.Level1_1 import getClassByName
from game.levels.LevelSplash import LevelSplash
from game.scripts import FollowPlayer
from game.technical.Trigger import Trigger
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.loaders.LevelLoader import LevelLoader
from gameengine.managers.SceneManager import SceneManager


class Level1_2(Scene):
	major = 1
	minor = 2

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

		time = World.findByTag("Time")[0]
		time.fastMusic = Resources.ugMusicFast
		time.time = 500
		time.restart()

		World.findByTag("Level")[0].major = 1
		World.findByTag("Level")[0].minor = 2

		LevelLoader.loadMap("res/maps/level1-2.tmx", getClassByName)


		onGroundY = tileSize.y * 2

		# player = World.instantiate(Player, (tileSizeNum * 5, onGroundY))

		self.mainCamera.addScript(FollowPlayer, 145)

		self.mainCamera.zoom = 3
		self.mainCamera.backgroundColor = (107, 140, 255, 0)

		# camera.transform.position -= (8, 8)
		self.mainCamera.transform.position -= (8, 0)
		# camera.transform.position += (0, tileSizeNum * 16)
		self.mainCamera.backgroundColor = (0, 0, 0, 0)


		World.instantiate(Goomba, (tileSizeNum * 13, onGroundY), theme="ug")
		World.instantiate(Goomba, (tileSizeNum * 14.5, onGroundY), theme="ug")

		World.instantiate(Goomba, (tileSizeNum * 28, onGroundY), theme="ug")


		def f():
			World.instantiate(KoopaTroopa, (tileSizeNum * 45, onGroundY+10), theme="ug")
			World.instantiate(KoopaTroopa, (tileSizeNum * 46.5, onGroundY+10), theme="ug")
			World.instantiate(KoopaTroopa, (tileSizeNum * 57, onGroundY+10), theme="ug")

		World.instantiate(Trigger, (tileSizeNum * 25, onGroundY), (1, 1000), "Player", f)

		def f():
			World.instantiate(Goomba, (tileSizeNum * 64, onGroundY), theme="ug")
			World.instantiate(Goomba, (tileSizeNum * 67, onGroundY), theme="ug")

		World.instantiate(Trigger, (tileSizeNum * 45, onGroundY), (1, 1000), "Player", f)

		def f():
			World.instantiate(Goomba, (tileSizeNum * 73, tileSizeNum * 10), theme="ug")

			World.instantiate(Goomba, (tileSizeNum * 78.5, tileSizeNum * 6), theme="ug")
			World.instantiate(Goomba, (tileSizeNum * 80, tileSizeNum * 6), theme="ug")

		World.instantiate(Trigger, (tileSizeNum * 53, onGroundY), (1, 1000), "Player", f)

		def f():
			World.instantiate(Goomba, (tileSizeNum * 97, onGroundY), theme="ug")
			World.instantiate(Goomba, (tileSizeNum * 98.5, onGroundY), theme="ug")
			World.instantiate(Goomba, (tileSizeNum * 100, onGroundY), theme="ug")

		World.instantiate(Trigger, (tileSizeNum * 75, onGroundY), (1, 1000), "Player", f)

		World.instantiate(Goomba, (tileSizeNum * 112, onGroundY), theme="ug")

		def f():
			World.instantiate(Goomba, (tileSizeNum * 137, tileSizeNum * 6), theme="ug")
			World.instantiate(Goomba, (tileSizeNum * 135.5, tileSizeNum * 6), theme="ug")

		World.instantiate(Trigger, (tileSizeNum * 116, onGroundY), (1, 1000), "Player", f)

		World.instantiate(KoopaTroopa, (tileSizeNum * 147, onGroundY+5), theme="ug", smart=True)


		World.instantiate(Platform, (tileSizeNum * 139, tileSizeNum * 15), Platform.UpOrDown, velocity=(0, -50))
		World.instantiate(Platform, (tileSizeNum * 139, tileSizeNum * 7), Platform.UpOrDown, velocity=(0, -50))
		World.instantiate(Platform, (tileSizeNum * 155, tileSizeNum * 15), Platform.UpOrDown, velocity=(0, 50))
		World.instantiate(Platform, (tileSizeNum * 155, tileSizeNum * 7), Platform.UpOrDown, velocity=(0, 50))

		if not World.findByTag("Player"):
			player = World.instantiate(Player, (tileSizeNum * 3, tileSizeNum * 12))
			player.keepBetweenScenes = True

		World.findByTag("Player")[0].transform.position = (tileSizeNum * 3, tileSizeNum * 12)

		exitPipe = World.findByTag("Exit")[0]

		def exit(player):
			from game.levels.Level1_3 import Level1_3
			SceneManager().loadScene(LevelSplash, Level1_3, 1, 3)

		exitPipe.teleport = exit

		# from game.levels.Level1_3 import Level1_3
		# World.findByTag("Flag")[0].setNextLevel(Level1_3, 1, 3)

		setBgMusic(Resources.ugMusic).play()
