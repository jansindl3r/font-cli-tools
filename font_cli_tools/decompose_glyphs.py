import argparse
from defcon import Font
import re

parser = argparse.ArgumentParser()
parser.add_argument("font", type=Font)
parser.add_argument("glyphs", type=str)
parser.add_argument("--decompose_mixed_glyphs", action="store_true")
args = parser.parse_args()


font = args.font
decompose_mixed_glyphs = args.decompose_mixed_glyphs

glyphs_to_decompose = [i.strip() for i in args.glyphs.split(",")]


for layer in font.layers:
    for glyph in layer:
        if decompose_mixed_glyphs and len(glyph):
            contours = glyph.decomposeAllComponents()
        for rule in glyphs_to_decompose:
            match = re.match(f"^{rule}$", glyph.name)
            if match:
                glyph.decomposeAllComponents()
                break

font.save()
