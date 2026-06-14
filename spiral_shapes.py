from manim import *
from math import *
import numpy as np

class SpiralShapes(ThreeDScene):
    def construct(self):
        # Set Constants
        graph_write_time = 10
        num_curves = 6
        steps_per_curve = 2
        evolution_time = graph_write_time*num_curves*steps_per_curve
        num_cam_rotations = num_curves
        omega = 5
        t_ = 2*PI

        # Init axes for plots
        axes = ThreeDAxes()
        axes.set_opacity(0)
        self.add(axes)

        # Define parametric shapes
        def spiralCone(t, omega=omega):
            return (t*cos(omega**2*t), t*sin(omega**2*t), t)
        

        def spiralConeB(t, omega=omega):
            x, y, z = spiralCone(t, omega)
            return (x, -y, z)

        
        def spiralCylinder(t, omega=omega, t_=t_):
            return (t_*cos(omega**2*t), t_*sin(omega**2*t), t)
        

        def spiralCylinderB(t, omega=omega):
            x, y, z = spiralCylinder(t, omega)
            return (x, -y, z)
        

        def spiralParabola(t, omega=omega, t_=t_):
            return (cos(omega**2*t)*t, sin(omega**2*t)*t, np.sign(t)*t_*(t/t_)**4)
        

        def spiralParabolaB(t, omega=omega, t_=t_):
            x, y, z = spiralParabola(t, omega=omega, t_=t_)
            return (x, -y, z)
        

        def spiralSphere(t, omega=omega, t_=t_):
            return (
                cos(omega**2*t)*np.sqrt(t_**2-t**2),
                sin(omega**2*t)*np.sqrt(t_**2-t**2),
                t,
            )
        

        def spiralSphereB(t, omega=omega, t_=t_):
            x, y, z = spiralSphere(t, omega=omega, t_=t_)
            return(x, -y, z)
        
        
        # Create Mobjects
        my_graph = axes.plot_parametric_curve(
            spiralCone, color=BLUE, t_range=[-t_, t_],
            )
        
        my_graph_2 = axes.plot_parametric_curve(
            spiralConeB, color=RED, t_range=[-t_, t_],
            )
        
        my_graph_3 = axes.plot_parametric_curve(
            spiralParabola, color=GOLD, t_range=[-t_, t_],
            )
        
        my_graph_4 = axes.plot_parametric_curve(
            spiralParabolaB, color=GREEN, t_range=[-t_, t_],
            )
        
        my_graph_5 = axes.plot_parametric_curve(
            spiralSphere, color=LIGHT_GRAY, t_range=[-t_, t_],
            )
        
        my_graph_6 = axes.plot_parametric_curve(
            spiralSphereB, color=PURPLE, t_range=[-t_, t_],
            )
        
        # Set camera params
        self.set_camera_orientation(
            phi=PI/3, theta=PI/4, zoom=0.75
            )
        self.begin_ambient_camera_rotation(
            rate=num_cam_rotations * (2*PI)/ evolution_time, 
            about="theta"
        )

        kwargs_ = {
            "run_time": graph_write_time,
            "rate_func": rate_functions.ease_in_out_sine,
        }

        # Define animation
        self.move_camera(
            phi=PI/6,
            zoom=1,
            added_anims=[Create(my_graph,)],
            **kwargs_
        )
        self.move_camera(
            phi=0,
            zoom=0.75,
            added_anims=[Uncreate(my_graph,)],
            **kwargs_
        )
        self.move_camera(
            phi=PI/6,
            zoom=0.5,
            added_anims=[Create(my_graph_2,)],
            **kwargs_
        )
        self.move_camera(
            phi=PI/3,
            zoom=0.75,
            added_anims=[Uncreate(my_graph_2,)],
            **kwargs_
        )
        self.move_camera(
            phi=PI/2,
            zoom=1,
            added_anims=[Create(my_graph_3,)],
            **kwargs_
        )
        self.move_camera(
            phi=2*PI/3,
            zoom=0.75,
            added_anims=[Uncreate(my_graph_3,)],
            **kwargs_
        )
        self.move_camera(
            phi=5*PI/6,
            zoom=0.5,
            added_anims=[Create(my_graph_4,)],
            **kwargs_
        )
        self.move_camera(
            phi=2*PI/3,
            zoom=0.75,
            added_anims=[Uncreate(my_graph_4,)],
            **kwargs_
        )
        self.move_camera(
            phi=PI/2,
            zoom=1,
            added_anims=[Create(my_graph_5,)],
            **kwargs_
        )
        self.move_camera(
            phi=0,
            zoom=0.75,
            added_anims=[Uncreate(my_graph_5,)],
            **kwargs_
        )
        self.move_camera(
            phi=-PI/6,
            zoom=0.5,
            added_anims=[Create(my_graph_6,)],
            **kwargs_
        )
        self.move_camera(
            phi=-PI/3,
            zoom=0.75,
            added_anims=[Uncreate(my_graph_6,)],
            **kwargs_
        )
