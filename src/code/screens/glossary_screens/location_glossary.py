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