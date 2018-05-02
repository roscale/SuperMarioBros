from game.Resources import tileSizeNum
from gameengine.components.Physics import Physics
from gameengine.core.Script import Script
from gameengine.core.World import World


class FollowPlayer(Script):
	def init(self, rightLimit):
		self.rightLimit = rightLimit

	def onLateUpdate(self):
		if not self.enabled:
			return

		players = World.findByTag("Player")
		if not players:
			return

		player = players[0]

		cameraPos = self.gameObject.transform.position
		playerPos = player.transform.position

		# Forward only
		nextPos = playerPos.x - World.window.width / 10
		if nextPos > cameraPos.x:
			cameraPos.x = nextPos

		# Left limit
		if cameraPos.x < -8:
			cameraPos.x = -8

		elif cameraPos.x > tileSizeNum * self.rightLimit - 8:
			cameraPos.x = tileSizeNum * self.rightLimit - 8

		# Block player going out of the camera on the left
		if playerPos.x < cameraPos.x:
			playerPos.x = cameraPos.x
			player.getComponent(Physics).velocity.x = 0


class DestroyOutOfWorld(Script):
	def onUpdate(self):
		if self.gameObject.transform.position.y < 0:
			World.destroy(self.gameObject)