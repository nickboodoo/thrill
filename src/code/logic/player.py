from logic.character import Character


class Player(Character):
    def __init__(self, name='Player', health=100, attack=25, mana=100):
        super().__init__(name, health, attack, mana)
        self.max_health = health
        self.inventory = []
        self.souls = 0

    def add_souls(self, amount):
        self.souls += amount
        print(f"You found {amount} souls!")
    
    def buy_item(self, item):
        if self.souls >= item.cost:
            self.souls -= item.cost
            self.add_item(item)
            print(f"{item.name} purchased successfully. You spent {item.cost} souls.")
        else:
            print("Not enough souls to purchase this item.")