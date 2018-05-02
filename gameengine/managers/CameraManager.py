from gameengine.core.Camera import Camera
from gameengine.managers.Manager import Manager
from gameengine.util.Singleton import Singleton


@Singleton
class CameraManager(Manager[Camera]):
	def _byOrder(self, camera):
		return camera.order

	def sortByOrder(self):
		self.collection.sort(key=self._byOrder, reverse=True)

	def collectionChanged(self):
		self.sortByOrder()

