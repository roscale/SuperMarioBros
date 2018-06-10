from game.levels.GameOverSplash import GameOverSplash
from game.levels.LevelDeniss import *
from game.levels.Level1_1 import Level1_1
from game.levels.Level1_2 import Level1_2
from game.levels.Level1_3 import Level1_3
from game.levels.Level1_4 import Level1_4
from game.levels.LevelSplash import LevelSplash
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager

World.init("Super Mario Bros", True, 1296, 720)

SceneManager().loadScene(LevelSplash, Level1_1, 1, 1)

World.run()