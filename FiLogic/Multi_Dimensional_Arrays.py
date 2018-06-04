# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Array file for [PROJECT NAME].
"""
import FiLogic.Variables as FiVar
import pygame
import numpy
import decimal


key_to_function = {
    pygame.K_RIGHT: (lambda x: x.translate([-10, 0, 0])),
    pygame.K_LEFT: (lambda x: x.translate([10, 0, 0])),
    pygame.K_UP: (lambda x: x.translate([0, 10, 0])),
    pygame.K_DOWN: (lambda x: x.translate([0, -10, 0])),
    4: (lambda x: x.scale(1.25, True)),
    5: (lambda x: x.scale(0.8, True)),
    pygame.K_EQUALS: (lambda x: x.scale(1.25)),
    pygame.K_MINUS: (lambda x: x.scale(0.8)),
    pygame.K_q: (lambda x: x.rotate_x(0.1)),
    pygame.K_w: (lambda x: x.rotate_x(-0.1)),
    pygame.K_a: (lambda x: x.rotate_y(0.1)),
    pygame.K_s: (lambda x: x.rotate_y(-0.1)),
    pygame.K_z: (lambda x: x.rotate_z(0.1)),
    pygame.K_x: (lambda x: x.rotate_z(-0.1))
}


class ThreeDimensionalRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.objects = {}
        self.mouse_pos = pygame.mouse.get_pos()
        self.active_text = False

    def update(self, name=None, given_object=None):
        if name is not None and given_object is not None:
            self.objects[name] = given_object
        else:
            for object_ in self.objects.values():
                for n1, n2 in object_.edges:
                    pygame.draw.aaline(self.screen, FiVar.colors["white"], object_.nodes[n1][:2], object_.nodes[n2][:2],
                                       1)
                for node in object_.nodes:
                    pygame.draw.circle(self.screen, FiVar.colors["white"], (numpy.int_(node[0]),
                                                                            numpy.int_(node[1])), 4, 0)
                    if self.active_text:
                        self.screen.blit(FiVar.tnr_20.render(f"{round(node[0]), round(node[1])}", True,
                                                             FiVar.colors["green"]),
                                         (numpy.int_(node[0]), numpy.int_(node[1])))

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key](self)
            if event.key == pygame.K_t:
                if not self.active_text:
                    self.active_text = True
                elif self.active_text:
                    self.active_text = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(self.screen, FiVar.colors["white"], self.mouse_pos, 4)
            if event.button in key_to_function:
                key_to_function[event.button](self)
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                self.translate([(pygame.mouse.get_pos()[0] - self.mouse_pos[0]), 0, 0])
                self.translate([0, (pygame.mouse.get_pos()[1] - self.mouse_pos[1]), 0])
            if pygame.mouse.get_pressed()[1]:
                self.rotate_y((pygame.mouse.get_pos()[0] - self.mouse_pos[0]) / 100)
                self.rotate_x((pygame.mouse.get_pos()[1] - self.mouse_pos[1]) / 100)
            self.mouse_pos = pygame.mouse.get_pos()

    def translate(self, vector):
        matrix = ThreeDimensionalObject.translation_matrix(*vector)
        for object_ in self.objects.values():
            object_.transform(matrix)

    def scale(self, scale, mouse=False):
        if mouse:
            centre = [int(axis) for axis in pygame.mouse.get_pos()]
        else:
            centre = [int(axis/2) for axis in self.screen.get_size()]
        matrix = ThreeDimensionalObject.scale_matrix(scale, scale, scale)
        for object_ in self.objects.values():
            object_.transform(ThreeDimensionalObject.translation_matrix(-centre[0], -centre[1], 0))
            object_.transform(matrix)
            object_.transform(ThreeDimensionalObject.translation_matrix(*centre, 0))

    def rotate_x(self, radians):
        matrix = ThreeDimensionalObject.rotate_x_matrix(radians)
        for object_ in self.objects.values():
            centre = object_.find_centre()
            object_.transform(ThreeDimensionalObject.translation_matrix(-centre[0], -centre[1], -centre[2]))
            object_.transform(matrix)
            object_.transform(ThreeDimensionalObject.translation_matrix(*centre))

    def rotate_y(self, radians):
        matrix = ThreeDimensionalObject.rotate_y_matrix(radians)
        for object_ in self.objects.values():
            centre = object_.find_centre()
            object_.transform(ThreeDimensionalObject.translation_matrix(-centre[0], -centre[1], -centre[2]))
            object_.transform(matrix)
            object_.transform(ThreeDimensionalObject.translation_matrix(*centre))

    def rotate_z(self, radians):
        matrix = ThreeDimensionalObject.rotate_z_matrix(radians)
        for object_ in self.objects.values():
            centre = object_.find_centre()
            object_.transform(ThreeDimensionalObject.translation_matrix(-centre[0], -centre[1], -centre[2]))
            object_.transform(matrix)
            object_.transform(ThreeDimensionalObject.translation_matrix(*centre))


class ThreeDimensionalObject:
    def __init__(self):
        self.nodes = numpy.zeros((0, 4))
        self.edges = []

    def add_nodes(self, node_array):
        ones_column = numpy.ones((len(node_array), 1))
        ones_added = numpy.hstack((node_array, ones_column))
        self.nodes = numpy.vstack((self.nodes, ones_added))

    def add_edges(self, edgelist):
        self.edges += edgelist

    def find_centre(self):
        num_nodes = len(self.nodes)
        mean_x = sum([node[0] for node in self.nodes]) / num_nodes
        mean_y = sum([node[1] for node in self.nodes]) / num_nodes
        mean_z = sum([node[2] for node in self.nodes]) / num_nodes

        return [mean_x, mean_y, mean_z]

    def transform(self, matrix):
        self.nodes = numpy.dot(self.nodes, matrix)

    @staticmethod
    def translation_matrix(dx=0, dy=0, dz=0):
        return numpy.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [dx, dy, dz, 1]])

    @staticmethod
    def scale_matrix(sx=0, sy=0, sz=0):
        return numpy.array([[sx, 0, 0, 0],
                            [0, sy, 0, 0],
                            [0, 0, sz, 0],
                            [0, 0, 0, 1]])

    @staticmethod
    def rotate_x_matrix(radians):
        c = numpy.cos(radians)
        s = numpy.sin(radians)
        return numpy.array([[1, 0, 0, 0],
                            [0, c, -s, 0],
                            [0, s, c, 0],
                            [0, 0, 0, 1]])

    @staticmethod
    def rotate_y_matrix(radians):
        c = numpy.cos(radians)
        s = numpy.sin(radians)
        return numpy.array([[c, 0, s, 0],
                            [0, 1, 0, 0],
                            [-s, 0, c, 0],
                            [0, 0, 0, 1]])

    @staticmethod
    def rotate_z_matrix(radians):
        c = numpy.cos(radians)
        s = numpy.sin(radians)
        return numpy.array([[c, -s, 0, 0],
                            [s, c, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
