from screens.game_screen_parent import GameScreen
from screens.glossary_screens.about_game import AboutGameGlossaryScreen
from screens.glossary_screens.enemy_glossary import EnemyGlossaryScreen
from screens.glossary_screens.location_glossary import LocationGlossaryScreen
from screens.glossary_screens.magic_glossary import MagicGlossaryScreen


class GlossaryScreen(GameScreen):
    def display(self):
        while True:
            self.clear_screen()
            self.print_dashes()
            print("Glossary Menu:".center(90))
            self.print_dashes()
            print("1. About the Game")
            print("2. Rooms")
            print("3. Enemies")
            print("4. Spells and Enchantments")
            print("5. Back")
            self.print_dashes()
            choice = input("Choose a category: ")

            if choice == '1':
                AboutGameGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '2':
                LocationGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '3':
                EnemyGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '4':
                MagicGlossaryScreen(self.location, self.game_loop).display()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
            input("Press Enter to continue...")