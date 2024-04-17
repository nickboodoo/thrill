# FOR THE THRILL OF THE HUNT

THRILL is a text-based navigation game developed in Python, where players aim to reach a designated "goal location" on a dynamically generated map. The game leverages a simple text-based interface and utilizes Dijkstra's algorithm to offer hints on finding the shortest path to the goal.

## Installation

To play this game, download the latest [release](https://github.com/nickboodoo/thrill/releases).

## How to Play

1. **Start the Game**: Double-click on the thrill.exe file that you just downloaded from the release page. 

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

## Game Design

### StateEngine

The `StateEngine` is the core of THRILL's gameplay mechanics. It manages the current state of the game by updating which screen is displayed to the user based on their interactions. The engine handles transitions between different game states such as exploration, hints, and victory screens, ensuring a seamless user experience.

### Screen Concept

THRILL employs a screen-based approach to manage user interactions. Each screen (such as `ExplorationScreen`, `HintScreen`, and `VictoryScreen`) represents a different state of the game. This modular design allows for easy updates and maintenance of each individual part of the game without affecting others.

### Tree and Tree Traversal

- **Graph/Tree Structure**
  - The `Map` class constructs a linear sequence of connected `Location` nodes, potentially with additional random connections. The primary structure is tree-like with the possibility of cycles due to additional edges, which technically makes it a graph. However, since each location only connects to its subsequent and possibly some random locations, it retains a somewhat hierarchical, tree-like structure.

- **Traversal**
  - **Exploration Traversal**
    - When players move from one location to another, they are effectively performing a traversal of this graph/tree. The traversal in this game can be akin to a depth-first search (DFS) or breadth-first search (BFS), depending on how the player chooses to explore the connections.
  - **Pathfinding with Dijkstra's Algorithm**
    - In the `HintScreen`, there's an implementation of Dijkstra’s algorithm to find the shortest path to the goal, which is a form of graph traversal optimized for graphs with weighted edges (though the weights are uniform here). This provides players with guidance on how to reach the goal location efficiently, functioning similarly to a level-order traversal by exploring the shortest path first.

- **Dynamic Tree Traversal**
  - The game allows dynamic traversal where the player can choose their path at runtime. This is particularly evident in how the `ExplorationScreen` lets the player choose which location to move to next, allowing for a personalized traversal experience.

## Contributing

Contributions are welcome! Please reach out to me before you attempt to submit pull requests or open issues for bugs, feature requests, or documentation improvements. Thank you!!

## License

This project is licensed under the [MIT License](./LICENSE).

