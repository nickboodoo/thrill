# FOR THE THRILL OF THE HUNT

THRILL is a text-based navigation game developed in Python, where players aim to reach a designated "goal location" on a dynamically generated map. The game leverages a simple text-based interface and utilizes Dijkstra's algorithm to offer hints on finding the shortest path to the goal.

## Features

- **Dynamic Map Generation**: The game generates a new map for each session, with locations connected in various ways to challenge the player.

- **Text-based User Interface**: Interact with the game through a simple and intuitive text-based interface.

- **Hint System**: At any point, players can request a hint that provides the shortest path to the goal using Dijkstra's algorithm.

- **Victory and Game Over Screens**: The game acknowledges the player's success upon reaching the goal and allows for easy game termination at any point.

## How to Play

1. **Start the Game**: Run the game script in a Python environment.

2. **Navigate**: Use the number keys to choose a path from the available connections at each location.

3. **Use Hints**: Press 'H' during gameplay to receive guidance on the shortest path to the goal.

4. **Quit Anytime**: Press 'Q' to quit the game at any point.

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

bash

git clone https://github.com/nickboodoo/THRILL.git

cd THRILL

python3 thrill.py

## Contributing

Contributions are welcome! Please reach out to me before you attempt to submit pull requests or open issues for bugs, feature requests, or documentation improvements. Thank you!!

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

