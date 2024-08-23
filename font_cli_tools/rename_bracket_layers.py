import argparse
from fontTools.designspaceLib import DesignSpaceDocument
from defcon import Font
import re


parser = argparse.ArgumentParser()
parser.add_argument("font", type=Font)
parser.add_argument("designspace", type=DesignSpaceDocument.fromfile)
parser.add_argument("--appendix", type=str, default="rvrn")

args = parser.parse_args()

doc = args.designspace
font = args.font

assert doc or font


def renameBracket(glyph_name):
    match = re.match(r"(?P<glyph_name>.*)\.BRACKET\.varAlt(?P<var_alt>\d+)", glyph_name)
    if match:
        group_dict = match.groupdict()
        new_name = f"{group_dict['glyph_name']}.{args.appendix}.{group_dict['var_alt']}"
        return new_name


if doc:
    for rule in doc.rules:
        for s, (from_sub, to_sub) in enumerate(rule.subs):
            new_to_sub = renameBracket(to_sub)
            if new_to_sub:
                rule.subs[s] = (from_sub, new_to_sub)

    doc.write(doc.path)

if font:
    for glyph in font:
        new_glyph_name = renameBracket(glyph.name)
        if new_glyph_name:
            glyph.name = new_glyph_name

    font.save()
