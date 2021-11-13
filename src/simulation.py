import pygame
import Box2D
from Box2D.examples.framework import Framework
from Box2D.examples.backends.pygame_framework import PygameFramework
from Box2D import b2FixtureDef, b2PolygonShape, b2LoopShape, b2_dynamicBody
from pygame.locals import QUIT, KEYDOWN
from cv.image_processor import ImageProcessor
from agent import Agent


agent = Agent()


class CustomPygameFramework(Box2D.examples.backends.pygame_framework.PygameFramework):

    def __init__(self):
        super().__init__()
        self.f_sys = pygame.font.SysFont('arial', 15)
        self.pixel_array = None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN):
                return False
        return True

    def Print(self, my_str="", color=(229, 153, 153, 255)):
        sc_text = self.f_sys.render(
            'Surprise indicator: %s' % self.agent_message['surprise'], True, color, (0, 0, 0)
        )
        sc_text_2 = self.f_sys.render(
            'Current timeframe: %s' % self.agent_message['current_tick'], True, color, (0, 0, 0)
        )
        text_pos = sc_text.get_rect(topleft=(13, 13))
        text_pos_2 = sc_text.get_rect(topleft=(13, 33))
        self.screen.blit(sc_text, text_pos)
        self.screen.blit(sc_text_2, text_pos_2)

    def run(self):
        running = True
        while running:
            running = self.check_events()
            self.SimulationLoop()
            self.Print()
            self.pixel_array = self.screen
            pygame.display.update()
        self.world.renderer = None


class Simulation(CustomPygameFramework):
    last_step = None
    agent_message = {'surprise': 0, 'current_tick': 0}
    ground_vertices = [(-32, 38), (-32, 0), (32, 0), (32, 38)]

    def __init__(self):
        super(Simulation, self).__init__()
        world = self.world
        world.CreateBody(shapes=b2LoopShape(vertices=self.ground_vertices))
        self.make_up_object(world, vertices=[(-5, 0), (0, 5), (0, 0), ], offset=-10)
        self.make_up_object(world, vertices=[(3, 0), (-5, 0), (0, 3), ], offset=10)

    def make_up_object(self, world, vertices, offset):
        vertices = [(2 * x, 2 * y) for x, y in vertices]
        world.CreateBody(type=b2_dynamicBody,
                         position=(offset, 0),
                         fixtures=b2FixtureDef(shape=b2PolygonShape(vertices=vertices),
                                               density=10,
                                               restitution=0.2),
                         gravityScale=1.0,
                         awake=True)

    def viewing_the_status(self):
        self.cur_step = {
            'data': self.cur_step
        }

    def Step(self, settings):
        img_processor = ImageProcessor(self.world)
        self.cur_step = img_processor.run(self.last_step)
        self.last_step = [obj['center'] for obj in self.cur_step]
        self.viewing_the_status()
        self.agent_message = agent.env_step(self.cur_step)
        super(Simulation, self).Step(settings)


def main(test_class):
    test = test_class()
    test.Step(test.settings)
    test.run()


if __name__ == "__main__":
    main(Simulation)
