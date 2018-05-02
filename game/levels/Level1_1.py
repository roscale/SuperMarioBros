from game.blocks.Grass import GrassLeft, GrassMiddle, GrassRight, Pillar
from game.misc.Castle import Castle
from game.Player import Player
from game.Resources import tileSize, tileSizeNum, Resources, setBgMusic
from game.blocks.Brick import Brick
from game.blocks.Ground import Ground
from game.blocks.HardBlock import HardBlock
from game.blocks.Pipe import VPipeHead, VPipeBody, HPipeHead, HPipeBody, HPipeConnection
from game.blocks.QuestionBlock import QuestionBlock, RotatingCoin
from game.entities.Goomba import Goomba
from game.entities.KoopaTroopa import KoopaTroopa
from game.hud.Coins import Coins
from game.hud.Level import Level
from game.hud.Score import Score
from game.hud.Time import Time
from game.misc.Flag import FlagPoleBody, FlagPoleHead, Flag
from game.powerups.Coin import Coin
from game.powerups.PlayerUpgrade import PlayerUpgrade
from game.powerups.SuperStar import SuperStar
from game.scripts import FollowPlayer
from game.technical.Trigger import Trigger
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.loaders.LevelLoader import LevelLoader
from gameengine.managers.CollisionManager import Sides


def getClassByName(name: str) -> type:
	if name == "Ground": return Ground
	if name == "Brick": return Brick
	if name == "HardBlock": return HardBlock
	if name == "QuestionBlock": return QuestionBlock
	if name == "RotatingCoin": return RotatingCoin

	if name == "Pillar": return Pillar
	if name == "GrassLeft": return GrassLeft
	if name == "GrassMiddle": return GrassMiddle
	if name == "GrassRight": return GrassRight

	if name == "VPipeHead": return VPipeHead
	if name == "VPipeBody": return VPipeBody
	if name == "HPipeHead": return HPipeHead
	if name == "HPipeBody": return HPipeBody
	if name == "HPipeConnection": return HPipeConnection

	if name == "SuperStar": return SuperStar
	if name == "PlayerUpgrade": return PlayerUpgrade
	if name == "Coin": return Coin

	if name == "FlagPoleBody": return FlagPoleBody
	if name == "FlagPoleHead": return FlagPoleHead
	if name == "Flag": return Flag


@World.collisionListener
def collisionListener(first, second, side):
	if "Player" in first.tags and "Solid" in second.tags:
		if "Invisible" in second.tags:
			if side == Sides.TOP_SIDE:
				return True
			else:
				return False
		else:
			return True

	if "MovingEnemy" in first.tags and "Solid" in second.tags:
		return True

	if "MovingEnemy" in first.tags and "MovingEnemy" in second.tags:
		return True

	if ("Player" in first.tags and "MovingEnemy" in second.tags and side == Sides.BOTTOM_SIDE) or \
			("MovingEnemy" in first.tags and "Player" in second.tags and side == Sides.TOP_SIDE):

		if ("MovingEnemy" in first.tags and "Bowling" in first.tags) or (
				"MovingEnemy" in second.tags and "Bowling" in second.tags):
			return False
		else:
			return True

	if ("Player" in first.tags and "MovingEnemy" in second.tags) or (
			"MovingEnemy" in first.tags and "Player" in second.tags):
		if side == Sides.LEFT_SIDE or side == Sides.RIGHT_SIDE:
			return False

	if "Fireball" in first.tags and "Solid" in second.tags:
		return True

	if "PowerUp" in first.tags and "Solid" in second.tags:
		return first.popped

	if "PowerUp" in first.tags and "PowerUp" in second.tags:
		return True

	if ("PiranhaPlant" in first.tags and "Player" in second.tags) or \
			("Player" in first.tags and "PiranhaPlant" in second.tags):
		return False

	if ("PiranhaPlant" in first.tags and "Enemy" in second.tags) or \
			("Enemy" in first.tags and "PiranhaPlant" in second.tags):
		return False

	if "Flag" in first.tags and "Solid" in second.tags:
		return True

	if "Player" in first.tags and "Platform" in second.tags:
		if side == Sides.BOTTOM_SIDE:
			return True

	if "Platform" in first.tags and "Player" in second.tags:
		if side == Sides.TOP_SIDE:
			return True

	return False


class Level1_1(Scene):
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

		level = World.findByTag("Level")[0]
		level.major = 1
		level.minor = 1

		if not World.findByTag("Time"):
			time = World.instantiate(Time, (1100, self.mainCamera.size.y - 50))
			time.keepBetweenScenes = True

		World.findByTag("Time")[0].fastMusic = Resources.owMusicFast


		LevelLoader.loadMap("res/maps/level1-1.tmx", getClassByName)

		onGroundY = tileSize.y * 2

		World.instantiate(Goomba, (tileSizeNum * 24, onGroundY))

		World.instantiate(Goomba, (tileSizeNum * 40, onGroundY))

		World.instantiate(Goomba, (tileSizeNum * 48, onGroundY))
		World.instantiate(Goomba, (tileSizeNum * 49.5, onGroundY))

		def f():
			World.instantiate(Goomba, (tileSizeNum * 82, tileSizeNum * 10.2))
			World.instantiate(Goomba, (tileSizeNum * 83.5, tileSizeNum * 10.2))

		tr = World.instantiate(Trigger, (tileSizeNum * 63, onGroundY), (1, 1000), "Player", f)

		def f():
			World.instantiate(Goomba, (tileSizeNum * 109, onGroundY))
			World.instantiate(Goomba, (tileSizeNum * 110.5, onGroundY))

			World.instantiate(KoopaTroopa, (tileSizeNum * 120, tileSizeNum * 5))

		World.instantiate(Trigger, (tileSizeNum * 85, onGroundY), (1, 1000), "Player", f)

		def f():
			World.instantiate(Goomba, (tileSizeNum * 127, onGroundY))
			World.instantiate(Goomba, (tileSizeNum * 128.5, onGroundY))
			World.instantiate(Goomba, (tileSizeNum * 130.5, onGroundY))
			World.instantiate(Goomba, (tileSizeNum * 132, onGroundY))

		World.instantiate(Trigger, (tileSizeNum * 109, onGroundY), (1, 1000), "Player", f)

		World.instantiate(Goomba, (tileSizeNum * 166, onGroundY))
		World.instantiate(Goomba, (tileSizeNum * 167.5, onGroundY))

		###

		if not World.findByTag("Player"):
			player = World.instantiate(Player, (tileSizeNum * 5, onGroundY))
			# player = World.instantiate(Player, (tileSizeNum * 175, onGroundY))
			player.keepBetweenScenes = True

		self.mainCamera.addScript(FollowPlayer, 187)
		self.mainCamera.zoom = 3
		self.mainCamera.backgroundColor = (107, 140, 255, 0)
		self.mainCamera.transform.position = (-8, 0)

		World.instantiate(Castle, (tileSizeNum * 203, onGroundY + 32))

		enterPipe = World.findByTag("Enter")[0]
		def enter(player):
			mainCamera = World.findByTag("MainCamera")[0]

			mainCamera.backgroundColor = (0, 0, 0, 0)
			mainCamera.transform.position = (-8, tileSizeNum * 16)
			mainCamera.getScript(FollowPlayer).enabled = False
			player.transform.position = (tileSizeNum * 2, tileSizeNum * 28)

		enterPipe.teleport = enter


		exitPipe = World.findByTag("Exit")[0]
		def exit(player):
			mainCamera = World.findByTag("MainCamera")[0]

			mainCamera.backgroundColor = (107, 140, 255, 0)
			mainCamera.transform.position.y = 0
			mainCamera.getScript(FollowPlayer).enabled = True
			player.transform.position = (tileSizeNum * 163.5, tileSizeNum * 4)

		exitPipe.teleport = exit

		setBgMusic(Resources.owMusic).play()


