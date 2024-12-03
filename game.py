from itertools import chain
from random import randint, sample
from typing import List, Optional

from PyQt5.QtGui import QVector2D

from constants import Sprite, GRID_SIZE
from core import GameAPI
from game_constants import MAX_OBSTACLE_NUMBER, MIN_OBSTACLE_NUMBER, Names, SquadInfo, CharacterTypes, GRID_LETTERS
from obstacle import Obstacle
from character import Character, Squad, CharacterFactory
from world_grid import WorldGrid


class Game(object):
	def __init__(self):
		self.worldGrid = WorldGrid()
		self.squadsInfo = [SquadInfo(Names.PURPLE_SQUAD, Names.PURPLE_SQUAD_CHARACTERS, Sprite.PURPLE_TEAM,
									 (CharacterTypes.rogue, CharacterTypes.ranger, CharacterTypes.mage)),
						   SquadInfo(Names.GREEN_SQUAD, Names.GREEN_SQUAD_CHARACTERS, Sprite.GREEN_TEAM,
									 (CharacterTypes.rogue, CharacterTypes.ranger, CharacterTypes.mage))]
		self.greenTeam = self.purpleTeam = self.activeTeam = None
		self.selectedCharacter = None
		self.isGameFinished = False
		self.canClick = True
		self.animFinishedCallback = None

	def start(self, api: GameAPI) -> None:
		api.addMessage('Game starts')

		squads = []
		self._buildSquads(squads, api)
		self.purpleTeam = squads[0]
		self.greenTeam = squads[1]
		self.activeTeam = self.greenTeam if randint(1,2) == 1 else self.purpleTeam

		obstacleNumber = randint(MIN_OBSTACLE_NUMBER, MAX_OBSTACLE_NUMBER)
		emptyCells = [index for index in range(GRID_SIZE * GRID_SIZE)]
		for character in chain(self.greenTeam.squad, self.purpleTeam.squad):
			emptyCells.remove(int(character.position.x()) + int(character.position.y()) * GRID_SIZE)
		obstacleCells = sample(emptyCells, obstacleNumber)
		obstacles = []
		self._createObstacles(obstacleCells, api, obstacles)

		entities = list(chain(self.greenTeam.squad, self.purpleTeam.squad, obstacles))
		self.worldGrid.addEntities(entities)
		api.addMessage('{} move first'.format(self.activeTeam.name))
		api.addMessage('-- -- {} -- --'.format(self.activeTeam.name))

	def click(self, api: GameAPI, x: int, y: int) -> None:
		if self.isGameFinished or not self.canClick:
			return
		if not self.canClick:
			return
		selectedPosition = QVector2D(x, y)
		selectedCell = self.worldGrid.getCell(selectedPosition)
		if self.selectedCharacter is None and type(selectedCell) is Character and selectedCell in self.activeTeam.squad:
			self._setSelectionStatus(selectedCell, True, selectedCell)
		elif self.selectedCharacter is not None and type(selectedCell) is Character and selectedCell is self.selectedCharacter:
			self._setSelectionStatus(selectedCell, False, None)
		elif self.selectedCharacter is not None and type(selectedCell) is not Obstacle and type(selectedCell) is not Character:
			if self.selectedCharacter.position.distanceToPoint(selectedPosition) <= self.selectedCharacter.speed:
				attackingTeam = self.greenTeam if self.activeTeam.name == self.purpleTeam.name else self.purpleTeam
				self.animFinishedCallback = lambda : self._startAttackingPhase(attackingTeam, api)
				moveMessage = self._startMovingPhase(selectedPosition)
				api.addMessage(moveMessage)
				self._setSelectionStatus(self.selectedCharacter, False, None)


	def onAnimFinished(self) -> None:
		self.animFinishedCallback()


	def _buildSquads(self, squads: List[Squad], api: GameAPI) -> None:
		squad = []
		x = 0
		for info in self.squadsInfo:
			y = 1
			for (characterName, characterSprite, characterType) in zip(info.names, info.sprites, info.types):
				position = QVector2D(x, y)
				character = CharacterFactory.createCharacter(characterType, characterName, position, api.addMarker(characterSprite,
																												   int(position.x()),
																												   int(position.y())))
				character.marker.anim.finished.connect(self.onAnimFinished)
				squad.append(character)
				y += 2
			squads.append(Squad(squad.copy(), info.name))
			squad.clear()
			x = GRID_SIZE - 1

	def _createObstacles(self, obstacleCells: List[int], api: GameAPI, obstacles: List[Obstacle]) -> None:
		for obstacle in obstacleCells:
			isRock = randint(1, 2) == 1
			obstacleType = Sprite.ROCK if isRock else Sprite.BUSH
			isBlockingDamage = True if isRock else False
			obstaclePosition = QVector2D(obstacle % GRID_SIZE, obstacle // GRID_SIZE)
			obstacles.append(Obstacle(api.addImage(obstacleType, int(obstaclePosition.x()), int(obstaclePosition.y())),
									  isBlockingDamage, obstaclePosition))

	def _getCellIndex(self, position: QVector2D) -> str:
		index = GRID_LETTERS[int(position.x())] + str((int(position.y()) + 1))
		return index

	def _startMovingPhase(self, position: QVector2D) -> str:
		self.canClick = False
		self.selectedCharacter.marker.moveTo(int(position.x()), int(position.y()))
		self.worldGrid.addEntity(None, self.selectedCharacter.position)
		self.selectedCharacter.position = position
		self.worldGrid.addEntity(self.selectedCharacter, position)
		return '{} moves to {}'.format(self.selectedCharacter.name, self._getCellIndex(position))

	def _startAttackingPhase(self, attackingTeam: Squad, api: GameAPI) -> None:
		for character in attackingTeam.squad:
			for attackMessage in character.attack(self.worldGrid, self.activeTeam):
				api.addMessage(attackMessage)
		for character in self.activeTeam.squad:
			if not character.alive:
				self.worldGrid.addEntity(None, character.position)
				self.activeTeam.removeCharacter(character)
		if self.activeTeam.isDefeated():
			self.isGameFinished = True
			api.addMessage('{} won!'.format(attackingTeam.name))
		else:
			self.activeTeam = self.greenTeam if self.activeTeam.name == self.purpleTeam.name else self.purpleTeam
			api.addMessage('-- -- {} -- --'.format(self.activeTeam.name))
		self.canClick = True

	def _setSelectionStatus(self, character: Character, status: bool, value: Optional[Character]) -> None:
		character.marker.setSelected(status)
		self.selectedCharacter = value

