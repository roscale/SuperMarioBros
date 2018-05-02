from abc import ABC, abstractmethod


class IOrderable(ABC):
	@property
	@abstractmethod
	def order(self) -> int:
		pass

	@order.setter
	@abstractmethod
	def order(self, val):
		pass