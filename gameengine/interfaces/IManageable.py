from abc import ABC, abstractmethod

from typing import List

from gameengine.managers.Manager import Manager


class IManageable(ABC):
	@property
	@abstractmethod
	def managers(self) -> List[Manager]:
		pass