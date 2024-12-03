from PyQt5.QtGui import QVector2D

from core import Image

class Obstacle(object):
	def __init__(self, image: Image, blockingAttacks: bool, position: QVector2D):
		self.sprite = image
		self.isBlockingAttacks = blockingAttacks
		self.position = position