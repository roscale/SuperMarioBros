from gameengine.core.Timer import Timer

from time import sleep


def fun1(text):
	print(text)

t1 = Timer.add(fun1, ("1"), 1000, 500, 3)
t2 = Timer.add(fun1, ("2"), 750, 500, -1)
t3 = Timer.add(fun1, ("3"), 100, 1000, 1)
t4 = Timer.add(fun1, ("2"), 750, 500, -1)

Timer.remove(t4)

while True:
	Timer.tick()

	sleep(0.01)
