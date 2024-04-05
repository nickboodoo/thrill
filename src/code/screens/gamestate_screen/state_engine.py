from logic.enemy import Enemy
from logic.map import Map
from logic.player import Player
from logic.vendor import Vendor
from screens.exploration_screen import ExplorationScreen
from screens.exploration_screens.combat_screen import CombatScreen
from screens.exploration_screens.vendor_screen import VendorScreen
from screens.gamestate_screen.defeat_screen import DefeatScreen
from screens.gamestate_screen.victory_screen import VictoryScreen


class StateEngine:
    def __init__(self, size=8):
        self.graph = Map(size)
        self.current_node = self.graph.nodes[0]
        self.previous_node = None
        self.player = Player()
        self.coming_from_vendor = False

    def update_screen(self):
        if not self.player.is_alive():
            self.current_screen = DefeatScreen(self.current_node, self)
        elif self.have_defeated_all_enemies():
            self.current_screen = VictoryScreen(self.current_node, self)
        elif isinstance(self.current_node.content, Enemy) and self.current_node.content.is_alive():
            self.current_screen = CombatScreen(self.current_node, self.player, self.current_node.content, self)
        elif isinstance(self.current_node.content, Vendor) and not self.coming_from_vendor:
            self.current_screen = VendorScreen(self.current_node, self.player, self)
            self.coming_from_vendor = True
        else:
            self.current_screen = ExplorationScreen(self.current_node, self)
            self.coming_from_vendor = False

    def play(self):
        while self.player.is_alive() and not self.have_defeated_all_enemies():
            self.update_screen()
            self.current_screen.display()

        if not self.player.is_alive():
            DefeatScreen(self.current_node).display()
        elif self.have_defeated_all_enemies():
            VictoryScreen(self.current_node).display()

    def have_defeated_all_enemies(self):
        return not any(isinstance(node.content, Enemy) and node.content.is_alive() for node in self.graph.nodes)