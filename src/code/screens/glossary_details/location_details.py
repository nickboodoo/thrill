from screens.game_screen_parent import GameScreen


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