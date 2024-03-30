import random
import os

class Character:
    def __init__(self, name, health, attack, mana=0):
        self.name = name
        self.health = health
        self.max_health = health  # Initialize max_health with the value of health
        self.strength = attack
        self.mana = mana

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        damage = random.randint(1, self.strength)
        target.health -= damage
        return damage
    
    def cast_spell(self, spell_name, target):
        """Placeholder for casting spells."""
        pass

class Enemy(Character):
    enemies = [
    {"name": "Riverblade Marauder", "health": 35, "attack": 12},
    {"name": "Jungle Stalker", "health": 30, "attack": 7},
    {"name": "Canopy Assassin", "health": 28, "attack": 15},
    {"name": "Swamp Witch", "health": 50, "attack": 8},
    {"name": "Pirate Cannoneer", "health": 40, "attack": 25},
    {"name": "Vine Shaman", "health": 45, "attack": 5},
    {"name": "Mud Golem", "health": 80, "attack": 10},
    {"name": "Crimson Duelist", "health": 35, "attack": 18},
    {"name": "Raptor Rider", "health": 55, "attack": 12},
    {"name": "Serpent Priestess", "health": 40, "attack": 8},
    {"name": "Crocodile Brute", "health": 70, "attack": 15},
    {"name": "Piranha Swarmer", "health": 20, "attack": 5},
    {"name": "Quicksand Guardian", "health": 60, "attack": 10},
    {"name": "Plunder Captain", "health": 65, "attack": 20},
    {"name": "Thunderbird Caller", "health": 50, "attack": 10}
]

    @staticmethod
    def generate_random_enemy():
        enemy_info = random.choice(Enemy.enemies)
        return Enemy(enemy_info["name"], enemy_info["health"], enemy_info["attack"])

class Player(Character):
    def __init__(self, name='Player', health=100, attack=25, mana=100):
        super().__init__(name, health, attack, mana)
        self.max_health = 100

    def heal(self):
        heal_cost = 25
        heal_amount = 50
        if self.mana >= heal_cost and self.health < self.max_health:
            self.mana -= heal_cost
            self.health = min(self.health + heal_amount, self.max_health)  # Ensure health does not exceed max_health
            return heal_amount
        else:
            print("Not enough mana or health is full!")
            return 0
        
    def cast_spell(self, spell_name, target):
        if spell_name.lower() == "heal":
            return self.heal()
        else:
            print("Spell not recognized.")
            return 0

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

    def generate_graph(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].connect(self.nodes[i + 1])
            if i > 0 and random.choice([True, False]):
                self.nodes[i].connect(random.choice(self.nodes[:i]))

class GameScreen:
    def __init__(self, location):
        self.location = location

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_dashes(self, x=30):
        print('-' * x)

    def display(self):
        pass

class VictoryScreen(GameScreen):
    def display(self):
        self.clear_screen()
        print("Congratulations! You have defeated all the enemies and survived.")
        print("You are a true hero!")
        print("\nWould you like to play again? (yes/no)")
        choice = input().lower()
        if choice == 'yes':
            game = GameLoop()
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
            game = GameLoop()
            game.play()
        else:
            print("Thank you for playing! Better luck next time.")
            exit()

class ExplorationScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location)
        self.game_loop = game_loop

    def display(self):
        while True:
            self.clear_screen()
            print(f"You are in {self.location.name}.")
            if self.location.enemy and self.location.enemy.is_alive():
                print(f"An enemy {self.location.enemy.name} is here!")
            print("Connections:")
            for i, connection in enumerate(self.location.connections):
                print(f" {i + 1}: {connection.name}")
            print("\nChoose an action: \n l: List rooms \n [number]: Move to connection \n q: Quit")
            
            action = input("What do you want to do? ")
            self.clear_screen()

            if action == 'l':
                self.display_rooms(self.game_loop.graph.nodes)
            elif action.isdigit() and int(action) - 1 < len(self.location.connections):
                self.game_loop.current_node = self.location.connections[int(action) - 1]
                self.game_loop.current_node.visited = True
                break
            elif action == 'q':
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
    def __init__(self, location, player, enemy, game_loop):  # Add game_loop parameter
        super().__init__(location)
        self.player = player
        self.enemy = enemy
        self.game_loop = game_loop

    def display_health_bars(self):
        player_health_blocks = int((self.player.health / self.player.max_health) * 20)
        enemy_health_blocks = int((self.enemy.health / self.enemy.max_health) * 20)

        # Creating the health bar strings
        player_health_bar = f"{'█' * player_health_blocks}{' ' * (20 - player_health_blocks)}"
        enemy_health_bar = f"{'█' * enemy_health_blocks}{' ' * (20 - enemy_health_blocks)}"

        # Now, use two lines for the print statement to keep it tidy
        print(f"Player   HP: {player_health_bar} {self.player.health}/{self.player.max_health}")
        print(f"\nEnemy    HP: {enemy_health_bar} {self.enemy.health}/{self.enemy.max_health}")

    def display_combat_options(self):
        # self.display_health_bars()  # Display health bars before showing options
        print("Choose your action: \n1. Attack \n2. Magic")

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
        elif action == "2":
            MagicMenuScreen(self.location, self.player).display()
        else:
            print("Invalid action, try again.")
        self.display_health_bars()  # Update and display health bars after actions
        return 'continue'

    def display(self):
        print(f"You encounter an enemy! The fight begins. It's a {self.enemy.name}.")
        self.display_health_bars()
        while self.player.is_alive() and self.enemy.is_alive():
            self.display_combat_options()
            result = self.handle_combat_action()
            if result in ['enemy_defeated', 'fled']:
                break
            if not self.player.is_alive():
                print("Game Over. You have been defeated.")
                break

class MagicMenuScreen(GameScreen):
    def __init__(self, location, player):
        super().__init__(location)
        self.player = player

    def display(self):
        while True:
            self.clear_screen()
            print("Magic Menu:")
            print("1. Heal - 25 Mana")
            print("2. Back")
            choice = input("Choose a spell: ")
            if choice == '1':
                healed_amount = self.player.cast_spell("heal", self.player)
                print(f"Healed for {healed_amount} HP. Current health: {self.player.health}.")
                input("Press Enter to continue...")
                break
            elif choice == '2':
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

class GameLoop:
    def __init__(self, size=3):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None  # Initialize previous_node as None
        self.player = Player()

    def move_to_location(self, new_location):
        if self.current_node is not None:
            self.previous_node = self.current_node
        self.current_node = new_location

    def update_screen(self):
        if not self.player.is_alive():
            self.current_screen = DefeatScreen(self.current_node)
        elif self.have_defeated_all_enemies():
            self.current_screen = VictoryScreen(self.current_node)
        elif self.current_node.enemy and self.current_node.enemy.is_alive():
            # Pass 'self' to provide GameLoop reference to CombatScreen
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
        # Check each node for an alive enemy to accurately reflect the game's win condition
        for node in self.graph.nodes:
            if node.enemy and node.enemy.is_alive():
                return False  # There's at least one enemy alive
        return True  # All enemies are defeated

if __name__ == "__main__":
    game = GameLoop()
    game.play()
