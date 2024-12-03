from PyQt5.QtGui import QVector2D

from world_grid import WorldGrid
from game_constants import CharacterTypes
from obstacle import Obstacle
from constants import GRID_SIZE
from core import Marker

from typing import List, Callable


class Character(object):
    def __init__(self, name: str, marker: Marker, damage: int, health: int, speed: int,
                 attackType: Callable[[int, QVector2D, WorldGrid, 'Squad'], List[str]],
                 damageHandlingType: Callable[[int, int], int],
                 position: QVector2D):
        self.name = name
        self.marker = marker
        self.marker.setHealth(1.0)
        self.damage = damage
        self.health = health
        self.refHealth = health
        self.speed = speed
        self.attackType = attackType
        self.damageHandling = damageHandlingType
        self.position = position
        self.alive = True

    def attack(self, view: WorldGrid, enemy: 'Squad') -> List[str]:
        return self.attackType(self.damage, self.position, view, enemy)

    def handleDamage(self, damage: int, distance: int, attackingCharacter: str) -> str:
        finalDamage = self.damageHandling(damage, distance)
        if finalDamage == 0:
            return '{} blocks all damage from {}'.format(self.name, attackingCharacter)
        self.health -= finalDamage
        if self.health <= 0:
            self.marker.setHealth(0)
            self.marker.remove()
            self.alive = False
            return '{} attacks {} for {} damage\n{} is killed!'.format(attackingCharacter, self.name,
                                                                     finalDamage, self.name)
        else:
            percent = self.health / self.refHealth
            self.marker.setHealth(percent)
            return '{} attacks {} for {} damage'.format(attackingCharacter, self.name, finalDamage)


class Squad(object):
    def __init__(self, squad: List[Character], name: str):
        self.squad = squad
        self.name = name

    def removeCharacter(self, character: Character) -> None:
        for item in self.squad:
            if item is character:
                self.squad.remove(character)
                break

    def isDefeated(self) -> bool:
        return len(self.squad) == 0


class CharacterFactory(object):
    @staticmethod
    def createCharacter(characterType: CharacterTypes, characterName: str, characterPosition: QVector2D, characterMarker: Marker) -> Character:
        if characterType == CharacterTypes.ranger:
            return Character(characterName, characterMarker, 20, 40, 3,
                             attackStraight, ignoreHalfDamage, characterPosition)
        elif characterType == CharacterTypes.mage:
            return Character(characterName, characterMarker, 25, 60, 2,
                             attackStraight, ignoreDamage, characterPosition)
        else:
            return Character(characterName, characterMarker, 35, 30, 4,
                             attackAround, ignoreHalfDamage, characterPosition)


def attackStraight(damage: int, attackPosition: QVector2D, view: WorldGrid, enemy: Squad) -> List[str]:
    messages = []
    charactersToAttack = []

    def _checkLine(toCheck: List[int], isVertical: bool):
        for index in toCheck:
            aim = QVector2D(attackPosition.x(), index) if isVertical else QVector2D(index, attackPosition.y())
            entity = view.getCell(aim)
            if type(entity) is Obstacle and entity.isBlockingAttacks == True:
                return
            elif type(entity) is Character and entity in enemy.squad:
                charactersToAttack.append(entity)

    _checkLine(list(range(int(attackPosition.y() + 1), GRID_SIZE)), True)
    _checkLine(list(range(int(attackPosition.y() - 1), -1, -1)), True)
    _checkLine(list(range(int(attackPosition.x() + 1), GRID_SIZE)), False)
    _checkLine(list(range(int(attackPosition.x() - 1), -1, -1)), False)
    finalDamage = damage // len(charactersToAttack) if len(charactersToAttack) > 0 else 0
    for character in charactersToAttack:
        distance = int(attackPosition.distanceToPoint(character.position))
        messages.append(character.handleDamage(finalDamage, distance, view.getCell(attackPosition).name))
    return messages


def attackAround(damage: int, attackPosition: QVector2D, view: WorldGrid, enemy: Squad) -> List[str]:
    messages = []
    charactersToAttack = []

    for x in range(int(attackPosition.x() - 1), int(attackPosition.x() + 2)):
        for y in range(int(attackPosition.y() - 1), int(attackPosition.y() + 2)):
            if 0 <= x <= GRID_SIZE - 1 and 0 <= y <= GRID_SIZE - 1:
                aim = QVector2D(x, y)
                cell = view.getCell(aim)
                if aim != attackPosition and type(cell) is Character:
                    if cell in enemy.squad:
                        charactersToAttack.append(cell)

    finalDamage = damage // len(charactersToAttack) if len(charactersToAttack) > 0 else 0
    for character in charactersToAttack:
        messages.append(character.handleDamage(finalDamage, 1, view.getCell(attackPosition).name))
    return messages


def ignoreHalfDamage(damage: int, distance: int) -> int:
    return damage // 2 if distance > 2 else damage


def ignoreDamage(damage: int, distance: int) -> int:
    return 0 if damage <= 10 else damage
