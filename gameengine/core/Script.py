from gameengine.interfaces.IEvents import IEvents
from gameengine.interfaces.IOrderable import IOrderable


class Script(IEvents, IOrderable):
	def __init__(self):
		self.gameObject = None
		self._order = 0

		self.enabled = True

	def attachGameObject(self, gameObject):
		self.gameObject = gameObject

	def init(self, *args, **kwargs):
		pass

	@property
	def order(self) -> int:
		return self._order

	@order.setter
	def order(self, val):
		self._order = val
		self.gameObject._sortScripts()

	@staticmethod
	def _byOrder(script):
		return script._order

	def onDestroy(self):
		pass