import textwrap
from screens.game_screen_parent import GameScreen


class MagicDetailsGlossary(GameScreen):
    def __init__(self, location, magic_item, game_loop=None):
        super().__init__(location, game_loop)
        self.magic_item = magic_item
        self.WRAP_WIDTH = 75

    def display(self):
        self.clear_screen()
        self.print_dashes()

        wrapped_header = textwrap.wrap(f"{self.magic_item['name']} - {self.magic_item['effect']} ({self.magic_item['cost']})", 
                                       width=self.WRAP_WIDTH)
        for line in wrapped_header:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()

        wrapped_lore_lines = textwrap.wrap(self.magic_item['lore'], width=self.WRAP_WIDTH)
        wrapped_lore2_lines = textwrap.wrap(self.magic_item['lore2'], width=self.WRAP_WIDTH)
        for line in wrapped_lore_lines:
            print(line.center(self.DASH_WIDTH))
        print('')
        for line in wrapped_lore2_lines:
            print(line.center(self.DASH_WIDTH))

        self.print_dashes()
        input("\nPress Enter to go back...")