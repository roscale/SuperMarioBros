from pyglet import image
from pyglet.image import AbstractImage, Animation, pyglet

from gameengine.util.Vector2 import Vector2

def getRegion(image: AbstractImage, x, y, size: Vector2) -> AbstractImage:
	image = image.get_region(x, int(image.height - size.y - y), *size.toIntTuple())
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return image


tileSize = Vector2(16, 16)
tileSizeNum = 16

def setBgMusic(res):
	if Resources.bgMusic is not None:
		Resources.bgMusic.pause()

	looper = pyglet.media.SourceGroup(res.audio_format, None)
	looper.loop = True
	looper.queue(res)

	Resources.bgMusic = pyglet.media.Player()
	Resources.bgMusic.queue(looper)
	Resources.bgMusic.volume = 0.15

	return Resources.bgMusic


class Resources:
	pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
	audioPath = "res/audio/"

	owMusic = pyglet.media.load(audioPath + "ow.wav", streaming=False)
	owMusicFast = pyglet.media.load(audioPath + "ow_fast.wav", streaming=False)
	ugMusic = pyglet.media.load(audioPath + "ug.wav", streaming=False)
	ugMusicFast = pyglet.media.load(audioPath + "ug_fast.wav", streaming=False)
	jumpSmall = pyglet.media.load(audioPath + "jump_small.wav", streaming=False)
	jumpSuper = pyglet.media.load(audioPath + "jump_super.wav", streaming=False)
	breakblock = pyglet.media.load(audioPath + "breakblock.wav", streaming=False)

	stomp = pyglet.media.load(audioPath + "stomp.wav", streaming=False)
	kick = pyglet.media.load(audioPath + "kick.wav", streaming=False)
	bump = pyglet.media.load(audioPath + "bump.wav", streaming=False)

	coin = pyglet.media.load(audioPath + "coin.wav", streaming=False)
	fireball = pyglet.media.load(audioPath + "fireball.wav", streaming=False)

	powerupAppears = pyglet.media.load(audioPath + "powerup_appears.wav", streaming=False)
	powerup = pyglet.media.load(audioPath + "powerup.wav", streaming=False)
	powerdown = pyglet.media.load(audioPath + "powerdown.wav", streaming=False)

	flagpole = pyglet.media.load(audioPath + "flagpole.wav", streaming=False)

	mariodie = pyglet.media.load(audioPath + "mariodie.wav", streaming=False)
	hurryUp = pyglet.media.load(audioPath + "hurry_up.wav", streaming=False)

	bgMusic = None

	###

	spritesPath = "res/sprites/"

	playerSmallSize = Vector2(16, 16)
	playerBigSize = Vector2(16, 32)
	enemySmallSize = Vector2(16, 16)
	enemyBigSize = Vector2(16, 24)
	fireBallSize = Vector2(8, 8)
	fireBallExplosionSize = Vector2(16, 16)
	powerUpSize = Vector2(16, 16)


	bg = image.load(spritesPath + "bgLevel1-1.png")
	player = image.load(spritesPath + "player.png")

	tileset = image.load(spritesPath + "tileset.png")
	items = image.load(spritesPath + "items.png")
	misc = image.load(spritesPath + "misc.png")
	castle = image.load(spritesPath + "castle.png")
	enemies = image.load(spritesPath + "enemies.png")

	platform = image.load(spritesPath + "platform.png")

	theme = {
		"ow": {
			"ground": getRegion(tileset, 0, 0, tileSize),
			"brick": getRegion(tileset, 0 + tileSizeNum, 0, tileSize),
			"brickPieces": [
				getRegion(misc, 304, 112 + 8, Vector2(8, 8)),
				getRegion(misc, 304 + 8, 112 + 8, Vector2(8, 8)),
				getRegion(misc, 304, 112, Vector2(8, 8)),
				getRegion(misc, 304 + 8, 112, Vector2(8, 8)),
			],
			"hardBlock": getRegion(tileset, 0, 16, tileSize),
			"questionBlock": Animation.from_image_sequence([
				getRegion(tileset, 384, 0, tileSize),
				getRegion(tileset, 384 + tileSizeNum, 0, tileSize),
				getRegion(tileset, 384 + 2 * tileSizeNum, 0, tileSize),
				getRegion(tileset, 384 + tileSizeNum, 0, tileSize),
				getRegion(tileset, 384, 0, tileSize),
				getRegion(tileset, 384, 0, tileSize)
			], 0.125),
			"questionBlockHit": getRegion(tileset, 432, 0, tileSize),
			"coin": Animation.from_image_sequence([
				getRegion(items, 0, 96, powerUpSize),
				getRegion(items, 16, 96, powerUpSize),
				getRegion(items, 32, 96, powerUpSize),
				getRegion(items, 16, 96, powerUpSize),
				getRegion(items, 0, 96, powerUpSize),
				getRegion(items, 0, 96, powerUpSize)
			], 0.125),
			"pillar": getRegion(tileset, 80, 16, tileSize),
			"grassLeft": getRegion(tileset, 80, 128, tileSize),
			"grassMiddle": getRegion(tileset, 96, 128, tileSize),
			"grassRight": getRegion(tileset, 112, 128, tileSize),

			###

			"goombaWalking": Animation.from_image_sequence([
				getRegion(enemies, 0, 16, enemySmallSize),
				getRegion(enemies, 16, 16, enemySmallSize)
			], 0.20),
			"goombaSmashed": getRegion(enemies, 32, 16, enemySmallSize),
			"goombaFlipped": getRegion(enemies, 0, 16, enemySmallSize),

			"green": {
				"koopaTroopaWalking": Animation.from_image_sequence([
					getRegion(enemies, 96, 8, enemyBigSize),
					getRegion(enemies, 112, 8, enemyBigSize)
				], 0.25),
				"koopaTroopaStomped": getRegion(enemies, 160, 16, enemySmallSize),
				"koopaTroopaRecovering": Animation.from_image_sequence([
					getRegion(enemies, 160, 16, enemySmallSize),
					getRegion(enemies, 176, 16, enemySmallSize)
				], 0.25),
			},

			"red": {
				"koopaTroopaWalking": Animation.from_image_sequence([
					getRegion(enemies, 96, 8 + 64, enemyBigSize),
					getRegion(enemies, 112, 8 + 64, enemyBigSize)
				], 0.25),
				"koopaTroopaStomped": getRegion(enemies, 160, 16 + 64, enemySmallSize),
				"koopaTroopaRecovering": Animation.from_image_sequence([
					getRegion(enemies, 160, 16 + 64, enemySmallSize),
					getRegion(enemies, 176, 16 + 64, enemySmallSize)
				], 0.25),
			},

			"piranhaPlant": Animation.from_image_sequence([
				getRegion(enemies, 192, 8, enemyBigSize),
				getRegion(enemies, 192 + 16, 8, enemyBigSize),
			], 0.25),

			###

			"vPipeHead": getRegion(tileset, 0, 128, Vector2(32, 16)),
			"vPipeBody": getRegion(tileset, 2, 144, Vector2(28, 16)),
			"hPipeHead": getRegion(tileset, 32, 128, Vector2(16, 32)),
			"hPipeBody": getRegion(tileset, 48, 129, Vector2(16, 30)),
			"hPipeConnection": getRegion(tileset, 64, 128, Vector2(16, 32)),

			###

			"flagPoleBody": getRegion(tileset, 256, 144, tileSize),
			"flagPoleHead": getRegion(tileset, 256, 128, tileSize),
			"flag": getRegion(items, 128, 32, tileSize),

			###

			"superMushroom": getRegion(items, 0, 0, powerUpSize),
			"oneUp": getRegion(items, 16, 0, powerUpSize),

			"fireFlower": Animation.from_image_sequence([
				getRegion(items, 0, 32, powerUpSize),
				getRegion(items, 16, 32, powerUpSize),
				getRegion(items, 32, 32, powerUpSize),
				getRegion(items, 48, 32, powerUpSize)
			], 0.02),
			"superStar": Animation.from_image_sequence([
				getRegion(items, 0, 48, powerUpSize),
				getRegion(items, 16, 48, powerUpSize),
				getRegion(items, 32, 48, powerUpSize),
				getRegion(items, 48, 48, powerUpSize)
			], 0.02)
		},

		"ug": {
			"ground": getRegion(tileset, 0, 0+32, tileSize),
			"brick": getRegion(tileset, 16 + tileSizeNum, 0+32, tileSize),
			"brickPieces": [
				getRegion(misc, 304, 112 + 16 + 8, Vector2(8, 8)),
				getRegion(misc, 304 + 8, 112 + 16 + 8, Vector2(8, 8)),
				getRegion(misc, 304, 112 + 16, Vector2(8, 8)),
				getRegion(misc, 304 + 8, 112 + 16, Vector2(8, 8)),
			],
			"hardBlock": getRegion(tileset, 0, 16+32, tileSize),
			"questionBlock": Animation.from_image_sequence([
				getRegion(tileset, 384, 0+32, tileSize),
				getRegion(tileset, 384 + tileSizeNum, 0+32, tileSize),
				getRegion(tileset, 384 + 2 * tileSizeNum, 0+32, tileSize),
				getRegion(tileset, 384 + tileSizeNum, 0+32, tileSize),
				getRegion(tileset, 384, 0+32, tileSize),
				getRegion(tileset, 384, 0+32, tileSize)
			], 0.125),
			"questionBlockHit": getRegion(tileset, 432, 0+32, tileSize),
			"coin": Animation.from_image_sequence([
				getRegion(items, 144, 96, powerUpSize),
				getRegion(items, 160, 96, powerUpSize),
				getRegion(items, 176, 96, powerUpSize),
				getRegion(items, 160, 96, powerUpSize),
				getRegion(items, 144, 96, powerUpSize),
				getRegion(items, 144, 96, powerUpSize)
			], 0.125),

			###

			"goombaWalking": Animation.from_image_sequence([
				getRegion(enemies, 0, 16 + 32, enemySmallSize),
				getRegion(enemies, 16, 16 + 32, enemySmallSize)
			], 0.20),
			"goombaSmashed": getRegion(enemies, 32, 16 + 32, enemySmallSize),
			"goombaFlipped": getRegion(enemies, 0, 16 + 32, enemySmallSize),

			"green": {
				"koopaTroopaWalking": Animation.from_image_sequence([
					getRegion(enemies, 96, 8 + 32, enemyBigSize),
					getRegion(enemies, 112, 8 + 32, enemyBigSize)
				], 0.25),
				"koopaTroopaStomped": getRegion(enemies, 160, 16 + 32, enemySmallSize),
				"koopaTroopaRecovering": Animation.from_image_sequence([
					getRegion(enemies, 160, 16 + 32, enemySmallSize),
					getRegion(enemies, 176, 16 + 32, enemySmallSize)
				], 0.25),
			},

			"red": {
				"koopaTroopaWalking": Animation.from_image_sequence([
					getRegion(enemies, 96, 8 + 64, enemyBigSize),
					getRegion(enemies, 112, 8 + 64, enemyBigSize)
				], 0.25),
				"koopaTroopaStomped": getRegion(enemies, 160, 16 + 64, enemySmallSize),
				"koopaTroopaRecovering": Animation.from_image_sequence([
					getRegion(enemies, 160, 16 + 64, enemySmallSize),
					getRegion(enemies, 176, 16 + 64, enemySmallSize)
				], 0.25),
			},

			"piranhaPlant": Animation.from_image_sequence([
				getRegion(enemies, 192, 8 + 32, enemyBigSize),
				getRegion(enemies, 192 + 16, 8 + 32, enemyBigSize),
			], 0.25),


			###

			"vPipeHead": getRegion(tileset, 0, 128+32, Vector2(32, 16)),
			"vPipeBody": getRegion(tileset, 2, 144+32, Vector2(28, 16)),
			"hPipeHead": getRegion(tileset, 32, 128+32, Vector2(16, 32)),
			"hPipeBody": getRegion(tileset, 48, 129+32, Vector2(16, 30)),
			"hPipeConnection": getRegion(tileset, 64, 128+32, Vector2(16, 32)),

			###

			"flagPoleBody": getRegion(tileset, 256, 144+32, tileSize),
			"flagPoleHead": getRegion(tileset, 256, 128+32, tileSize),
			"flag": getRegion(items, 272, 32, tileSize),
		},

		"castle": {
			"ground": getRegion(tileset, 32, 80, tileSize),
		}
	}

	redKoopaTroopaWalking = Animation.from_image_sequence([
		getRegion(enemies, 96, 8 + 32, enemyBigSize),
		getRegion(enemies, 112, 8 + 32, enemyBigSize)
	], 0.25)
	redKoopaTroopaStomped = getRegion(enemies, 160, 16 + 32, enemySmallSize)
	redKoopaTroopaRecovering = Animation.from_image_sequence([
		getRegion(enemies, 160, 16 + 32, enemySmallSize),
		getRegion(enemies, 176, 16 + 32, enemySmallSize)
	], 0.25)

	fireBall = Animation.from_image_sequence([
		getRegion(items, 96, 144, fireBallSize),
		getRegion(items, 104, 144, fireBallSize),
		getRegion(items, 96, 152, fireBallSize),
		getRegion(items, 104, 152, fireBallSize),
	], 0.05)

	fireBallExplosion = Animation.from_image_sequence([
		getRegion(items, 112, 144, fireBallExplosionSize),
		getRegion(items, 112, 160, fireBallExplosionSize),
		getRegion(items, 112, 176, fireBallExplosionSize),
	], 0.02, False)

	rotatingCoin = Animation.from_image_sequence([
		getRegion(items, 0, 112, tileSize),
		getRegion(items, 0 + tileSizeNum, 112, tileSize),
		getRegion(items, 0 + 2 * tileSizeNum, 112, tileSize),
		getRegion(items, 0 + 3 * tileSizeNum, 112, tileSize),
	], 0.05)

	playerSprites = {
		"mario": {
			"small": {
				"stand": getRegion(player, 80, 34, playerSmallSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 34, playerSmallSize),
					getRegion(player, 114, 34, playerSmallSize),
					getRegion(player, 131, 34, playerSmallSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 34, playerSmallSize),
					getRegion(player, 114, 34, playerSmallSize),
					getRegion(player, 131, 34, playerSmallSize), ], 0.05),
				"break": getRegion(player, 148, 34, playerSmallSize),
				"jump": getRegion(player, 165, 34, playerSmallSize),
				"crouch": getRegion(player, 80, 34, playerSmallSize),
				"die": getRegion(player, 182, 34, playerSmallSize)
			},

			"big": {
				"stand": getRegion(player, 80, 1, playerBigSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 1, playerBigSize),
					getRegion(player, 114, 1, playerBigSize),
					getRegion(player, 131, 1, playerBigSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 1, playerBigSize),
					getRegion(player, 114, 1, playerBigSize),
					getRegion(player, 131, 1, playerBigSize), ], 0.05),
				"break": getRegion(player, 148, 1, playerBigSize),
				"jump": getRegion(player, 165, 1, playerBigSize),
				"crouch": getRegion(player, 182, 1, playerBigSize)
			}
		},

		"luigi": {
			"small": {
				"stand": getRegion(player, 80, 99, playerSmallSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 99, playerSmallSize),
					getRegion(player, 114, 99, playerSmallSize),
					getRegion(player, 131, 99, playerSmallSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 99, playerSmallSize),
					getRegion(player, 114, 99, playerSmallSize),
					getRegion(player, 131, 99, playerSmallSize), ], 0.05),
				"break": getRegion(player, 148, 99, playerSmallSize),
				"jump": getRegion(player, 165, 99, playerSmallSize),
				"crouch": getRegion(player, 80, 99, playerSmallSize),
				"die": getRegion(player, 182, 99, playerSmallSize)
			},

			"big": {
				"stand": getRegion(player, 80, 66, playerBigSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 66, playerBigSize),
					getRegion(player, 114, 66, playerBigSize),
					getRegion(player, 131, 66, playerBigSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 66, playerBigSize),
					getRegion(player, 114, 66, playerBigSize),
					getRegion(player, 131, 66, playerBigSize), ], 0.05),
				"break": getRegion(player, 148, 66, playerBigSize),
				"jump": getRegion(player, 165, 66, playerBigSize),
				"crouch": getRegion(player, 182, 66, playerBigSize)
			}
		},

		"fire": {
			"stand": getRegion(player, 80, 129, playerBigSize),
			"walk": Animation.from_image_sequence([
				getRegion(player, 97, 129, playerBigSize),
				getRegion(player, 114, 129, playerBigSize),
				getRegion(player, 131, 129, playerBigSize),
			], 0.1),
			"run": Animation.from_image_sequence([
				getRegion(player, 97, 129, playerBigSize),
				getRegion(player, 114, 129, playerBigSize),
				getRegion(player, 131, 129, playerBigSize),
			], 0.05),
			"break": getRegion(player, 148, 129, playerBigSize),
			"jump": getRegion(player, 165, 129, playerBigSize),
			"crouch": getRegion(player, 182, 129, playerBigSize)
		},

		"invincible": {
			"small": {
				"stand": getRegion(player, 80, 225, playerSmallSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 225, playerSmallSize),
					getRegion(player, 114, 225, playerSmallSize),
					getRegion(player, 131, 225, playerSmallSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 225, playerSmallSize),
					getRegion(player, 114, 225, playerSmallSize),
					getRegion(player, 131, 225, playerSmallSize), ], 0.05),
				"break": getRegion(player, 148, 225, playerSmallSize),
				"jump": getRegion(player, 165, 225, playerSmallSize),
				"crouch": getRegion(player, 80, 225, playerSmallSize),
			},

			"big": {
				"stand": getRegion(player, 80, 192, playerBigSize),
				"walk": Animation.from_image_sequence([
					getRegion(player, 97, 192, playerBigSize),
					getRegion(player, 114, 192, playerBigSize),
					getRegion(player, 131, 192, playerBigSize), ], 0.1),
				"run": Animation.from_image_sequence([
					getRegion(player, 97, 192, playerBigSize),
					getRegion(player, 114, 192, playerBigSize),
					getRegion(player, 131, 192, playerBigSize), ], 0.05),
				"break": getRegion(player, 148, 192, playerBigSize),
				"jump": getRegion(player, 165, 192, playerBigSize),
				"crouch": getRegion(player, 182, 192, playerBigSize)
			}
		}
	}

	castle1 = getRegion(castle, 0, 0, Vector2(47, 80))
	castle2 = getRegion(castle, 48, 0, Vector2(32, 80))


