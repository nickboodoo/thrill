import os
import random
import heapq

#==========================================#
#            CHARACTER CLASSES             #
#==========================================#

class Character:
    def __init__(self, hp, attack_damage, defense):
        self.hp = hp
        self.max_hp = hp
        self.attack_damage = attack_damage
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)

class Player(Character):
    def __init__(self, hp, attack_damage, defense, fury):
        super().__init__(hp, attack_damage, defense)
        self.fury = fury
        self.max_fury = fury

class Enemy(Character):
    pass


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
            print("Choose an action: \n [#]: Move to room \n [G]: Glossary \n [H]: Hint \n [Q]: Quit")
            action = input("What do you want to do? ")

            if action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.move_to_location(self.location.connections[int(action) - 1])
                break
            elif action.lower() == 'g':
                self.game_loop.access_glossary()
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
        if not new_location.is_goal:
            CombatScreen(new_location, self.game_loop).display()

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
        self.game_loop.update_screen()

class VictoryScreen(GameScreen):
    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Congratulations! You have reached the goal and won the game!".center(self.DASH_WIDTH))
        self.print_dashes()
        input("\nPress Enter to exit the game...")
        exit()

#==========================================#
#             COMBAT INTERFACE             #
#==========================================#

class CombatScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)
        self.enemy = Enemy(100, 10, 2)
        self.player = self.game_loop.player

    def display(self):
        while self.player.is_alive() and self.enemy.is_alive():
            self.clear_screen()
            print(f"Player HP: {self.player.hp}/{self.player.max_hp}  Fury: {self.player.fury}/{self.player.max_fury}")
            print(f"Enemy HP: {self.enemy.hp}/{self.enemy.max_hp}")
            print("Actions: [A]ttack [D]efend [R]age [H]eal [F]lee")
            action = input("Choose your action: ").lower()

            if action == "a":
                damage = random.randint(1, self.player.attack_damage)
                self.enemy.take_damage(damage)
                self.player.fury = min(self.player.max_fury, self.player.fury + 5)
                print(f"You attacked the enemy dealing {damage} damage. Your fury increased to {self.player.fury}.")

            elif action == "d":
                damage = self.enemy.attack_damage * 0.25
                self.player.take_damage(damage)
                self.player.fury = min(self.player.max_fury, self.player.fury + int(self.enemy.attack_damage * 2))
                print(f"You defended. Enemy attacked and you took {damage} damage. Fury increased to {self.player.fury}.")

            elif action == "r":
                if self.player.fury >= 15:
                    self.player.fury -= 15
                    self.player.attack_damage += 5  # Increasing attack damage temporarily
                    print(f"Rage activated! Attack damage increased to {self.player.attack_damage}. Fury reduced to {self.player.fury}.")

            elif action == "h":
                if self.player.fury > 0:
                    heal_amount = min(self.player.max_hp - self.player.hp, self.player.fury)
                    self.player.hp += heal_amount
                    self.player.fury -= heal_amount
                    print(f"Healed {heal_amount} HP. Your HP is now {self.player.hp}. Fury reduced to {self.player.fury}.")

            elif action == "f":
                if self.player.fury >= 50:
                    self.player.fury -= 50
                    print("You fled the battle. Returning to the previous location...")
                    self.game_loop.current_node = self.game_loop.previous_node
                    break

            if self.enemy.is_alive():
                enemy_damage = self.enemy.attack_damage
                self.player.take_damage(enemy_damage)
                print(f"The enemy attacks back dealing {enemy_damage} damage to you. Your HP is now {self.player.hp}.")

            if not self.enemy.is_alive():
                print("Enemy defeated!")
                input("Press Enter to continue...")
                break

            if not self.player.is_alive():
                print("You have been defeated!")
                input("Press Enter to exit...")
                exit()

            input("Press Enter to continue to the next turn...")  # Pause between turns

#==========================================#
#           GLOSSARY INTERFACES            #
#==========================================#

class GlossaryScreen(GameScreen):
    def __init__(self, game_loop):
        super().__init__(None, game_loop)
        self.terms = [
            "HP", "Fury", "Attack Damage", "Defense", "Hint", "Victory", "Defeat",
            "Enemy", "Attack Action", "Defend Action", "Rage Action", "Heal Action", "Flee Action"
        ]

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Glossary of Terms".center(self.DASH_WIDTH))
        self.print_dashes()
        for idx, term in enumerate(self.terms, 1):
            print(f"{idx}. {term}")
        self.print_dashes()
        choice = input("Enter the number for more details or Q to quit: ")
        if choice.lower() == 'q':
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(self.terms):
            term_index = int(choice) - 1
            SubGlossaryScreen(self.terms[term_index], self.game_loop).display()
        else:
            print("Invalid selection. Please try again.")
            input("Press Enter to continue...")
            self.display()

class SubGlossaryScreen(GameScreen):
    def __init__(self, term, game_loop):
        super().__init__(None, game_loop)
        self.term = term
        self.descriptions = {
            "HP": "Health Points: Determines how much damage you can take before you're defeated.",
            "Fury": "A resource used to perform special actions like Rage, Heal, and Flee.",
            "Attack Damage": "The potential maximum damage you can deal to enemies in one attack.",
            "Defense": "Reduces the amount of damage you receive from enemy attacks.",
            "Hint": "Provides a suggested path towards the goal in the game.",
            "Victory": "Occurs when you reach the game's final destination or goal.",
            "Defeat": "Occurs when your HP reaches zero and you lose the game.",
            "Enemy": "Opponents you must fight in combat scenarios.",
            "Attack Action": "A combat action allowing you to deal damage to an enemy.",
            "Defend Action": "A combat action that reduces the damage you take and increases Fury.",
            "Rage Action": "Consumes Fury to significantly increase your attack damage temporarily.",
            "Heal Action": "Consumes Fury to restore your HP.",
            "Flee Action": "Consumes a large amount of Fury to escape combat, returning you to the previous location."
        }

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print(f"{self.term}".center(self.DASH_WIDTH))
        self.print_dashes()
        print(self.descriptions[self.term])
        self.print_dashes()
        input("\nPress Enter to return to the glossary...")
        self.game_loop.current_screen = GlossaryScreen(self.game_loop)
        self.game_loop.current_screen.display()

#==========================================#
#        STATE ENGINE (UI CONTROLLER)      #
#==========================================#

class StateEngine:
    def __init__(self, size=8):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None
        self.player = Player(100, 10, 3, 100)

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

    def access_glossary(self):
        glossary_screen = GlossaryScreen(self)
        glossary_screen.display()

#==========================================#
#             LOCATION AND MAP             #
#==========================================#

class Location:
    def __init__(self, name, is_goal=False, index=None):
        self.name = name
        self.connections = []
        self.visited = False
        self.is_goal = is_goal
        self.index = index

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

        for i in range(1, size):
            self.nodes[i - 1].connect(self.nodes[i])

        additional_connections = size // 3
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
                distance = current_distance + 1
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
