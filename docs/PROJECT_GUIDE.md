# Tanzania geology — real outline and smooth geological borders

## Open

1. Extract the entire ZIP.
2. Open **Tanzania_Geology_Same_Colours.qgz** in QGIS 3.34 or later, including QGIS 3.40.
3. Open **Project → Layouts → Tanzania geology — real outline and smooth contacts** to print or export.
4. Install the included Barlow TTF files for matching legend and label typography.

All data is local with relative paths. CRS: EPSG:4326, WGS 84.

## Current map

The Cretaceous marine-sediment patch southwest of Dar es Salaam has been restored from the supplied reference. It uses the pale Cretaceous marine-sediment colour, and the smooth outer outline and other accepted styling are retained.

The outer mainland outline now comes from **real Tanzania GIS boundaries**, rather than the small image trace. Natural Earth 1:10 million country and lake polygons define the national land outline, coastline and lake edges. A light 0.001-degree vector generalisation removes details below the print-map scale.

The internal geological contacts are gently curved. Shared boundaries were generalised together at 2.2 reference-image pixels to remove pixel noise, then curved with three Chaikin passes. The resulting classes were clipped to the real mainland outline. Small gaps between the old image footprint and the real boundary were assigned the nearest reference class; those edge assignments are cartographic interpretations.

The 15 original reference colours and ten detailed real island polygons remain. Pemba, Unguja, Mafia and the Lake Victoria islands use geoBoundaries geometry. Island colours follow the reference, not a new geological survey.

The active group is **REAL TANZANIA OUTLINE + SMOOTH GEOLOGY**. Earlier trace, smooth and straightened comparison layers remain hidden. The unchanged source figure is available in **Original figure — exact image appearance**.

## Data and editing

`data/natural_outline_geology.gpkg` contains:

- `geology_natural`: 15 editable multipart geological colour classes, with smooth shared contacts and real outer clipping.
- `mainland_outline`: the real Tanzania mainland GIS outline used for clipping and the outline stroke.

The real islands and geographic labels remain in `data/straightened_geology.gpkg`. Towns and reference-position kimberlite symbols remain in `data/smoothed_geology.gpkg`. All data is local and linked with relative paths.

Edit the active geological layer in QGIS. Each colour unit is multipart; individual patches can be edited as parts, or converted with Multipart to Singleparts if desired. Change colours in Properties → Symbology. The palette is recorded in `Reference_palette.csv`.

The legend is made from editable layout swatches and labels. Update it when changing colours. The print map locks its layer list; change that list in the map item's properties to include optional layers. The original raster linework is hidden so its pixel borders do not cover the smooth vectors.

`validation.json` records the checks. The classes cover the real mainland mask without material gaps or overlaps, and all output geometries are valid. The island polygons retain their source vertices.

## Interpretation and scale

The mainland exterior is a real GIS outline. The geology inside it still derives from the supplied 492 × 657 image, with approximate registration to the printed graticule. One original image pixel is roughly 3.6 km. Generalising, curving and clipping the map improves its presentation but does not create new survey accuracy. Original ages, source generalisation and obscured image boundaries limit interpretation.

The island geometries have their own geographic coordinates. Accurate island outlines do not validate the reference-led geological colours. A small clearance where necessary prevents the approximate geology mask from covering a real island.

This is a national overview. The original optional GIS geology preserves its separate geological fields; `Optional_GIS_source_crosswalk.csv` applies to that separate dataset.

## Sources and rights

**Real islands:** geoBoundaries gbOpen, Tanzania ADM0, boundary ID **TZA-ADM0-36199320**, year represented **2021**, boundary source **Sentinel-2 10-Meter Land Use/LandCover**, licence **Creative Commons Attribution 4.0 (CC BY 4.0)**. Credit: geoBoundaries / William & Mary geoLab and the stated source-data contributors. The main land part was excluded; selected island parts were extracted without simplifying their geometry.

https://www.geoboundaries.org/api/current/gbOpen/TZA/ADM0/

https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/TZA/ADM0/geoBoundaries-TZA-ADM0.geojson

https://creativecommons.org/licenses/by/4.0/

**Reference geology and colours:** the image you supplied, captioned *Geological overview of Tanzania (modified after Muhongo, 1989, and Pinna et al., 2004).* Original publication and image rights remain with their rights holders.

**Optional GIS geology:** Heed725, Tanzania_Geology_Shapefile, Version 2 project package, downloaded 19 October 2026. Its original source and educational/research-use terms remain unchanged.
https://github.com/Heed725/Tanzania_Geology_Shapefile

**Mainland outline and lake edges:** Natural Earth 1:10 million countries and lakes, public domain. Extracted from the existing source project and used to clip the geological map. The largest Tanzania country polygon was used, mapped lakes were subtracted, and a light 0.001-degree generalisation was applied.
https://www.naturalearthdata.com/

**Optional GIS faults:** GEM Global Active Faults Database, East African Macgregor_AfricaFaults catalogue, CC BY-SA 4.0. These are distinct from the old figure's schematic lines. See `GEM_LICENSE.txt`.
https://github.com/GEMScienceTools/gem-global-active-faults

Barlow fonts: SIL Open Font License; see `fonts/OFL.txt`.
