
class NeuralZone:

    def __init__(self, name: str, agent):
        self.container = agent.container
        self.areas = []
        self.name = name
        self.agent = agent

    def on_area_updated(self, area):
        pass
