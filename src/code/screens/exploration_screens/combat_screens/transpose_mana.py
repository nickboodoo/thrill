from screens.game_screen_parent import GameScreen


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