import random
import os
import csv

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
    
    def cast_spell(self, spell_name, target):
        pass

class Enemy(Character):
    enemies = []

    @classmethod
    def load_enemies_from_csv(cls, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cls.enemies.append({"name": row["name"], "health": int(row["health"]), "attack": int(row["attack"])})

    @staticmethod
    def generate_random_enemy():
        if not Enemy.enemies:
            Enemy.load_enemies_from_csv('src/tests/enemies.csv')
        enemy_info = random.choice(Enemy.enemies)
        return Enemy(enemy_info["name"], enemy_info["health"], enemy_info["attack"])

class Player(Character):
    def __init__(self, name='Player', health=100, attack=25, mana=100):
        super().__init__(name, health, attack, mana)
        self.max_health = 100
        self.unseen_predator_turns = 0

    def heal(self):
        heal_cost = 25
        heal_amount = 50
        if self.mana >= heal_cost and self.health < self.max_health:
            self.mana -= heal_cost
            self.health = min(self.health + heal_amount, self.max_health)
            return heal_amount
        else:
            print("Not enough mana or health is full!")
            return 0

    def cast_spell(self, spell_name, target):
        spell_name = spell_name.lower()
        if spell_name == "heal":
            return self.heal()
        elif spell_name == "smite":
            if target.health <= target.max_health * 0.25:
                damage = random.randint(1, self.strength) * 3
                target.health -= damage
                print(f"Smite deals triple damage! {damage} damage done.")
            else:
                print("Enemy health is too high for Smite.")
            return 0
        elif spell_name == "unseen predator":
            self.is_immune = True
            self.unseen_predator_turns = 3
            print("You've become an Unseen Predator! You will take no damage for 3 turns but deal 50% less damage.")
            return 0
        elif spell_name == "mana reave":
            damage = random.randint(1, self.strength) * 0.25
            target.health -= damage
            self.mana += 50
            print(f"Mana Reave restores 50 mana. {damage} damage dealt to the enemy.")
            return 0
        else:
            print("Spell not recognized.")
            return 0

    def update_effects(self):
        # Call this method each turn to update spell effects
        if self.unseen_predator_turns > 0:
            self.unseen_predator_turns -= 1
            if self.unseen_predator_turns == 0:
                self.is_immune = False
                print("Unseen Predator's effect has worn off.")

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
        # Ensure at least one enemy exists on the map
        if not any(node.enemy for node in self.nodes):
            # Randomly select a location to place an enemy if none exist
            random.choice(self.nodes[1:]).enemy = Enemy.generate_random_enemy()  # Skip Room 0 for enemy placement

class GameScreen:
    def __init__(self, location):
        self.location = location

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_dashes(self, x=72):
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
                self.move_to_location(self.location.connections[int(action) - 1])  # Adjusted to use the new method
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
    def __init__(self, location, player, enemy, game_loop):
        super().__init__(location)
        self.player = player
        self.enemy = enemy
        self.game_loop = game_loop

    def display_health_bars(self):
        # Display Health
        super().print_dashes()
        player_health_blocks = int((self.player.health / self.player.max_health) * 20)
        enemy_health_blocks = int((self.enemy.health / self.enemy.max_health) * 20)
        player_health_bar = f"{'█' * player_health_blocks}{' ' * (20 - player_health_blocks)}"
        enemy_health_bar = f"{'█' * enemy_health_blocks}{' ' * (20 - enemy_health_blocks)}"
        print(f"\nPlayer   HP: {player_health_bar} {self.player.health}/{self.player.max_health}")

        # Display Mana
        max_mana_blocks = 20  # Assuming 100 is the max mana for uniform bar size
        player_mana_blocks = int((self.player.mana / 100) * max_mana_blocks)  # Adjust if your max mana differs
        player_mana_bar = f"{'█' * player_mana_blocks}{' ' * (max_mana_blocks - player_mana_blocks)}"
        print(f"\n       Mana: {player_mana_bar} {self.player.mana}/100")  # Adjust if your max mana differs

        print(f"\n\nEnemy    HP: {enemy_health_bar} {self.enemy.health}/{self.enemy.max_health}\n")
        super().print_dashes()

    def display_combat_options(self):
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

            # Check if player is immune due to Unseen Predator spell
            if not self.player.is_immune:
                damage_taken = self.enemy.attack(self.player)
                print(f"The {self.enemy.name} attacks you for {damage_taken} damage.")
            else:
                print("The Unseen Predator effect protects you. You take no damage this turn.")

        elif action == "2":
            MagicMenuScreen(self.location, self.player).display()
        else:
            print("Invalid action, try again.")

        self.display_health_bars()
        return 'continue'

    def display(self):
        super().print_dashes()
        print(f"You encounter an enemy! The fight begins. It's a {self.enemy.name}.".center(72, ' '))
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
            print("1. Heal - 25 Mana (Heal 50 HP)")
            print("2. Smite - If enemy below 25% HP, deal triple damage")
            print("3. Unseen Predator - Take no damage for 3 turns but deal 50% less damage")
            print("4. Mana Reave - Attack enemy for 75% less damage but restore 50 Mana")
            print("5. Back")
            choice = input("Choose a spell: ")

            if choice == '1':
                healed_amount = self.player.cast_spell("heal", None)  # No target needed for heal
                print(f"Healed for {healed_amount} HP. Current health: {self.player.health}.")
            elif choice in ['2', '3', '4']:
                if not self.location.enemy or not self.location.enemy.is_alive():
                    print("There is no enemy here.")
                else:
                    if choice == '2':
                        self.player.cast_spell("smite", self.location.enemy)
                    elif choice == '3':
                        self.player.cast_spell("unseen predator", None)  # No target needed for unseen predator
                    elif choice == '4':
                        self.player.cast_spell("mana reave", self.location.enemy)
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
            
            input("Press Enter to continue...")
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
