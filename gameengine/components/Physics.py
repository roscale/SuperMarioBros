from gameengine.components.Component import Component
from gameengine.util.Vector2 import Vector2


class Physics(Component):
	def __init__(self):
		super().__init__()

		from gameengine.managers.PhysicsManager import PhysicsManager
		PhysicsManager().add(self)

		self.velocity = Vector2()
		self.acceleration = Vector2()
		self.drag = Vector2(1, 1)
		self.mass = 1.0

		self.customGravity: Vector2 = None

	def addForce(self, f):
		self.velocity += f

	def addAcceleration(self, a):
		self.acceleration += a

	def step(self, dt):
		self.velocity += self.acceleration
		self.velocity *= self.drag
		self.acceleration *= 0

		if self.velocity.x == 0 and self.velocity.y == 0:
			return

		from gameengine.components.Collider import Collider
		collider = self.gameObject.getComponent(Collider)
		if collider is not None:
			from gameengine.managers.CollisionManager import CollisionManager
			CollisionManager().queueMovement(self.gameObject.getComponent(Collider), *(self.velocity * dt))

		else:
			self.gameObject.transform.position += (self.velocity * dt)