from logic.magic import Magic
from screens.game_screen_parent import GameScreen
from screens.glossary_details.magic_details import MagicDetailsGlossary


class MagicGlossaryScreen(GameScreen):
    MAX_ENTRIES_PER_COLUMN = 10

    def display(self):
        self.display_magic()

    def display_magic(self):
        self.clear_screen()
        self.print_dashes()
        print("Select a magic item to learn more:".center(self.DASH_WIDTH))
        self.print_dashes()

        abilities = [item for item in Magic.items if item['type'].lower() == 'ability']
        spells = [item for item in Magic.items if item['type'].lower() == 'spell']
        enchantments = [item for item in Magic.items if item['type'].lower() == 'enchantment']

        magic_items = abilities + spells + enchantments
        indexed_magic_items = {i + 1: item for i, item in enumerate(magic_items)}

        max_rows = max(len(abilities), len(spells), len(enchantments))

        print(f"{'Abilities'.center(30)}{'Spells'.center(30)}{'Enchantments'.center(30)}")
        self.print_dashes()

        for i in range(max_rows):
            ability = f"{i + 1}. {abilities[i]['name']}" if i < len(abilities) else ''
            spell = f"{i + len(abilities) + 1}. {spells[i]['name']}" if i < len(spells) else ''
            enchantment = f"{i + len(abilities) + len(spells) + 1}. {enchantments[i]['name']}" if i < len(enchantments) else ''
            
            print(f"{ability.ljust(30)}{spell.ljust(30)}{enchantment.ljust(30)}")

        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice: ")

        self.handle_choice(choice, indexed_magic_items)

    def handle_choice(self, choice, indexed_magic_items):
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            elif choice in indexed_magic_items:
                selected_magic = indexed_magic_items[choice]
                details_screen = MagicDetailsGlossary(self.location, selected_magic, self.game_loop)
                details_screen.display()
                self.display_magic()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
                self.display_magic()
        else:
            print("Please enter a number.")
            input("Press Enter to continue...")
            self.display_magic()