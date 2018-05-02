class IEvents:
	def onUpdate(self):
		pass

	def onLateUpdate(self):
		pass

	# Input
	def onMouseMotion(self, x, y, dx, dy):
		pass

	def onMousePress(self, x, y, button, modifiers):
		pass

	def onMouseRelease(self, x, y, button, modifiers):
		pass

	def onMouseDrag(self, x, y, dx, dy, buttons, modifiers):
		pass

	def onMouseScroll(self, x, y, scroll_x, scroll_y):
		pass

	def onKeyPress(self, symbol, modifiers):
		pass

	def onKeyRelease(self, symbol, modifiers):
		pass

	# Collision
	def onCollisionEnter(self, other, side):
		pass

	def onCollisionStay(self, other):
		pass

	def onCollisionExit(self, other):
		pass