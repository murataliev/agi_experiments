from src.neuro.areas.encoder_area import EncoderArea
from src.neuro.areas.primitives_receptive_area import PrimitivesReceptiveArea
from src.neuro.neural_zone import NeuralZone


class VisualRecognitionZone(NeuralZone):

    def __init__(self, name: str, agent):
        super().__init__(name, agent)
        self._build_areas()

    def _build_areas(self):
        self.primitives_receptive_area = PrimitivesReceptiveArea.add(
            name='receptive area',
            agent=self.agent,
            zone=self,
        )

        self.shape = EncoderArea.add(
            name='simple patterns area',
            agent=self.agent,
            zone=self,
            surprise_level=2,
            recognition_threshold=0.9
        )

        self.shape_abstract = EncoderArea.add(
            name='abstract patterns area',
            agent=self.agent,
            zone=self,
            surprise_level=2,
            recognition_threshold=0.2
        )

        self.container.add_connection(source=self.primitives_receptive_area, target=self.shape)
        self.container.add_connection(source=self.shape, target=self.shape_abstract)

    def activate_on_body(self, body_data):
        self.primitives_receptive_area.activate_on_body(body_data['general_presentation'], body_data['name'])
