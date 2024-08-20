from fontTools.ttLib import TTFont

# from extractor.formats.opentype import extractOpenTypeFeatures
from fontFeatures.ttLib import unparse

tt_font = TTFont("/Users/jansindler/Desktop/Arial.ttf")

features = unparse(tt_font)

for rule in features.allRules():
    if rule.stage == "sub":
        print(rule.asFea())
