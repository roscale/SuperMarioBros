from game.Player import Player
from game.blocks.QuestionBlock import RotatingCoin
from game.powerups.FireFlower import FireFlower
from game.powerups.SuperMushroom import SuperMushroom
from gameengine.core.GameObject import GameObject
from gameengine.core.World import World


class PlayerUpgrade(GameObject):
	def init(self, *args):
		player: Player = World.findByTag("Player")[0]
		state = str(player.state)

		if state == "Small":
			World.instantiate(SuperMushroom, self.transform.position)
		elif state == "Big":
			World.instantiate(FireFlower, self.transform.position)
		elif state == "Fire":
			World.instantiate(RotatingCoin, self.transform.position)
