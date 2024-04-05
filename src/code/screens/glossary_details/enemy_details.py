from logic.enemy import Enemy
from screens.game_screen_parent import GameScreen


class EnemyDetailScreen(GameScreen):
    def __init__(self, location, enemy):
        super().__init__(location)
        self.enemy = enemy

    def display(self):
        self.clear_screen()
        enemy_info = Enemy.format_enemy_info(self.enemy)
        self.print_dashes()
        print("Enemy Details:".center(90))
        self.print_dashes()
        print(enemy_info)
        self.print_dashes()