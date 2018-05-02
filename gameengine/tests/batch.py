import pyglet
from pyglet.graphics import Batch

image = pyglet.image.load("image.png")

game_window = pyglet.window.Window(800, 600, fullscreen=False, vsync=False)



fps_display = pyglet.window.FPSDisplay(game_window)

batchUnused = Batch()
batch = Batch()

sprites = []

for i in range(1000):
	sprite = pyglet.sprite.Sprite(img=image, batch=batchUnused, x=100, y=100)
	sprites.append(sprite)
	sprite.batch = batch


@game_window.event
def on_draw():
	game_window.clear()
	batch.draw()
	fps_display.draw()

def on_update(dt):
	pass

if __name__ == '__main__':
	pyglet.clock.schedule_interval(on_update, 1 / 99999)
	pyglet.app.run()
