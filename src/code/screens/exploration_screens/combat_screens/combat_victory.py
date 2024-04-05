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