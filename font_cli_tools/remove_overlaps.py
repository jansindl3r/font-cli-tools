import argparse
from defcon import Font
from booleanOperations.booleanGlyph import BooleanGlyph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Font)
    parser.add_argument("glyph_names", type=lambda x: x.split(","))

    args = parser.parse_args()

    font = args.font
    glyph_names = args.glyph_names

    for glyph_name in glyph_names:
        glyph = font[glyph_name]
        removed_overlap = BooleanGlyph(glyph).removeOverlap()
        glyph.clearContours()
        removed_overlap.draw(glyph.getPen())

    font.save()
