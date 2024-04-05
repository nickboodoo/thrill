from logic.magic import Magic
from screens.gamestate_screen.state_engine import StateEngine


if __name__ == "__main__":
    Magic.load_magic_from_csv('src/data/scrolls.csv')
    game = StateEngine()
    game.play()