from logic.magic import Magic


class Vendor:
    def __init__(self):
        self.scrolls = Magic.generate_scrolls()

    def display_items(self):
        for index, scroll in enumerate(self.scrolls):
            print(f"{index + 1}. {scroll.name} - {scroll.lore}")