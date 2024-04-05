class Location:
    def __init__(self, name, generate_content_flag=True):
        self.name = name
        self.connections = []
        self.visited = False  # Track if visited
        self.content_type = None  # Track the type of content ('enemy', 'vendor', 'none')
        self.content = self.generate_content() if generate_content_flag else None

    def generate_content(self):
        choice = random.choice(['enemy', 'vendor', None])
        self.visited = True
        if choice == 'enemy':
            self.content_type = 'enemy'
            return Enemy.generate_random_enemy()
        elif choice == 'vendor':
            self.content_type = 'vendor'
            return Vendor()
        else:
            self.content_type = 'none'
            return None

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    def generate_enemy(self):
        if random.choice([True, False]):
            return Enemy.generate_random_enemy()
        return None