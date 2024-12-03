from PyQt5.QtGui import QVector2D

from constants import GRID_SIZE

from typing import List, Any

class WorldGrid(object):
	def __init__(self):
		self.grid = [[None for column in range(GRID_SIZE)] for row in range(GRID_SIZE)]

	def addEntity(self, entity, position: QVector2D) -> None:
		self.grid[int(position.y())][int(position.x())] = entity

	def addEntities(self, entities: List[Any]) -> None:
		for entity in entities:
			self.addEntity(entity, entity.position)

	def getCell(self, position: QVector2D) -> Any:
		return self.grid[int(position.y())][int(position.x())]
