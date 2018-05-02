from gameengine.components.Input import Input
from gameengine.core.Camera import Camera
from gameengine.core.World import World
from gameengine.managers.CameraManager import CameraManager
from gameengine.managers.Manager import Manager
from gameengine.util.Rect import Rect
from gameengine.util.Singleton import Singleton
from gameengine.util.Vector2 import Vector2


@Singleton
class InputManager(Manager[Input]):
	def __init__(self):
		super().__init__()

		self.draggingInput = None

		# Fix dragging into another camera with another zoom level
		self.draggingInputCamera = None

	def _byOrder(self, input):
		return input._order

	def sortByOrder(self):
		self.collection.sort(key=self._byOrder)

	def collectionChanged(self):
		super().collectionChanged()
		self.sortByOrder()

	def on_mouse_motion(self, x, y, dx, dy):
		camera = self._getCameraAt(x, y)

		if camera is not None:
			worldCoords = camera.windowToWorldCoords(Vector2(x, y))
			scaledDelta = Vector2(dx, dy) / camera.zoom

			for input in self.collection:
				if input.rect.collidePoint(*worldCoords):
					for script in input.gameObject.scripts:
						script.onMouseMotion(*worldCoords, *scaledDelta)
					break


	def on_mouse_press(self, x, y, button, modifiers):
		camera = self._getCameraAt(x, y)

		if camera is not None:
			worldCoords = camera.windowToWorldCoords(Vector2(x, y))

			for input in self.collection:
				if input.rect.collidePoint(*worldCoords):
					self.draggingInput = input
					self.draggingInputCamera = camera

					for script in input.gameObject.scripts:
						print(button)
						script.onMousePress(*worldCoords, button, modifiers)
					break

	def on_mouse_release(self, x, y, button, modifiers):
		self.draggingInput = None
		self.draggingInputCamera = None

		camera = self._getCameraAt(x, y)

		if camera is not None:
			worldCoords = camera.windowToWorldCoords(Vector2(x, y))

			for input in self.collection:
				if input.rect.collidePoint(*worldCoords):
					for script in input.gameObject.scripts:
						script.onMouseRelease(*worldCoords, button, modifiers)
					break

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.draggingInput is not None and self.draggingInput.gameObject is not None:
			worldCoords = self.draggingInputCamera.windowToWorldCoords(Vector2(x, y))
			scaledDelta = Vector2(dx, dy) / self.draggingInputCamera.zoom

			for script in self.draggingInput.gameObject.scripts:
				script.onMouseDrag(*worldCoords, *scaledDelta, buttons, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		camera = self._getCameraAt(x, y)

		if camera is not None:
			worldCoords = camera.windowToWorldCoords(Vector2(x, y))

			for input in self.collection:
				if input.rect.collidePoint(*worldCoords):
					for script in input.gameObject.scripts:
						script.onMouseScroll(*worldCoords, scroll_x, scroll_y)
					break

	def on_key_press(self, symbol, modifiers):
		for gameObject in World.gameObjects.copy():
			for script in gameObject.scripts:
				script.onKeyPress(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		for gameObject in World.gameObjects.copy():
			for script in gameObject.scripts:
				script.onKeyRelease(symbol, modifiers)

	def _getCameraAt(self, x, y) -> Camera:
		for camera in CameraManager().collection:
			rect = Rect(*camera.windowPosition, *camera.size)

			if rect.collidePoint(x, y):
				return camera

		return None