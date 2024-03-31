import random
import os
import csv
import textwrap

class Character:
    def __init__(self, name, health, attack, mana=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = attack
        self.mana = mana
        self.is_immune = False

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = random.randint(1, self.strength)
        if self.is_immune:
            damage //= 2
        target.health -= damage
        return damage

class Enemy(Character):
    enemies = []

    @classmethod
    def load_enemies_from_csv(cls, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            cls.enemies = []
            for row in reader:
                cls.enemies.append({
                    "name": row["name"], 
                    "health": int(row["health"]), 
                    "attack": int(row["attack"]),
                    "lore": row.get("lore", "Lore not available.")
                })

    @staticmethod
    def generate_random_enemy():
        if not Enemy.enemies:
            Enemy.load_enemies_from_csv('src/tests/enemies.csv')
        enemy_info = random.choice(Enemy.enemies)
        return Enemy(enemy_info["name"], enemy_info["health"], enemy_info["attack"])

    @staticmethod
    def format_enemy_info(enemy):
        name_and_stats = f'{enemy["name"]} ({enemy["health"]} HP, {enemy["attack"]} Attack):\n'
        lore = f'"{enemy["lore"]}"'
        wrapped_lore_lines = textwrap.wrap(lore, width=GameScreen.LORE_TEXT_WIDTH)
        centered_lore_lines = [line.center(GameScreen.LORE_TEXT_WIDTH) for line in wrapped_lore_lines]
        centered_lore = "\n".join(centered_lore_lines)
        info = f"{name_and_stats}\n{centered_lore}"
        return info

class Player(Character):
    def __init__(self, name='Player', health=100, attack=25, mana=100):
        super().__init__(name, health, attack, mana)
        self.max_health = 100
        self.unseen_predator_turns = 0

class Location:
    def __init__(self, name, generate_enemy_flag=True):
        self.name = name
        self.connections = []
        self.visited = False
        self.enemy = self.generate_enemy() if generate_enemy_flag else None

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    def generate_enemy(self):
        if random.choice([True, False]):
            return Enemy.generate_random_enemy()
        return None

class Map:
    def __init__(self, size):
        self.nodes = [Location("Room 0", generate_enemy_flag=False)] + [Location(f"Room {i}") for i in range(1, size)]
        self.generate_graph()
        self.ensure_at_least_one_enemy()

    def generate_graph(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].connect(self.nodes[i + 1])
            if i > 0 and random.choice([True, False]):
                self.nodes[i].connect(random.choice(self.nodes[:i]))

    def ensure_at_least_one_enemy(self):
        if not any(node.enemy for node in self.nodes):
            random.choice(self.nodes[1:]).enemy = Enemy.generate_random_enemy()

class GameScreen:
    DASH_WIDTH = 90
    LORE_TEXT_WIDTH = 65

    def __init__(self, location, game_loop=None):
        self.location = location
        self.game_loop = game_loop

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_dashes(self):
        print('-' * self.DASH_WIDTH)

    def display(self):
        pass

class GlossaryScreen(GameScreen):
    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print("Glossary Menu:".center(90))
            self.print_dashes()
            print("1. About the Game")
            print("2. Rooms")
            print("3. Enemies")
            print("4. Back")
            self.print_dashes()
            choice = input("Choose a category: ")

            if choice == '1':
                AboutGameScreen(self.location, self.game_loop).display()
            elif choice == '2':
                RoomGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '3':
                EnemyGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
            input("Press Enter to continue...")

class AboutGameScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("About the Game".center(90))
        self.print_dashes()
        game_about_lore = """Thrill is developed and written by Nick Boodoo. 
                            This game is loosely based on the Thrill of the Hunt 
                            concept inspired by Rengar from League of Legends."""
        wrapped_about_lore = textwrap.wrap(game_about_lore, width=75)
        for line in wrapped_about_lore:
            # Center each line individually
            print(line.center(90))
        self.print_dashes()
        input("\nPress Enter to return to the Glossary...")


class EnemyGlossaryScreen(GameScreen):
    MAX_ENTRIES_PER_COLUMN = 10

    def display(self):
        self.display_enemies()

    def display_enemies(self):
        self.clear_screen()
        self.print_dashes()
        print("Select an enemy to learn more:".center(90))
        self.print_dashes()
        enemies = Enemy.enemies

        columns = (len(enemies) + self.MAX_ENTRIES_PER_COLUMN - 1) // self.MAX_ENTRIES_PER_COLUMN

        max_name_length = max(len(enemy["name"]) for enemy in enemies) + 4
        column_width = max_name_length + len(str(len(enemies))) + 2

        for i in range(self.MAX_ENTRIES_PER_COLUMN):
            row = []
            for j in range(columns):
                index = i + j * self.MAX_ENTRIES_PER_COLUMN
                if index < len(enemies):
                    cell = f"{index + 1}. {enemies[index]['name']}".ljust(column_width)
                    row.append(cell)
            if row:
                print("".join(row))

        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice: ")
        self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            elif 1 <= choice <= len(Enemy.enemies):
                selected_enemy = Enemy.enemies[choice - 1]
                EnemyDetailScreen(self.location, selected_enemy).display()
            else:
                print("Invalid choice.")
                input("Press Enter to try again...")
                self.display_enemies()
        else:
            print("Please enter a number.")
            input("Press Enter to try again...")
            self.display_enemies()

class RoomGlossaryScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Rooms List:".center(90))
        self.print_dashes()
        for i, node in enumerate(self.game_loop.graph.nodes):
            visited_status = "Visited" if node.visited else "Not Visited"
            print(f"{i + 1}. {node.name}: {visited_status}")
        
        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice to see connections or 0 to go back: ")
        
        if choice.isdigit():
            choice = int(choice) - 1
            if 0 <= choice < len(self.game_loop.graph.nodes):
                self.display_connections(self.game_loop.graph.nodes[choice])
            elif choice == -1:
                return
            else:
                print("Invalid choice.")
                input("Press Enter to try again...")
                self.display()
        else:
            print("Please enter a number.")
            input("Press Enter to try again...")
            self.display()

    def display_connections(self, node):
        # Transition to RoomDetailScreen instead of displaying connections directly
        detail_screen = RoomDetailScreen(self.location, self.game_loop, node)
        detail_screen.display()

class EnemyDetailScreen(GameScreen):
    def __init__(self, location, enemy):
        super().__init__(location)
        self.enemy = enemy

    def display(self):
        self.clear_screen()
        enemy_info = Enemy.format_enemy_info(self.enemy)
        self.print_dashes()
        print("Enemy Details:".center(90))
        self.print_dashes()
        print(enemy_info)
        self.print_dashes()

class RoomDetailScreen(GameScreen):
    def __init__(self, location, game_loop, room):
        super().__init__(location, game_loop)
        self.room = room  # The room whose details are to be displayed

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print(f"Room Details: {self.room.name}".center(self.DASH_WIDTH))
        self.print_dashes()
        visited_status = "Visited" if self.room.visited else "Not Visited"
        print(f"Visited Status: {visited_status}")
        print("Connections:")
        for i, connected_node in enumerate(self.room.connections):
            print(f" {i + 1}. {connected_node.name}")
        self.print_dashes()

class VictoryScreen(GameScreen):
    def display(self):
        self.clear_screen()
        print("Congratulations! You have defeated all the enemies and survived.")
        print("You are a true hero!")
        print("\nWould you like to play again? (yes/no)")
        choice = input().lower()
        if choice == 'yes':
            game = StateEngine()
            game.play()
        else:
            print("Thank you for playing! Goodbye.")
            exit()

class DefeatScreen(GameScreen):
    def display(self):
        self.clear_screen()
        print("Alas, you have been defeated. The world mourns the loss of a brave hero.")
        print("\nWould you like to try again? (yes/no)")
        choice = input().lower()
        if choice == 'yes':
            game = StateEngine()
            game.play()
        else:
            print("Thank you for playing! Better luck next time.")
            exit()

class ExplorationScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location)
        self.game_loop = game_loop

    def move_to_location(self, new_location):
        if self.game_loop.current_node is not None:
            self.game_loop.previous_node = self.game_loop.current_node
        self.game_loop.current_node = new_location

    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print(f"You are in {self.location.name}.".center(self.DASH_WIDTH))
            self.print_dashes()
            if self.location.enemy and self.location.enemy.is_alive():
                print(f"An enemy {self.location.enemy.name} is here!")
            print("Connections:")
            for i, connection in enumerate(self.location.connections):
                print(f" {i + 1}: {connection.name}")
            self.print_dashes()
            print("Choose an action: \n [G]: Glossary \n [#]: Move to room \n [Q]: Quit")
            self.print_dashes()
            action = input("What do you want to do? ")
            self.clear_screen()

            if action.lower() == 'g':
                GlossaryScreen(self.location, self.game_loop).display()
            elif action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.move_to_location(self.location.connections[int(action) - 1])
                self.game_loop.current_node.visited = True
                break
            elif action.lower() == 'q':
                exit()
            else:
                print("Invalid action, try again.")
                input("Press Enter to continue...")
                self.clear_screen()

    def display_rooms(self, nodes):
        print("Rooms:")
        for node in nodes:
            visited_marker = "Visited" if node.visited else "Not Visited"
            print(f"{node.name}: {visited_marker}")
        input("Press Enter to continue...")
        self.clear_screen()

class CombatScreen(GameScreen):
    def __init__(self, location, player, enemy, game_loop):
        super().__init__(location)
        self.player = player
        self.enemy = enemy
        self.game_loop = game_loop

    def display_health_bars(self):
        super().print_dashes()
        player_health_blocks = int((self.player.health / self.player.max_health) * 20)
        enemy_health_blocks = int((self.enemy.health / self.enemy.max_health) * 20)
        player_health_bar = f"{'█' * player_health_blocks}{' ' * (20 - player_health_blocks)}"
        enemy_health_bar = f"{'█' * enemy_health_blocks}{' ' * (20 - enemy_health_blocks)}"
        print(f"\nPlayer   HP: {player_health_bar} {self.player.health}/{self.player.max_health}")

        max_mana_blocks = 20
        player_mana_blocks = int((self.player.mana / 100) * max_mana_blocks)
        player_mana_bar = f"{'█' * player_mana_blocks}{' ' * (max_mana_blocks - player_mana_blocks)}"
        print(f"\n       Mana: {player_mana_bar} {self.player.mana}/100")

        print(f"\n\nEnemy    HP: {enemy_health_bar} {self.enemy.health}/{self.enemy.max_health}\n")
        super().print_dashes()

    def display_combat_options(self):
        print("Choose your action: \n1. Attack")

    def handle_combat_action(self):
        action = input("Action: ")
        self.clear_screen()

        if action == "1":
            damage_dealt = self.player.attack(self.enemy)
            print(f"You attack the {self.enemy.name} for {damage_dealt} damage.")
            if not self.enemy.is_alive():
                print(f"The {self.enemy.name} is defeated.")
                return 'enemy_defeated'
            
            damage_taken = self.enemy.attack(self.player)
            print(f"The {self.enemy.name} attacks you for {damage_taken} damage.")
            if not self.player.is_alive():
                print("You have been defeated.")
                return 'player_defeated'

        else:
            print("Invalid action, try again.")

        self.display_health_bars()
        return 'continue'

    def display(self):
        super().print_dashes()
        print(f"You encounter an enemy! The fight begins. It's a {self.enemy.name}.".center(90, ' '))
        self.display_health_bars()
        while self.player.is_alive() and self.enemy.is_alive():
            self.display_combat_options()
            result = self.handle_combat_action()
            if result in ['enemy_defeated', 'fled']:
                break
            if not self.player.is_alive():
                print("Game Over. You have been defeated.")
                break

class StateEngine:
    def __init__(self, size=3):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None
        self.player = Player()

    def update_screen(self):
        if not self.player.is_alive():
            self.current_screen = DefeatScreen(self.current_node)
        elif self.have_defeated_all_enemies():
            self.current_screen = VictoryScreen(self.current_node)
        elif self.current_node.enemy and self.current_node.enemy.is_alive():
            self.current_screen = CombatScreen(self.current_node, self.player, self.current_node.enemy, self)
        else:
            self.current_screen = ExplorationScreen(self.current_node, self)

    def play(self):
        while self.player.is_alive() and not self.have_defeated_all_enemies():
            self.update_screen()
            self.current_screen.display()

        if not self.player.is_alive():
            DefeatScreen(self.current_node).display()
        elif self.have_defeated_all_enemies():
            VictoryScreen(self.current_node).display()

    def have_defeated_all_enemies(self):
        for node in self.graph.nodes:
            if node.enemy and node.enemy.is_alive():
                return False
        return True

if __name__ == "__main__":
    game = StateEngine()
    game.play()
