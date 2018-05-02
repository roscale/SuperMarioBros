from typing import Dict, List, Callable

from abc import ABC


class EventBus(ABC):
	_handlers: Dict[str, List[Callable]] = {}

	@classmethod
	def addHandler(self, key, h):
		if key not in self._handlers.keys():
			self._handlers[key] = []

		exists = False
		for handler in self._handlers[key]:
			if handler == h:
				exists = True
				break

		if not exists:
			self._handlers[key].append(h)

	@classmethod
	def removeHandler(self, key, h):
		if key in self._handlers.keys():
			if h in self._handlers[key]:
				self._handlers[key].remove(h)

				if not self._handlers[key]:
					self._handlers.pop(key)

	@classmethod
	def clearHandlers(self):
		self._handlers = {}

	@classmethod
	def post(self, key, *args, **kwargs):
		if key in self._handlers.keys():
			for handler in self._handlers[key]:
				handler(*args, **kwargs)