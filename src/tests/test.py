import random
import os
import csv
import textwrap
import logging

logging.basicConfig(level=logging.DEBUG)

#==========================================#
#              LOGIC CLASSES               #
#              -------------               #
#==========================================#

LORE_TEXT_WIDTH = 65

class CSVLoader:
    cache = {}

    @staticmethod
    def load_csv(filepath, key_mapping=None, preprocess=None, use_cache=True):
        if use_cache and filepath in CSVLoader.cache:
            return CSVLoader.cache[filepath]

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            for row in reader:
                if key_mapping:
                    row = {key_mapping.get(k, k): v for k, v in row.items()}
                if preprocess:
                    row = preprocess(row)
                items.append(row)

        if use_cache:
            CSVLoader.cache[filepath] = items
        return items

def preprocess_magic_data(row):
    # Extracting cost and handling non-integer formats
    cost_str = row["Cost"]
    try:
        # Assuming the format could be 'X:X Mana:Souls' and you need the first part as an integer cost
        cost = int(cost_str.split()[0])  # This splits the string and converts the first part to integer
    except ValueError:
        cost = 0  # Default value if conversion fails

    return {
        "type": row["Type"],
        "name": row["Name"],
        "effect": row["Effect"],
        "cost": cost,
        "lore": row.get("Lore", "No lore available."),
        "lore2": row.get("Lore2", "Ancient secrets remain untold.")
    }

class Scroll:
    def __init__(self, name, effect, lore, cost):
        self.name = name
        self.effect = effect
        self.lore = lore
        self.cost = cost
        self.quantity = 1

class Character:
    def __init__(self, name, health, attack, mana=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = attack
        self.mana = mana
        self.is_immune = False
        self.inventory = []

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
        if item in self.inventory and isinstance(item, Scroll):
            item.use(target or self)
            item.quantity -= 1
            if item.quantity <= 0:
                self.remove_item(item)

class Enemy(Character):
    enemies = []

    @classmethod
    def load_enemies(cls):
        filepath = 'src/tests/enemies.csv'
        cls.enemies = CSVLoader.load_csv(filepath, preprocess=preprocess_enemy_data)

    @staticmethod
    def generate_random_enemy():
        if not Enemy.enemies:
            Enemy.load_enemies_from_csv('src/tests/enemies.csv')
        enemy_info = random.choice(Enemy.enemies)
        return Enemy(enemy_info["name"], enemy_info["health"], enemy_info["attack"])

    @staticmethod
    def format_enemy_info(enemy):
        wrapped_lore_lines = textwrap.wrap(enemy["lore"], width=LORE_TEXT_WIDTH)
        centered_lore = "\n".join(line.center(LORE_TEXT_WIDTH) for line in wrapped_lore_lines)
        info = f'{enemy["name"]} ({enemy["health"]} HP, {enemy["attack"]} Attack):\n{centered_lore}'
        return info

class Player(Character):
    def __init__(self, name='Player', health=100, attack=25, mana=100):
        super().__init__(name, health, attack, mana)
        self.max_health = health
        self.inventory = []
        self.souls = 0

    def add_souls(self, amount):
        self.souls += amount
        print(f"You found {amount} souls!")
    
    def buy_item(self, item):
        if self.souls >= item.cost:
            self.souls -= item.cost
            self.add_item(item)
            print(f"{item.name} purchased successfully. You spent {item.cost} souls.")
        else:
            print("Not enough souls to purchase this item.")

class Vendor:
    def __init__(self):
        self.scrolls = Magic.generate_scrolls()

    def display_items(self):
        for index, scroll in enumerate(self.scrolls):
            print(f"{index + 1}. {scroll.name} - {scroll.lore}")

class Magic:
    items = []

    @classmethod
    def load_magic(cls):
        filepath = 'src/tests/scrolls.csv'
        cls.items = CSVLoader.load_csv(filepath, preprocess=preprocess_magic_data)

    @classmethod
    def generate_scrolls(cls):
        scrolls = []
        for item in cls.items:
            if item["type"].lower() in ["spell", "enchantment"]:
                # Make sure to convert the 'cost' from string to an integer
                scroll = Scroll(name=item["name"], effect=item["effect"], lore=item.get("lore", "No lore available."), cost=int(item["cost"]))
                scrolls.append(scroll)
        return scrolls

    @staticmethod
    def format_magic_info(magic):
        name_and_effect = f'{magic["name"]} - {magic["effect"]} ({magic["cost"]})\n'
        lore = f'"{magic["lore"]}"\n'
        lore2 = f'"{magic["lore2"]}"\n'
        wrapped_lore_lines = textwrap.wrap(lore, width=50)
        wrapped_lore2_lines = textwrap.wrap(lore2, width=50)
        centered_lore_lines = [line.center(50) for line in wrapped_lore_lines]
        centered_lore2_lines = [line.center(50) for line in wrapped_lore2_lines]
        centered_lore = "\n".join(centered_lore_lines)
        centered_lore2 = "\n".join(centered_lore2_lines)
        info = f"{name_and_effect}\n{centered_lore}\n{centered_lore2}"
        return info

class Location:
    def __init__(self, name, generate_content_flag=True):
        self.name = name
        self.connections = []
        self.visited = False  # Track if visited
        self.content_type = None  # Track the type of content ('enemy', 'vendor', 'none')
        self.content = self.generate_content() if generate_content_flag else None

    def generate_content(self):
        choice = random.choice(['enemy', 'vendor', None])
        self.visited = True
        if choice == 'enemy':
            self.content_type = 'enemy'
            return Enemy.generate_random_enemy()
        elif choice == 'vendor':
            self.content_type = 'vendor'
            return Vendor()
        else:
            self.content_type = 'none'
            return None

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    def generate_enemy(self):
        if random.choice([True, False]):
            return Enemy.generate_random_enemy()
        return None

class Map:
    def __init__(self, size, locations_csv_path='src/tests/locations.csv'):
        self.nodes = [Location("Soulink Shrine", generate_content_flag=False)]
        location_names = self.load_location_names(locations_csv_path)
        random.shuffle(location_names)
        extended_location_names = (location_names * ((size // len(location_names)) + 1))[:size-1]
        self.nodes += [Location(name, generate_content_flag=True) for name in extended_location_names]
        
        self.generate_graph()
        self.ensure_at_least_one_enemy()

    def load_location_names(self, csv_path):
        names = []
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                names.append(row['Location'])
        return names

    def generate_graph(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].connect(self.nodes[i + 1])
            if i > 0 and random.choice([True, False]):
                self.nodes[i].connect(random.choice(self.nodes[:i]))

    def ensure_at_least_one_enemy(self):
        if not any(isinstance(node.content, Enemy) for node in self.nodes):
            chosen_location = random.choice(self.nodes[1:])
            chosen_location.content = Enemy.generate_random_enemy()

#==========================================#
#             USER INTERFACES              #
#             ---------------              #
#==========================================#


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

#==========================================#
#               GAMELOOP UI                #
#==========================================#

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
            print("4. Spells and Enchantments")
            print("5. Back")
            self.print_dashes()
            choice = input("Choose a category: ")

            if choice == '1':
                AboutGameGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '2':
                LocationGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '3':
                EnemyGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '4':
                MagicGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
            input("Press Enter to continue...")

class InventoryScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Inventory".center(self.DASH_WIDTH))
        self.print_dashes()
        print(f"Souls: {self.player.souls}")
        self.print_dashes()
        if self.player.inventory:
            for index, item in enumerate(self.player.inventory, start=1):
                print(f"{index}. {item.name} - {item.description} (x{item.quantity})")
        else:
            print("Your inventory is empty.")
        self.print_dashes()
        print("Select an item to use or 0 to exit:")
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(self.player.inventory):
                item = self.player.inventory[choice - 1]
                self.player.use_item(item)
            elif choice == 0:
                return
        else:
            print("Invalid selection.")

class ExplorationScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location)
        self.game_loop = game_loop

    def move_to_location(self, new_location):
        self.game_loop.previous_node = self.game_loop.current_node
        new_location.visited = True
        self.game_loop.current_node = new_location

    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print(f"You are in {self.location.name}.".center(self.DASH_WIDTH))
            self.print_dashes()
            if isinstance(self.location.content, Enemy) and self.location.content.is_alive():
                print(f"An enemy {self.location.content.name} is here!")
            elif isinstance(self.location.content, Vendor):
                print("A mysterious vendor is here, offering scrolls of magical power.")
            print("Connections:")
            for i, connection in enumerate(self.location.connections):
                print(f" {i + 1}: {connection.name}")
            self.print_dashes()
            print("Choose an action: \n [G]: Glossary \n [I]: Inventory \n [#]: Move to room \n [Q]: Quit")
            self.print_dashes()
            action = input("What do you want to do? ")
            self.clear_screen()

            if action.lower() == 'g':
                GlossaryScreen(self.location, self.game_loop).display()
            elif action.lower() == 'i':
                InventoryScreen(self.location, self.game_loop.player, self.game_loop).display()
            elif action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.move_to_location(self.location.connections[int(action) - 1])
                break
            elif action.lower() == 'q':
                exit()
            else:
                print("Invalid action, try again.")
                input("Press Enter to continue...")
                self.clear_screen()

#==========================================#
#         GLOSSARY SUBDIRECTORY UI         #
#==========================================#


class AboutGameGlossaryScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("About the Game".center(self.DASH_WIDTH))
        self.print_dashes()

        game_about_lore_sections = [
            "Seek the Thrill of the Hunt.",
            "Consume the souls of the fallen to gain new strength.",
            "Fight your way through this hostile jungle for the glory of the Hunt."
        ]

        for section in game_about_lore_sections:
            wrapped_section = textwrap.wrap(section, width=75)
            for line in wrapped_section:
                print(line.center(90))
            print("\n".center(90))  

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
    MAX_ENTRIES_PER_COLUMN = 10

    def display(self):
        self.display_magic()

    def display_magic(self):
        self.clear_screen()
        self.print_dashes()
        print("Select a magic item to learn more:".center(self.DASH_WIDTH))
        self.print_dashes()

        abilities = [item for item in Magic.items if item['type'].lower() == 'ability']
        spells = [item for item in Magic.items if item['type'].lower() == 'spell']
        enchantments = [item for item in Magic.items if item['type'].lower() == 'enchantment']

        magic_items = abilities + spells + enchantments
        indexed_magic_items = {i + 1: item for i, item in enumerate(magic_items)}

        max_rows = max(len(abilities), len(spells), len(enchantments))

        print(f"{'Abilities'.center(30)}{'Spells'.center(30)}{'Enchantments'.center(30)}")
        self.print_dashes()

        for i in range(max_rows):
            ability = f"{i + 1}. {abilities[i]['name']}" if i < len(abilities) else ''
            spell = f"{i + len(abilities) + 1}. {spells[i]['name']}" if i < len(spells) else ''
            enchantment = f"{i + len(abilities) + len(spells) + 1}. {enchantments[i]['name']}" if i < len(enchantments) else ''
            
            print(f"{ability.ljust(30)}{spell.ljust(30)}{enchantment.ljust(30)}")

        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice: ")

        self.handle_choice(choice, indexed_magic_items)

    def handle_choice(self, choice, indexed_magic_items):
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            elif choice in indexed_magic_items:
                selected_magic = indexed_magic_items[choice]
                details_screen = MagicDetailsGlossary(self.location, selected_magic, self.game_loop)
                details_screen.display()
                self.display_magic()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
                self.display_magic()
        else:
            print("Please enter a number.")
            input("Press Enter to continue...")
            self.display_magic()

class LocationGlossaryScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("Rooms List:".center(90))
        self.print_dashes()
        for i, node in enumerate(self.game_loop.graph.nodes):
            print(f"{i + 1}. {node.name}")
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
        detail_screen = LocationDetailScreen(self.location, self.game_loop, node)
        detail_screen.display()

#==========================================#
#     GLOSSARY DETAILS SUBDIRECTORY UI     #
#==========================================#


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
        self.WRAP_WIDTH = 75

    def display(self):
        self.clear_screen()
        self.print_dashes()

        wrapped_header = textwrap.wrap(f"{self.magic_item['name']} - {self.magic_item['effect']} ({self.magic_item['cost']})", 
                                       width=self.WRAP_WIDTH)
        for line in wrapped_header:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()

        wrapped_lore_lines = textwrap.wrap(self.magic_item['lore'], width=self.WRAP_WIDTH)
        wrapped_lore2_lines = textwrap.wrap(self.magic_item['lore2'], width=self.WRAP_WIDTH)
        for line in wrapped_lore_lines:
            print(line.center(self.DASH_WIDTH))
        print('')
        for line in wrapped_lore2_lines:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()
        input("\nPress Enter to go back...")

class LocationDetailScreen(GameScreen):
    def __init__(self, location, game_loop, room):
        super().__init__(location, game_loop)
        self.location = room

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print(f"Room Details: {self.location.name}".center(self.DASH_WIDTH))
        self.print_dashes()
        print("Connections and Encounters:")
        for i, connected_node in enumerate(self.location.connections):
            visit_status = "Not Visited" if not connected_node.visited else connected_node.content_type.capitalize()
            print(f" {i + 1}. {connected_node.name} - {visit_status}")
        self.print_dashes()
        input("Press Enter to return...")


#==========================================#
#       EXPLORATION SUBDIRECTORY UI        #
#==========================================#

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
        print("Choose your action:")
        print("1. Attack")
        print("2. Consume Souls")
        print("3. Forsake Your Humanity")

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
            if self.player.souls > 0:
                souls_screen = CombatSoulsScreen(self.location, self.player, self.game_loop)
                souls_screen.display()
            else:
                print("You have no souls to consume.")

        elif action == "3":
            if self.player.mana > 0:
                transpose_screen = TransposeManaScreen(self.location, self.player, self.game_loop)
                transpose_screen.display()
            else:
                print("You have no mana to consume.")

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

class VendorScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print("Welcome to the Vendor's Shop!".center(self.DASH_WIDTH))
            self.print_dashes()
            for index, scroll in enumerate(self.location.content.scrolls, start=1):
                print(f"{index}. {scroll.name} - Cost: {scroll.cost} souls")
            self.print_dashes()
            print("Select a scroll to purchase, or 0 to exit:")
            choice = input("Your choice: ").strip()

            if choice == '0':
                print("Exiting the Vendor's Shop...")
                self.game_loop.coming_from_vendor = False
                break

            else:
                print("Please enter '0' This code is not implemented yet.")

        self.game_loop.update_screen()


#==========================================#
#          COMBAT SUBDIRECTORY UI          #
#==========================================#


class CombatSoulsScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        if self.player.souls <= 0:
            print("You have no souls to consume.")
            input("Press Enter to continue...")
            return

        print(f"You have {self.player.souls} souls.")
        print("How would you like to use your souls?")
        print("1. Heal HP")
        print("2. Heal Mana")
        print("3. Buff Attack")
        choice = input("Choose an option: ")

        if choice == '1':
            hp_deficit = self.player.max_health - self.player.health  # Corrected
            hp_to_heal = min(self.player.souls, hp_deficit)
            self.player.health += hp_to_heal
            self.player.souls -= hp_to_heal
            print(f"Healed {hp_to_heal} HP.")
        elif choice == '2':
            mana_deficit = 100 - self.player.mana
            mana_to_heal = min(self.player.souls, mana_deficit)
            self.player.mana += mana_to_heal
            self.player.souls -= mana_to_heal
            print(f"Restored {mana_to_heal} Mana.")
        elif choice == '3':
            if self.player.souls >= 25:
                self.player.strength += 5
                self.player.souls -= 25
                print("Increased attack strength by 5.")
            else:
                print("Not enough souls. You need 25 souls to buff attack.")
        else:
            print("Invalid choice.")
        
        print(f"Remaining souls: {self.player.souls}")
        input("Press Enter to continue...")
        self.clear_screen()

class CombatVictoryScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        souls_reward = random.randint(2, 100)
        self.player.add_souls(souls_reward)
        
        self.clear_screen()
        self.print_dashes()
        print("Victory!".center(self.DASH_WIDTH))
        self.print_dashes()

        victory_message = f"You have defeated the enemy in {self.location.name}! " \
                          f"You take a moment to catch your breath and prepare for the next challenge. " \
                          f"You found {souls_reward} souls!"
        
        wrapped_victory_message = textwrap.wrap(victory_message, width=65)
        for line in wrapped_victory_message:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()
        print(f"Total Souls: {self.player.souls}")
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

class TransposeManaScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        print(f"Current Mana: {self.player.mana}")
        print("How much mana do you want to transpose into souls? (0 to cancel)")
        
        while True:
            try:
                mana_to_transpose = input("Enter amount: ")
                if mana_to_transpose.strip() == "0" or mana_to_transpose.strip() == "":
                    print("Transpose cancelled.")
                    break
                mana_to_transpose = int(mana_to_transpose)
                if 0 < mana_to_transpose <= self.player.mana:
                    self.player.mana -= mana_to_transpose
                    self.player.add_souls(mana_to_transpose)
                    print(f"Transposed {mana_to_transpose} mana into souls.")
                    break
                else:
                    print("Invalid amount. Please enter a number between 1 and your current mana, or 0 to cancel.")
            except ValueError:
                print("Please enter a valid number.")
        input("Press Enter to continue...")
        self.clear_screen()

#==========================================#
#              GAME ENDING UI              #
#==========================================#


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

#==========================================#
#       STATE ENGINE (UI CONTROLLER)       #
#==========================================#


class StateEngine:
    def __init__(self, size=8):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None
        self.player = Player()
        self.coming_from_vendor = False

    def update_screen(self):
        if not self.player.is_alive():
            self.current_screen = DefeatScreen(self.current_node, self)
        elif self.have_defeated_all_enemies():
            self.current_screen = VictoryScreen(self.current_node, self)
        elif isinstance(self.current_node.content, Enemy) and self.current_node.content.is_alive():
            self.current_screen = CombatScreen(self.current_node, self.player, self.current_node.content, self)
        # Check if the current content is a Vendor and if we are not coming from the vendor screen
        elif isinstance(self.current_node.content, Vendor) and not self.coming_from_vendor:
            self.current_screen = VendorScreen(self.current_node, self.player, self)
            self.coming_from_vendor = True  # Set the flag when entering the vendor screen
        else:
            self.current_screen = ExplorationScreen(self.current_node, self)
            self.coming_from_vendor = False  # Reset the flag to ensure correct flow for next interactions




    def play(self):
        while self.player.is_alive() and not self.have_defeated_all_enemies():
            self.update_screen()
            self.current_screen.display()

        if not self.player.is_alive():
            DefeatScreen(self.current_node).display()
        elif self.have_defeated_all_enemies():
            VictoryScreen(self.current_node).display()

    def have_defeated_all_enemies(self):
        # Iterate through each node in the graph and check if the content is an Enemy and if it's alive
        return not any(isinstance(node.content, Enemy) and node.content.is_alive() for node in self.graph.nodes)

#==========================================#
#             MODULE  CHECKING             #
#==========================================#

if __name__ == "__main__":
    Magic.load_magic()  # Updated method name
    game = StateEngine()
    game.play()
