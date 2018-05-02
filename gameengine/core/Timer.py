import time
from abc import ABC

from typing import Callable, Tuple, List, NewType


def getMillis() -> int:
	return int(time.time() * 1000)


Id = NewType("Id", int)
class IDGenerator:
	id = -1

	@classmethod
	def next(cls) -> Id:
		cls.id += 1
		return cls.id


class Entry:
	def __init__(self, callback: Callable[..., None], args, startDelay, interval, cycles):
		self.callback = callback
		self.args: tuple = args
		self.startDelay = startDelay
		self.interval = interval
		self.cycles = cycles

		self.currentCycle = 0
		self.previous = getMillis()

	def execute(self):
		self.callback(*self.args)

		self.currentCycle += 1
		self.previous = getMillis()


class Timer(ABC):
	pairs: List[Tuple[id, Entry]] = []

	@classmethod
	def add(cls, callback: Callable[..., None], args, startDelay, interval, cycles) -> Id:
		entry = Entry(callback, args, startDelay, interval, cycles)
		id = IDGenerator.next()

		cls.pairs.append((id, entry))
		return id

	@classmethod
	def remove(cls, id) -> bool:
		for i, entry in enumerate(cls.pairs):
			if id == entry[0]:
				del cls.pairs[i]
				return True
		return False

	@classmethod
	def tick(cls):
		for i, (id, entry) in enumerate(cls.pairs):
			# -1 never ends
			if entry.cycles != -1 and entry.currentCycle >= entry.cycles:
				del cls.pairs[i]
				continue

			# start delay
			if entry.currentCycle == 0:
				if getMillis() - entry.previous >= entry.startDelay:
					entry.execute()

			# interval
			else:
				if getMillis() - entry.previous >= entry.interval:
					entry.execute()