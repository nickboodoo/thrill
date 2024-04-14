import os
import random
import textwrap
import heapq

#==========================================#
#             USER INTERFACES              #
#==========================================#

class GameScreen:
    DASH_WIDTH = 90

    def __init__(self, location, game_loop=None):
        self.location = location
        self.game_loop = game_loop

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_dashes(self):
        print('-' * self.DASH_WIDTH)

    def display(self):
        pass

class ExplorationScreen(GameScreen):
    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print(f"You are in {self.location.name}.".center(self.DASH_WIDTH))
            self.print_dashes()
            if self.location.is_goal:
                self.game_loop.victory()
                break
            print("Connections:")
            for i, connection in enumerate(self.location.connections):
                print(f" {i + 1}: {connection.name}")
            self.print_dashes()
            print("Choose an action: \n [#]: Move to room \n [H]: Hint \n [Q]: Quit")
            action = input("What do you want to do? ")

            if action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.move_to_location(self.location.connections[int(action) - 1])
                break
            elif action.lower() == 'h':
                self.game_loop.show_hint(self.location)
                break
            elif action.lower() == 'q':
                exit()
            else:
                print("Invalid action, try again.")
                input("Press Enter to continue...")
                self.clear_screen()

    def move_to_location(self, new_location):
        self.game_loop.previous_node = self.game_loop.current_node
        new_location.visited = True
        self.game_loop.current_node = new_location

class HintScreen(GameScreen):
    def display(self):
        path = self.game_loop.graph.dijkstra(self.location)
        path_names = " -> ".join(node.name for node in path)
        self.clear_screen()
        self.print_dashes()
        print("Hint: Follow this path to reach the goal".center(self.DASH_WIDTH))
        self.print_dashes()
        print(path_names)
        self.print_dashes()
        input("\nPress Enter to return to the exploration...")
        self.game_loop.update_screen()  # Return to the exploration screen after showing the hint

class VictoryScreen(GameScreen):
    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Congratulations! You have reached the goal and won the game!".center(self.DASH_WIDTH))
        self.print_dashes()
        input("\nPress Enter to exit the game...")
        exit()

#==========================================#
#        STATE ENGINE (UI CONTROLLER)      #
#==========================================#

class StateEngine:
    def __init__(self, size=8):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None

    def update_screen(self):
        self.current_screen = ExplorationScreen(self.current_node, self)

    def show_hint(self, location):
        hint_screen = HintScreen(location, self)
        hint_screen.display()

    def play(self):
        while True:
            self.update_screen()
            self.current_screen.display()

    def victory(self):
        VictoryScreen(self.current_node, self).display()

#==========================================#
#             LOCATION AND MAP             #
#==========================================#

class Location:
    def __init__(self, name, is_goal=False, index=None):
        self.name = name
        self.connections = []
        self.visited = False
        self.is_goal = is_goal
        self.index = index  # Unique identifier for each location

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

class Map:
    def __init__(self, size):
        self.nodes = []
        for i in range(size):
            name = "Location " + str(i) if i > 0 else "Starting Area"
            self.nodes.append(Location(name, is_goal=(i == size - 1), index=i))

        # Connect nodes linearly and ensure at least a chain from start to goal
        for i in range(1, size):
            self.nodes[i - 1].connect(self.nodes[i])

        # Optionally connect random nodes to create a more complex map
        additional_connections = size // 3  # Adjust as needed
        for _ in range(additional_connections):
            a, b = random.sample(self.nodes, 2)
            a.connect(b)

    def dijkstra(self, start):
        distances = {node: float('infinity') for node in self.nodes}
        previous_nodes = {node: None for node in self.nodes}
        distances[start] = 0
        pq = [(0, start.index, start)]

        while pq:
            current_distance, _, current_node = heapq.heappop(pq)

            if current_node.is_goal:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                return path[::-1]

            if current_distance > distances[current_node]:
                continue

            for neighbor in current_node.connections:
                distance = current_distance + 1  # All edges are equal weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor.index, neighbor))

        return []

#==========================================#
#             MODULE CHECKING              #
#==========================================#

if __name__ == "__main__":
    game = StateEngine()
    game.play()
