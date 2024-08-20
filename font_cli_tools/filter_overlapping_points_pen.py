class FilterOverlappingPointsPen:
    def __init__(self, otherPen):
        self.otherPen = otherPen
        self.lastPoint = None

    def moveTo(self, point):
        self.otherPen.moveTo(point)
        self.lastPoint = point

    def lineTo(self, point):
        if point != self.lastPoint:
            self.otherPen.lineTo(point)
        self.lastPoint = point

    def curveTo(self, *points):
        self.otherPen.curveTo(*points)
        self.lastPoint = points[-1]

    def closePath(self):
        self.otherPen.closePath()

    def addComponent(self, *component):
        self.otherPen.addComponent(*component)
