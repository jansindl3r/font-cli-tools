import argparse
from defcon import Font
import re


parser = argparse.ArgumentParser()
parser.add_argument("font", type=Font)

args = parser.parse_args()

font = args.font

rvrn_glyphs = []
for glyph in font:
    if re.match(r".*\.rvrn\..*", glyph.name):
        rvrn_glyphs.append(glyph.name)

font.lib["public.skipExportGlyphs"].extend(rvrn_glyphs)
font.lib["public.skipExportGlyphs"] = list(set(font.lib["public.skipExportGlyphs"]))

font.save()
