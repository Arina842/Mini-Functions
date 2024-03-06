Rc = 39.35
Rp = 5.1
def circlepoints(points, radius, center):
    x = []
    y = []
    slice = 2 * np.pi / (points-1)
    for i in range(points):
        angle = slice * i
        x.append(center[0] + radius*np.cos(angle))
        y.append(center[1] + radius*np.sin(angle))

    return x, y
xc, yc = np.asarray(circlepoints(10000, Rc, [Rc,0]))
xp, yp = np.asarray(circlepoints(10000, Rp, [-Rp,0]))
