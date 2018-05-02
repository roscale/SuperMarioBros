from gameengine.core.GameObject import GameObject
from gameengine.core.World import World

World.init("instantiation", True, 800, 600)


class MyGameObject(GameObject):
	def __init__(self):
		super().__init__()

go = World.instantiate(MyGameObject, (), (0, 0))
go.transform.translate((0.1, 0.1))

World.instantiate(MyGameObject, (100, 100))
World.instantiate(MyGameObject, (1234, -1234))

print(World.gameObjects)
for gameObject in World.gameObjects:
	print(gameObject, gameObject.transform.position)

World.run()