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