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