from abc import ABC
from queue import Queue
from typing import TypeVar, Type, Set, List

import pyglet
from pyglet.gl import glEnable, GL_BLEND, GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA, glBlendFunc, glAlphaFunc
from pyglet.window import key

from gameengine.core.GameObject import GameObject
from gameengine.core.Timer import Timer


class World(ABC):
	window: pyglet.window.Window = None
	fps_display: pyglet.window.FPSDisplay = None
	maxFps = 9999
	dt = 0.016
	frameCount = 0

	keys = key.KeyStateHandler()

	gameObjects: Set[GameObject] = set()
	callableQueue = Queue()



	@classmethod
	def init(cls, caption: str, vsync: bool, w: int, h: int):
		cls.window = pyglet.window.Window(caption=caption, vsync=vsync, width=w, height=h)
		cls.window.push_handlers(cls.keys)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glEnable(pyglet.gl.GL_ALPHA_TEST)
		glAlphaFunc(pyglet.gl.GL_GREATER, .1)

		cls.window.on_draw = cls.on_draw

		from gameengine.managers.InputManager import InputManager
		cls.window.on_mouse_motion = InputManager().on_mouse_motion
		cls.window.on_mouse_press = InputManager().on_mouse_press
		cls.window.on_mouse_release = InputManager().on_mouse_release
		cls.window.on_mouse_drag = InputManager().on_mouse_drag
		cls.window.on_mouse_scroll = InputManager().on_mouse_scroll

		cls.window.on_key_press = InputManager().on_key_press
		cls.window.on_key_release = InputManager().on_key_release

		cls.fps_display = pyglet.window.FPSDisplay(cls.window)

	@classmethod
	def run(cls):
		pyglet.clock.schedule_interval(cls.on_update, 1 / cls.maxFps)
		pyglet.app.run()

	# Decorator
	class collisionListener:
		def __init__(self, f):
			self.f = f
			World._collisionListener = f

		def __call__(self, *args, **kwargs):
			self.f(*args, **kwargs)

	@classmethod
	def _collisionListener(cls, this: GameObject, other: GameObject, side) -> bool:
		return True

	@classmethod
	def on_update(cls, dt: float):
		cls.dt = dt

		while not cls.callableQueue.empty():
			callable = cls.callableQueue.get()
			callable()

		for gameObject in cls.gameObjects:
			for script in gameObject.scripts:
				script.onUpdate()

		from gameengine.managers.CameraManager import CameraManager
		for camera in CameraManager().collection:
			for script in camera.scripts:
				script.onUpdate()

		from gameengine.managers.PhysicsManager import PhysicsManager
		PhysicsManager().onUpdate(dt)

		from gameengine.managers.CollisionManager import CollisionManager
		CollisionManager().onUpdate(dt)

		Timer.tick()

		for gameObject in cls.gameObjects.copy():
			for script in gameObject.scripts:
				script.onLateUpdate()

		from gameengine.managers.CameraManager import CameraManager
		for camera in CameraManager().collection:
			for script in camera.scripts:
				script.onLateUpdate()

		cls.frameCount += 1

	@classmethod
	def on_draw(cls):
		cls.window.clear()

		from gameengine.managers.DrawingManager import DrawingManager
		DrawingManager().draw()

		cls.fps_display.draw()

	@classmethod
	def findByTag(cls, tag: str) -> List[GameObject]:
		found: List[GameObject] = []
		for gameObject in cls.gameObjects:
			if tag in gameObject.tags:
				found.append(gameObject)
		return found

	GO = TypeVar("GameObject")
	@classmethod
	def instantiate(cls, Class: Type[GO], position: tuple, *args, **kwargs) -> GO:
		if isinstance(Class, type):
			gameObject = Class()
			gameObject.transform.position.set(position)
			gameObject.init(*args, **kwargs)

			cls.gameObjects.add(gameObject)
			return gameObject

	@classmethod
	def destroy(cls, gameObject, delay=0):
		def f():
			if gameObject not in cls.gameObjects:
				return

			gameObject.prepareDestroy()
			cls.gameObjects.remove(gameObject)

		if delay == 0:
			cls.callableQueue.put(f)
		else:
			Timer.add(cls.callableQueue.put, (f,), delay, 0, 1)
