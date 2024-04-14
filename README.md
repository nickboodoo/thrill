# FOR THE THRILL OF THE HUNT

THRILL is a text-based navigation game developed in Python, where players aim to reach a designated "goal location" on a dynamically generated map. The game leverages a simple text-based interface and utilizes Dijkstra's algorithm to offer hints on finding the shortest path to the goal.

## Features

- **Dynamic Map Generation**: The game generates a new map for each session, with locations connected in various ways to challenge the player.

- **Text-based User Interface**: Interact with the game through a simple and intuitive text-based interface.

- **Combat System**: Engage in turn-based combat at each location (except the goal node). Players and enemies exchange blows, with actions determined by the player's strategic choices.

- **Player Encounter Actions**: Players can choose from several actions during combat:
  - **Attack**: Deal damage to enemies and gain fury.
  - **Defend**: Reduce incoming damage and significantly increase fury.
  - **Rage**: Boost attack damage at the cost of fury.
  - **Heal**: Restore health using fury.
  - **Flee**: Escape from combat by using a substantial amount of fury, reverting to the previous location.

- **Glossary**: Access a detailed glossary from the exploration screen explaining key terms such as HP, Fury, Attack Damage, and specific actions, enhancing player understanding of game mechanics.

- **Hint System**: At any point, players can request a hint that provides the shortest path to the goal using Dijkstra's algorithm.

- **Victory and Game Over Screens**: The game acknowledges the player's success upon reaching the goal and provides a distinct game over screen if the player is defeated in combat.

## How to Play

1. **Start the Game**: Run the game script in a Python environment.

2. **Navigate**: Use the number keys to choose a path from the available connections at each location. Each new location may trigger a combat scenario.

3. **Engage in Combat**: When encountering enemies:
   - Choose your action:
     - **Attack** ('A'): Deal damage and gain fury.
     - **Defend** ('D'): Minimize incoming damage and increase fury.
     - **Rage** ('R'): Consume fury to increase your attack power.
     - **Heal** ('H'): Use fury to recover health.
     - **Flee** ('F'): Use fury to escape combat and return to the previous location.

4. **Access Glossary**: Press 'G' to access the glossary and learn about game mechanics and terms.

5. **Use Hints**: Press 'H' during gameplay to receive guidance on the shortest path to the goal.

6. **Victory or Defeat**: Reach the game's goal to win or face defeat if your HP reaches zero in combat.

7. **Quit Anytime**: Press 'Q' to quit the game at any point.

## Game Design

### StateEngine

The `StateEngine` is the core of THRILL's gameplay mechanics. It manages the current state of the game by updating which screen is displayed to the user based on their interactions. The engine handles transitions between different game states such as exploration, hints, and victory screens, ensuring a seamless user experience.

### Screen Concept

THRILL employs a screen-based approach to manage user interactions. Each screen (such as `ExplorationScreen`, `HintScreen`, and `VictoryScreen`) represents a different state of the game. This modular design allows for easy updates and maintenance of each individual part of the game without affecting others.

### Dijkstra's Algorithm

The game utilizes Dijkstra's algorithm to compute the shortest path from the current location to the goal. This algorithm helps in providing hints to the player, making it easier to navigate complex maps efficiently. The implementation relies on maintaining a priority queue to explore the most promising paths first.

### heapq

This game utilizes a heap queue to implement the priority queue required by Dijkstra's algorithm. It allows the game to quickly determine the next location to explore based on the shortest known distance from the start, facilitating efficient pathfinding across the game map.

## Installation

This game requires you to have Python 3.x to run properly. 

bash script:
```
git clone https://github.com/nickboodoo/THRILL.git

cd THRILL

python3 thrill.py
```
## Contributing

Contributions are welcome! Please reach out to me before you attempt to submit pull requests or open issues for bugs, feature requests, or documentation improvements. Thank you!!

## License

This project is licensed under the [MIT License](./LICENSE).

