from screens.game_screen_parent import GameScreen


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

            elif choice.isdigit():
                choice = int(choice) - 1
                if 0 <= choice < len(self.location.content.scrolls):
                    self.player.buy_item(self.location.content.scrolls[choice])
                else:
                    print("Invalid choice. Please select a valid number or 0 to exit.")
            else:
                print("Please enter a valid number.")

        self.game_loop.update_screen()