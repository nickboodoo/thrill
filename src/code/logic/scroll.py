class Scroll:
    def __init__(self, name, effect, lore, cost):
        self.name = name
        self.effect = effect
        self.lore = lore
        self.cost = cost
        self.quantity = 1

    def use(self, target):
        if self.effect == 'Heal':
            heal_amount = 20
            target.health += heal_amount
            target.health = min(target.health, target.max_health)
            print(f"{target.name} healed for {heal_amount} HP!")