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

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def use_item(self, item, target=None):
        if item in self.inventory and isinstance(item):
            item.use(target or self)
            item.quantity -= 1
            if item.quantity <= 0:
                self.remove_item(item)

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
        self.inventory = []

class Magic:
    items = []  # Combined list for spells and enchantments

    @classmethod
    def load_magic_from_csv(cls, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            cls.items = []  # Reset items
            for row in reader:
                # Assuming 'Type' can be 'Spell' or 'Enchantment' or a new unified type
                cls.items.append({
                    "type": row["Type"],
                    "name": row["Name"],
                    "effect": row["Effect"],
                    "cost": row["Cost"],
                    "lore": row.get("Lore", "No lore available.")
                })

    @staticmethod
    def format_magic_info(magic):
        name_and_effect = f'{magic["name"]} - {magic["effect"]} ({magic["cost"]})\n'
        lore = f'"{magic["lore"]}"'
        wrapped_lore_lines = textwrap.wrap(lore, width=50)  # Assuming a fixed width for simplicity
        centered_lore_lines = [line.center(50) for line in wrapped_lore_lines]
        centered_lore = "\n".join(centered_lore_lines)
        info = f"{name_and_effect}\n{centered_lore}"
        return info

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
            print("4. Spells and Enchantments")  # New option for Spells and Enchantments
            print("5. Back")
            self.print_dashes()
            choice = input("Choose a category: ")

            if choice == '1':
                AboutGameScreen(self.location, self.game_loop).display()
            elif choice == '2':
                RoomGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '3':
                EnemyGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '4':
                MagicGlossaryScreen(self.location, self.game_loop).display()  # Display the MagicGlossaryScreen
            elif choice == '5':
                break  # Exit the loop to go back
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

class MagicGlossaryScreen(GameScreen):
    MAX_ENTRIES_PER_COLUMN = 10  # This might not be needed depending on your display needs

    def display(self):
        self.display_magic()

    def display_magic(self):
        self.clear_screen()
        self.print_dashes()
        print("Select a magic item to learn more:".center(90))
        self.print_dashes()

        # Ensure magic items are loaded.
        Magic.load_magic_from_csv('src/tests/scrolls.csv')

        # Separate spells and enchantments into two lists.
        spells = [item for item in Magic.items if item['type'].lower() == 'spell']
        enchantments = [item for item in Magic.items if item['type'].lower() == 'enchantment']

        # Print the headers for each column.
        print(f"{'Spells'.center(40)}{'Enchantments'.center(40)}")
        self.print_dashes()

        # Calculate the maximum number of rows needed.
        max_rows = max(len(spells), len(enchantments))

        for i in range(max_rows):
            # Prepare the spell name if within the index range.
            spell_name = f"{i + 1}. {spells[i]['name']} (Spell)" if i < len(spells) else "".ljust(40)
            
            # Prepare the enchantment name if within the index range, adjusting the index as needed.
            enchantment_name = ""
            if i < len(enchantments):
                enchantment_index = i + len(spells) + 1
                enchantment_name = f"{enchantment_index}. {enchantments[i]['name']} (Enchantment)"
            
            # Print the row with both spell and enchantment names.
            print(f"{spell_name.ljust(40)}{enchantment_name}")

        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice: ")
        self.handle_choice(choice, spells + enchantments)

    def handle_choice(self, choice, magic_items):
        if choice.isdigit():
            choice = int(choice) - 1  # Adjust for zero-based indexing
            if choice == -1:
                return  # Go back
            elif 0 <= choice < len(magic_items):
                selected_magic = magic_items[choice]
                # Create and display a MagicDetailsGlossary for the selected magic item
                details_screen = MagicDetailsGlossary(self.location, selected_magic, self.game_loop)
                details_screen.display()
                self.display_magic()  # Optionally redisplay the magic list afterwards
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
                self.display_magic()
        else:
            print("Please enter a number.")
            input("Press Enter to continue...")
            self.display_magic()

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

class InventoryScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Inventory".center(self.DASH_WIDTH))
        self.print_dashes()
        for index, item in enumerate(self.player.inventory, start=1):
            print(f"{index}. {item.name} - {item.description} (x{item.quantity})")
        self.print_dashes()
        print("Select an item to use or 0 to exit:")
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(self.player.inventory):
                item = self.player.inventory[choice - 1]
                self.player.use_item(item)
            elif choice == 0:
                return  # Exit inventory
        else:
            print("Invalid selection.")

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

class MagicDetailsGlossary(GameScreen):
    def __init__(self, location, magic_item, game_loop=None):
        super().__init__(location, game_loop)
        self.magic_item = magic_item

    def display(self):
        self.clear_screen()
        self.print_dashes()

        # Header with the magic item's name, effect, and cost
        header = f"{self.magic_item['name']} - {self.magic_item['effect']} ({self.magic_item['cost']})"
        print(header.center(self.DASH_WIDTH))

        self.print_dashes()

        # Display the lore with word wrapping for better readability
        wrapped_lore_lines = textwrap.wrap(self.magic_item['lore'], width=self.LORE_TEXT_WIDTH)
        for line in wrapped_lore_lines:
            # Center each line of the lore text
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()
        input("\nPress Enter to go back...")

        # You might want to return to the previous screen or perform some action after this

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
        print("Choose your action: \n1. Attack \n2. Inventory")

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

        elif action == "2":
            inventory_screen = InventoryScreen(self.location, self.player, self.game_loop)
            inventory_screen.display()

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
            if result == 'enemy_defeated':
                CombatVictoryScreen(self.location, self.player, self.game_loop).display()
                return
            elif result == 'player_defeated':
                print("Game Over. You have been defeated.")
                break
        
        if not self.player.is_alive():
            DefeatScreen(self.location, self.game_loop).display()

class CombatVictoryScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        victory_message = f"You have defeated the enemy in {self.location.name}! " \
                          "You take a moment to catch your breath and prepare for the next challenge."
        
        self.clear_screen()
        self.print_dashes()
        print("Victory!".center(self.DASH_WIDTH))
        self.print_dashes()

        wrapped_victory_message = textwrap.wrap(victory_message, width=65)
        for line in wrapped_victory_message:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()
        print("Choose your next action:")
        print("1. Continue Exploring")
        print("2. View Character Status")
        print("3. Open the Glossary")
        self.print_dashes()
        choice = input("What do you want to do? ")

        if choice == '1':
            self.game_loop.update_screen()
        elif choice == '2':
            self.view_character_status()
        elif choice == '3':
            GlossaryScreen(self.location, self.game_loop).display()
        else:
            print("Invalid choice, try again.")
            input("Press Enter to continue...")
            self.display()

    def view_character_status(self):
        self.clear_screen()
        self.print_dashes()
        print(f"Character Status: {self.player.name}".center(self.DASH_WIDTH))
        self.print_dashes()
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Attack: {self.player.strength}")
        print(f"Mana: {self.player.mana}")
        self.print_dashes()
        input("Press Enter to return to victory screen...")
        self.display()

class StateEngine:
    def __init__(self, size=5):
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
