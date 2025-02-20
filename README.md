# TankTroubleDupe

Ever wanted to play a tank game?

## Requirements
Python must be installed on your local computer

Pygame must also be installed by running `pip install pygame` in the command terminal

The minimum screen dimensions to play this game is 800 x 600 pixels

## Introduction

Welcome to Flanki, a game inspired by both Tanki Online and Tank Trouble. Get the top-down feel of tank trouble with the variety and mobility from the prime feel of Tanki Online

## Features

A fully immplemented single and local two player setup with easy and hard difficulties

### Controls

Player 1: 
> WASD : Movement

> RT   : Turret left / right (disabled in easy mode)

> Y    : Shoot

Player 2:
> Arrow Keys : Movement

> ,.         : Turret left / right (disabled in easy mode)

> /          : Shoot

## Installation

This game has no current release featured on Github

This game can be played locally on the command terminal by navigating to the directory where the main.py file is located and running the command
`python main.py`

## How to Play

When on the menu screen, there are several options to play:

Easy mode (1 or 2 players)

This will immediately bring you into the game, if you are in single player mode, then there will be an AI to control the player 1 tank and you will be playing with the player 2 controls. If you are playing with two players, both controls will be active

Hard mode (1 or 2 players)

This will prompt you with the selction screen, where you can choose from a range of different turrets and hulls as well as colour customisation allowing for a completely unique feel, each turret and hull have their own advantages and disadvantages so you must choose wisely in order to outplay your opponent, once both players are ready hit the `play` button in the middle.

This will then bring you into the game, if you are in single player mode, then there will be an AI to control the player 1 tank and you will be playing with the player 2 controls. If you are playing with two players, both controls will be active



## Known issues

There is an issue where the game will suddenly crash due to the maze failing to generate, hwoever this bug is difficult to replicate

## Roadmap (future plans)

No current plans
Ideas:
1. Improve the AI to avoid bullets
1. Add `Inferno` turret, concept: A laser that will deal more damage over time as it stays on its target, also takes self damage after too long
1. Add `Bucket` turret, concept: A "Bucket" that can't shoot, however can pick up and reflect any bullet shot at it
1. Add `Avalanche` turret: A turret that will slow down the enemies in its range
1. Add kill streak sounds / change battle track
1. Add introduction cards for each tank

## Credits

Thank you to the following people
    Bin-Coder14, Goodnews888, Ekiel, Beta

Thanks to you for playing the game

All rights belong to their respective owners, if your work was featured in here and you would like it removed, please contact me




# Statistics

|  Tank |  Health | Speed |
|-------|---------|-------|
| Panther | 1500 | 0.1 |
| Cicada | 2000 | 0.08 |
| Gater | 3000 | 0.07 |
| Bonsai | 3500 | 0.05 |
| Fossil | 4000 | 0.03 |

| Gun | Damage | Reload | Bullet Speed | Notes |
|-----|--------|--------|--------------|-------|
| Chamber | 810 | 1500 | 10 |3 radii of 270 each, splash damage |
| Huntsman | 600 | 1000 | 15 | 40% chance for double damage |
| Judge | 1520 | 2400 | 8 |3 rounds each with 800 reload and 2400 long, bounces once, 20 bullets each 76 damage |
| Sidewinder | 350 | 500 | 12 | 5 bounces per bullet |
| Silencer | 1400 | 2400 | 50 | No Notes |
| Tempest | 200 | 200 | 10 | No Notes |
| Watcher | 3300 | 1500 | 50 | Scope comes attached, damage scales over time |
