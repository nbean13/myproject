from manim import *
from math import *
import numpy as np

class Solids(ThreeDScene):
    def construct(self):
        # Constants
        step_time = 2
        num_steps = 8
        _kwargs = {"run_time":step_time}

        # Shapes
        cone = Cone()
        cylinder = Cylinder()
        cube = Cube()
        prism = Prism()
        sphere = Sphere()
        torus = Torus()



        self.set_camera_orientation(phi=PI/3, theta=PI/4)
        self.begin_ambient_camera_rotation(
            rate=2*(2*PI)/(step_time*num_steps),
            about="theta"
            )
        self.play(Create(cone), **_kwargs)
        self.play(ReplacementTransform(cone,cylinder), **_kwargs)
        self.play(ReplacementTransform(cylinder,cube), **_kwargs)
        self.play(ReplacementTransform(cube,prism), **_kwargs)
        self.play(ReplacementTransform(prism,sphere), **_kwargs)
        self.play(ReplacementTransform(sphere,torus), **_kwargs)
        self.play(ReplacementTransform(torus,cone), **_kwargs)
        self.play(Uncreate(cone), **_kwargs)


class Polyhedra(ThreeDScene):
    def construct(self):
        # Constants

        # Define Shapes
        axes = ThreeDAxes()
        self.add(axes)

        def get_square_pyramid():
            vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, np.sqrt(2)]
            ]
            faces_list = [
                [0, 1, 4],
                [1, 2, 4],
                [2, 3, 4],
                [3, 0, 4],
                [0, 1, 2, 3]
            ]
            return (vertex_coords, faces_list)
        
        def get_triangle_pyramid():
            vertex_coords = [
            [0, np.sqrt(3)-1/np.sqrt(3), 0],
            [1, -1/np.sqrt(3), 0],
            [-1, -1/np.sqrt(3), 0],
            [0, 0, np.sqrt(3)]
            ]
            faces_list = [
                [0, 1, 2],
                [0, 1, 3],
                [0, 2, 3],
                [1, 2, 3],
            ]
            return (vertex_coords, faces_list)
        
        square_pyramid = Polyhedron(*get_square_pyramid())
        triangle_pyramid = Polyhedron(*get_triangle_pyramid())

        self.set_camera_orientation(phi=PI/3, theta=PI/4)
        self.play(Create(square_pyramid))
        self.play(Rotate(square_pyramid,2*PI),run_time=4)
        self.play(Uncreate(square_pyramid))
        self.play(Create(triangle_pyramid))
        self.play(Rotate(triangle_pyramid,2*PI),run_time=4)
        self.play(Uncreate(triangle_pyramid))
        
