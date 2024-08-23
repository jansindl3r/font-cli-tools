collection of CLI tools that I use for font production

# plot_font
is a tool that plots .ufo to a .pdf

it takes these arguments:

Argument | | Required | | 
--- | --- | --- | ---
`plot_font` |  | Yes | Path
`--dimensions` | `-d` | No | Dimensions of the output pdf
`--handle-size` | `-hs` | No | Size of handle
`--point-size` | `-ps` | No | Size of point
`--handle-thickness` | `-ps` | No | Thickness of line that is between the handle and point

# x_ray_pen
Pen that exposes drawing's bezier construction 

Argument                | Required  | Type
---                     | ---       | --- 
`point_layer`           | Yes       | Object with a pen protocol
`handle_line_layer`     | Yes       | Object with a pen protocol 
`line_width`            | No        | Number 
`point_size`            | No        | Number 
`handle_size`           | No        | Number 
`use_components`        | No        | Boolean
`handle_component_name` | No        | Str
`point_component_name`  | No        | Str

# rename_bracket_layers
Renames "Bracket" layers that are in ufo produced in Glyphs.
```A.BRACKET.01 -> A.r.01``` Could be a way to reduce a glyph's name below required maximum. 

Argument 			| 				| Type
--- 				| --- 			| --- 
`font`           	|       		| Path
`designspace`		|        		| Path
`--appendix`		| `-a`  		| Str, default "rvrn"