
from compas.geometry import Frame, Box

if __name__ == "__main__":

    frame0 = Frame([0, 0.0, 0], [1, 0, 0], [0, 1, 0])
    frame1 = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    box0 = Box(frame=frame0, xsize=0.2, ysize=0.2, zsize=3)
    box1 = Box(frame=frame1, xsize=1, ysize=0.3, zsize=1)
    print(box0.has_collision(box1))

    # print(has_obb_collision(box0, box1))

    # viewer = app.App(show_grid=False)
    # viewer.add(box0)
    # viewer.add(box1)
    # viewer.run()