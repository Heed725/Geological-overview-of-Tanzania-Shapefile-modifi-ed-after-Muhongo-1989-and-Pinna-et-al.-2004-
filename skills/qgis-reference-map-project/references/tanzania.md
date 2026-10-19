# Accepted Tanzania baseline

Repository:
https://github.com/Heed725/Geological-overview-of-Tanzania-Shapefile-modifi-ed-after-Muhongo-1989-and-Pinna-et-al.-2004-

Download `downloads/Tanzania_Geology_Same_Colours.zip`; extract everything and open `Tanzania_Geology_Same_Colours/Tanzania_Geology_Same_Colours.qgz`.

Layout: **Tanzania geology — real outline and smooth contacts**.
Main layer: `data/natural_outline_geology.gpkg|layername=geology_natural`, containing 15 editable multipart colour classes. Preserve [tanzania_palette.csv](tanzania_palette.csv).

The exterior uses Natural Earth 1:10 million Tanzania countries minus mapped lakes. Ten real island polygons use geoBoundaries gbOpen TZA ADM0 2021 (CC BY 4.0), including Pemba, Unguja, Mafia and Lake Victoria islands. Their reference-led fill does not establish geological survey accuracy.

Reference caption: *Geological overview of Tanzania (modified after Muhongo, 1989, and Pinna et al., 2004).* Preserve attribution and separate source terms. Internal geology remains image-derived with approximate WGS 84 registration.

## Dar es Salaam regression

A pale Cretaceous marine-sediment patch southwest of Dar es Salaam was lost during changed-face relabelling. The accepted baseline restores it. Require `map_key=cretaceous` to have four disconnected polygon parts, including this patch:

- Bounds: 38.611111–39.035948°E, 7.368421–6.907895°S.
- Colour: `#f2f3b7`.

Check the location visually as well as the part count. Do not replace it with adjacent volcanic yellow or alluvial pale yellow. The accepted repair changed the Cretaceous class and overlapping alluvium/volcanic areas while retaining the other styling and geometry.

Audit with `--exact-parts cretaceous=4 --require-point cretaceous=38.7171500545,-7.1340460526 --mask-table mainland_outline --require-checksums`. Read the project's interpretation and source limitations before describing it publicly.
