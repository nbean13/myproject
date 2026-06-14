from manim import *
from math import *
import random
import numpy as np

## GLOBALS
KWARGS = dict(
    depth=8,
    radius=0.8,
    create_time = 0.2,
    move_time = 0.8,
    max_move_time = 1.6,
    color_hot = RED_A,
    color_cool = LOGO_BLUE,
    random=False,
    reverse=False
)

##UTILS
def isclose_xyz(xyz0, xyz1, rel_tol=1e-9, abs_tol=1e-9):
    x0, y0, z0 = xyz0
    x1, y1, z1 = xyz1

    return isclose(x0,x1,rel_tol=rel_tol,abs_tol=abs_tol) and \
           isclose(y0,y1,rel_tol=rel_tol,abs_tol=abs_tol) and \
           isclose(z0,z1,rel_tol=rel_tol,abs_tol=abs_tol)


def getPetalPoints(radius=None, depth=None, n_stems=None):
    if radius is None:
        radius = 1

    if depth is None:
        depth = 3

    if n_stems is None:
        n_stems=6
    
    points = []
    dtheta = TAU / n_stems
    phase0 = 0

    for i in range(depth):
        if i == 0:
            points.append([0, 0, 0])
        else:
            new_points = []
            for point in points:
                for j in range(6):
                    new_point = [
                        point[0] + radius*cos(j * dtheta + phase0),
                        point[1] + radius*sin(j * dtheta + phase0),
                        0
                    ]
                    new_point = [0 if isclose(coord, 0) else coord for coord in new_point]
                    
                    if not any(isclose_xyz(new_point, point) for point in points + new_points):
                        new_points.append(new_point)

                    new_points.sort(
                        key=lambda i: atan2(i[1], i[0]) if i[1] >= 0 else atan2(i[1], i[0]) + TAU
                        )
                    
            points  = points + new_points

    return points


def getTotalMoveTime(points, move_time, radius, max_move_time):
    total_move_time = 0
    for point in points:
        mag_norm = np.sqrt(point[0]**2 + point[1]**2) / radius
        total_move_time = total_move_time + min(mag_norm * move_time, max_move_time)
    return total_move_time


## "MAIN"
def constructFlowerOfLife(
        # Manual Constants
        self,
        depth=None,
        radius=None,
        create_time=None,
        move_time=None,
        max_move_time=None,
        color_hot=None,
        color_cool=None,
        random=None,
        reverse=None,
    ):
    global KWARGS

    if depth is None:
        depth = KWARGS['depth']

    if radius is None:
        radius = KWARGS['radius']

    if create_time is None:
        create_time = KWARGS['create_time']
    
    if move_time is None:
        move_time = KWARGS['move_time']
    
    if max_move_time is None:
        max_move_time = KWARGS['max_move_time']
    
    if color_hot is None:
        color_hot = KWARGS['color_hot']
    
    if color_cool is None:
        color_cool = KWARGS['color_cool']
    
    if random is None:
        random = KWARGS['random']
    
    if reverse is None:
        reverse = KWARGS['reverse']

    petal_points = getPetalPoints(depth=depth, radius=radius)
    num_petals = len(petal_points)
    total_time = (num_petals + 2) * create_time \
            + getTotalMoveTime(petal_points, move_time, radius, max_move_time) \
            + depth*move_time
    num_camera_rotations = sum(range(depth)) / 3

    # Define scene
    self.set_camera_orientation(gamma=PI/2)
    self.begin_ambient_camera_rotation(
        rate=num_camera_rotations * TAU / total_time,
        about="theta"
    )
    
    if random:
        random.seed(42069)
        random.shuffle(petal_points)
    if reverse:
        petal_points.reverse()
    
    for petal_point in petal_points:
        circle_hot = Circle(radius=radius, color=color_hot)
        self.play(Create(circle_hot), run_time=create_time,)
        circle_cool = Circle(radius=radius, color=color_cool,).shift(petal_point)
        circle_cool.set_fill(color=color_cool, opacity=0.1)
        petal_mag = np.sqrt(petal_point[0]**2 + petal_point[1]**2)
        run_time = min(move_time * petal_mag / radius, max_move_time)
        self.play(
            Transform(circle_hot, circle_cool),
            run_time = run_time if run_time > 0 else create_time,
        )

    # Draw big border circle
    circle = Circle(radius=radius, color=color_hot)
    big_circle = Circle(radius=radius*depth, color=color_cool)
    self.play(Create(circle, run_time=create_time))
    self.play(Transform(circle, big_circle), run_time=depth*move_time)

    # Unspin and zoom while flipping
    self.stop_ambient_camera_rotation(about="theta")
    self.move_camera(theta=self.camera.get_theta()/2, zoom=2, run_time=num_camera_rotations/1.5, rate_func=rate_functions.rush_into)
    self.move_camera(theta=PI/2, zoom=1, run_time=num_camera_rotations/1.5, rate_func=rate_functions.rush_from)
    self.begin_ambient_camera_rotation(about="phi", rate=2*PI/6)
    self.wait(3)
    self.move_camera(zoom=5, run_time=12)


## VARIANTS
class FlowerOfLife(ThreeDScene):
    def construct(self):
        constructFlowerOfLife(
            self,
            random=False,
            reverse=False,
        )


class FlowerOfLifeRandom(ThreeDScene):
    # Random petal order
    def construct(self):
        constructFlowerOfLife(
            self,
            random=True,
            reverse=False,
        )


class FlowerOfLifeReverse(ThreeDScene):
    # Reverse petal order
    def construct(self):
        constructFlowerOfLife(
            self,
            random=False,
            reverse=True,
        )
        
       