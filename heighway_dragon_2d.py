from manim import *
from math import *
import numpy as np

class HeighwayDragon(MovingCameraScene):
    def construct(self):
        # -----------
        # init constants
        # -----------
        _side = 3
        _stroke_width = 4
        _cam_ratio = 1.2
        _init_points = np.array([
                [0, 0, 0],
                [0, _side-1, 0],
                [1, _side, 0],
                [_side, _side, 0],
            ],
            dtype=np.float64)
        _depth = 15
        _hot_color = WHITE
        _cool_color = BLUE
        _points_len = []

        # -----------
        # helper fxns
        # -----------
        def rotZ90( points, angle=PI/2, rc=np.array([0,0,0])):
            # define rotation matrix about Z-axis
            r = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle),  0],
                [0,             0,              1],
            ])

            # define translation matrix
            t = np.ones_like(points) * rc

            points_adj = points - t
            points_adj = (r @ points_adj.T).T + t
            return np.round(points_adj, decimals=8)


        def chamfer_extend( old, new ):
            if (old[-1] != new[0]).any():
                raise ValueError("Last point in `old` and first point in `new` must match.")

            old_adj, new_adj = old.copy(), new.copy()
            old_adj[-1][0] -= 1
            new_adj[0][1]  -= 1

            return np.concatenate((old_adj, new_adj), axis=0)


        # ----------
        # init shape
        # ----------
        shape = VMobject()
        shape.set_points_as_corners(_init_points)
        shape.set_color(_cool_color)
        points = _init_points.copy()
        self.play(
                self.camera.frame.animate
                .move_to(shape.get_center())
                .set(height=_cam_ratio*shape.height)
                )
        self.play(Create(shape))

        # ----------------------
        # Begin constructor loop
        # ----------------------
        i = 0
        t0 = 1
        dt = 0.2
        while i < _depth:
            _t = t0 + dt * i
            _points_len.append(len(points)-1)

            new_points = points.copy()[::-1]
            new_shape = VMobject(stroke_width=(i+1)*_stroke_width).set_points_as_corners(new_points).set_color(_hot_color)

            group = VGroup()
            group.add(shape)
            group.add(new_shape)

            new_points = rotZ90(new_points.copy(), rc=new_shape.get_start())
            points = chamfer_extend(points.copy(), new_points.copy())
            cool_shape = VMobject(stroke_width=int((i+2)*_stroke_width)).set_points_as_corners(points).set_color(_cool_color)

            # -------------------
            # Smart Camera Update
            # -------------------
            if self.camera.frame.width < _cam_ratio*cool_shape.width or self.camera.frame.height < _cam_ratio*cool_shape.height:
                height_ratio = self.camera.frame.height / cool_shape.height
                width_ratio  = self.camera.frame.width  / cool_shape.width
                if height_ratio <= width_ratio:
                    cam_kwargs = {"height": _cam_ratio*cool_shape.height}
                else:
                    cam_kwargs = {"width": _cam_ratio*cool_shape.width}
            self.play(
                self.camera.frame.animate
                .move_to(cool_shape.get_center())
                .set(**cam_kwargs),
                run_time=_t
                )

            # -----------------
            # Play Construction
            # -----------------
            self.play(Create(new_shape), run_time=_t)
            self.play(Rotate(new_shape, angle=PI/2, about_point=new_shape.get_start()), run_time=_t)
            self.play(TransformMatchingShapes(group, cool_shape))
            self.clear()
            self.add(cool_shape)
            self.wait()

            print(self.mobjects)

            shape = cool_shape.copy()
            i+=1

        _points_len = _points_len + (np.cumsum([p+1 for p in _points_len[:-1][::-1]])+_points_len[-1]).tolist()
        print(_points_len)
        _tracking_points = points[_points_len]

        path = VMobject(stroke_opacity=0.).set_points_smoothly(_tracking_points)
        path_inv = VMobject(stroke_opacity=0.).set_points_smoothly(_tracking_points[::-1])
        self.add(path, path_inv)

        self.play(
            self.camera.frame.animate.move_to(path.get_start()).set(width=50)
        )
        self.play(
            MoveAlongPath(self.camera.frame, path),
            run_time=int(np.arange(_depth).sum()),
            rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            MoveAlongPath(self.camera.frame, path_inv),
            run_time=int(np.arange(_depth).sum()),
            rate_func=rate_functions.ease_in_out_sine
        )
