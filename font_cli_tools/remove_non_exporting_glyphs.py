import argparse
from defcon import Font
import json
from pathlib import Path
from fontTools.designspaceLib import AxisLabelDescriptor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fonts", type=Font, nargs="+")

    args = parser.parse_args()
    fonts = args.fonts

    for font in fonts:

        skip_glyphs = font.lib.get("public.skipExportGlyphs", [])

        for glyph in font:
            for component in glyph.components:
                base_glyph = component.baseGlyph
                if base_glyph in skip_glyphs:
                    glyph.decomposeAllComponents()
                    break

        for glyph_name in skip_glyphs:
            try:
                del font[glyph_name]
            except KeyError:
                pass

        font.lib.pop("public.skipExportGlyphs", None)

        font.save()


if __name__ == "__main__":
    main()
