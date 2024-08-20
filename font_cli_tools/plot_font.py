from drawbot_skia.document import PDFDocument
import drawbot_skia as db
from defcon import Font
from pathlib import Path
from .x_ray_pen import XRayPen
from drawbot_skia.path import BezierPath
from drawbot_skia.drawing import Drawing


def scale_glyph(glyph, scale):
    for contour in glyph:
        for point in contour:
            point.x *= scale
            point.y *= scale
    for component in glyph.components:
        transformation = list(component.transformation)
        transformation[4] *= scale
        transformation[5] *= scale
        component.transformation = transformation
    glyph.width *= scale


def draw_glyph(drawing, glyph, font, handle_thickness, point_size, handle_size):

    contour = BezierPath(glyphSet=font)

    handle_layer = BezierPath(glyphSet=font)
    point_layer = BezierPath(glyphSet=font)

    x_ray_pen = XRayPen(handle_layer, point_layer, handle_thickness, point_size, handle_size)
    glyph.draw(x_ray_pen)
    glyph.draw(contour)

    drawing.fill(0.8)
    drawing.stroke(0.2)
    drawing.drawPath(contour)

    drawing.fill(0)
    drawing.stroke(None)
    drawing.drawPath(handle_layer)

    drawing.stroke(None)
    drawing.fill(0)
    drawing.drawPath(point_layer)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path)
    parser.add_argument("--dimensions", "-d", type=int, nargs=2, default=(1920, 1080))
    parser.add_argument("--handle-size", "-hs", type=int, default=5)
    parser.add_argument("--point-size", "-ps", type=int, default=10)
    parser.add_argument("--handle-thickness", "-ht", type=int, default=2)

    args = parser.parse_args()
    base = args.font.parent

    font = Font(args.font)

    original_sizes = {}
    for glyph in font:
        original_sizes[glyph.name] = [glyph.width, glyph.leftMargin, glyph.rightMargin]

    scale_factor = 1000 / font.info.unitsPerEm * 0.6
    for glyph in font:
        original_sizes[glyph.name] = [glyph.width, glyph.leftMargin, glyph.rightMargin]
        scale_glyph(glyph, scale_factor)

    output_path = str(base / f"{args.font.stem}.pdf")

    drawing = Drawing()

    for glyph_name in font.glyphOrder:
        drawing.newPage(*args.dimensions)
        drawing.fill(0)
        glyph = font[glyph_name]
        with drawing.savedState():
            translate_x = drawing.width() / 2 - glyph.width / 2
            translate_y = (
                drawing.height() / 2
                - (
                    abs(font.info.descender * scale_factor)
                    + font.info.ascender * scale_factor
                )
                / 2
            )
            drawing.translate(translate_x, translate_y)

            zones = sorted(
                font.info.postscriptBlueValues + font.info.postscriptOtherBlues
            )
            drawing.stroke(None)
            drawing.fill(0.9)
            for z in range(0, len(zones), 2):
                drawing.rect(
                    -translate_x,
                    zones[z] * scale_factor,
                    drawing.width(),
                    (zones[z + 1] - zones[z]) * scale_factor,
                )

            drawing.stroke(0)
            drawing.line((0, -translate_y), (0, drawing.height()))
            drawing.line((glyph.width, -translate_y), (glyph.width, drawing.height()))
            drawing.line((-translate_x, 0), (drawing.width(), 0))
            drawing.line(
                (-translate_x, font.info.xHeight * scale_factor),
                (drawing.width(), font.info.xHeight * scale_factor),
            )
            drawing.line(
                (-translate_x, font.info.descender * scale_factor),
                (drawing.width(), font.info.descender * scale_factor),
            )
            drawing.line(
                (-translate_x, font.info.ascender * scale_factor),
                (drawing.width(), font.info.ascender * scale_factor),
            )
            drawing.line(
                (-translate_x, font.info.capHeight * scale_factor),
                (drawing.width(), font.info.capHeight * scale_factor),
            )

            draw_glyph(drawing, glyph, font, args.handle_thickness, args.point_size, args.handle_size)

        drawing.fontSize(50)
        drawing.text(
            f"{glyph_name}\n{', '.join([str(i) for i in original_sizes[glyph.name]])}",
            (drawing.width() / 2, drawing.height() - 200),
            align="center",
        )

    drawing.saveImage(output_path)


if __name__ == "__main__":
    main()
