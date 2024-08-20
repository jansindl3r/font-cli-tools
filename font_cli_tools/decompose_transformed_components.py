import argparse
from defcon import Font

parser = argparse.ArgumentParser()
parser.add_argument("font", type=Font)
args = parser.parse_args()

font = args.font

for glyph in font:
    for component in glyph.components:
        *to_compare, x, y = component.transformation
        if to_compare != [1, 0, 0, 1]:
            glyph.decomposeComponent(component)

font.save()
