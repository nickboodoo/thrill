class CombatSoulsScreen(GameScreen):
    def __init__(self, location, player, game_loop):
        super().__init__(location, game_loop)
        self.player = player

    def display(self):
        if self.player.souls <= 0:
            print("You have no souls to consume.")
            input("Press Enter to continue...")
            return

        print(f"You have {self.player.souls} souls.")
        print("How would you like to use your souls?")
        print("1. Heal HP")
        print("2. Heal Mana")
        print("3. Buff Attack")
        choice = input("Choose an option: ")

        if choice == '1':
            hp_deficit = self.player.max_health - self.player.health  # Corrected
            hp_to_heal = min(self.player.souls, hp_deficit)
            self.player.health += hp_to_heal
            self.player.souls -= hp_to_heal
            print(f"Healed {hp_to_heal} HP.")
        elif choice == '2':
            mana_deficit = 100 - self.player.mana
            mana_to_heal = min(self.player.souls, mana_deficit)
            self.player.mana += mana_to_heal
            self.player.souls -= mana_to_heal
            print(f"Restored {mana_to_heal} Mana.")
        elif choice == '3':
            if self.player.souls >= 25:
                self.player.strength += 5
                self.player.souls -= 25
                print("Increased attack strength by 5.")
            else:
                print("Not enough souls. You need 25 souls to buff attack.")
        else:
            print("Invalid choice.")
        
        print(f"Remaining souls: {self.player.souls}")
        input("Press Enter to continue...")
        self.clear_screen()