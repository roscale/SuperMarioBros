from queue import PriorityQueue

from typing import TypeVar, Generic, List

from gameengine.components.Collider import Collider
from gameengine.managers.Manager import Manager
from gameengine.util.Rect import Rect
from gameengine.util.Singleton import Singleton
from gameengine.util.pyqtree import Index


class Sides:
	TOP_SIDE = 1
	LEFT_SIDE = 2
	RIGHT_SIDE = 3
	BOTTOM_SIDE = 4
	TOTAL_SIDES = 5


def vecToSide(dx: float, dy: float) -> int:
	if dx < 0:
		return Sides.LEFT_SIDE
	elif dx > 0:
		return Sides.RIGHT_SIDE
	if dy > 0:
		return Sides.TOP_SIDE
	elif dy < 0:
		return Sides.BOTTOM_SIDE


def clampOff(thisRect: Rect, otherRect: Rect, side):
	if side == Sides.TOP_SIDE:
		thisRect.bottom = otherRect.top
	elif side == Sides.RIGHT_SIDE:
		thisRect.right = otherRect.left
	elif side == Sides.BOTTOM_SIDE:
		thisRect.top = otherRect.bottom
	elif side == Sides.LEFT_SIDE:
		thisRect.left = otherRect.right


class ColliderMovement:
	def __init__(self, collider, dx: float, dy: float):
		self.collider = collider
		self.dx = dx
		self.dy = dy

	# One has higher priority than the other if it has bigger movement
	# TODO: Player dies running into KoopaTroopa
	def __lt__(self, other):
		return self.dx ** 2 + self.dy ** 2 > other.dx ** 2 + other.dy ** 2


T = TypeVar("T")


class Pair(Generic[T]):
	def __init__(self, first: T, second: T):
		self.first: T = first
		self.second: T = second

	def contains(self, item: T):
		return item == self.first or item == self.second

	def other(self, item: T):
		if item == self.first:
			return self.second
		elif item == self.second:
			return self.first

	def __eq__(self, other):
		return (self.first == other.first and self.second == other.second) or \
		       (self.first == other.second and self.second == other.first)

	def __str__(self):
		return "Pair: {} {}".format(self.first, self.second)


@Singleton
class CollisionManager(Manager[Collider]):
	def __init__(self):
		super().__init__()
		self.quadtree = Index((0, 0, 5000, 5000))
		self.movementQueue = PriorityQueue()

		self.justEntered: List[Pair[Collider]] = []
		self.stayPairs: List[Pair[Collider]] = []

	def add(self, object: Collider):
		super().add(object)
		self.quadtree.insert(object, (*object.rect.topLeft, *(object.rect.topLeft + object.rect.size)))

	def remove(self, object: Collider):
		super().remove(object)
		self.quadtree.remove(object, (*object.rect.topLeft, *(object.rect.topLeft + object.rect.size)))

		for pair in self.justEntered[:]:
			if pair.contains(object):
				self.justEntered.remove(pair)

		for pair in self.stayPairs[:]:
			if pair.contains(object):
				self.stayPairs.remove(pair)

	def queueMovement(self, collider, dx, dy):
		self.movementQueue.put(ColliderMovement(collider, dx, dy))

	def onUpdate(self, dt: float):
		evaluatedStayPairs: List[Pair[Collider]] = []

		while not self.movementQueue.empty():
			movement: ColliderMovement = self.movementQueue.get()

			rectBefore = movement.collider.rect.copy()
			rectAfter = rectBefore.copy()
			rectAfter.move(movement.dx, movement.dy)

			newPossibleCollisions: List[Collider] = self.quadtree.intersect(bbox=rectAfter.bbox())

			# Remove yourself
			if movement.collider in newPossibleCollisions:
				newPossibleCollisions.remove(movement.collider)

			self.resolveCollision(movement.collider, rectBefore, newPossibleCollisions, movement.dx, movement.dy)
			clampedRect = rectBefore

			#####

			intersection: List[Collider] = self.quadtree.intersect(bbox=clampedRect.bbox())

			# Remove yourself
			if movement.collider in intersection:
				intersection.remove(movement.collider)

			for other in intersection:
				pair = Pair(movement.collider, other)

				if pair in evaluatedStayPairs:
					continue

				if pair not in self.justEntered:
					def dispatchStayCollision(collider, other):
						for script in collider.gameObject.scripts:
							script.onCollisionStay(other.gameObject)
						for script in other.gameObject.scripts:
							script.onCollisionStay(collider.gameObject)

						collider.isColliding = True
						other.isColliding = True

					dispatchStayCollision(pair.first, pair.second)
					evaluatedStayPairs.append(pair)

			exitPairs = [pair for pair in self.stayPairs if
			             pair.contains(movement.collider) and pair.other(movement.collider) not in intersection]

			for pair in exitPairs:
				def dispatchExitCollision(collider, other):
					for script in collider.gameObject.scripts:
						script.onCollisionExit(other.gameObject)
					for script in other.gameObject.scripts:
						script.onCollisionExit(collider.gameObject)

				dispatchExitCollision(pair.first, pair.second)
				self.stayPairs.remove(pair)

			self.justEntered.clear()

			movement.collider.gameObject.transform.position = rectBefore.topLeft - movement.collider.offset

	def resolveCollision(self, collider, rect, possibleCollisions, dx=0, dy=0):
		if dx == 0 and dy == 0:
			return

		if dx != 0 and dy != 0:
			self.resolveCollision(collider, rect, possibleCollisions, dx, 0)
			self.resolveCollision(collider, rect, possibleCollisions, 0, dy)
			return

		rect.move(dx, dy)

		colliding = []
		side = vecToSide(dx, dy)

		# Filter on each axes
		for other in possibleCollisions:
			otherRect = other.rect

			if rect.collideRect(otherRect):
				colliding.append(other)

		def dispatchEnterCollision(collider, other, side):
			for script in collider.gameObject.scripts:
				script.onCollisionEnter(other.gameObject, side)
			for script in other.gameObject.scripts:
				script.onCollisionEnter(collider.gameObject, Sides.TOTAL_SIDES - side)

			collider.isColliding = True
			other.isColliding = True

		for other in colliding:
			from gameengine.core.World import World

			pair = Pair(collider, other)

			if pair not in self.stayPairs:
				dispatchEnterCollision(collider, other, side)

				if World._collisionListener(collider.gameObject, other.gameObject, side):
					from gameengine.components.Physics import Physics

					try:
						thisMass = collider.gameObject.getComponent(Physics).mass
						otherMass = other.gameObject.getComponent(Physics).mass

						if thisMass <= otherMass:
							clampOff(rect, other.rect, side)

						else:
							clampOff(other.rect, rect, Sides.TOTAL_SIDES - side)

					except AttributeError:
						clampOff(rect, other.rect, side)

				else:
					if pair not in self.justEntered:
						self.justEntered.append(pair)

					if pair not in self.stayPairs:
						self.stayPairs.append(pair)