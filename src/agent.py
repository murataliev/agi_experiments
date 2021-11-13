from neuro.container import Container
from neuro.network import Network
from src.neuro.zones.visual_recognition_zone import VisualRecognitionZone


class Agent:

    def __init__(self):
        self.container = Container()
        self._build_network()
        self.network = Network(container=self.container, agent=self)
        self.focused_body_idx = None
        self.surprise = 0
        self.areas_reported = {}

    def _build_network(self):
        self.zone = VisualRecognitionZone(name='VR', agent=self)

    def on_message(self, data):
        if data == 'pattern_created':
            self.surprise += 1
        elif data['message'] == 'encoder':
            area_name = data['area'].name
            if area_name not in self.areas_reported:
                self.areas_reported[area_name] = 0
            if self.areas_reported[area_name] > 1:
                return
            pattern = data['pattern']
            if data['is_new']:
                print(f'Area "{area_name}" created a new pattern {pattern.data}')
            else:
                print(
                    f'Area "{area_name}" recognized an existing pattern {pattern.data}, similarity={data["similarity"]}'
                )
            self.areas_reported[area_name] += 1

    def activate_receptive_areas(self, packet):
        data = packet['data']
        if len(data) == 0 or len(data) > 3:
            return

        data[0]['name'] = 'shape 1'
        data[1]['name'] = 'shape 2'
        previous_focused_body_idx = self.focused_body_idx

        if self.focused_body_idx is None:
            self.focused_body_idx = 0
        elif self.focused_body_idx >= len(data) - 1:
            self.focused_body_idx = 0
        else:
            self.focused_body_idx += 1

        prev_body_data = None

        if previous_focused_body_idx:
            prev_body_data = data[previous_focused_body_idx]

        body_data = data[self.focused_body_idx]
        self._serial_activate_on_body(body_data, prev_body_data)

    def _serial_activate_on_body(self, body_data, prev_body_data):
        self.zone.activate_on_body(body_data)
        self.surprise = 0
        self.network.verbose = False
        self.network.step()

    def env_step(self, packet):
        self.activate_receptive_areas(packet)

        if self.container.network.verbose:
            print(f'Surprise: {self.surprise}')

        return {
            'current_tick': self.network.current_tick + 1,
            'surprise': self.surprise,
        }
