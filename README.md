# Magic Fight
## How to run
```
$ & path_to/python.exe path_to/main.py
```

## How to play
### Characters Stats
#### Rogue
+ Attack = 35
+ Health = 30 
+ Moving speed = 4
+ Attack type = 8 cells around
+ Damage handling = ignores half of damage if attacker is further than 2 cells away 

#### Ranger
+ Attack = 25
+ Health = 40 
+ Moving speed = 3
+ Attack type = 4 rays: straight up, straight down, straight left, straight right
+ Damage handling = ignores half of damage if attacker is further than 2 cells away 

#### Mage
+ Attack = 25
+ Health = 60 
+ Moving speed = 2
+ Attack type = 4 rays: straight up, straight down, straight left, straight right
+ Damage handling = ignores damage if it is less than 10 points 

#### Squads
+ Green = Forest defenders
+ Purple = Night warriors

### Rules
1) On random is decided, which squad moves first.
2) On a player's turn one clicks on a character they want to move. Than clicks on an empty cell to move selected character to it or clicks on the character again to deselect. Characters can move through bushes and rocks, but cannot stop moving on them. Characters move according to their speed stat.
3) After player's move opponent's squad attacks player's squad according to its characters attack stats. if one character attacks several characters, the damage is devided between the attacked. Characters can attack through bushes and other characters, but rocks block the damage. No friendly fire.
4) If one's health (red healthbar) is zero or below, the character dies.
5) Wins the squad with alive characters left. 