from fontTools.pens.basePen import AbstractPen
from math import atan2, cos, sin, pi


def circle(pen, center, diameter, tension=1):
    x, y = center
    radius = diameter / 2
    pen.moveTo((x, y + radius))
    pen.curveTo(
        (x - radius * tension, y + radius),
        (x - radius, y + radius * tension),
        (x - radius, y),
    )
    pen.curveTo(
        (x - radius, y - radius * tension),
        (x - radius * tension, y - radius),
        (x, y - radius),
    )
    pen.curveTo(
        (x + radius * tension, y - radius),
        (x + radius, y - radius * tension),
        (x + radius, y),
    )
    pen.curveTo(
        (x + radius, y + radius * tension),
        (x + radius * tension, y + radius),
        (x, y + radius),
    )
    pen.closePath()


def square(pen, center, size):
    x, y = center
    pen.moveTo((x - size / 2, y - size / 2))
    pen.lineTo((x + size / 2, y - size / 2))
    pen.lineTo((x + size / 2, y + size / 2))
    pen.lineTo((x - size / 2, y + size / 2))
    pen.closePath()


def line_shape(pen, point_a, point_b, thickness):
    (x_a, y_a), (x_b, y_b) = point_a, point_b
    angle = atan2(y_b - y_a, x_b - x_a) + pi / 2
    x_offset = cos(angle) * thickness / 2
    y_offset = sin(angle) * thickness / 2

    pen.moveTo((x_a + x_offset, y_a + y_offset))
    for point in [
        (x_b + x_offset, y_b + y_offset),
        (x_b - x_offset, y_b - y_offset),
        (x_a - x_offset, y_a - y_offset),
    ]:
        pen.lineTo(point)


class XRayPen(AbstractPen):
    def __init__(
        self,
        point_layer,
        handle_line_layer,
        line_width=2,
        point_size=10,
        handle_size=5,
        use_components=False,
        handle_component_name=None,
        point_component_name=None
        ):
        self.point_layer = point_layer
        self.handle_line_layer = handle_line_layer
        self.line_width = line_width
        self.point_size = point_size
        self.handle_size = handle_size
        self.use_components = use_components
        self.handle_component_name = handle_component_name
        self.point_component_name = point_component_name

        if use_components:
            assert handle_component_name is not None and point_component_name is not None, "Component for \"point\" and \"handle\" must be provided when using components. The output layers need to have access to the \"glyphSet\" as well."

        self.last_point = None

    def handle(self, point):
        if self.use_components:
            self.point_layer.addComponent(
                self.handle_component_name, (1, 0, 0, 1, point[0], point[1])
            )
        else:
            circle(self.point_layer, point, self.handle_size, tension=0.66)

    def point(self, point):
        if self.use_components:
            self.point_layer.addComponent(
                self.point_component_name, (1, 0, 0, 1, point[0], point[1])
            )
        else:
            square(self.point_layer, point, self.point_size)

    def moveTo(self, point):
        self.point(point)
        self.last_point = point

    def lineTo(self, point):
        self.point(point)
        self.last_point = point

    def curveTo(self, point_1, point_2, point_3):
        line_shape(self.handle_line_layer, self.last_point, point_1, self.line_width)
        line_shape(self.handle_line_layer, point_2, point_3, self.line_width)

        self.handle(point_1)
        self.handle(point_2)
        self.point(point_3)

        self.last_point = point_3

    def qCurveTo(self, *points):
        line_shape(self.handle_line_layer, self.last_point, points[0], self.line_width)
        for from_point, to_point in zip(points[1:], points):
            line_shape(self.handle_line_layer, from_point, to_point, self.line_width)
        for point in points[:-1]:
            self.handle(point)
        self.point(points[-1])
        self.last_point = points[-1]

    def addComponent(self, glyph_name, transformation, **kwargs) -> None:
        self.handle_line_layer.addComponent(glyph_name, transformation)
        self.point_layer.addComponent(glyph_name, transformation)
