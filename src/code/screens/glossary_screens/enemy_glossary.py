from logic.enemy import Enemy
from screens.game_screen_parent import GameScreen
from screens.glossary_details.enemy_details import EnemyDetailScreen


class EnemyGlossaryScreen(GameScreen):
    MAX_ENTRIES_PER_COLUMN = 10

    def display(self):
        self.display_enemies()

    def display_enemies(self):
        self.clear_screen()
        self.print_dashes()
        print("Select an enemy to learn more:".center(90))
        self.print_dashes()
        enemies = Enemy.enemies

        columns = (len(enemies) + self.MAX_ENTRIES_PER_COLUMN - 1) // self.MAX_ENTRIES_PER_COLUMN

        max_name_length = max(len(enemy["name"]) for enemy in enemies) + 4
        column_width = max_name_length + len(str(len(enemies))) + 2

        for i in range(self.MAX_ENTRIES_PER_COLUMN):
            row = []
            for j in range(columns):
                index = i + j * self.MAX_ENTRIES_PER_COLUMN
                if index < len(enemies):
                    cell = f"{index + 1}. {enemies[index]['name']}".ljust(column_width)
                    row.append(cell)
            if row:
                print("".join(row))

        print("\n0. Back")
        self.print_dashes()
        choice = input("\nEnter your choice: ")
        self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            elif 1 <= choice <= len(Enemy.enemies):
                selected_enemy = Enemy.enemies[choice - 1]
                EnemyDetailScreen(self.location, selected_enemy).display()
            else:
                print("Invalid choice.")
                input("Press Enter to try again...")
                self.display_enemies()
        else:
            print("Please enter a number.")
            input("Press Enter to try again...")
            self.display_enemies()