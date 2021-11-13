from src.neuro.neural_pattern import NeuralPattern


class NeuralArea:
    def __init__(self, name: str, agent, zone):
        self.agent = agent
        self.container = agent.container
        self.name = name
        self.inputs = []
        self.input_sizes = []
        self.output: NeuralPattern = None
        self.output_space_size = 0
        self.zone = zone
        self.is_receptive = False

    @classmethod
    def add(cls, name, agent, zone, **kwargs) -> 'NeuralArea':
        area = cls(name, agent, zone, **kwargs)
        agent.container.add_area(area)
        zone.areas.append(area)
        return area

    def update(self):
        self.zone.on_area_updated(self)
