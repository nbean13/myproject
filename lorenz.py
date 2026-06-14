from manim import *
from math import *
from scipy.integrate import solve_ivp
import numpy as np


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# def for_later():
#     tail = VGroup(
#         TracingTail(dot, time_traced=3).match_color(dot)
#         for dot in dots
#     )


class LorenzAttractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
        )
        axes.center()
        axes.set_opacity(0)

        # Compute a set of solutions
        epsilon = 1e-4
        evolution_time = 30
        n_points = 1
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        # curves = VGroup()
        # for state, color in zip(states, colors):
        #     points = ode_solution_points(lorenz_system, state, evolution_time)
        #     axes.get_par
        #     curve = VMobject().set_points(axes.c2p(*points.T))
        #     curve.set_stroke(color, 2, 1)
        #     curves.add(curve)


        points = ode_solution_points(lorenz_system, states[0], evolution_time)
        curve = VMobject().set_points_smoothly(
            points=axes.c2p(*points)
            )        
        curve.set_stroke(colors[0], 2, 1)

        print(points.shape)

        self.add(axes)
        self.set_camera_orientation(phi=PI/3, theta=-1*PI/4)
        self.begin_ambient_camera_rotation(
            rate=2 * TAU / evolution_time,
            about="theta"
        )
        self.play(
            Write(curve), #, rate_func=linear),
            run_time=evolution_time,
        )
