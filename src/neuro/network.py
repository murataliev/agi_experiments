from src.neuro.container import Container


class Network:

    def __init__(self, container: Container, agent: None):
        self.container = container
        self.agent = agent
        self.current_tick = 0
        self.verbose = True
        self.container.network = self

    def step(self):
        self.current_tick += 1

        for area in self.container.areas:
            area.update()

        for connection in self.container.connections:
            connection.update()
