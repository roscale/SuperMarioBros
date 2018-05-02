from gameengine.components.Collider import Collider
from gameengine.core.GameObject import GameObject
from gameengine.core.Script import Script
from gameengine.core.World import World


class Trigger(GameObject):
	def init(self, size, tagTrigger, callback):
		self.addComponent(Collider).size = size

		self.tagTrigger = tagTrigger
		self.callback = callback

		self.addScript(self.TriggerScript)


	class TriggerScript(Script):
		def onCollisionEnter(self, other, side):
			if self.gameObject.tagTrigger in other.tags:
				self.gameObject.callback()

				World.destroy(self.gameObject)