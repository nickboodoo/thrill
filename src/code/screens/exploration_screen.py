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