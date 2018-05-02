from gameengine.components.Physics import Physics
from gameengine.managers.Manager import Manager
from gameengine.util.Singleton import Singleton
from gameengine.util.Vector2 import Vector2


@Singleton
class PhysicsManager(Manager[Physics]):
	def __init__(self):
		super().__init__()
		self.gravity = Vector2(0, -20)

	def onUpdate(self, dt):
		for component in self.collection:
			component.addAcceleration(component.customGravity if component.customGravity is not None else self.gravity)
			component.step(dt)