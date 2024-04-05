if __name__ == "__main__":
    Magic.load_magic_from_csv('src/tests/scrolls.csv')
    game = StateEngine()
    game.play()