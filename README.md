# TankTroubleDupe

Ever wanted to play a tank game?

## Requirements
Python must be installed on your local computer

Pygame must also be installed by running `pip install pygame` in the command terminal

The minimum screen dimensions to play this game is 800 x 600 pixels, a full screen version may be available later

## Introduction

Welcome to Flanki, a game inspired by both Tanki Online and Tank Trouble. Get the top-down feel of tank trouble with the variety and mobility from the feel of prime Tanki Online

### Controls

Player 1: 
> WASD : Movement

> RT   : Turret left / right (disabled in easy mode)

> Y    : Shoot

Player 2:
> Arrow Keys : Movement

> ,.         : Turret left / right (disabled in easy modes)

> /          : Shoot

## Installation

This game has a current release featured on Github which can be downloaded and run without needing any pre-installed requirements

This game can be played locally on the command terminal by navigating to the directory where the main.py file is located and running the command

`python main.py`

## How to Play

When on the menu screen, there are several options to play:

Whenever selecting a one-player option, you will always play as player two using the player two controls.

# Scrapyard

> Scrapyard is a One-Hit Kill gamemode which will run indefinitely, resetting after each kill with a freeze-frame

## Modes:
- 1P Yard: One player vs an AI both using simple tanks

- 1P Scrapyard: One player vs an AI both using the advanced tanks

- 2P Yard: Player vs Player both using simple tanks

- 2P Scrapyard: Palyer vs Player both using the advanced tanks

# Death Match

> Deathmatch is a 5 mintues gamemode which players will compete for the most kills

- 1P Brawl: One player vs an AI both using simple tanks

- 1P Deathmatch: One player vs an AI both using the advanced tanks

- 2P Brawl: Player vs Player both using simple tanks

- 2P DeathMatch: Player vs Player both using the advanced tanks

# CTF (Capture The Flag)

> Capture the Flag is a 10 minute gamemode which teams of 2 players will compete for the most captures of the enemy flag

- 1P CTF: Player + AI vs AI + AI both using the advanced tanks and a pre-determined map. This gamemode include flags which the score will be based off

- 2P CTF: Player + AI vs Player + AI both using the advanced tanks and a pre-determined map. This gamemode includes flags which the score will be based off

# Team Modes (in concept)
## Future Plans:

> TDM (Team DeathMatch) 2v2 with the option of either 1 or 2 players, the other 2 tanks will be AI's. Most Kills wins

> CTF (Capture the Flag) 2v2 with the option of either 1 or 2 players, the other 2 tanks will be AI's. However the win condition is whoever captures the most enemy flags

## Known issues

There is an issue with the music if the switch between varying scenes (e.g. home -> 1p easy) where the music track will not properly transition to the battle track

## Roadmap (future plans)

Ideas (Not currently in development):
1. Add `Firestorm` turret, concept: A powerful flame thrower that will slowly deal damage over time as the enemy stays within its range for longer
1. Improve the AI to avoid bullets
1. Add # Missing Name #, concept: A turret similar to the hunstman which will deal a short stun upon a hit, impacting tank movement for a brief period. The affected turret will still be operational
1. Add `Inferno` turret, concept: A laser that will deal more damage over time as it stays on its target, also takes self damage after too long
1. Add `Bucket` turret, concept: A "Bucket" that can't shoot, however can pick up and reflect any bullet shot at it
1. Add Ghost hull, concept: A hull which becomes less visible the more damage it takes
1. Add kill streak sounds
1. Add introduction cards for each tank

## Credits

Thank you to the following people
- Bin-Coder14
- Goodnews888
- Ekiel
- Beta

Thanks to you for playing the game

All rights belong to their respective owners, if your work was featured and you would like it removed, please contact me


# Statistics

|  Tank | Health | Speed |
|-------|---------|-------|
| Panther | 1500 | 0.1 |
| Cicada | 2100 | 0.08 |
| Gater | 3300 | 0.07 |
| Bonsai | 4500 | 0.05 |
| Fossil | 5100 | 0.03 |

| Gun | Damage | Reload | Bullet Speed | Notes |
|-----|--------|--------|--------------|-------|
| Chamber | 750 | 1500 | 10 |3 radii of 250 each, splash damage |
| Huntsman | 600 | 1000 | 15 | 40% chance for double damage |
| Judge | 800 | 2400 | 8 |3 rounds each with 800 reload and 2400 long, bounces once, 20 bullets each 80 damage |
| Sidewinder | 300 | 500 | 12 | 5 bounces per bullet |
| Silencer | 1300 | 2400 | 50 | Wind-up time before shooting |
| Tempest | 150 | 200 | 10 | No Notes |
| Watcher | 3300 | 1500 | 50 | Scope comes attached, damage scales over time |

Supply Statistics

| Supply | Effect |
|--|--|
| Damage | Deal 150% Damage|
| Armor | Take 50% Less Damage|
| Speed | 40% Increased Tank Speed and 20% Increased Turret Rotation Speed|
