from gameengine.core.World import World

World.init("windowing", False, 800, 600)
World.maxFps = 100

World.run()