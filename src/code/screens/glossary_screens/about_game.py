import textwrap
from screens.game_screen_parent import GameScreen


class AboutGameGlossaryScreen(GameScreen):
    def __init__(self, location, game_loop):
        super().__init__(location, game_loop)

    def display(self):
        self.clear_screen()
        self.print_dashes()
        print("About the Game".center(self.DASH_WIDTH))
        self.print_dashes()

        game_about_lore_sections = [
            "Seek the Thrill of the Hunt.",
            "Consume the souls of the fallen to gain new strength.",
            "Fight your way through this hostile jungle for the glory of the Hunt."
        ]

        for section in game_about_lore_sections:
            wrapped_section = textwrap.wrap(section, width=75)
            for line in wrapped_section:
                print(line.center(90))
            print("\n".center(90))  

        self.print_dashes()
        input("\nPress Enter to return to the Glossary...")